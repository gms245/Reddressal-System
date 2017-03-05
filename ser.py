import asyncio
import websockets
clients=[]
async def hello(websocket, path):
    clients.append(websocket)
    print(websocket,"\n is connected to chat....")
    while(1):
        msg = await websocket.recv()
        for client in clients:
            if client != websocket:
                await client.send(msg)
    print(websocket,"\n is disconnected from chat....")
    

start_server = websockets.serve(hello, '0.0.0.0', 9000)
print('Server started  localhost:9000...\nServer Logs....\n')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
