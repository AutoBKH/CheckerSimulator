import asyncio
import uuid
from config.confing import DELAY_TIME_SECONDS,PRODUCT_DB_URI,RESPONSE_AFTER_DELAY
from aiohttp import ClientSession

class ProductModel():
    def __init__(self,instanceid:str,response:str,name:str = None):
        self.instance_id = instanceid
        self.response = response
        self.name = name
        self.guid = str(uuid.uuid4())

    def json(self):
        return {'instanceid': self.instance_id,'responce':  self.response,'name': self.name, 'guid': self.guid}

    async def delay_time(self):
        '''
            sending get request after dakay time

        '''
        await asyncio.sleep(DELAY_TIME_SECONDS)
        url = PRODUCT_DB_URI
        self.response = RESPONSE_AFTER_DELAY
        async with  ClientSession() as client:
            async with client.get( url, data=self.json()) as response:
                print(await response.json())






