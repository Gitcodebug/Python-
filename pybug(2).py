from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options,executable_path='d:\chromedriver.exe')
driver.implicitly_wait(100)
url = 'https://book.douban.com/annual/2018?source=navigation'
driver.get(url)
title = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[3]/h2/a')
bookpage = title.get_attribute('href')
driver.get(bookpage)
image = driver.find_element_by_xpath('//*[@id="mainpic"]/a/img')
address = image.get_attribute('src')
bookname = image.get_attribute('alt')
# 在这里将image、address、bookname插入数据库


print(bookname)
driver.back()
# book_list = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/ul')
books = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/ul/li/a')
# print(len(books))
book_hrefs = []
for book in books:
    # print('\n'.join(['%s:%s' % item for item in book.__dict__.items()]))
    # print('++++++++++')
    # print(book.get_attribute('href'))
    book_hrefs.append(book.get_attribute('href'))

for book_href in book_hrefs:
    driver.get(book_href)
    image = driver.find_element_by_xpath('//*[@id="mainpic"]/a/img')
    address = image.get_attribute('src')
    bookname = image.get_attribute('alt')
    print(bookname)
    print(address)
    # 在这里将image、address、bookname插入数据库

driver.quit()