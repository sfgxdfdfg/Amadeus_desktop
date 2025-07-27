from PyCharacterAI import get_client
from modules.data_handlers.handle_data import *
import asyncio
from dotenv import load_dotenv
import os


class AI:
    def __init__(self) -> None:
        load_dotenv()  
        self.client_token = os.getenv("CHARACTER_AI_TOKEN")
        self.character_id = "Ce2mdN0e7xozlZ8dKl75rCOoRJTWE2FI5Ha7gN7QEgE"
    
    async def create_chatroom(self, user_id: str) -> str | None:
        try:
            client = await get_client(token=self.client_token)

            #initializing mange data class
            manage_data = EditData()

            #getting chat id
            chat, greeting_message = await client.chat.create_chat(self.character_id)
            chat_id = chat.chat_id
            manage_data.add_chatroom(user_id, chat_id)

            return chat_id
        except Exception as e:
            print(e)
            pass

    async def interpret(self, message: str, chat_id: str) -> str | None:
        try:
            client = await get_client(token=self.client_token)

            answer = await client.chat.send_message(self.character_id, chat_id, message)
            return f'{answer.get_primary_candidate().text}'
        except Exception as e:
            print(e)
            pass




'''Using aiocai but since it broken we'll use pycharaterai insteaad (28/06/2025)'''

'''
from characterai import aiocai
import asyncio

class AI:
    def __init__(self, input):
        self.client = aiocai.Client('token')
        self.character_id = "character_id"
        self.message = input
        self.chat_id = None
    
    async def interpret(self):
        try:
            me = await self.client.get_me()
            
            async with await self.client.connect()as chat:
                new_chat, initial_message = await chat.new_chat(self.character_id, me.id)
                self.chat_id = new_chat.chat_id

                message = await chat.send_message(self.character_id, self.chat_id, self.message)

                response = f'{message.text}'
                
            return response
        except asyncio.TimeoutError:
            print("The operation timed out.")
            return '....'
        except Exception as e:
            print(f"An error occurred: {e}")
            return '....'
'''