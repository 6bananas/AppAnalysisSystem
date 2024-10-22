import json
from channels.generic.websocket import AsyncWebsocketConsumer

# WebSocket连接处理
class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('progress_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('progress_group', self.channel_name)

    async def send_progress_update(self, progress):
        #print(progress['progress'])
        await self.send(text_data=json.dumps({
            'progress': progress['progress']
        }))