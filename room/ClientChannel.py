

class ClientChannel:
    channels = []

    def __init__(self):
        pass

    async def addChannel(self, obj, channel):
        self.channels.append(channel)
        await obj.channel_layer.group_add(channel, obj.channel_name)
