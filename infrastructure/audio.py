import pygame as pg


class Sound:
    def __init__(self, game, sound_loader=None, music_loader=None):
        self.game = game
        pg.mixer.init()
        sound_loader = sound_loader or pg.mixer.Sound
        music_loader = music_loader or pg.mixer.music.load
        self.path = game.theme.resource_dir / 'sound'
        self.shotgun = sound_loader(self.path / game.theme.fire_sound)
        self.npc_pain = sound_loader(self.path / 'npc_pain.wav')
        self.npc_death = sound_loader(self.path / 'npc_death.wav')
        self.npc_shot = sound_loader(self.path / 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
        self.player_pain = sound_loader(self.path / 'player_pain.wav')
        self.theme = music_loader(self.path / 'theme.mp3')
        pg.mixer.music.set_volume(0.3)
