async def fetch(session, url):
    async with session.get(url) as response:
        json_response = await response.json()
        return json_response