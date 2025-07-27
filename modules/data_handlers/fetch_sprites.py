import os
from modules.data_handlers.executable_file_redirector import *

class FetchSprites:
    def __init__(self, directory: str) -> None:
        self.sprites = []
        self.directory = convert().get_resource_path(directory)
        
    def begin(self) -> list:
        for filename in os.listdir(self.directory):
            self.sprites.append(self.directory+ '/' + filename)
        return self.sprites