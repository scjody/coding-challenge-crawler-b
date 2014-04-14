import re

from scrapy.http import FormRequest
from scrapy.selector import Selector

from megabus.items import StopItem
from megabus.spiders.megabus_spider import MegabusSpider


class StopSpider(MegabusSpider):
    name = "megabus_stop"
    start_urls = [
        "http://ca.megabus.com/BusStops.aspx"
    ]

    def parse(self, response):
        """Initial parse function: extracts a list of stops and yields
        further requests that will get data on those stops."""

        return self.parse_stops(response, self.select_to)

    def select_to(self, response):
        """Parse a response where the "from" stop was selected in the
        request, and return a request with an appropriate "to" stop
        selected."""
        sel = Selector(response)
        stops = sel.css(
            '#confirm1_ddlTravellingTo option'
        ).xpath('@value')
        stops = [stop for stop in stops if stop != '-1']

        stop = stops[1].extract()
        return FormRequest.from_response(
            response,
            formdata={'confirm1$ddlTravellingTo': stop,
                      'confirm1$btnSearch': 'Search'},
            dont_click=True,
            callback=self.parse_stop_data
        )

    def parse_stop_data(self, response):
        """Parse stop data from a response where the "from" and "to"
        stops were selected in the request."""
        sel = Selector(response)

        stop_name = sel.css('#confirm1_hlFrom').xpath('text()').extract()[0]
        stop_location = sel.css('#divFrom').xpath('p[1]/text()').extract()[0]

        latlong = sel.re(r'Location\(([\d\.\-,]+)\)')[0]
        (stop_lat, stop_long) = latlong.split(',')

        return StopItem(
            stop_name=stop_name,
            stop_location=self.sanitize_stop_location(stop_location),
            lat=stop_lat,
            long=stop_long
        )

    def sanitize_stop_location(self, stop_location):
        """Sanitize a megabus stop location."""
        stop_location = stop_location.strip()

        stop_location = re.sub(r'The bus stop is located at the', '',
                               stop_location)
        stop_location = re.sub(r'In .* the bus stops at the', '',
                               stop_location)
        stop_location = re.sub(r'The .* is located (on|at|within)', '',
                               stop_location)
        stop_location = re.sub(r'The .* is situated at', '', stop_location)
        stop_location = re.sub(r'Arrivals and departures are located at', '',
                               stop_location)

        return stop_location.replace('\r\n', ' ').strip().capitalize()
