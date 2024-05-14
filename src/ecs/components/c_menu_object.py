import pygame


class CMenuObject:
    def __init__(self, final_pos: pygame.Vector2, alignment: int, blink: bool = False, is_scrolled: bool = False):
        self.final_pos = final_pos
        self.alignment = alignment
        self.blink = blink
        self.is_scrolled = is_scrolled
        self.counter = 0
