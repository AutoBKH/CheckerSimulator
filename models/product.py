import asyncio
import uuid
from config.confing import PRODUCT_DB_URI,IMMEDIATE_RESPONSE,DELAY_TIME_SECONDS,DELAYED_RESPONSE
from aiohttp import ClientSession
from event_loop import event_loop
import os

class ProductModel():
    def __init__(self,instanceid:str, data):
        self.instance_id = instanceid
        self.immediate_response = self.get_immediate_response()
        self.delay_response = self.get_delay_response()
        self.delay_time_seconds = self.get_delay_time_seconds()
        self.name = self.get_name(data)
        self.guid = str(uuid.uuid4())
        self.response = ""

    def get_immediate_response(self):
        if os.getenv('IMMEDIATE_RESPONSE') is None:
            return IMMEDIATE_RESPONSE
        return os.getenv('IMMEDIATE_RESPONSE')

    def get_delay_response(self):
        if os.getenv('DELAYED_RESPONSE') is None:
            return DELAYED_RESPONSE
        return os.getenv('DELAYED_RESPONSE')

    def get_delay_time_seconds(self):
        if os.getenv('DELAY_TIME_SECONDS') is None:
            return int(DELAY_TIME_SECONDS)
        return int(os.getenv('DELAY_TIME_SECONDS'))

    def get_name(self,data):
        if data['name'] is None:
            return ""
        return data['name']

    def json(self):
        return {'instanceid': self.instance_id,'responce':  self.response,'name': self.name, 'guid': self.guid}

    async def delay_time(self):
        '''
            sending get request after dakay time

        '''
        await asyncio.sleep(self.get_delay_time_seconds())
        url = PRODUCT_DB_URI
        self.response = self.get_delay_response()
        async with ClientSession() as client:
            async with client.get( url, data=self.json()) as response:
                print(await response.json())

    def get_response(self):
       if self.get_delay_time_seconds() > 0:
           asyncio.run_coroutine_threadsafe(self.delay_time(), event_loop)
       self.response = self.get_immediate_response()
       return {'message': self.json()}, 202








