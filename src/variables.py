from src.config import Config

class Variables:

    #Main Page
    MAIN_SEARCH_BUTTON = '//button[@data-element="search-button"]'
    MAIN_SEARCH_FORM = '//form[@data-element="search-form"]'
    MAIN_SEARCH_INPUT = f'{MAIN_SEARCH_FORM}//input[@data-element="search-form-input"]'
    MAIN_SEARCH_SUBMIT_BUTTON = f'{MAIN_SEARCH_FORM}//button[@data-element="search-submit-button"]'

    #Results Page
    RESULTS_SORT_BY_SELECT = '//div[@class="search-results-module-sorts"]//select'
    RESULTS_SORT_BY_SELECT_NEWEST_OPTION = f'{RESULTS_SORT_BY_SELECT}//option[@value="1"]'

    RESULTS_FILTERS_1 = '//div[@class="search-results-module-filters-content SearchResultsModule-filters-content"]/div[1]//button'
    RESULTS_FILTERS_2 = '//div[@class="search-results-module-filters-content SearchResultsModule-filters-content"]/div[2]//button'
    RESULTS_FILTERS_CHECKBOX = f"//label[span[text()='{Config.NEWS_SEARCH_FILTER}']]/input"

    RESULTS_NEWS_LIST_ITEM = '//ul[@class="search-results-module-results-menu"]//li'

    RESULTS_NEWS_LIST_ITEM_CLASSNAMES = {
        "title": "promo-title",
        "description": "promo-description",
        "timestamp": "promo-timestamp",
        "media": "promo-media"
    }

    RESULTS_NEXT_BUTTON = '//div[@class="search-results-module-next-page"]/a'
