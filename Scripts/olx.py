from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import config
import time
import pages
import uuid

class Olx:
    def __init__(self, loadTimes = 2 ):
        self.links = []
        self.phoneNumbers = []
        self.username = config.USERNAME
        self.password = config.PASSWORD
        self.path = config.CHROME_DRIVER
        self.loadAds = loadTimes
        self.driver = webdriver.Chrome(self.path)

        self.driver.get(config.OLX_URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

        self.load_all_adds()
        time.sleep(2)

        self.log_in()
        time.sleep(2)


        pagesource = self.driver.page_source
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_links = soup.find_all('a', class_='fhlkh')
        for a in all_links:
            href = a.get('href')
            self.links.append(href)
        
        self.get_number()
    
    def get_number(self):
        try:
            print(len(self.links))
            host = "https://www.olx.co.id"
            for val in self.links:
                targetUrl = host + val
                self.driver.get(targetUrl)
                self.wait.until(lambda driver:driver.find_element_by_xpath(pages.btnShowNmbr))
                self.driver.find_element_by_xpath(pages.btnShowNmbr).click()
                self.wait.until(lambda driver:driver.find_element_by_xpath(pages.phoneNumbers))
                waNmbr = self.driver.find_element_by_xpath(pages.phoneNumbers).text
                print (waNmbr)


        except NoSuchElementException as e:
            print (e)

    
    def log_in(self):
        try:
            elemLogo = self.wait.until(lambda driver:driver.find_element_by_xpath(pages.olxLogo))
            self.driver.find_element_by_xpath(pages.btnLogin).click()
            self.wait.until(lambda driver:driver.find_element_by_xpath(pages.emailLoginMethod))
            self.driver.find_element_by_xpath(pages.emailLoginMethod).click()
            username = self.driver.find_element_by_name("email")
            username.send_keys(self.username)
            username.send_keys(Keys.RETURN)

            self.wait.until(lambda driver:driver.find_element_by_xpath(pages.btnNextLogin))
            elemPass = self.driver.find_elements_by_xpath(pages.lblPass)
            elemPass[0].send_keys(self.password)
            elemPass[0].send_keys(Keys.RETURN)

            #when Logged in
            self.wait.until(lambda driver:driver.find_elements_by_xpath(pages.popUpAfterLogin))
            (self.driver.find_elements_by_xpath(pages.popUpAfterLogin)[0]).click()
            self.wait.until(lambda driver:driver.find_element_by_xpath(pages.olxLogo))

        except NoSuchElementException as e:
            print (e)
    
    def load_all_adds(self):
        try:
            for val in range(self.loadAds):
                load_more = self.driver.find_element_by_xpath("//span[.='muat lainnya']")
                time.sleep(2)
                load_more.click()
                time.sleep(3)
        except Exception:
            pass

if __name__ == '__main__':
    olx = Olx()