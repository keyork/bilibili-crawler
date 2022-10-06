"""
@ File Name     :   run.py
@ Time          :   2022/10/06
@ Author        :   Cheng Kaiyue
@ Version       :   1.0
@ Contact       :   chengky18@icloud.com
@ Description   :   None
@ Function List :   func1() -- func desc1
@ Class List    :   Class1 -- class1 desc1
@ Details       :   None
"""

import time
from bilibilicrwaler import BilibiliCrawler

if __name__ == "__main__":
    crawler = BilibiliCrawler(
        "https://space.bilibili.com/674510452/video", "data_月亮3.csv"
    )
    crawler.settings()
    crawler.start_browser()
    page_num = crawler.get_page_num()
    for i in range(page_num):
        crawler.get_main_data()
        if i != page_num - 1:
            crawler.next_page()
        time.sleep(0.7)
    time.sleep(100)
    crawler.close_browser()
