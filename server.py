import asyncio
import json
from websockets.asyncio.server import serve, ServerConnection


class Connection:

    def __init__(self, id: str, connection: ServerConnection, filter: dict):
        self.id = id
        self.connection = connection
        self.filter = filter

    async def send(self, message: str):
        await self.connection.send(message)


class Server:

    def __init__(self, port: int):
        self.port = port
        self.__connections: dict[str, Connection] = dict()

    def filters(self):
        for con_id, con in self.__connections.items():
            yield con_id, con.filter

    async def handle(self, websocket: ServerConnection):
        message = json.loads(await websocket.recv())
        if message['event'] != 'connect': return

        data = message['data']
        con_id = data['id']
        filter = data['filter']
        self.__connections[con_id] = Connection(con_id, websocket, filter)
        print('Hi,', con_id)
        
        while True:
            try:
                message = await websocket.recv()
            except Exception as e:
                print(f'Connection {con_id}:', e)
                del self.__connections[con_id]
                break
            print(message)

    async def send(self, con_id: str, message: dict):
        await self.__connections[con_id].send(json.dumps(message))

    async def start(self):
        async with serve(self.handle, "", self.port):
            await asyncio.get_running_loop().create_future()