#!/usr/bin/env python
# -*- coding: utf-8
import argparse
import datetime
import os

from scraper import scrape_stops, scrape_routes, scrape_departures

def parse_date(s):
    """Parse a date string

    Arguments:
    s -- Date as string in format: YYYY-MM-DD
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def today(offset=0):
    """Get today's date, with an optional offset

    Keyword arguments:
    offset -- offset the number of days to offset from today (default 0)
    """
    return datetime.date.today() + datetime.timedelta(days=offset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl web site.')
    parser.add_argument('--extract', required=True, choices=['stops', 'routes', 'departures'],
                        help='the type of extraction to perform')
    parser.add_argument('--output', required=True,
                        help='the path of the output file to generate')
    parser.add_argument('--startdate', required=False, type=parse_date, default=today(),
                        help='the beginning of the departure date range')
    parser.add_argument('--enddate', required=False, type=parse_date, default=today(7),
                        help='the end of the departure date range')
    parser.add_argument('--routes', required=False, default='routes.json',
                        help='the file containing route data for departures mode')

    args = parser.parse_args()
    output = os.path.abspath(args.output)

    if args.extract == 'stops':
        print 'Downloading stops to {}'.format(output)
        scrape_stops(output)

    elif args.extract == 'routes':
        print 'Downloading routes to {}'.format(output)
        scrape_routes(output)

    elif args.extract == 'departures':
        print ('Downloading departures to {0} for dates {1} through {2} '
               'for routes in {3}').format(output, args.startdate,
                                           args.enddate, args.routes)
        scrape_departures(output, args.startdate, args.enddate,
                          args.routes)
