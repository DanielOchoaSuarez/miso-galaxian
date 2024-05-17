import esper


from src.create.prefab_creator_interface import TextAlignment, TypeText, create_game_text
from src.ecs.components.c_game_text import CGameText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_paused_game(world: esper.World, interface_cfg: dict, delta_time: float, is_paused: bool, player_tag: CTagPlayer):
    components = world.get_components(CSurface, CTransform, CGameText)

    c_s: CSurface
    c_t: CTransform
    c_g: CGameText
    for entity, (c_s, c_t, c_g) in components:

        print(f'update {player_tag.update_score} - type {c_g.type_text}')

        if player_tag.update_score and c_g.type_text == TypeText.SCORE.value:
            player_tag.update_score = False
            world.delete_entity(entity)
            create_game_text(world, interface_cfg, 'player_score_text',
                             TextAlignment.RIGHT, TypeText.SCORE, 255, str(player_tag.score))

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
