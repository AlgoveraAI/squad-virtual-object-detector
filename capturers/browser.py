import asyncio
from pyppeteer import launch

class browser:
    async def load(self):
        self.browser = await launch()
        self.page = await self.browser.newPage()
        
    async def goTo(self, page: str):
        await self.page.goto(page)
        
    async def getImage(self, imagePath, fullPage=True):
        await self.page.screenshot({'path': imagePath, 'fullPage': fullPage})
        
    async def close(self):
        await self.browser.close()
        
    async def evaluate(self, func):
        return await self.page.evaluate('''() => { ''' + str(func) + '''}''');

async def init(web_page, delay, filename, callback):       
    b = browser()
    await b.load()
    await b.goTo(web_page)
    await asyncio.sleep(delay)
    await b.getImage(filename)
    if not callback == None:
        callback(filename)

def run(web_page, delay, filename, callback):
    asyncio.get_event_loop().run_until_complete(init(web_page, delay, filename, callback))