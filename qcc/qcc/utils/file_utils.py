import os
import aiohttp, asyncio
import logging
from qcc.spiders import const

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

# file_name: 绝对路径
def write_file(file_name, data_type, content):
    with open(file_name, data_type) as file:
        file.write(content + "\n")


class DownloadFile(object):
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.path = const.STORE_PATH
        os.chdir(self.path)  # 进入文件下载路径

    async def __get_content(self, file_name, file_url):
        async with aiohttp.ClientSession() as session:
            content = ''
            attempts = 0
            success = False
            while attempts < 3 and not success:
                response = await session.get(file_url)
                status_code = response.status
                if 200 != status_code:
                    logging.info(f'------- 当前文件下载失败，重试中 {attempts} 次------- '+file_url)
                    attempts += 1
                    continue
                logging.info(f'------- 当前文件下载成功------- ' + file_name)
                success = True
                content = await response.read()
            return content

    async def __download_img(self, file_name, file_url):
        content = await self.__get_content(file_name, file_url)
        if '' == content:
            logging.info(f'------- 当前文件下载失败 -------{file_name}')
            return
        with open(file_name, 'wb') as f:
            f.write(content)

    def download_file(self, file_urls):
        tasks = [asyncio.ensure_future(self.__download_img(file_name=url['file_name'], file_url=url['file_url'])) for url in file_urls]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
