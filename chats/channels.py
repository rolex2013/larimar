from channels.generic.websocket import WebsocketConsumer

class AppConsumer(WebsocketConsumer):
    def forward_message(self, event):
        """
        Utility handler for messages to be broadcasted to groups.  Will be
        called from channel layer messages with `"type": "forward.message"`.
        """
        print('***===***===***')
        self.send(event["message"])