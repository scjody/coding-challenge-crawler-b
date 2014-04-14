#!/usr/bin/env python

import json
import os

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from megabus.spiders.stop_spider import StopSpider
from megabus.spiders.route_spider import RouteSpider
from megabus.spiders.departure_spider import DepartureSpider


def scrape_stops(output):
    """
    Download stops to a file.

    :param output: filename for output (will be overwritten)
    """
    spider = StopSpider()
    scrape(spider, output)


def scrape_routes(output):
    """
    Download routes to a file.

    :param output: filename for output (will be overwritten)
    """
    spider = RouteSpider()
    scrape(spider, output)


def scrape_departures(output, start_date, end_date, route_filename):
    """
    Download departures to a file.

    :param output: filename for output (will be overwritten)
    :param start_date: start date
    :param end_date: end date
    :param route_filename: filename for route data in JSON format
    """

    route_file = open(route_filename)
    routes = json.load(route_file)

    spider = DepartureSpider(start_date, end_date, routes)
    scrape(spider, output)


def scrape(spider, output):
    """
    Run the given spider, producing JSON output.

    :param spider: an initialized Spider
    :param output: a filename for JSON output (will be overwritten)
    """
    try:
        os.unlink(output)
    except OSError:
        pass

    settings = get_project_settings()
    settings.overrides['FEED_FORMAT'] = 'json'
    settings.overrides['FEED_URI'] = output
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    #log.start(loglevel=log.DEBUG)
    reactor.run()
