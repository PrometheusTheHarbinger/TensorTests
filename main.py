from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging

logger = logging.getLogger('pages')


class PageSearch:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('http://www.yandex.ru')
        logger.info("Search page initialized")

    def get_search_form(self):
        try:
            frame = self.driver.find_element(By.CSS_SELECTOR, '.dzen-search-arrow-common iframe')
            self.driver.switch_to.frame(frame)
            search_form = self.driver.find_element(By.CSS_SELECTOR, '.arrow__input.mini-suggest__input')
        except NoSuchElementException:
            search_form = None
        finally:
            return search_form

    def are_suggestions_up(self):
        return self.driver.find_element(By.CSS_SELECTOR, 'ul[id^="suggest-list"]').is_displayed()

    def search_button_click(self):
        self.driver.find_element(By.CSS_SELECTOR, '.arrow__button').click()

    def get_first_link(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.driver.find_element(By.CSS_SELECTOR, "#search-result li a")


class PagePictures:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('http://www.yandex.ru')
        logger.info("Picture page initialized")

    def get_picture_link(self):
        try:
            frame = self.driver.find_element(By.CSS_SELECTOR, '.dzen-search-arrow-common iframe')
            self.driver.switch_to.frame(frame)
            search_form = self.driver.find_element(By.CSS_SELECTOR, '.arrow__input.mini-suggest__input')
            search_form.click()
            return self.driver.find_element(By.LINK_TEXT, 'Картинки')
        except NoSuchElementException:
            return None

    def follow_picture_link(self):
        self.driver.switch_to.default_content()
        self.get_picture_link().click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def current_page_url(self):
        return self.driver.current_url

    def follow_popular_category(self):
        to_return = self.driver.find_element(By.CSS_SELECTOR, '.PopularRequestList-Item .PopularRequestList-SearchText').text
        self.driver.find_element(By.CSS_SELECTOR, '.PopularRequestList-Item .PopularRequestList-Shadow').click()
        return to_return

    def get_search_text(self):
        return self.driver.find_element(By.NAME, 'text').get_attribute("value")

    def get_big_picture(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.MediaViewer .MMImage-Origin')

    def open_first_picture(self):
        self.driver.find_element(By.CSS_SELECTOR, '.serp-item__preview img').click()

    def open_next_picture(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MediaViewer-ButtonNext i').click()

    def open_prev_picture(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MediaViewer-ButtonPrev i').click()
