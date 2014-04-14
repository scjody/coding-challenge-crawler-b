from scrapy.contrib.spiders.init import InitSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest


class MegabusSpider(InitSpider):
    allowed_domains = ["ca.megabus.com"]
    landing_url = "http://ca.megabus.com/landingcanada.aspx"

    def init_request(self):
        """This function is called before crawling starts.  Request the
        landing page, so we can select a language."""
        return Request(url=self.landing_url, callback=self.select_lang)

    def select_lang(self, response):
        """Select a language on the landing page."""
        return FormRequest.from_response(response,
                                         formdata={'btnEnglishCanada': ''},
                                         callback=self.initialized)

    def parse_stops(self, response, callback):
        """
        Extract a list of stops and yield a FormRequest for each stop.
        (Helper function shared between subclasses)

        :param response: a Response object containing stops
        :param callback: callback sent to the FormRequest
        """
        sel = Selector(response)
        stops = sel.css(
            '#confirm1_ddlLeavingFromMap option'
        ).xpath('@value').extract()
        stops = [stop for stop in stops if stop != '-1']

        for stop in stops:
            yield FormRequest.from_response(
                response,
                formdata={'confirm1$ddlLeavingFromMap': stop},
                callback=callback
            )
