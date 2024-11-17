import csv
from datetime import datetime


def validate_row(start_date, end_date, start_time, end_time, event_type, location, location_start, location_end, weather):
    try:
        datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
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
    