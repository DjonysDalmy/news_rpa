import time

from RPA.Browser.Selenium import By, Selenium
from src.logger import Logger
from src.utils import Utils
from src.config import Config
from src.variables import Variables

class News:
    def __init__(self):
        self.results = []
        self.capturing = True
        self.browser = Selenium()        
        self.browser_opts = {
            "arguments": ["--headless", "--disable-gpu"]
        }

    def start(self):
        Logger.info("🚀 Running News Robot Task")

        self.browser.open_available_browser(
            "https://www.latimes.com/", options=self.browser_opts
        )

        self.__search() #Search for news using filters and sorting 

        time.sleep(3)

        self.__capture() #Capture news from the search results

    def __search(self):
        Logger.info("🔎 Searching for News")
        
        self.browser.wait_until_element_is_visible(Variables.MAIN_SEARCH_BUTTON)
        self.browser.click_element(Variables.MAIN_SEARCH_BUTTON)

        self.browser.wait_until_element_is_visible(Variables.MAIN_SEARCH_INPUT)
        self.browser.input_text(Variables.MAIN_SEARCH_INPUT, Config.NEWS_SEARCH_TEXT)

        self.browser.click_element(Variables.MAIN_SEARCH_SUBMIT_BUTTON)
        
        Logger.info(f"🔎 Searching for: {Config.NEWS_SEARCH_TEXT}")

        self.__sort_by()

        if Config.NEWS_SEARCH_FILTER:
            self.__filter()

    def __sort_by(self):
        Logger.info("🔎 Sorting by newest")
        #Sort by newest by default
        self.browser.click_element_when_visible(Variables.RESULTS_SORT_BY_SELECT)
        self.browser.click_element(Variables.RESULTS_SORT_BY_SELECT_NEWEST_OPTION)

    def __filter(self):
        Logger.info("🔎 Filtering results")

        time.sleep(2)

        #Expand filters 1
        if self.browser.is_element_visible(Variables.RESULTS_FILTERS_1):
            self.browser.scroll_element_into_view(Variables.RESULTS_FILTERS_1)
            self.browser.click_element(Variables.RESULTS_FILTERS_1)

        #Expand filters 2
        if self.browser.is_element_visible(Variables.RESULTS_FILTERS_2):
            self.browser.scroll_element_into_view(Variables.RESULTS_FILTERS_2)
            self.browser.click_element(Variables.RESULTS_FILTERS_2)

        #Check filter
        Logger.info(f"🔎 Filtering by: {Config.NEWS_SEARCH_FILTER}")
        if self.browser.is_element_visible(Variables.RESULTS_FILTERS_CHECKBOX):
            self.browser.scroll_element_into_view(Variables.RESULTS_FILTERS_CHECKBOX)
            self.browser.click_element(Variables.RESULTS_FILTERS_CHECKBOX)

    def __capture(self):
        Logger.info("📰 Capturing news")
        
        Logger.info(f"📰 Capturing news from the last {Config.NEWS_SEARCH_MONTHS} months")

        try:
            page = 1

            while self.capturing:
                time.sleep(1)
                
                Logger.info(f"📰 Capturing page {page}")
                news = self.browser.get_webelements(Variables.RESULTS_NEWS_LIST_ITEM)

                for item in news:
                    if self.__capture_item(item):
                        break

                if self.capturing:
                    if self.browser.is_element_visible(Variables.RESULTS_NEXT_BUTTON):
                        self.browser.click_element(Variables.RESULTS_NEXT_BUTTON)
                        Logger.info("📰⏭️ Go to next page")
                        page += 1
                    else:
                        Logger.info("📰🛑 Stop capturing: No more pages")
                        self.capturing = False

            Logger.info(f"📰✅ Captured {len(self.results)} news")

        except Exception as e:
            Logger.error(f"🚨 An error occurred while capturing news: {e}")
            Logger.warning(f"📰⚠️ Captured {len(self.results)} news")

        finally:
            if self.results:
                Logger.info("📤 Exporting results to Excel")
                Utils.export_to_excel(self.results)
            else:
                Logger.warning("📤⚠️ No results to export")

    def __capture_item(self, item):
        try:
            timestamp = item.find_element(By.CLASS_NAME, Variables.RESULTS_NEWS_LIST_ITEM_CLASSNAMES["timestamp"]).get_attribute('data-timestamp')
            
            if not Utils.check_date(timestamp, Config.NEWS_SEARCH_MONTHS):
                Logger.info("📰🛑 Stop capturing: News are older than the specified months")
                self.capturing = False
                return True
                
            title = item.find_element(By.CLASS_NAME, Variables.RESULTS_NEWS_LIST_ITEM_CLASSNAMES["title"]).text

            description = item.find_element(By.CLASS_NAME, Variables.RESULTS_NEWS_LIST_ITEM_CLASSNAMES["description"]).text

            filename = None
            if item.find_elements(By.CLASS_NAME, Variables.RESULTS_NEWS_LIST_ITEM_CLASSNAMES["media"]):
                media = item.find_element(By.CLASS_NAME, Variables.RESULTS_NEWS_LIST_ITEM_CLASSNAMES["media"]).find_element(By.TAG_NAME, 'img').get_attribute('src')
                filename = Utils.download_file(media)

            count_search = Utils.count_search(Config.NEWS_SEARCH_TEXT, f"{title} {description}")

            contains_money = Utils.contains_money(f"{title} {description}")

            self.results.append({
                    "title": title,
                    "date": timestamp,
                    "description": description,
                    "filename": filename,
                    "count_search": count_search,
                    "contains_money": contains_money,
                })
            
        except Exception as e:
            Logger.error(f"🚨 An error occurred while capturing news: {e}")