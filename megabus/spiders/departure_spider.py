from datetime import datetime, timedelta
import re

from scrapy.http import FormRequest
from scrapy.selector import Selector

from megabus.items import DepartureItem
from megabus.spiders.megabus_spider import MegabusSpider


class DepartureSpider(MegabusSpider):
    name = "megabus_departure"
    start_urls = [
        "http://ca.megabus.com/Default.aspx"
    ]

    def __init__(self, start_date, end_date, routes, *args, **kwargs):
        """
        :param start_date: start date
        :param end_date: end date
        :param routes: list of {origin: "String", destination: "String"}
        """

        super(DepartureSpider, self).__init__(*args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date
        self.routes = routes

    def parse(self, response):
        """Initial parse function: yield requests to find all departures
        from all routes on all dates in the range."""

        delta = timedelta(days=1)

        loc_map = self.parse_loc_map(response)

        for route in self.routes:
            date = self.start_date
            while date <= self.end_date:
                date_str = date.strftime('%d/%m/%Y')
                from_value = loc_map[route['origin']]
                to_value = loc_map[route['destination']]

                yield FormRequest(
                    url='http://ca.megabus.com/JourneyResults.aspx',
                    method='GET',
                    formdata={
                        'originCode': from_value,
                        'destinationCode': to_value,
                        'outboundDepartureDate': date_str,
                        'passengerCount': '1',
                    },
                    callback=self.parse_departures,
                    meta={
                        'origin': route['origin'],
                        'destination': route['destination'],
                        'date': date
                    }
                )

                date += delta

    def parse_loc_map(self, response):
        """Returns a location map based on response:
        a dictionary mapping location strings to <option> values"""
        loc_map = {}

        sel = Selector(response)
        for option in sel.css('#JourneyPlanner_ddlLeavingFrom option'):
            location = option.xpath('text()').extract()[0]
            value = option.xpath('@value').extract()[0]
            loc_map[location] = value

        return loc_map

    def parse_combine_dt(self, date, time_str):
        """Parses the time and combines it with the date"""
        time = datetime.strptime(time_str, "%H:%M").time()
        return datetime.combine(date, time)

    def parse_departures(self, response):
        """Parse departure data from a response where departure data
        was set in the request."""

        sel = Selector(response)

        for departure in sel.css('ul.journey.standard'):
            date = response.meta['date']

            departure_time_str = departure.css('.two').re(r'\d\d:\d\d')[0]
            departure_dt = self.parse_combine_dt(date, departure_time_str)

            arrival_time_str = departure.css('.two .arrive').re(r'\d\d:\d\d')[0]
            arrival_dt = self.parse_combine_dt(date, arrival_time_str)

            if departure_dt > arrival_dt:
                arrival_dt += timedelta(days=1)

            duration_str = departure.css('.three p').xpath(
                'text()'
            ).extract()[0].strip()
            match = re.match(r'(\d+)hrs (\d+)mins', duration_str)
            duration_hours = int(match.group(1))
            duration_mins = int(match.group(2))

            price = departure.css('.five p').xpath(
                'text()'
            ).extract()[0].strip('\n\r\t $')

            yield DepartureItem(
                origin=response.meta['origin'],
                destination=response.meta['destination'],
                departure_time=departure_dt.isoformat(),
                arrival_time=arrival_dt.isoformat(),
                duration="%d:%02d" % (duration_hours, duration_mins),
                price=price
            )
