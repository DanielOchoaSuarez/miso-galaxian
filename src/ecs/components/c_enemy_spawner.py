import pygame

class CEnemySpawner:
    def __init__(self, screen:pygame.Rect) -> None:
        self.enemy_rows:int = 6
        self.enemy_start_chase:float = 3.0
        self.enemy_start_chase_counter:float = 0.0
        self.enemy_tiles:int = 10 # must be even
        self.enemy_list:list = []
        self.screen_width:int = screen.width
        self.reverse_limit:int = 20
        self.should_reverse:bool = False
        self.l_r_velocity:pygame.Vector2 = pygame.Vector2(10, 0)
        self.r_l_velocity:pygame.Vector2 = pygame.Vector2(-10, 0)
        self.enemy_separation:int = 4
        self.enemy_size_x:int = 12
        self.enemy_size_y:int = 8
        self.enemy_group_x_pos = self.get_topleft()
        enemy_group_y_pos = 50
        no_enemmies_spots = [0,1,2,4,5,7,8,9,10,11,18,19,20,29]
        enemy_type_d = [3,6]
        enemy_type_c = [12,13,14,15,16,17]
        enemy_type_b = [21,22,23,24,25,26,27,28]
        counter = 0
        reversed_anim = True
        for _ in range(0, self.enemy_rows):
            x_init_pos = self.enemy_group_x_pos
            for _ in range(0, self.enemy_tiles):
                if counter not in no_enemmies_spots:
                    enemy_type = 'typeA'
                    pixel_shiftx = 0
                    pixel_shifty = 0
                    if counter in enemy_type_d:
                        enemy_type = 'typeD'
                        pixel_shifty = -2
                    elif counter in enemy_type_c:
                        enemy_type = 'typeC'
                        pixel_shiftx = 1
                    elif counter in enemy_type_b:
                        enemy_type = 'typeB'
                        pixel_shiftx= 2
                        pixel_shifty = 1


                    self.enemy_list.append(EnemyData((x_init_pos + pixel_shiftx), (enemy_group_y_pos + pixel_shifty), self.l_r_velocity, reversed_anim, enemy_type))
                x_init_pos += (self.enemy_size_x + self.enemy_separation)
                counter += 1
                reversed_anim = False if counter % 2 == 0 else True

            enemy_group_y_pos += (self.enemy_size_y + self.enemy_separation)


    def get_topleft(self):
        half_screen = (self.screen_width / 2)
        enemies_on_half_screen = (self.enemy_tiles / 2)
        topleft = half_screen - ((enemies_on_half_screen * self.enemy_size_x) + (self.enemy_separation * (enemies_on_half_screen - 1)) + (self.enemy_separation / 2))
        return topleft

class EnemyData:
    def __init__(self, pos_x, pos_y, init_vel, reversed_anim, enemy_type) -> None:
        self.is_spawned:bool = False
        self.entity_id:int = 0
        self.enemy_type:str = enemy_type
        self.reversed_anim:bool = reversed_anim
        self.on_idle_vel = init_vel
        self.init_pos:pygame.Vector2 = pygame.Vector2(pos_x, pos_y)