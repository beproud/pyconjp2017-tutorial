"""
PyQ Cats からネコ画像をダウンロードするプログラム(発展課題1の回答例)
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


def get_article_info(url):
    """
    記事一覧ページから記事URLを取得

    :param url: 記事一覧ページのURL
    :return: 記事の日付とURLのタプルが入ったリスト
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all('h2', class_='article-title')
    article_info = []
    for title in titles:
        link = title.find('a')
        # 記事の日付を取得します
        article_date = link['href'].split('/')[-1].replace('.html', '')
        # 記事の日付とURLの要素でタプルを作成してリストに入れます
        article_info.append((article_date, link['href']))
    return article_info


def get_image_info(url):
    """
    記事ページから画像URLを取得

    :param url: 記事ページのURL
    :return: 画像のalt属性とURLのタプルが入ったリスト
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    images = soup.find_all('img', class_='article-img')
    # 画像のalt属性と画像URLの要素でタプルを作成してリスト入れ返します
    return [(image['alt'], image['src']) for image in images]


def download_image(image_alt, image_url, article_date, download_dir):
    """
    画像をダウンロードする

    :param image_name: 画像のalt属性
    :param image_url: 画像のURL
    :param article_date: 記事の日付
    :param download_dir: ダウンロードした画像を保存するディレクトリ
    """
    parsed_url = urlparse(image_url)
    file_name = parsed_url.path.split('/')[-1]
    # ファイル拡張子を取得
    file_extname = file_name.split('.')[-1]
    # {記事の日付}_{alt属性の値}.{画像の拡張子}の文字列を作ります
    new_file_name = article_date + '_' + image_alt + '.' + file_extname
    file_path = os.path.join(download_dir, new_file_name)

    # 画像をダウンロードするフォルダが存在するか確認を行い、存在していなければ作成
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(file_path, 'wb') as f:
        print('Downloading: {}'.format(image_url))
        r = requests.get(image_url)
        f.write(r.content)
        # サーバーに負荷をかけないために1秒あける
        sleep(1)


def main():
    """
    メイン処理
    """
    # 記事一覧ページから各記事のURLを取得する
    article_info = get_article_info(TOP_URL)
    for article_date, article_url in article_info:
        # 各記事から画像URLを取得する
        image_info = get_image_info(article_url)
        for image_alt, image_url in image_info:
            # 画像URLから画像をダウンロードする
            download_image(image_alt, image_url, article_date, DOWNLOAD_DIR)


if __name__ == "__main__":
    main()
