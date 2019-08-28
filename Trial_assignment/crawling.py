import requests
from bs4 import BeautifulSoup
import re
import time
import os
page_num : int = 0
def crwl():
    base_url=  "https://www.baitoru.com/kanto/jlist/"
    station_url: str = "yamanotesen/"
    url: str = base_url + station_url 
    # htmlでデータ分析できる形に保存
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, 'lxml')
    time.sleep(1)
    # ページネーションの最後のページ番号を取得
    global page_num
    page_num = bs.find("li",class_="last").get_text().strip()
    print(page_num)

    newdir = "crawled_file"
    if os.path.exists(newdir):
        print("exist.")
    else:
        os.mkdir(newdir)
    with open('./crawled_file/page_number.txt', 'w') as file:
        file.write(page_num)
    with open('./crawled_file/baitoru_1.html', 'w') as file:
        file.write(response.text)
    #全ページをhtmlに保存
    for i in range(2 , int(page_num)+1) :
        page_url : str = url + "page" + str(i)
        response = requests.get(page_url)
        response.encoding = response.apparent_encoding
        bs = BeautifulSoup(response.text, 'lxml')
        time.sleep(1)

        with open('./crawled_file/baitoru_{}.html'.format(i), 'w') as file:
            file.write(response.text)
        if i%10 == 0:
            print("{}/".format(i)+page_num+"page")

if __name__ == "__main__":
    crwl()
