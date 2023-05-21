import scrapy
from mainScraper.mainScraper.json_handlers.match_ids_extractor import retrieve_matches_ids, loadAndSave
from mainScraper.mainScraper.items import MainscraperItem
from tqdm import tqdm

class PresentLineupsSpider(scrapy.Spider):
    name = "present_lineups"

    def __init__(self):
        print("collecting lineups teams data :")
        self.start_urls = ['https://api.sofascore.com/api/v1/event/' + str(i) + '/lineups' for i in retrieve_matches_ids()]

    def start_requests(self):
        with tqdm(total=len(self.start_urls)) as pbar:
            for url in self.start_urls:
                pbar.update(1)
                yield scrapy.Request(url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        item = MainscraperItem()
        mainJson = loadAndSave(response.text, response.url)
        match_Id = str(response.url).split("/")[-2]
        if mainJson is not None:
            item['matchId'] = match_Id
            item["lineups"] = mainJson
            yield item

