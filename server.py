from websockets.asyncio.server import serve, ServerConnection
import asyncio
import json

class Connection:

    def __init__(self, id: str, connection: ServerConnection, filters: list[dict]):
        self.id = id
        self.connection = connection
        self.filters = filters


class Server:

    def __init__(self, port: int):
        self.port = port

        self.__connections: dict[str, Connection] = dict()

    def filters(self):
        for con_id, con in self.__connections.items():
            yield con_id, con.filters

    async def handle(self, websocket: ServerConnection):
        message = await websocket.recv()
        data = json.loads(message)
        con_id = data['id']
        filters = data['filters']
        self.__connections[con_id] = Connection(con_id, websocket, filters)
        while True:
            try:
                message = await websocket.recv()
            except Exception as e:
                print(f'Connection {con_id}:', e)
                del self.__connections[con_id]
                break
            print(message)

    async def send(self, con_id: str, message: dict):
        await self.__connections[con_id].connection.send(json.dumps(message))

    async def start(self):
        async with serve(self.handle, "", self.port):
            await asyncio.get_running_loop().create_future()