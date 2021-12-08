# 首先pip install selenium
# 然后下载chromedriver.exe放在conda环境中的Scripts文件夹中

from selenium import webdriver
import time
import os
import requests
import threading

# 使用代理的方法 ，可以直接windows使用代理，不用这么麻烦
# browserOptions = webdriver.ChromeOptions()
# browserOptions.add_argument('--proxy-server=ip:port)
# browser = webdriver.Chrome(chrome_options=browserOptions)

#修改keyword便可以修改搜索关键词
keywords = ['杨洋', '迪丽热巴', '古力娜扎', '王力宏', '周杰伦', '林俊杰', '王俊凯', '庆怜', '米卡',
            '谢娜', '何炅', '金晨', '鞠婧祎', '邓紫棋', '关晓彤', '赵丽颖', '蔡徐坤', '陈立农', '许佳琪',
            '张新成', '宋威龙', '孙艺珍']
keywords_2 = ['李承铉', '陈小春', '吴昕', '宋慧乔', '胡一天', '杨幂', 'Angelababy', '李晨', '宋小宝', '贾玲']


class Crawler_google_images(threading.Thread):
    # 初始化
    def __init__(self, url, save_folder, count, nums):
        threading.Thread.__init__(self)
        self.url = url
        self.save_folder = save_folder
        self.count = count
        self.nums = nums

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    #下载图片
    def download_images(self, browser):
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []

        pos = 0
        i = 0
        while(i < self.nums):
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)
            # 找到图片
            # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
            #直接通过tag_name来抓取是最简单的，比较方便
            img_elements = browser.find_elements_by_tag_name('img')
            #遍历抓到的webElement
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        #将干扰的goole图标筛去
                        if 'images' in img_url:
                            #判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                            #实际上这里可以修改一下，将列表只存储上一次的url，这样可以节省开销，不过我懒得写了···
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    #下载并保存图片到当前目录下
                                    filename = self.save_folder + '2_' + str(self.count) + ".jpg"
                                    r = requests.get(img_url)
                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    self.count += 1
                                    i += 1
                                    print('this is '+str(self.count)+'st img')
                                    #防止反爬机制
                                    time.sleep(0.2)
                                except:
                                    print('failure')


    def run(self):
        browser = self.init_browser()
        self.download_images(browser)#可以修改爬取的页面数，基本10页是100多张图片
        browser.close()
        print("爬取完成")


if __name__ == '__main__':
    save_folder = 'D:/datasets/debug/'
    for i, keyword in enumerate(keywords_2):
        url = 'https://www.google.com.hk/search?q='+keyword+'&tbm=isch'
        thread = Crawler_google_images(url, save_folder, i * 1000, 1000)
        thread.start()
        # craw = Crawler_google_images(url, save_folder, i * 1000, 1000)
        # craw.run()
