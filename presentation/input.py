import pygame as pg


class InputAdapter:
    def poll(self):
        return pg.event.get()
