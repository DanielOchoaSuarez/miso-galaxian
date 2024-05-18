from enum import Enum
import pygame
import esper


from src.create.prefab_creator import create_sprite
from src.ecs.components.c_game_text import CGameText
from src.ecs.components.c_lives_counter import CLives
from src.ecs.components.c_menu_object import CMenuObject
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_live import CTagLive
from src.engine.service_locator import ServiceLocator


class TextAlignment(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2


class TypeText(Enum):
    NA = 0
    SCORE = 1
    HIGH_SCORE = 2


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


def create_game_text(world: esper.World, interface_cfg: dict, text_dict: str, alignment: TextAlignment, type_text: TypeText, alpha: int = 255, text_str: str = None) -> int:
    paused_text: dict = interface_cfg[text_dict]

    font: str = paused_text['font']
    text_size: int = paused_text['size']
    blink = paused_text['blink']

    if text_str is not None:
        text = text_str
    else:
        text: str = paused_text['text']

    color_cfg = interface_cfg[paused_text['color']]
    color = pygame.Color(color_cfg['r'], color_cfg['g'], color_cfg['b'], alpha)

    position = pygame.Vector2(
        paused_text['position']['x'],
        paused_text['position']['y'])

    entity = create_text(world, font, text, text_size,
                         color, position, alignment)

    world.add_component(entity, CGameText(
        pos=position, alignment=alignment.value, blink=blink, type_text=type_text.value))

    return entity


def create_lives(world: esper.World):
    lives_entity = world.create_entity()
    world.add_component(lives_entity, CLives(counter=3))
    return lives_entity


def create_img_lives(world: esper.World, interface_cfg: dict, lives_entity: int) -> int:
    lives_info: dict = interface_cfg['lives_img']
    img_sprite = ServiceLocator.images_service.get(lives_info['image'])
    img_size = img_sprite.get_size()

    init_pos = pygame.Vector2(
        lives_info['position']['x'],
        (lives_info['position']['y']))

    vel = pygame.Vector2(0, 0)

    lives = world.component_for_entity(lives_entity, CLives)

    for i in range(lives.counter):
        pos = pygame.Vector2(init_pos.x + (i * img_size[0]), init_pos.y)
        logo_entity = create_sprite(world, pos, vel, img_sprite)
        world.add_component(logo_entity, CTagLive())

    return logo_entity
