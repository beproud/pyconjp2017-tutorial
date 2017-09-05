"""
PyQ Cats からネコ画像をダウンロードするプログラム(関数定義バージョン)
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


def get_article_urls(url):
    """
    記事一覧ページから記事URLを取得

    :param url: 記事一覧ページのURL
    :return: 記事URLのリスト
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all('h2', class_='article-title')
    urls = []
    for title in titles:
        link = title.find('a')
        urls.append(link['href'])
    return urls


def get_image_urls(url):
    """
    記事ページから画像URLを取得

    :param url: 記事ページのURL
    :return: 画像URLのリスト
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    images = soup.find_all('img', class_='article-img')
    urls = []
    for image in images:
        urls.append(image)
    return urls


def download_image(url, download_dir):
    """
    画像をダウンロードする

    :param url: 画像のURL
    :param download_dir: ダウンロードした画像を保存するディレクトリ
    """
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]
    file_path = os.path.join(download_dir, file_name)

    # 画像をダウンロードするフォルダが存在するか確認を行い、存在していなければ作成
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(file_path, 'wb') as f:
        print('Downloading: {}'.format(url))
        r = requests.get(url)
        f.write(r.content)
        # サーバーに負荷をかけないために1秒あける
        sleep(1)


def main():
    """
    メイン処理
    """
    # 記事一覧ページから各記事のURLを取得する
    article_urls = get_article_urls(TOP_URL)
    for article_url in article_urls:
        # 各記事から画像URLを取得する
        image_urls = get_image_urls(article_url)
        for image_url in image_urls:
            # 画像URLから画像をダウンロードする
            download_image(image_url, DOWNLOAD_DIR)


if __name__ == "__main__":
    main()
