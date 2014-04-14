# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StopItem(Item):
    """Bus stop data."""
    stop_name = Field()
    stop_location = Field()
    lat = Field()
    long = Field()


class RouteItem(Item):
    """An origin-destination pair of bus stops."""
    origin = Field()
    destination = Field()


class DepartureItem(Item):
    """Information on one departure from a particular stop."""
    origin = Field()
    destination = Field()
    departure_time = Field()
    arrival_time = Field()
    duration = Field()
    price = Field()
