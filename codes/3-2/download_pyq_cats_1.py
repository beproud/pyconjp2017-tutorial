"""
PyQ Cats からネコ画像をダウンロードするプログラム
"""
import os
from time import sleep
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# 記事一覧のURL
TOP_URL = "http://docs.pyq.jp/_static/assets/pyq-cats/articles.html"
# ダウンロードした画像を保存するディレクトリ
DOWNLOAD_DIR = "images"


# 画像をダウンロードするフォルダが存在するか確認を行い、存在していなければ作成
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

top_url_response = requests.get(TOP_URL)
soup = BeautifulSoup(top_url_response.content, 'html.parser')
# 記事の要素を全て取得します
titles = soup.find_all('h2', class_='article-title')
for title in titles:
    # aタグからhrefの内容を取得します
    link = title.find('a')
    article_url_response = requests.get(link['href'])
    soup = BeautifulSoup(article_url_response.content, 'html.parser')
    images = soup.find_all('img', class_='article-img')
    for image in images:
        # imgタグからsrcの内容を取得します
        parsed_url = urlparse(image['src'])
        # 画像名を取得します
        file_name = parsed_url.path.split('/')[-1]
        # /{ダウンロード先のフォルダ名}/{画像名} というファイルパスを作成します
        file_path = os.path.join(DOWNLOAD_DIR, file_name)

        with open(file_path, 'wb') as f:
            print('Downloading: {}'.format(image['src']))
            image_url_response = requests.get(image['src'])
            f.write(image_url_response.content)
            # サーバーに負荷をかけないために1秒あける
            sleep(1)
