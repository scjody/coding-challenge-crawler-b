from scrapy.selector import Selector

from megabus.items import RouteItem
from megabus.spiders.megabus_spider import MegabusSpider


class RouteSpider(MegabusSpider):
    name = "megabus_route"
    start_urls = [
        "http://ca.megabus.com/BusStops.aspx"
    ]

    def parse(self, response):
        """Initial parse function: extracts a list of stops and yields
        further requests that will get routes from those stops."""

        return self.parse_stops(response, self.parse_routes)

    def parse_routes(self, response):
        """Parse route data from a response where the "from" stop was
        selected in the request."""

        sel = Selector(response)

        origin = sel.xpath("//select[@id='confirm1_ddlLeavingFromMap']"
                           "//option[@selected]/text()").extract()[0]
        destinations = sel.css("#confirm1_ddlTravellingTo "
                               "option").xpath("text()").extract()
        destinations = [dest for dest in destinations if dest != 'Select']

        for destination in destinations:
            yield RouteItem(
                origin=origin,
                destination=destination
            )
