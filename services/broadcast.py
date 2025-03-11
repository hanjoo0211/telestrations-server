async def broadcast(message: dict, clients):
    for client in clients:
        await client.send_json(message)
