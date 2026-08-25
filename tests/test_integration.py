"""Test the complete API integration flow."""
import json
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

# Add src to path
SRC_DIR = Path(__file__).resolve().parent.parent / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from infrastructure.scores import BrowserHighScores, HighScores


def test_browser_high_scores_with_api():
    """Test that BrowserHighScores properly integrates with the API."""
    
    api_url = "http://api.example.com"
    scores = BrowserHighScores(api_url=api_url)
    
    # Mock the API responses
    mock_api_scores = [
        {"id": 1, "player_name": "Alice", "kills": 50, "city": "London", "country": "UK", "created_at": "2026-08-24T10:00:00Z"},
        {"id": 2, "player_name": "Bob", "kills": 40, "city": "NYC", "country": "USA", "created_at": "2026-08-24T09:00:00Z"},
    ]
    
    with patch('infrastructure.scores.urlopen') as mock_urlopen:
        # Mock the API response for loading scores
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_api_scores).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Load scores from API
        loaded_scores = scores.load()
        
        # Verify scores were loaded from API
        assert len(loaded_scores) == 2
        assert loaded_scores[0].player_name == "Alice"
        assert loaded_scores[0].kills == 50
        print("✓ Scores loaded from API")
        
        # Verify the correct URL was called
        mock_urlopen.assert_called()
        call_args = mock_urlopen.call_args
        request_obj = call_args[0][0]
        assert f"{api_url}/scores" in request_obj.full_url
        print("✓ Correct API endpoint called for loading scores")
    
    with patch('infrastructure.scores.urlopen') as mock_urlopen:
        # Add a new score
        mock_response = MagicMock()
        mock_response.read.return_value = b''
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = scores.add("Charlie", 60)
        
        # Verify the score was added
        assert len(result) == 3
        assert result[0].player_name == "Charlie"
        assert result[0].kills == 60
        print("✓ New score added and submitted to API")
        
        # Verify the submission was made to the API
        mock_urlopen.assert_called()
        call_args = mock_urlopen.call_args
        request_obj = call_args[0][0]
        assert f"{api_url}/scores" in request_obj.full_url
        assert request_obj.data is not None
        submitted_data = json.loads(request_obj.data.decode('utf-8'))
        assert submitted_data['player_name'] == "Charlie"
        assert submitted_data['kills'] == 60
        print("✓ Score data properly formatted and submitted")


def test_web_session_recording():
    """Test that web sessions are recorded via API."""
    api_url = "http://api.example.com"
    scores = BrowserHighScores(api_url=api_url)
    
    with patch('infrastructure.scores.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b''
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Record a session
        scores.record_session("TestPlayer")
        
        # Verify session was submitted to API
        mock_urlopen.assert_called()
        call_args = mock_urlopen.call_args
        request_obj = call_args[0][0]
        assert f"{api_url}/sessions" in request_obj.full_url
        
        submitted_data = json.loads(request_obj.data.decode('utf-8'))
        assert submitted_data['player_name'] == "TestPlayer"
        print("✓ Web session recorded via API")


def test_local_scores_sync_to_remote_api():
    with tempfile.TemporaryDirectory() as directory:
        scores = HighScores(Path(directory) / 'scores.sqlite3')
        scores.add('Alice', 25)
        scores.add('Bob', 10)

        with patch('infrastructure.scores.urlopen') as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = MagicMock()
            scores.sync('http://api.example.com', direction='push')

        assert mock_urlopen.call_count == 2
        submitted = [json.loads(call.args[0].data.decode('utf-8')) for call in mock_urlopen.call_args_list]
        assert submitted == [
            {'player_name': 'Alice', 'kills': 25},
            {'player_name': 'Bob', 'kills': 10},
        ]


def test_remote_scores_sync_to_local_database():
    with tempfile.TemporaryDirectory() as directory:
        scores = HighScores(Path(directory) / 'scores.sqlite3')
        scores.add('Old score', 1)
        remote = [{'player_name': 'Alice', 'kills': 25}, {'player_name': 'Bob', 'kills': 10}]

        with patch('infrastructure.scores.urlopen') as mock_urlopen:
            response = MagicMock()
            response.read.return_value = json.dumps(remote).encode('utf-8')
            mock_urlopen.return_value.__enter__.return_value = response
            result = scores.sync('http://api.example.com', direction='pull')

        assert [(score.player_name, score.kills) for score in result] == [('Alice', 25), ('Bob', 10)]


if __name__ == '__main__':
    print("\nTesting API integration...\n")
    test_browser_high_scores_with_api()
    test_web_session_recording()
    print("\n✅ All integration tests passed!")
