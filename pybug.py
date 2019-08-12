from reading import db
from reading.models import RankedBooks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def clawler():
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
    db.session.add(RankedBooks(bookname,address))
    print(address)
    print(bookname)
    # driver.get(url)
    # lies = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/ul').find_elements_by_tag_name('li')
    # for li in lies:
    #     bookpage = li.find_element_by_tag_name('a').get_attribute('href')
    #     print(bookpage)
    #     print('-------------------')
    #     driver.get(bookpage)
    #     image = driver.find_element_by_xpath('//*[@id="mainpic"]/a/img')
    #     address = image.get_attribute('src')
    #     bookname = image.get_attribute('alt')
    #     db.session.add(RankedBooks(bookname,address))

    db.session.commit()