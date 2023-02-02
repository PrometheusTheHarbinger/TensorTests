import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import pytest
from main import PageSearch, PagePictures


logger = logging.getLogger('testing')


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    logger.info("Created driver")
    yield driver
    logger.info("Quitting...")
    driver.quit()


def test_search(browser):
    page = PageSearch(browser)
    search_input = page.get_search_form()  # Шаг 1
    if not search_input:
        logger.error('Search field is not present')
        assert search_input is not None  # Шаг 2
    logger.info("Found input field, typing")
    search_input.send_keys("ТЕНЗОР")  # Шаг 3
    try:
        WebDriverWait(browser, timeout=5).until(lambda driver: page.are_suggestions_up)
    except TimeoutError:
        logger.error("Suggestions' list is not present")
        assert page.are_suggestions_up() is True  # Шаг 4
    logger.info("Pressing search button")
    page.search_button_click()  # Шаг 5
    assert page.get_first_link().get_attribute("href") == "https://tensor.ru/"  # Шаг 6


def test_pictures(browser):
    browser.implicitly_wait(3)
    page = PagePictures(browser)  # Шаг 1
    pics_link = page.get_picture_link()
    if not pics_link:
        logger.error("No link to picture subpage found")
        assert pics_link is not None  # Шаг 2
    page.follow_picture_link()  # Шаг 3
    logger.info("Followed the link to images subpage")
    assert page.current_page_url().startswith("https://yandex.ru/images/") is True  # Шаг 4
    category_name = page.follow_popular_category()  # Шаг 5
    logger.info("Clicked on most popular category")
    assert page.get_search_text() == category_name  # Шаг 6
    page.open_first_picture()  # Шаг 7
    logger.info("Opened first picture")
    first_pic = page.get_big_picture().get_property("src")
    assert bool(first_pic) is True  # Шаг 8
    page.open_next_picture()  # Шаг 9
    logger.info("Went to the next one")
    assert page.get_big_picture().get_property("src") != first_pic  # Шаг 10
    page.open_prev_picture()  # Шаг 11
    logger.info("Returned back to the first one")
    assert page.get_big_picture().get_property("src") == first_pic  # Шаг 12
    browser.implicitly_wait(0)
