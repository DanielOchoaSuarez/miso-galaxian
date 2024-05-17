from enum import Enum
import pygame
import esper


from src.create.prefab_creator import create_sprite
from src.ecs.components.c_menu_object import CMenuObject
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


class TextAlignment(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, font_asset: str, txt: str, size: int,
                color: pygame.Color, pos: pygame.Vector2, alignment: TextAlignment) -> int:

    font = ServiceLocator.fonts_service.get(font_asset, size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity, CTransform(pos + origin))
    return text_entity


def create_logo_title(world: esper.World, window_height: int, interface_cfg: dict) -> int:
    logo_info: dict = interface_cfg['logo_title']
    logo_sprite = ServiceLocator.images_service.get(logo_info['image'])
    logo_size = logo_sprite.get_size()

    init_pos = pygame.Vector2(
        logo_info['position']['x'] - (logo_size[0] / 2),
        (logo_info['position']['y'] + window_height) - (logo_size[1] / 2))

    final_pos = pygame.Vector2(
        logo_info['position']['x'] - (logo_size[0] / 2),
        logo_info['position']['y'] - (logo_size[1] / 2))

    vel = pygame.Vector2(
        interface_cfg['scroll_velocity']['x'],
        interface_cfg['scroll_velocity']['y'])

    logo_entity = create_sprite(world, init_pos, vel, logo_sprite)
    world.add_component(logo_entity, CMenuObject(
        final_pos=final_pos, alignment=0))
    return logo_entity


def create_menu_text(world: esper.World, window_height: int, interface_cfg: dict, text_dict: str, alignment: TextAlignment) -> int:
    menu_text: dict = interface_cfg[text_dict]

    font_asset: str = menu_text['font']
    text: str = menu_text['text']
    text_size: int = menu_text['size']
    blink = menu_text['blink']

    color_cfg = interface_cfg[menu_text['color']]
    color = pygame.Color(color_cfg['r'], color_cfg['g'], color_cfg['b'])

    init_pos = pygame.Vector2(
        menu_text['position']['x'],
        menu_text['position']['y'] + window_height)

    final_pos = pygame.Vector2(
        menu_text['position']['x'],
        menu_text['position']['y'])

    vel = pygame.Vector2(
        interface_cfg['scroll_velocity']['x'],
        interface_cfg['scroll_velocity']['y'])

    entity = create_text(world, font_asset, text, text_size,
                         color, init_pos, alignment)
    world.add_component(entity, CVelocity(vel))
    world.add_component(entity, CMenuObject(
        final_pos=final_pos, blink=blink, alignment=alignment.value))

    return entity


def create_paused_text(world: esper.World, interface_cfg: dict, alignment: TextAlignment) -> int:
    paused_text: dict = interface_cfg['paused_text']

    font: str = paused_text['font']
    text: str = paused_text['text']
    text_size: int = paused_text['size']
    blink = paused_text['blink']

    color_cfg = interface_cfg[paused_text['color']]
    color = pygame.Color(color_cfg['r'], color_cfg['g'], color_cfg['b'], 0)

    position = pygame.Vector2(
        paused_text['position']['x'],
        paused_text['position']['y'])

    entity = create_text(world, font, text, text_size,
                         color, position, alignment)

    world.add_component(entity, CMenuObject(
        final_pos=position, blink=blink, alignment=alignment.value))

    return entity
