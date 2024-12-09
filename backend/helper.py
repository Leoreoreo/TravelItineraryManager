import csv
from datetime import datetime

# this is to convert csv (stores all trip data) into an array of dictionaries to later push into the psql db
def validate_row(start_date, end_date, start_time, end_time, event_type, location, location_start, location_end, weather):
	try:
		datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
		datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
		if start_date and end_date:
			datetime.strptime(start_date, "%Y-%m-%d")
			datetime.strptime(end_date, "%Y-%m-%d")

	except ValueError:
		# print("incorrect time format")
		# print(f"{start_date}, {end_date}, {start_time}, {end_time}")
		return False
	
	if event_type != "commute" and event_type != "stop": 
		return False
	if len(location) > 50 or len(location_start) > 50 or len(location_end) > 50 or len(weather)> 50: return False
	return True


def csv_to_trips(filename):
	trip_data = []
	prev_trip_name = ""
	i = -1
	bad_rows = 0
	total_rows = 0

	with open(filename, mode='r', newline='') as file:
		# trip_Nature_21_size_300.csv
		pref = filename.split('_')[1]
		age = filename.split('_')[2]
		reader = csv.DictReader(file)
		
		# for each row
		for row in reader:
			# print(row)
			trip_name = row["trip_name"]
			total_rows += 1
			# new trip
			if not validate_row(row["start_date"], row["end_date"], row["start_time"], row["end_time"], row["event_type"], row["location"], row["location_start"], row["location_end"], row["preferred_weather"]):
				bad_rows += 1
				continue
			
			if trip_name != prev_trip_name:
				i += 1
				prev_trip_name = trip_name
				trip_data.append({
					"trip_name": trip_name,
					"user_pref": pref,
					"age": age,
					"start_date": row["start_date"],
					"end_date": row["end_date"],
					"events": []
				})
			
			trip_data[i]["events"].append({
				"type": row["event_type"],
				"start_time": row["start_time"],
				"end_time": row["end_time"],
				"location": row["location"],
				"location_start": row["location_start"],
				"location_end": row["location_end"],
				"mode": row["mode"],
				"preferred_weather": row["preferred_weather"]
			})
			
	print(f"failed rows: {bad_rows}")
	print(f"total rows: {total_rows}")
	return trip_data




def get_sys_instr():
	system_instruction = '''
You are tasked with generating a trip itinerary. You will be given additional requirements, so follow them. You will only be asked to create one trip at a time, so try to make creative and new trips. If you follow this and make a good trip, you can win $1000. Only use the english language.

Follow these steps to create your trip itinerary:
1. For the beginning of the trip, the first stop you make is checking into your accomodation. The last stop of your trip is checking out.
For each day of your trip:
2. Start your day by leaving your accommodation at a random time between 9 AM and 3 PM. Plan to be out for 6 to 10 hours, visiting 3 to 6 locations or events, and coming back to your accomodation.
3. For each event (which can be either a stop or commute) that must exist in Chicago and in english:
  a. Stop: Include details: start_time, end_time, title, exact location.
  b. Commute: Include start location, end location, mode of transportation (that makes sense), and travel duration.
4. Around lunchtime and dinnertime, select a nearby restaurant as one of your stops.
5. Ensure each event's end_time aligns with the following event's start_time.
6. Ensure each place you stop is real, in english, and in Chicago.
7. Make a unique trip name and a random start date with the end date 1 day after.

RULES:
Please ensure that for every event, the start_time and end_time must strictly follow this format: <YYYY-MM-DD HH:MM:SS>. I repeat, ensure that the time formats adhere strictly to this format: <YYYY-MM-DD HH:MM:SS>. 
You must NOT include '\n', '\t', excess spaces or any newline or tab characters to your response. I repeat, do not include excess spaces or any newline or tab characters in your response.
Please ensure that you stick strictly to english. 
Please ensure each event detail (e.g. location) should have no more than 50 characters.
Please please please make sure you add the exact location (include city, state) so that the location can be searched and retrieved from google maps api.
If you don't, I will take $100 from you if any of these are breached.


For reference, here is an example trip itinerary formatted in JSON:

{
  "trip_name": "Adventurer's Urban Quest",
  "start_date": "2023-11-01",
  "end_date": "2023-11-02",
  "events": [
	{
	  "type": "stop",
	  "start_time": "2023-11-01 15:00:00",
	  "end_time": "2023-11-01 15:30:00",
	  "location": "Freehand Chicago",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "CLOUDY",
	  "mode": ""
	},
	{
	  "type": "commute",
	  "start_time": "2023-11-01 15:30:00",
	  "end_time": "2023-11-01 16:00:00",
	  "location": "",
	  "location_start": "Freehand Chicago",
	  "location_end": "Millennium Park",
	  "preferred_weather": "CLOUDY",
	  "mode": "WALK"
	},
	{
	  "type": "stop",
	  "start_time": "2023-11-01 16:00:00",
	  "end_time": "2023-11-01 18:00:00",
	  "location": "Millennium Park",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "CLOUDY",
	  "mode": ""
	},
	
	{
	  "type": "commute",
	  "start_time": "2023-11-01 18:00:00",
	  "end_time": "2023-11-01 18:15:00",
	  "location": "",
	  "location_start": "Millennium Park",
	  "location_end": "Portillo's Hot Dogs",
	  "preferred_weather": "CLOUDY",
	  "mode": "WALK"
	},
	{
	  "type": "stop",
	  "start_time": "2023-11-01 18:15:00",
	  "end_time": "2023-11-01 19:15:00",
	  "location": "Portillo's Hot Dogs",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "CLOUDY",
	  "mode": ""
	},
	
   {
	  "type": "commute",
	  "start_time": "2023-11-01 19:15:00",
	  "end_time": "2023-11-01 19:30:00",
	  "location": "",
	  "location_start": "Portillo's Hot Dogs",
	  "location_end": " The Field Museum",
	  "preferred_weather": "CLOUDY",
	  "mode": "BUS"
	},
	
	{
	  "type": "stop",
	  "start_time": "2023-11-01 19:30:00",
	  "end_time": "2023-11-01 21:30:00",
	  "location": "The Field Museum",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "CLOUDY",
	  "mode": ""
	},
	
	{
	  "type": "commute",
	  "start_time": "2023-11-01 21:30:00",
	  "end_time": "2023-11-01 21:45:00",
	  "location": "",
	  "location_start": "The Field Museum",
	  "location_end": "Freehand Chicago",
	  "preferred_weather": "CLOUDY",
	  "mode": "WALK"
	},
	
	{
	  "type": "stop",
	  "start_time": "2023-11-01 21:45:00",
	  "end_time": "2023-11-02 09:00:00",
	  "location": "Freehand Chicago",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "CLOUDY",
	  "mode": ""
	},
			
	{
	  "type": "commute",
	  "start_time": "2023-11-02 09:00:00",
	  "end_time": "2023-11-02 09:30:00",
	  "location": "",
	  "location_start": "Freehand Chicago",
	  "location_end": "Navy Pier",
	  "preferred_weather": "SUNNY",
	  "mode": "BUS"
	},
	
	{
	  "type": "stop",
	  "start_time": "2023-11-02 09:30:00",
	  "end_time": "2023-11-02 12:00:00",
	  "location": "Navy Pier",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "SUNNY",
	  "mode": ""
	},
	
	{
	  "type": "commute",
	  "start_time": "2023-11-02 12:00:00",
	  "end_time": "2023-11-02 12:20:00",
	  "location": "",
	  "location_start": "Navy Pier",
	  "location_end": "Lou Malnati's Pizzeria",
	  "preferred_weather": "SUNNY",
	  "mode": "WALK"
	},
	
	{
	  "type": "stop",
	  "start_time": "2023-11-02 12:20:00",
	  "end_time": "2023-11-02 13:20:00",
	  "location": "Lou Malnati's Pizzeria",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "SUNNY",
	  "mode": ""
	
  {
	  "type": "commute",
	  "start_time": "2023-11-02 13:20:00",
	  "end_time": "2023-11-02 13:40:00",
	  "location": "",
	  "location_start": "Lou Malnati's Pizzeria",
	  "location_end": "Lincoln Park Zoo",
	  "preferred_weather": "SUNNY",
	  "mode": "BUS"
	},
	
	{
	  "type": "stop",
	  "start_time": "2023-11-02 13:40:00",
	  "end_time": "2023-11-02 15:00:00",
	  "location": "Lincoln Park Zoo",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "SUNNY",
	  "mode": ""
	},
	
   {
	  "type": "commute",
	  "start_time": "2023-11-02 15:00:00",
	  "end_time": "2023-11-02 15:20:00",
	  "location": "",
	  "location_start": "Lincoln Park Zoo",
	  "location_end": "Piccolo Sogeuno Italiano",
	  "preferred_weather": "SUNNY",
	  "mode": "WALK"
	},

 {
	  "type": "stop",
	  "start_time": "2023-11-02 15:20:00",
	  "end_time": "2023-11-02 16:20:00",
	  "location": "Piccolo Sogno Italiano",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "SUNNY",
	  "mode": ""
	},
 
 {
	  "type": "commute",
	  "start_time": "2023-11-02 16:20:00",
	  "end_time": "2023-11-02 16:30:00",
	  "location": "",
	  "location_start": "Piccolo Sogno Italiano",
	  "location_end": "Freehand Chicago",
	  "preferred_weather": "SUNNY",
	  "mode": "WALK"
	},

	{
	  "type": "stop",
	  "start_time": "2023-11-02 16:30:00",
	  "end_time": "2023-11-02 17:00:00",
	  "location": "Freehand Chicago",
	  "location_start": "",
	  "location_end": "",
	  "preferred_weather": "SUNNY",
	  "mode": ""
	}
  ]
}

	'''
	return system_instruction


def get_trip_schema():
	trip_schema = {
	"type": "json_schema",
	"json_schema": {
		"name": "TripModel",
		"schema": {
			"type": "object",
			"properties": {
				"trip_name": {
					"type": "string",
					"description": "The name of the trip."
				},
				"start_date": {
					"type": "string",
					"description": "The start date of the trip in YYYY-MM-DD format."
				},
				"end_date": {
					"type": "string",
					"description": "The end date of the trip in YYYY-MM-DD format."
				},
				"events": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"type": {
								"type": "string",
								"enum": ["stop", "commute"]
							},
							"start_time": { "type": "string"},
							"end_time": { "type": "string" },
							"location": { "type": "string", },
							"location_start": { "type": "string" },
							"location_end": { "type": "string" },
							"preferred_weather": {
								"type": "string",
								"enum": ["SUNNY", "CLOUDY", "RAINING", "SNOWING", "WINDY", "COLD", "WARM"]
							},
							"mode": {
								"type": "string",
								"enum": ["WALK", "CAR", "BUS", "TRAIN", "RAILROAD", "PLANE", "SHIP"],
							}
						},
						"required": ["type", "start_time", "end_time", "location", "location_start", "location_end", "preferred_weather", "mode"],  # Only these fields are required
						"additionalProperties": False
					}
				}
			},
			
			"required": ["trip_name", "start_date", "end_date", "events"],
			"additionalProperties": False
		},
		"strict": True
	}
	}
	return trip_schema
