import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options


class SeleniumSpider(scrapy.Spider):
    name = "selenium"
    allowed_domains = ["app.apollo.io"]
    start_urls = ["https://app.apollo.io/"]

    def parse(self, response):

        driver = webdriver.Chrome()
        driver.get(response.url) 

        driver.implicitly_wait(10)

        email_text_box = driver.find_element(by=By.NAME, value="email")
        password_text_box = driver.find_element(by=By.NAME, value="password")

        email_text_box.send_keys("<Your Email address>")
        password_text_box.send_keys("<Your Password>")

        print('hello')

        login_button = driver.find_element(by=By.CLASS_NAME, value = "zp-button.zp_zUY3r.zp_H_wRH")

        login_button.click()

        driver.implicitly_wait(10)

        search_button = driver.find_element(by=By.ID, value = "searcher")

        search_button.click()

        company_button = driver.find_elements(by=By.CLASS_NAME, value='zp-accordion-header.zp_LPwjF')

        company_button[4].click()

        time.sleep(1)

        is_known_button = driver.find_elements(by=By.CLASS_NAME, value = "zp_E2c6O")

        driver.execute_script("arguments[0].scrollIntoView();", is_known_button[1])
        is_known_button[1].click()

        time.sleep(10)

        for page_number in range(0, 5):

            emails_list = []

            access_email_buttons = driver.find_elements(by=By.CLASS_NAME, value="zp_RFed0")

            for single_button in access_email_buttons:

                access_button_clickable = single_button.find_element(by=By.CLASS_NAME, value="zp-button.zp_zUY3r.zp_n9QPr.zp_MCSwB")
                time.sleep(1)        
                access_button_clickable.click()

                try:
                    copy_email = driver.find_element(by=By.CLASS_NAME, value="zp-button.zp_zUY3r.zp_r4MyT.zp_LZAms.zp_sNqr4")
                    email_element = driver.find_element(by=By.CLASS_NAME, value="zp_t08Bv")
                    email = email_element.text
                    emails_list.append(email)
                    copy_email.click()
                except:
                    emails_list.append('Unknown')
                    pass
        
            page_source=driver.page_source

            response2 = scrapy.http.HtmlResponse(url=response.url, body=page_source, encoding='utf-8')

            for item in self.parse_detail(response2,emails_list):
                yield item

            next_page_button = driver.find_elements(by=By.CLASS_NAME, value='zp-button.zp_zUY3r.zp_MCSwB.zp_xCVC8')
                
            next_page_button[4].click()

            time.sleep(5)

    def parse_detail(self,response,emails_list):

        table = response.css('div.zp_DUflC tbody.zp_RFed0')
        emails_list=emails_list


        for detail, email in zip(table,emails_list):

            yield {

                    'name' : detail.css('td.zp_aBhrx a::text').extract()[0],
                    'email' : email,
                    'title' : detail.css('td.zp_aBhrx span.zp_Y6y8d::text').extract()[0],
                    'company' : detail.css('td.zp_aBhrx a.zp_WM8e5.zp_kTaD7::text').extract()[0],
                    'location' : detail.css('td.zp_aBhrx span.zp_Y6y8d::text').extract()[1],
                    '#employees' : detail.css('td.zp_aBhrx span.zp_Y6y8d::text').extract()[2],
                    'industry' : detail.css('td.zp_aBhrx span.zp_lm1kV span.zp_PHqgZ.zp_TNdhR::text').extract(),
                    'keyword' : detail.css('td.zp_aBhrx div.zp_HlgrG.zp_y8Gpn.zp_uuO3B span::text').extract()
                            
                }


            print('success')

        
