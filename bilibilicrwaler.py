'''
@ File Name     :   bilibilicrwaler.py
@ Time          :   2022/10/06
@ Author        :   Cheng Kaiyue
@ Version       :   1.0
@ Contact       :   chengky18@icloud.com
@ Description   :   None
@ Function List :   func1() -- func desc1
@ Class List    :   Class1 -- class1 desc1
@ Details       :   None
'''

import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class BilibiliCrawler:
    def __init__(self, url, save_path):

        self.url = url
        self.save_path = save_path
        self.main_window = None
        with open(self.save_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["标题", "播放量", "弹幕数", "点赞", "投币", "收藏"])

    def settings(self):

        self.opt = Options()
        self.opt.add_argument("--windwos-size=2560, 1440")

    def start_browser(self):

        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.opt
        )
        self.browser.get(self.url)
        time.sleep(30)
        self.main_window = self.browser.current_window_handle

    def close_browser(self):

        self.browser.quit()

    def get_page_num(self):

        page_num = self.browser.find_element(
            by=By.CSS_SELECTOR,
            value="#submit-video-list > ul.be-pager > span.be-pager-total",
        ).text
        return int(page_num[2:-3])

    def next_page(self):

        self.browser.find_element(
            by=By.CSS_SELECTOR,
            value="#submit-video-list > ul.be-pager > li.be-pager-next",
        ).click()
        self.main_window = self.browser.current_window_handle

    def get_one_video(self, video):
        video.click()
        self.browser.switch_to.window(self.browser.window_handles[-1])
        time.sleep(0.1)
        try:
            like_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.like.on > span",
            ).text
        except:
            like_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.like > span",
            ).text
        try:
            coin_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.coin.on > span",
            ).text
        except:
            coin_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.coin > span",
            ).text
        try:
            collect_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.collect.on > span",
            ).text
        except:
            collect_data = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value="#arc_toolbar_report > div.toolbar-left > span.collect > span",
            ).text
        # share_data = self.browser.find_element(
        #     by=By.CSS_SELECTOR,
        #     value="#share-btn-outer > div > span",
        # ).text
        title_data = self.browser.find_element(
            by=By.CSS_SELECTOR,
            value="#viewbox_report > h1",
        ).text
        view_data = self.browser.find_element(
            by=By.CSS_SELECTOR, value="#viewbox_report > div > div > span.view.item"
        ).get_attribute("title")[4:]
        dm_data = self.browser.find_element(
            by=By.CSS_SELECTOR, value="#viewbox_report > div > div > span.dm.item"
        ).get_attribute("title")[7:]
        with open(self.save_path, "a+", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    title_data,
                    view_data,
                    dm_data,
                    like_data,
                    coin_data,
                    collect_data,
                ]
            )
        self.browser.close()
        time.sleep(0.01)
        self.browser.switch_to.window(self.main_window)
        time.sleep(0.01)

    def get_main_data(self):

        video_list_page = self.browser.find_element(
            by=By.XPATH, value='//*[@id="submit-video-list"]/ul[2]'
        )
        video_list = video_list_page.find_elements(by=By.XPATH, value="li/a[2]")
        for video in video_list:
            self.get_one_video(video)