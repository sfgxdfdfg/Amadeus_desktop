import pygame
import asyncio
import pygame_gui

from modules.functionality.record_audio import *
from modules.functionality.voice_to_text import *
from modules.functionality.text_to_voice import *
from modules.functionality.start_speaking import *

from modules.essentials.renderer import *
from modules.essentials.dialog_box_tkinter import *
from modules.essentials.character_ai_async import *
from modules.essentials.pygame_obj_generator import *
from modules.essentials.emotion_analysis_hugging_face import *

from modules.data_handlers.cleaner import *
from modules.data_handlers.handle_data import *



class Amadeus:
    def __init__(
            self, 
            screen:pygame.Surface,
            window_size:tuple[int, int], 
            window_title:str, 
            user_id:str
        ) -> None:

        #intial inputs
        self.ai_response = '...'
        self.user_input = '...'

        #fetching user_data
        self.user_id = user_id
        self.chat_id = FetchData().check_chatroom(user_id=self.user_id)

        #creating task list
        self.tasks = []
        self.cleaner = clean()
        self.running = True    

        #basic pygame data
        self.screen = screen
        self.window_size = window_size
        self.window_title = window_title

        #background animation metadata
        self.background_y_init_pos = 0
        self.background_animation_speed = 1
        self.background_fps = 0.0001
        
        #setting up GUI manager
        self.gui_manager = pygame_gui.UIManager(window_size, 'resources/themes/amadeus_theme.json')
        self.gui_generator = GenerateUI(self.gui_manager)

        #generating gui elements
        #for recording 
        self.is_recording = False
        self.start_recording_button = self.gui_generator.button(position=(995, 10), dimension=(50, 50), id='#start_recording_button', text='', tool_tip='start recording')
        self.stop_recording_button = self.gui_generator.button(position=(995, 10), dimension=(50, 50), id='#stop_recording_button', text='', tool_tip='stop recording')
        self.stop_recording_button.hide()
        self.stop_recording_button.disable()

        #for amadeus terminal
        self.terminal_log = [] 
        self.starting_text = "<font color='#FFCD00' size=3.5><b>Amadeus/log></b></font> sucessfully loaded data<br>"
        self.terminal = self.gui_generator.text_box(position=(10,388), dimension=(1035, 200), id="#terminal", html_text=self.starting_text)
        self.hide_terminal = self.gui_generator.button(position=(10, 352), dimension=(290, 35), id='#hide_terminal_button', text='amadeus terminal _ ', tool_tip='hide the amadeus terminal')
        self.show_terminal = self.gui_generator.button(position=(10, 553), dimension=(290, 35), id='#show_terminal_button', text='amadeus terminal ^ ', tool_tip='show the amadeus terminal')
        self.show_terminal.hide()
        self.show_terminal.disable()

        #for reset conversation
        self.reset_button = self.gui_generator.button(position=(10, 10), dimension=(50, 50), id='#reset_conversation_button', text='', tool_tip='restarts conversation')

        #initializing dialogbox
        self.dialog_box = DialogBox()
        self.emotion = "neutral"


    ''' Event handlers '''
    async def pygame_event_loop(self, event_queue:asyncio.Queue) -> None:
        while self.running:
            await asyncio.sleep(0)  
            event = pygame.event.poll()
            if event.type != pygame.NOEVENT:
                await event_queue.put(event)
    
    async def handle_events(self, event_queue:asyncio.Queue, start_recording:asyncio.Event) -> None:
        button_clicks = 0
        while self.running:
            if not event_queue.empty():
                event = await event_queue.get()
                if event.type == pygame.QUIT:
                    result = self.dialog_box.show_popup('yesno', 'Do you wish to exit the program?')

                    if result == True:
                        self.running = False
                        self.cleaner.terminate_tasks(self.tasks)
                        self.cleaner.terminate_temp()
                        self.cleaner.terminate_lingering_obj(self.__class__)   
                    else:
                        pass

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    '''control recording functionality'''
                    if event.ui_element == self.start_recording_button:
                        self.is_recording = True
                        start_recording.set()

                        #hide and disable start recording button
                        self.start_recording_button.hide()
                        self.start_recording_button.disable()

                        #show and enable sopt recording button
                        self.stop_recording_button.show()
                        self.stop_recording_button.enable()
                    
                    if event.ui_element == self.stop_recording_button:
                        self.is_recording = False
                        await asyncio.sleep(0.1)
                        start_recording.clear()

                        #hide and disable sopt recording button
                        self.stop_recording_button.hide()
                        self.stop_recording_button.disable()

                    '''control terminal visibility'''
                    if event.ui_element == self.hide_terminal:
                        self.show_terminal.show()
                        self.show_terminal.enable()

                        self.hide_terminal.hide()
                        self.hide_terminal.disable()

                        self.terminal.hide()

                    if event.ui_element == self.show_terminal:
                        self.hide_terminal.show()
                        self.hide_terminal.enable()

                        self.show_terminal.hide()
                        self.show_terminal.disable()

                        self.terminal.show()
                    
                    '''control reset conversation'''
                    if event.ui_element == self.reset_button:
                        print(self.chat_id)
                        if self.chat_id:
                            result = self.dialog_box.show_popup('yesno', 'do you want to reset conversation?')
                            if result:
                                EditData().delete_chatroom(self.user_id)
                                self.chat_id = None
                                self.terminal.clear()
                                self.terminal.append_html_text("<font color='#FFCD00' size=3.5><b>Amadeus/log></b></font> conversation restarted<br>")
                            else:
                                pass
                        else:
                            self.dialog_box.show_popup("error", f'user {self.user_id} has no existing conversation in the database!')
                
                self.gui_manager.process_events(event)
            await asyncio.sleep(0) 


    ''' Animation handlers '''
    async def idle_animation(
        self, 
        screen:pygame.Surface, 
        character:AmadeusWindowRenderer, 
        idle_fps:int, 
        start_idle:asyncio.Event
    ) -> None:
        
        character_state = 0
        self.last_character_update = 0
        self.last_background_update = 0
        last_frame_time = pygame.time.get_ticks() / 1000
    
        while self.running:
            await start_idle.wait()
            
            # Get current time in seconds
            current_time = pygame.time.get_ticks() / 1000
            time_delta = min(0.016, max(0.0001, current_time - last_frame_time)) 
            last_frame_time = current_time

            if current_time - self.last_background_update >= self.background_fps:
                self.background_y_init_pos += self.background_animation_speed
                if self.background_y_init_pos >= 1183:
                    self.background_y_init_pos = 0

                self.last_background_update = current_time
            
            if current_time - self.last_character_update >= idle_fps:
                character_state += 1
                self.last_character_update = current_time

            while self.terminal_log:
                msg = self.terminal_log.pop(0)
                self.terminal.append_html_text(msg)

            character.background_animation(screen, self.background_y_init_pos-1183, True)
            character.background_animation(screen, self.background_y_init_pos, False)
            character.idle(screen, character_state)
            
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(screen)
            pygame.display.flip()
            await asyncio.sleep(0)
            
    async def thinking_animation(
        self, 
        screen:pygame.Surface, 
        character:AmadeusWindowRenderer, 
        start_thinking:asyncio.Event, 
        fps:int
    ) -> None:
        
        last_frame_time = pygame.time.get_ticks() / 1000
        while self.running:
            await start_thinking.wait()

            # Get current time in seconds
            current_time = pygame.time.get_ticks() / 1000
            time_delta = min(0.016, max(0.0001, current_time - last_frame_time)) 
            last_frame_time = current_time

            if current_time - self.last_background_update >= self.background_fps:
                self.background_y_init_pos += self.background_animation_speed
                if self.background_y_init_pos >= 1183:
                    self.background_y_init_pos = 0
                self.last_background_update = current_time

            while self.terminal_log:
                msg = self.terminal_log.pop(0)
                self.terminal.append_html_text(msg)

            character.background_animation(screen, self.background_y_init_pos-1183, True)
            character.background_animation(screen, self.background_y_init_pos, False)
            character.thinking(screen)
            
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(screen)
            pygame.display.flip()
            await asyncio.sleep(0)

    async def talking_animation(
        self, 
        screen:pygame.Surface, 
        character:AmadeusWindowRenderer, 
        talking_fps: int, 
        start_talking:asyncio.Event
    ) -> None:
        
        character_state = 0
        last_frame_time = pygame.time.get_ticks() / 1000
    
        while self.running:
            await start_talking.wait()
            
            # Get current time in seconds
            current_time = pygame.time.get_ticks() / 1000
            time_delta = min(0.016, max(0.0001, current_time - last_frame_time)) 
            last_frame_time = current_time
            
            if current_time - self.last_background_update >= self.background_fps:
                self.background_y_init_pos += self.background_animation_speed
                if self.background_y_init_pos >= 1183:
                    self.background_y_init_pos = 0
                self.last_background_update = current_time
            
            if current_time - self.last_character_update >= 1/talking_fps:
                character_state += 1
                self.last_character_update = current_time
            
            while self.terminal_log:
                msg = self.terminal_log.pop(0)
                self.terminal.append_html_text(msg)

            character.background_animation(screen, self.background_y_init_pos-1183, True)
            character.background_animation(screen, self.background_y_init_pos, False)
            character.talking(screen, character_state)

            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(screen)
            pygame.display.flip()
            await asyncio.sleep(0)


    ''' functionality handlers '''
    async def record_voice(
        self, 
        start_recording:asyncio.Event, 
        start_voice_to_text:asyncio.Event, 
        start_idle:asyncio.Event, 
        start_thinking:asyncio.Event
    ) -> None:
        
        while self.running:
            await start_recording.wait()

            #stop flag
            stop_event = asyncio.Event()
            
            try:
                # recording in a thread
                record_task = asyncio.create_task(
                    asyncio.to_thread(StartRecording(self.is_recording, stop_event).begin)
                )
                
                while self.is_recording:
                    await asyncio.sleep(0.1)
                
                stop_event.set()
                await record_task
               
                #handle functionality flags
                start_recording.clear()
                start_voice_to_text.set()

                #handle animation flags
                start_idle.clear()
                start_thinking.set()
                
            except Exception as e:
                #display debig
                print(f'[ERROR] {e}')
                #stop recording
                start_recording.clear()

                #show and enable start recording button
                self.start_recording_button.show()
                self.start_recording_button.enable()
                self.dialog_box.show_popup(type="error", error_message="something went wrong with recording\n- check you microphone")
          
    async def voice_to_text(
        self, 
        start_voice_to_text:asyncio.Event, 
        start_generating_ai_response:asyncio.Event
    ) -> None:

        while self.running:
            await start_voice_to_text.wait()
            self.user_input = await asyncio.to_thread(VoiceToText().begin)

            terminal_user_log = f"<font color='#00B3FF' size=3.5><b>Users/salieri></b></font> {self.user_input}<br>"
            self.terminal_log.append(terminal_user_log)
            
            #handle functionality flags
            start_voice_to_text.clear()
            start_generating_ai_response.set()

    async def run_character_ai(
        self, 
        character:AmadeusWindowRenderer, 
        start_generating_ai_response:asyncio.Event, 
        start_ai_speaking:asyncio.Event, 
        start_idle:asyncio.Event, 
        start_thinking:asyncio.Event
    ) -> None:
        
        while self.running:
            await start_generating_ai_response.wait()
            start_generating_ai_response.clear() 
            try:
                #generate ai response
                if self.chat_id == None:
                    self.chat_id = await AI().create_chatroom(self.user_id)
                    
                self.ai_response = await AI().interpret(self.user_input, self.chat_id)

                #identify emotion and set appropriate sprites to express emotion
                self.emotion = await asyncio.to_thread(lambda: EmotionAnalysis().analyze_emotion(self.ai_response))
                character.character_talking_sprites = FetchSprites(f'resources/sprites/talking_all/talking_{self.emotion}').begin()
                character.character_idle_sprites = FetchSprites(f'resources/sprites/idle_all/idle_{self.emotion}').begin()

                #append in the amadeus terminal the AI's respoonse
                terminal_Ai_log = f"<font color='#FFCD00' size=3.5><b>Amadeus/log></b></font> {self.ai_response}<br>"
                self.terminal_log.append(terminal_Ai_log)
                
                #handle functionality flag
                start_ai_speaking.set()

            except Exception as e:
                self.dialog_box.show_popup('error', 'Had an error communicating with Makise Kurisu, try the following\n-check your internet connection\n-click restart conversation\nEl Psy Congroo...')
                
                #handle animation flags
                start_thinking.clear()
                start_idle.set()
                
                #show and enable start recording button
                self.start_recording_button.show()
                self.start_recording_button.enable()

    async def start_ai_speak(
        self, 
        character:AmadeusWindowRenderer,
        start_ai_speaking:asyncio.Event, 
        start_idle:asyncio.Event, 
        start_talking:asyncio.Event, 
        start_thinking:asyncio.Event
    ) -> None:

        while self.running:
            try:
                await start_ai_speaking.wait()
                await asyncio.to_thread(TextToVoice(self.ai_response).begin)

                #play the audio recording of ai response and manage talking animation
                await asyncio.to_thread(StartSpeaking(start_talking, start_idle,start_thinking, asyncio.get_event_loop()).begin)

                #setting the emotion back to neutral
                character.character_talking_sprites = FetchSprites(f'resources/sprites/talking_all/talking_neutral').begin()
                character.character_idle_sprites = FetchSprites(f'resources/sprites/idle_all/idle_neutral').begin()
                
                #handle functionality flags
                start_ai_speaking.clear()

                #handle animation flags
                start_talking.clear()
                start_idle.set()
                
                #show and enable start recording button
                self.start_recording_button.show()
                self.start_recording_button.enable()

            except Exception as e:
                print(f"Error in AI speech playback: {e}")
                

    ''' run function '''
    async def run(self) -> None:
        #setting up pygame window
        screen = self.screen
        pygame.display.set_caption(self.window_title)

        #initializing essentials
        character = AmadeusWindowRenderer()
        idle_fps = 1.5
        talking_fps =4

        #event queue
        event_queue = asyncio.Queue()

        #event flags for animation
        start_idle = asyncio.Event()
        start_idle.set()
        start_thinking = asyncio.Event()
        start_talking = asyncio.Event()

        #event flags for functionalities
        start_recording = asyncio.Event()
        start_voice_to_text = asyncio.Event()
        start_generating_ai_response = asyncio.Event()
        start_ai_speaking = asyncio.Event()
        

        self.tasks = [
            #event handlers
            asyncio.create_task(self.pygame_event_loop(event_queue)),
            asyncio.create_task(self.handle_events(event_queue, start_recording)),

            #animation handlers
            asyncio.create_task(self.idle_animation(screen, character, idle_fps, start_idle)),
            asyncio.create_task(self.thinking_animation(screen,character, start_thinking, idle_fps)),
            asyncio.create_task(self.talking_animation(screen, character, talking_fps, start_talking)),

            #functionality handlers
            asyncio.create_task(self.record_voice(start_recording, start_voice_to_text, start_idle, start_thinking)),
            asyncio.create_task(self.voice_to_text(start_voice_to_text, start_generating_ai_response)),
            asyncio.create_task(self.run_character_ai(character, start_generating_ai_response, start_ai_speaking, start_idle, start_thinking)),
            asyncio.create_task(self.start_ai_speak(character,start_ai_speaking, start_idle, start_talking, start_thinking)),

        ]

        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            pass
        finally:
            pygame.quit()
    
    
    ''' clean up '''
    def __del__(self):
        print(f"Destroyed instance: {self.__class__}")

