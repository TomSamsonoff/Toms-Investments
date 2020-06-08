import asyncio
import aiohttp
import async_timeout


def all_pages(urls):
    """Returns a list of strings of the html for each url from a given urls list.
     By making asynchronous sessions I minimize the running time significantly.
    """

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def fetch_page(session, url):
        # Making sure that one particularly long request won't stop
        # the whole process.
        async with async_timeout.timeout(10):
            # Requesting each url.
            async with session.get(url) as response:
                return await response.text()

    async def get_multiple_pages(loop, *urls):
        tasks = []
        # Creating a pool of sessions.
        async with aiohttp.ClientSession(loop=loop) as session:
            for url in urls:
                tasks.append(fetch_page(session, url))
            # Waiting for all the tasks to be done.
            return await asyncio.gather(*tasks)

    pages = loop.run_until_complete(get_multiple_pages(loop, *urls))
    return pages
