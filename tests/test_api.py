import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

from fastapi.testclient import TestClient

from api import main as score_api


class ScoreApiTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.database_path = score_api.DB_PATH
        score_api.DB_PATH = Path(self.directory.name) / 'scores.sqlite3'
        score_api._initialize_database()
        self.client = TestClient(score_api.app)

    def tearDown(self):
        score_api.DB_PATH = self.database_path
        self.directory.cleanup()

    def test_health_and_public_score_listing(self):
        self.assertEqual(self.client.get('/health').json(), {'status': 'ok'})
        self.assertEqual(self.client.get('/scores').json(), [])

    @patch('api.main._locate_ip', return_value=('Manchester', 'United Kingdom'))
    def test_score_submission_stores_derived_location_without_raw_ip(self, locate_ip):
        response = self.client.post(
            '/scores',
            json={'player_name': 'Alice', 'kills': 7},
            headers={'X-Forwarded-For': '203.0.113.10'},
        )

        self.assertEqual(response.status_code, 201)
        record = response.json()
        self.assertEqual(record['city'], 'Manchester')
        self.assertEqual(record['country'], 'United Kingdom')
        self.assertNotIn('ip_address', record)
        locate_ip.assert_called_once_with('203.0.113.10')
        self.assertEqual(self.client.get('/scores').json()[0]['kills'], 7)

    def test_invalid_score_is_rejected(self):
        response = self.client.post('/scores', json={'player_name': '', 'kills': -1})
        self.assertEqual(response.status_code, 422)

    @patch('api.main._locate_ip', return_value=('London', 'United Kingdom'))
    def test_web_session_submission(self, locate_ip):
        response = self.client.post(
            '/sessions',
            json={'player_name': 'Bob'},
            headers={'X-Forwarded-For': '203.0.113.20'},
        )

        self.assertEqual(response.status_code, 201)
        record = response.json()
        self.assertEqual(record['player_name'], 'Bob')
        self.assertEqual(record['city'], 'London')
        self.assertEqual(record['country'], 'United Kingdom')
        self.assertNotIn('ip_address', record)
        locate_ip.assert_called_once_with('203.0.113.20')

    def test_list_web_sessions(self):
        # Submit a session
        self.client.post('/sessions', json={'player_name': 'Charlie'})
        
        # List sessions
        response = self.client.get('/sessions')
        self.assertEqual(response.status_code, 200)
        sessions = response.json()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]['player_name'], 'Charlie')
        self.assertNotIn('ip_address', sessions[0])

    def test_invalid_session_is_rejected(self):
        response = self.client.post('/sessions', json={'player_name': ''})
        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
