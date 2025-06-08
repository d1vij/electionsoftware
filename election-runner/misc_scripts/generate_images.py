"""generate random images for candidates, 
images folder would be generated where this is run form
automatically imports candidates from ../api/utils.py

uses aiohttp to aynchronously fetch raw image data and aiofiles to asynchronously save them, script runs for about 3.5~4 seconds
"""

import aiohttp
import aiofiles
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from utils import candidate_data # type: ignore


url = "https://100k-faces.glitch.me/random-image"

async def fetch(url, session : aiohttp.ClientSession):
    async with session.get(url) as response:
        return await response.read()

async def save(name, content):
    async with aiofiles.open(f"./img/{name}.png","wb") as file:
        await file.write(content)
    

async def main():
    os.makedirs("./img", exist_ok=True)
    names = []
    for g in candidate_data.values():
        for n in g: names.append(n)
    print(f"{names = }")


    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for _ in range(len(names))]
        raw_content =  await asyncio.gather(*tasks)
    print("Fetched binary data for ", len(names), " images")

    save_tasks = [save(name, content) for name, content in zip(names,raw_content)]
    await asyncio.gather(*save_tasks)
    print("Done saving")
    
asyncio.run(main())