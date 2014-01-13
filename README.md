# Objective

Write a crawler for Megabus Canada that can extract:
* list of stops
* list of routes
* list of departures

## Step 1: get stops

This process is done once to create a mapping between their stops and ours.

From this [page](http://ca.megabus.com/BusStops.aspx), get the list of all bus stops including the address, latitude and longitude.  The output should be stored in a `stops.json` and the schema should be something like this:

```json
[
	{
		"stop_name": "Hamilton McMaster University, ON",
		"stop_location":"McMaster University at Mary Keyes and Cootes Drive",
		"lat":43.258736,
		"long":-79.92245
	}
]
```

The step should be invoked like so

```sh
python run.py --extract stops --output stops.json
```

## Step 2: get routes

This process is done once to get the list of all possible routes with departures from this operator.

From this [page](http://ca.megabus.com/BusStops.aspx), get the list of all possible routes, i.e., all valid stop pairings.  The output should stored in `routes.json` and the schema should be something like this:

```json
[
	{
		"origin": "Hamilton McMaster University, ON",
		"destination":"Cambridge, ON",
	},
	{
		"origin": "Hamilton McMaster University, ON",
		"destination":"Kitchener, ON",
	},
	{
		"origin": "Hamilton McMaster University, ON",
		"destination":"Waterloo, ON",
	}
]
```

The step should be invoked like so

```sh
python run.py --extract routes --output routes.json
```


## Step 3: get departures

This process is done repeatedly to update our database of departure. As an input, this function should accept an origin, destination and a range of dates for which departures will be returned.

1. Go to this [page](http://ca.megabus.com/Default.aspx)
1. For each route in the list generated in step 2, get the list of all one-way departures for one passenger.
1. For each departure extract the following information:

	* departure time
	* arrival time
	* duration
	* adult one-way price

The output should be stored in `departures.json` and the schema should look something like this:

```json
[
	{
		"origin": "Beamsville, ON",
		"destination": "Hamilton GO Centre, ON",
		"departure_time": "2013-06-05T07:20:00",
		"arrival_time": "2013-06-05T08:15:00",
		"duration": "0:55",
		"price": 5.00
	}
]
```

The step should be invoked like so

```sh
python run.py --extract departures --output departures.json --startdate 2013-11-13 --enddate 2013-11-20
```

# Non-functional requirements

* the code should be written in Python and compatible with Python 2.7.
* the code should be hosted on github, and the repo should be shared with Busbud
* the code should be written in a way that it can easily be extended to become a scheduled process that updates our
database of departure
* any packages required must be installable via `pip install -r requirements.txt`, see [pip](http://www.pip-installer.org/en/latest/)