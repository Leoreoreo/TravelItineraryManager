from openai import OpenAI
import json
import os
from helper import get_sys_instr, get_trip_schema, validate_row
from db_utils import *


key=os.environ.get("OPENAI_SECRET_KEY", "")
client = OpenAI(api_key=key)
system_instruction = get_sys_instr()
trip_schema = get_trip_schema()

#print(system_instruction)
#print(type(system_instruction))

def call_openai(pref, age, user_input):
# response = client.chat.completions.create(
	print(f"inside call openai {pref} {age} {user_input}")
	try:
		response = client.beta.chat.completions.parse(
		model="gpt-4o-mini",
		messages=[
		{"role": "system", "content": system_instruction},
		{
			"role": "user",
			"content": f'I am a {pref} who is {age} years old. This is the specific user request on the details of the trip (in [] brackets): [{user_input}]. Based on your age and preferences, choose an appropriate accommodation where you will stay for the trip. Based on your age and preferences and user requirements, choose and plan a trip itinerary. Try to create awesome trips.',
		}
		],
		max_tokens=10000,
		# response_format=TripModel,
		response_format=trip_schema,
		temperature=1.5
		)
	# print(response.usage.completion_tokens, response.usage.total_tokens)
	# completion_tokens=1902, prompt_tokens=1623, total_tokens=3525
	# response['usage']['prompt_tokens']
	# completion_tokens = response['usage']['completion_tokens']
	# total_tokens = response['usage']['total_tokens']
	# print(prompt_tokens, completion_tokens, total_tokens)
	
	# Accessing the message content and parsing it as JSON
	# content = response['choices']
	# content = content[0]
	# content = content.message['content']
	# return response.choices[0].message
	# return response
	# print(response.choices)
		return response.choices[0].message.content, response.usage.completion_tokens, response.usage.prompt_tokens, response.usage.total_tokens, response.usage.prompt_tokens_details.cached_tokens
	# return response.choices[0].message.parsed
	except Exception as e:
		print(f"error: {e}")
		return None, None, None, None, None


def generate_trip(user_id, user_input):
	# so we can try 3 times
	attempts = 0
	# get user info
	user_info = return_user_info(user_id)
	user_age = user_info[3] if user_info != None else 21
	user_trait = user_info[2] if user_info != None else "Adventurer"
	print(f"USER INFO: f{user_info}")
	# in case trip can't be generated.
	while attempts < 3:
		print(f"on attempt: {attempts}")
		trip, comp, prmpt, total, cache = call_openai(user_trait, user_age, user_input)
		if trip: break
		else: attempts += 1

	print(trip)
	print(comp, prmpt, total, cache)
	# if it went beyond 10k tokens, no trip will be returned, this is because hallucinations make garbage values that take a lot of tokens. But this could pose an issue where if a user wants a 10 day trip, it will be denied because it requires much more output. We could have it scale, e.g. # days * 2.5k, actually thats not bad but we need to find how many days first.
	if not trip: return None

	if isinstance(trip, str):
		trip = json.loads(trip)

	# add trip to db
	trip_info = add_trip_to_db(trip["trip_name"], user_id, trip["start_date"], trip["end_date"]) # {trip_id:, trip_name, start_date, end_date}
	# add events to db
	for event in trip["events"]:

		# if invalid row
		if not validate_row(None, None, event['start_time'], event['end_time'], event['type'], event['location'], event['location_start'], event['location_end'], event['preferred_weather']): continue

		if event["type"].lower() == "stop": add_stop_to_db(trip_info["trip_id"], event["location"], event["type"], event["start_time"], event["end_time"], event["location"], "", "", weather=event["preferred_weather"])
		elif event["type"].lower() == "commute": add_commute_to_db_GPT(trip_info["trip_id"], event['mode'], event['type'], event['start_time'], event['end_time'], event['location_start'], event['location_end'], event['mode'])
		else: print('\tinvalid event type')


	return trip_info["trip_id"]
	

	# add trip to db
	# create events
		# add stop
		# add commute

	# { trip_name:, start_date:, end_date:, events:	[ {type, start_time, end_time, location, location_start, location_end, preferred_weather, mode}...


	'''
	"trip_name":"Urban Adventures in Chicago","start_date":"2023-11-03","end_date":"2023-11-04","events":[{"type":"stop","start_time":"2023-11-03 09:00:00","end_time":"2023-11-03 09:15:00","location":"HI Chicago Hostel","location_start":"","location_end":"","preferred_weather":"WARM","mode":

"WALK"},{"type":"commute","start_time":"2023-11-03 09:15:00","end_time":"2023-11-03 09:30:00","location
	'''
