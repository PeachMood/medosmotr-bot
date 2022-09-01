from datetime import datetime
from numpy import append
import requests

def define_date():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d")

def send_request(date, count):
    url = "https://n801656.yclients.com/api/v1/activity/751869/search"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "authorization": "Bearer yusw3yeu6hrr4r9j3gw6",
    }
    params = {
        "form": date,
        "till": "9999-01-01",
        "count": count,
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def parse_date(date):
    parsedDate = datetime.strptime(date, "%Y-%m-%d %X")
    date = parsedDate.strftime("%d %B %Y")
    time = parsedDate.strftime("%H:%M")
    return date, time

def parse_json(json):
    records = {}
    for record in json["data"]:
        date, time = parse_date(record["date"])
        if date not in records:
            records[date] = []
        new_record = {
            "id": record["id"],
            "date": date,
            "time": time,
            "isFree": record["capacity"] != record["records_count"],
        }
        records[date].append(new_record)
    return records

def get_records():
    current_date = define_date
    records_count = 200
    json = send_request(current_date, records_count)
    return parse_json(json)

def get_free_records():
    records = get_records()
    for key, value in records.copy().items():
        records[key] = [record for record in value if record["isFree"]]
        if len(records[key]) == 0:
            records.pop(key)
    return records