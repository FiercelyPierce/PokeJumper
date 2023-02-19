import pygame

from sys import exit
from random import randint

WIDTH, HEIGHT = 900, 540
FPS = 60

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Rush Order")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.time = 0
        self.game_active = False

        self.text_font = pygame.font.Font(None, 50)

        self.space_surface = pygame.image.load('graphics/space-small.png').convert()

        self.ground_surface = pygame.image.load('graphics/float-ground.png').convert_alpha()
        self.ground_surface = pygame.image.load('graphics/float-ground.png').convert_alpha()
        self.ground_rect_1 = self.ground_surface.get_rect(center = (WIDTH/4,550))
        self.ground_rect_2 = self.ground_surface.get_rect(center = (700,550))

        self.score_surf = self.text_font.render('SCORE: ', False, (64,64,64))
        self.score_rect = self.score_surf.get_rect(center = (WIDTH/2,50))

        # Player
        self.player_walk_1 = pygame.image.load('graphics/bulba-quil/bulba-quil_1.png').convert_alpha()
        self.player_walk_1 = pygame.transform.rotozoom(self.player_walk_1,0,0.5)

        self.player_walk_2 = pygame.image.load('graphics/bulba-quil/bulba-quil_1.png').convert_alpha()
        self.player_walk_2 = pygame.transform.rotozoom(self.player_walk_2,0,0.5)

        self.player_walk = [self.player_walk_1,self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/bulba-dile.png').convert_alpha()

        self.player_surf = self.player_walk[self.player_index]
        self.player_rect = self.player_walk_1.get_rect(bottom = 400)
        self.player_gravity = 0
        

        self.player_stand = pygame.image.load('graphics/dragi-dash.png').convert_alpha()
        # self.player_stand = pygame.transform.rotozoom(self.player_stand,0,1.5)
        self.player_stand_rect = self.player_stand.get_rect(center = (WIDTH/2,HEIGHT/2))

        self.game_name = self.text_font.render('Poke Jumper',False,'White')
        self.game_name_rect = self.game_name.get_rect(center = (WIDTH/2,100))

        self.game_message = self.text_font.render('Press Space to start!',False,'White')
        self.game_message_rect = self.game_message.get_rect(center = (WIDTH/2,450))

        # Obstacles
        self.boss_surf = pygame.image.load('graphics/gengar.png').convert_alpha()
        self.boss_surf = pygame.transform.scale(self.boss_surf,(100,80))
        self.boss_2_surf = pygame.image.load('graphics/dark-eot.png').convert_alpha()
        self.boss_2_surf = pygame.transform.scale(self.boss_2_surf,(150,130))
        self.boss_2_surf = pygame.transform.flip(self.boss_2_surf,True,False)

        self.obstacle_rect_list = []

        # Timer
        self.obstaclt_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstaclt_timer,1500)


    def main(self):

        while True:
            self.clock.tick(FPS)
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player_gravity = -17

                    # Timer
                    if event.type == self.obstaclt_timer:
                        if randint(0,2):
                            self.obstacle_rect_list.append(self.boss_surf.get_rect(bottomright = (randint(-400,0), HEIGHT)))
                        else:
                            self.obstacle_rect_list.append(self.boss_2_surf.get_rect(bottomright = (randint(-400,0), 350)))

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        self.player_rect.left = 600
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                
            if self.game_active:    
                self.draw_space()
                self.draw_ground(self.ground_surface,self.ground_rect_1)
                self.draw_ground(self.ground_surface,self.ground_rect_2)

                # pygame.draw.rect(self.screen,'#c0e8ec',self.score_rect)
                # pygame.draw.rect(self.screen,'#c0e8ec',self.score_rect,10)
                # self.screen.blit(self.score_surf,self.score_rect)
                self.time = self.display_time()

                self.display_time()
                self.draw_player()

                # Obstacle Movement
                self.obstacle_rect_list = self.obstacle_movement(self.obstacle_rect_list)
                # self.draw_boss()

                # Collitions
                self.game_active = self.collitions(self.player_rect,self.obstacle_rect_list)
            else:
                self.screen.fill('Black')
                self.screen.blit(self.player_stand,self.player_stand_rect)
                self.obstacle_rect_list.clear()

                self.time_message = self.text_font.render(f'Time: {self.time}',False,'White')
                self.time_message_rect = self.time_message.get_rect(center = (WIDTH/2,450))
                self.screen.blit(self.game_name,self.game_name_rect)

                if self.time == 0:
                    self.screen.blit(self.game_message,self.game_message_rect)
                else:
                    self.screen.blit(self.time_message,self.time_message_rect)

            pygame.display.update()


    def draw_space(self):
        self.screen.blit(self.space_surface,(0,0))

    
    def draw_ground(self,ground_surf,ground_pos):
        self.screen.blit(ground_surf,ground_pos)


    def draw_player(self):
        self.player_gravity += 1
        self.player_rect.y += self.player_gravity
        if self.player_rect.bottom >= self.ground_rect_2.top + 15:
            self.player_rect.bottom = self.ground_rect_2.top + 15
        
        if self.player_rect.bottom < 605:
            self.player_surf = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]
        self.screen.blit(self.player_walk_1,self.player_rect)
        
        self.key_pressed = pygame.key.get_pressed()
        if self.key_pressed[pygame.K_a]:
            self.player_rect.x -= 5
        if self.key_pressed[pygame.K_d]:
            self.player_rect.x += 5


    def draw_boss(self):
        self.boss_rect.x += 3
        if self.boss_rect.left >= WIDTH:
            self.boss_rect.right = 0
        self.screen.blit(self.boss_surf,self.boss_rect)


    def obstacle_movement(self,obstacle_list):
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x += 5

                if obstacle_rect.bottom == HEIGHT:
                    self.screen.blit(self.boss_surf,obstacle_rect)
                else:
                    self.screen.blit(self.boss_2_surf,obstacle_rect)
            
            # obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > WIDTH + 100]

            return obstacle_list
        else: return []


    def collitions(self,player,obstacles):
        if obstacles:
            for self.obstacle_rect in obstacles:
                if player.colliderect(self.obstacle_rect):
                    return False
        return True

    
    def display_time(self):
        self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        time_surf = self.text_font.render(f'Time: {self.current_time}',False,'Black')
        time_rect = time_surf.get_rect(center = (WIDTH/2,50))
        self.screen.blit(time_surf,time_rect)
        return self.current_time


if __name__ == "__main__":
    game = Game()
    game.main()