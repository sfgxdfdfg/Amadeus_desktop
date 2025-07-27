import pygame
from modules.data_handlers.fetch_sprites import *
import os


class Renderer:
    def __init__(self)-> None:

        ''' Fetching Sprites and automatically converting them to be exe compatible '''
        #fetching sprites, NOTE: can be upgraded into sprites/character_name/idle
        self.character_idle_sprites = FetchSprites('resources/sprites/idle_all/idle_neutral').begin() 
        self.character_talking_sprites = FetchSprites('resources/sprites/talking_all/talking_neutral').begin()
        self.character_thinking_sprites = FetchSprites('resources/sprites/thinking').begin()

        #fetching amadeus window background srpite
        self.amadeus_window_background_sprite = FetchSprites('resources/sprites/background').begin()
        self.amadeus_window_background = pygame.image.load(self.amadeus_window_background_sprite[0])

        #fetching startup window sprites
        self.startup_window_sprites = FetchSprites('resources/sprites/startup').begin()
        
        #fetching initialize window sprites
        self.hour_glass_sprites = FetchSprites('resources/sprites/loading_hour_glass').begin()
        


        ''' setting up dimensions and position '''
        #dimensions
        self.character_dimension = (375, 584)
        self.character_position = (528, 310)

        self.startup_dimension = (612, 532)
        self.startup_position = (528,250)

''' Renders all animation in amadeus window '''
class AmadeusWindowRenderer(Renderer):
    def __init__(self)-> None:
        super().__init__()
    
    def background_animation(self, screen: pygame.Surface, y_position:int, flip_bg: bool)-> None:
        if flip_bg:
            amadeus_window_background = pygame.transform.flip(self.amadeus_window_background, False, True)
            screen.blit(amadeus_window_background, (0,y_position))
        else:
            screen.blit(self.amadeus_window_background, (0,y_position))
        
    def idle(self, screen: pygame.Surface, character_state: int)-> None:   
        if character_state%2 == 0:
            character_image = pygame.image.load(self.character_idle_sprites[0])
        elif character_state%2 != 0:
            character_image = pygame.image.load(self.character_idle_sprites[1])

        character_image = pygame.transform.scale(character_image, self.character_dimension)
        character_image_rect = character_image.get_rect(center=self.character_position)

        screen.blit(character_image, character_image_rect)
        
    def talking(self, screen: pygame.Surface, character_state: int)-> None:
    
        if character_state/3 == 1:
            character_image = pygame.image.load(self.character_talking_sprites[2])
        elif character_state%3 == 0:
            character_image = pygame.image.load(self.character_talking_sprites[0])
        elif character_state%3 != 0:
            character_image = pygame.image.load(self.character_talking_sprites[1])

        character_image = pygame.transform.scale(character_image, self.character_dimension)
        character_image_rect = character_image.get_rect(center=self.character_position)

        screen.blit(character_image, character_image_rect)
    
    def thinking(self, screen: pygame.Surface)-> None:
        character_image = pygame.image.load(self.character_thinking_sprites[0])
        character_image = pygame.transform.scale(character_image, self.character_dimension)
        character_image_rect = character_image.get_rect(center=self.character_position)

        screen.blit(character_image, character_image_rect)

''' Renders all animation in startup window '''
class StartupWindowRenderer(Renderer):
    def __init__(self)-> None:
        super().__init__()
    
    def start_up(self, screen: pygame.Surface, frame_count: int)-> None:
        filename = f'{frame_count}.png'
        background_color = (0,0,0)
        for file in self.startup_window_sprites:
            if filename == os.path.basename(file):
                startup = pygame.image.load(file)
                startup = pygame.transform.scale(startup, self.startup_dimension)
                startup_rect = startup.get_rect(center=self.startup_position)
                screen.fill(background_color)
                screen.blit(startup, startup_rect)
    
''' Renders all animation in initializing window '''
class InitializeWindowRenderer(Renderer):   
    def __init__(self)-> None:
        super().__init__()
    
    def hour_glass(self, screen: pygame.Surface, frame_count: int, position: tuple[int, int])-> None:
        filename = f'{frame_count}.png'
        for file in self.hour_glass_sprites:
            if filename == os.path.basename(file):
                hour_glass_sprite = pygame.image.load(file)
                screen.blit(hour_glass_sprite, position)
