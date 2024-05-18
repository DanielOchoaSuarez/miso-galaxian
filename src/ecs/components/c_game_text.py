import pygame


class CGameText:
    def __init__(self, pos: pygame.Vector2, alignment: int, blink: bool, type_text: int):
        self.pos = pos
        self.alignment = alignment
        self.blink = blink
        self.type_text = type_text
        self.counter = 0
