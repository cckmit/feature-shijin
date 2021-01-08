import os
import shutil

import aiohttp, asyncio
import logging
from pathlib import Path
from pharmcube_spider import const

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

# file_name: 绝对路径
#
def write_file(file_name, data_type, content):
    with open(file_name, data_type, encoding='utf-8') as file:
        file.write(content + "\n")

def delete_file_or_dir(path):
    file_or_dir = Path(path)
    if file_or_dir.exists():
        if file_or_dir.is_file():
            os.remove(path)
        if file_or_dir.is_dir():
            shutil.rmtree(path)
    else:
        logging.info(f'当前路径中的文件或目录不存在，请核实：{path}')

class DownloadFile(object):
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
        }
        self.path = const.STORE_PATH
        os.chdir(self.path)  # 进入文件下载路径

    async def __get_content(self, file_name, file_url):
        attempts = 0
        success = False
        while attempts<3 and not success:
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.get(file_url)
                    status_code = response.status
                    if 200 != status_code:
                        logging.info(f'------- 下载失败，重试中 {attempts} 次------- ' + file_url)
                        attempts += 1
                        continue
                    logging.info(f'------- 当前文件下载成功------- ' + file_name)
                    success = True
                    content = await response.read()
                return content
            except Exception as e:
                logging.info(f'下载失败，重试中 {attempts} 次；{str(e)} ' + file_url)
                attempts += 1

    async def __download_img(self, file_name, file_url):
        content = await self.__get_content(file_name, file_url)
        if '' == content or None == content:
            logging.info(f'当前文件下载失败，被过滤：{file_name}')
            return
        with open(file_name, 'wb') as f:
            f.write(content)

    def download_file(self, file_urls):
        if len(file_urls) == 0:
            logging.info('======= 当前无文件需要下载，被过滤 =======')
            return
        tasks = None
        if type(file_urls) is list:
            tasks = [asyncio.ensure_future(self.__download_img(file_name=url['file_name'], file_url=url['file_url'])) for url in file_urls]
        elif type(file_urls) is dict:
            tasks = [asyncio.ensure_future(self.__download_img(file_name=file_urls['file_name'], file_url=file_urls['file_url']))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
