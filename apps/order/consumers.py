from channels.generic.websocket import AsyncWebsocketConsumer
import json


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.group_name = f"order_{self.order_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print(f"✅ Order {self.order_id} WebSocket ga ulandi")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"❌ Order {self.order_id} WebSocket dan chiqdi")

    async def order_update(self, event):
        """Bemor uchun - status o'zgarganda"""
        await self.send(text_data=json.dumps({
            'type': 'ORDER_UPDATE',
            'data': event["data"]
        }))

    async def order_doctor_update(self, event):
        """Doktor uchun - faqat o'sha buyurtma bo'yicha"""
        await self.send(text_data=json.dumps({
            'type': 'DOCTOR_ORDER_UPDATE',
            'data': event["data"]
        }))