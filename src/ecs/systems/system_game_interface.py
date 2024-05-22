import esper


from src.create.prefab_creator_interface import TextAlignment, TypeText, create_game_text
from src.ecs.components.c_game import CGame
from src.ecs.components.c_game_text import CGameText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_game_interface(world: esper.World, interface_cfg: dict, delta_time: float, is_paused: bool, c_game_entity: int):
    c_game = world.component_for_entity(c_game_entity, CGame)
    components = world.get_components(CSurface, CTransform, CGameText)

    c_s: CSurface
    c_t: CTransform
    c_g: CGameText
    for entity, (c_s, c_t, c_g) in components:

        if c_game.update_score and c_g.type_text == TypeText.SCORE.value:
            c_game.update_score = False
            world.delete_entity(entity)
            create_game_text(world, interface_cfg, 'player_score_text',
                             TextAlignment.RIGHT, TypeText.SCORE, 255, str(c_game.score))

        high_score: int = int(interface_cfg['high_score_text'].get('text'))
        if c_g.type_text == TypeText.HIGH_SCORE.value and high_score < c_game.score:
            interface_cfg['high_score_text']['text'] = str(c_game.score)
            world.delete_entity(entity)
            create_game_text(world, interface_cfg, 'high_score_text',
                             TextAlignment.RIGHT, TypeText.HIGH_SCORE, 255, str(c_game.score))

        if c_g.blink:
            if not is_paused:
                c_s.surf.set_alpha(0)
                continue

            c_g.counter += delta_time

            if c_g.counter >= 0.6:
                c_g.counter = 0

                if c_s.surf.get_alpha() == 0:
                    c_s.surf.set_alpha(255)
                else:
                    c_s.surf.set_alpha(0)
