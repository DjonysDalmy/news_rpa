import json

with open('./devdata/env.json', 'r') as f:
    config_data = json.load(f)
class Config:
    NEWS_SEARCH_TEXT = config_data.get('NEWS_SEARCH_TEXT', 'Brazi')
    NEWS_SEARCH_FILTER = config_data.get('NEWS_SEARCH_FILTER', 'Sports')
    NEWS_SEARCH_MONTHS = config_data.get('NEWS_SEARCH_MONTHS', 1) 