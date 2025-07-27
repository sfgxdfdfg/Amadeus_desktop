import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton


'''
Some of the classes here isn't used in the app but still here as this is a reused 
module I made from my past projects
'''

#creating, editing and generating rect for images
class GenerateRect:
    def __init__(
        self, 
        scale:tuple, 
        position:tuple, 
        pygame_object:pygame.Surface
    ) -> None:

        self.scale = scale
        self.position = position
        self.py_object = pygame_object
        self.scaled_object = pygame.transform.scale(self.py_object, self.scale)
    
    def scaled(self) -> pygame.Surface:
        return self.scaled_object

    def rect(self) -> pygame.Rect:
        object_rect = self.scaled_object.get_rect(center = self.position)
        return object_rect

#creating, editing and generating rect for fonts
class GenerateFont:
    def __init__(self, font_color:tuple[int, int, int], font_path:str, size:int) -> None:
        self.font_color = font_color
        self.font_style = font_path
        self.size = size

        self.font = pygame.font.Font(filename=self.font_style, size = self.size)
    
    def render(self, text:str) -> pygame.Surface:
        font_render = self.font.render(text, True, self.font_color)
        return font_render

#GUI generator
class GenerateUI:
    def __init__(self, gui_manager:pygame_gui.UIManager) -> None:
        self.gui_manager = gui_manager
    
    def searchbar(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str, 
        class_name=None
    ) -> pygame_gui.elements.UITextEntryLine:
        
        search_bar = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(position,dimension),
            manager=self.gui_manager,
            object_id=ObjectID(class_id=class_name,object_id=id)
        
        )
        return search_bar
    
    def button(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        text:str, id:str, 
        class_name=None, 
        container=None, 
        anchor = None, 
        allow_double_clicks=None, 
        tool_tip = None
    ) -> pygame_gui.elements.UIButton:
        
        if tool_tip:
            tool_tip = f'<b><font color=#FF5733 size=4>Info</font></b><br><i>{tool_tip}</i>'
        else:
            pass

        if allow_double_clicks == None:
            allow_double_clicks = False

        button = UIButton(
            relative_rect=pygame.Rect(position, dimension),
            text=text, 
            manager=self.gui_manager,
            object_id=ObjectID(class_id=class_name,object_id=id),
            tool_tip_text=tool_tip,
            container = container,
            anchors = anchor,
            allow_double_clicks = allow_double_clicks
        )
        return button
    
    def scrollcontainer(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str
    ) -> pygame_gui.elements.UIScrollingContainer:
        
        scroll_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(position, dimension),
            manager=self.gui_manager,
            object_id = id,
            allow_scroll_y=True,  
            allow_scroll_x=False,
            should_grow_automatically=True
        )
        return scroll_container
    
    def panel(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str=None, 
        container = None
    ) -> pygame_gui.elements.UIPanel:
        

        panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(position, dimension),  
            starting_height=1,
            manager=self.gui_manager,
            element_id = id,
            container=container
        )
        return panel
    
    def image(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        image_surface,
        id:str ,
        container = None 
    ) -> pygame_gui.elements.ui_image.UIImage:
        
        image = pygame_gui.elements.ui_image.UIImage(
            relative_rect=pygame.Rect(position, dimension),  
            image_surface = image_surface,
            manager = self.gui_manager,
            container =  container,
            object_id = id
        )
        return image
    
    def label(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int],
        text:str, 
        id:str, 
        container=None, 
        class_name = None
    ) -> pygame_gui.elements.UILabel:
        
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, dimension),
            manager = self.gui_manager,
            container =  container,
            object_id = ObjectID(class_id=class_name,object_id=id),
            text=text
        )
        return label
    
    def filedialog(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int],
        text:str, 
        id:str, 
        initial_path:str
    ) -> pygame_gui.windows.ui_file_dialog.UIFileDialog:
        
        file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(
            rect=pygame.Rect(position, dimension),
            manager=self.gui_manager,
            window_title=text,
            allowed_suffixes={'.txt', '.png', '.jpg'},
            initial_file_path=initial_path, 
            object_id=id,
            allow_picking_directories=True  
        )
        return file_dialog
    
    def progressbar(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str, 
        container=None
    ) -> pygame_gui.elements.UIProgressBar:
        
        progress_bar = pygame_gui.elements.UIProgressBar(
            relative_rect =pygame.Rect(position, dimension),
            manager=self.gui_manager,
            object_id  = id,
            container  = container 

        )
        return progress_bar
    
    def confirmation_window(
        self,  
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str, 
        window_title:str, 
        blocking:bool, 
        long_desc:str
    ) -> pygame_gui.windows.UIConfirmationDialog:
        
        confirmation_window = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(position, dimension),
            manager=self.gui_manager,
            window_title=window_title,
            object_id=id,
            blocking=blocking,
            action_long_desc=long_desc
        )
        return confirmation_window
    
    def message_window(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str, 
        window_title:str,
        always_on_top:bool, 
        html_message:str
    ) -> pygame_gui.windows.UIMessageWindow:

        html_message = f'<b><font color=#FF5733 size=4>Warning</font></b><br><i>{html_message}</i>'
    

        message_window = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(position, dimension),
            manager=self.gui_manager,
            object_id=id,
            window_title=window_title,
            always_on_top = always_on_top,
            html_message = html_message
        )
        return message_window
    
    def text_box(
        self, 
        position:tuple[int, int], 
        dimension:tuple[int, int], 
        id:str, 
        html_text:str
    ) -> pygame_gui.elements.UITextBox:
        
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(position, dimension),
            manager=self.gui_manager,
            object_id=id,
            html_text=html_text
        )
        return text_box



