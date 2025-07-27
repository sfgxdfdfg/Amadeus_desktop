import pygame
import pygame_gui

from modules.essentials.renderer import *
from modules.essentials.dialog_box_tkinter import *
from modules.essentials.pygame_obj_generator import *

from modules.data_handlers.cleaner import *


class Startup:
    def __init__(
        self, 
        screen: pygame.Surface,
        window_size: tuple[int, int], 
        window_title: str, 
        background_color: tuple[int, int, int], 
        fps: int
    ) -> None:

        #basic pygame metadata
        self.window_title = window_title
        self.background_color = background_color
        self.fps = fps/3
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(self.fps)/1000.0 
        
        #setting up screen
        self.screen = screen
        pygame.display.set_caption(self.window_title)

        #initialize dialogbox
        self.dialogbox = DialogBox()

        #fetching start up sprites
        self.startup_renderer = StartupWindowRenderer()

        #setting up loop boolean
        self.running = True

        '''
        for optional trigger to propceed to the main amadeus script
        #setting up GUI manager and GUI generator
        self.gui_manager = pygame_gui.UIManager(window_size, 'resources/themes/start_up_theme.json')
        self.gui_generator = GenerateUI(self.gui_manager)

        self.connect = self.gui_generator.button(
            position=(400, 490), 
            dimension=(300, 70),
            id='#connect_button', 
            text='', 
            tool_tip='Connect to Amadeus')
        '''
    
    def run(self) -> None:
        frame_count = 0
        while self.running:
            #event handlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ans = self.dialogbox.show_popup("yesno","Quit The program?")
                    if ans == True:
                        self.running = False
                        pygame.quit()
                    else:
                        pass
                '''
                for optional trigger to propceed to the main amadeus script
                if event.type == pygame.KEYDOWN and frame_count>= 39:
                    if event.key == pygame.K_RETURN:
                        return True
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.connect:
                        self.connect.disable()
                        return True
                
                self.gui_manager.process_events(event)
                '''
            
            if frame_count < 39:
                self.startup_renderer.start_up(self.screen, frame_count)
                frame_count += 1
            if frame_count >= 39:
                '''
                for optional trigger to propceed to the main amadeus script
                self.start_up_sprites.start_up(self.screen, 38)
                self.gui_manager.update(self.time_delta)
                self.gui_manager.draw_ui(self.screen)
                '''
                return True



            # Update the display
            pygame.display.flip()

            # Cap the frame rate at 60 frames per second
            self.clock.tick(self.fps)

