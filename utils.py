import requests
from datetime import datetime, timedelta
from collections import Counter
import plotly.graph_objects as go
from typing import Optional
import json
import plotly


def plot(event_dict: Optional[dict] = None, offset_value: Optional[int] = 0):
    """
    Create a plot to be displayed in the
    :param event_dict:
    :param offset_value:
    :return:
    """
    if event_dict is None and offset_value == 0:
        offset_value = 10
        event_dict = events(offset=10)
    keys, values = dict_to_list(event_dict)
    fig = go.Figure(
        data=[go.Bar(x=keys, y=values)],
        layout_title_text=f"Showing all github api events for duration of {offset_value} minutes since {datetime.now() - timedelta(minutes=offset_value)}",
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json


def repo_avg_pull(username: str = "PyGithub", repo: str = "PyGithub"):
    """
    Calculate the average time between pull requests for a given repository
    :param username: Github username
    :param repo: Github public repository
    :return: Text displaying the average time between pull requests for a given repository
    """
    created_dates = {}
    datetime_objects = []
    pull_requests = requests.get("https://api.github.com/repos/" + str(username) + "/" + str(repo) + "/pulls")
    pull_requests_data = pull_requests.json()
    display_text = "There are no current pullrequests from this repository or repository is private or user/repository not found!"
    if len(pull_requests_data) > 2:
        for i in pull_requests_data:
            created_dates[i["id"]] = i["created_at"]
        for i, ids in enumerate(created_dates):
            datetime_objects.append(datetime.strptime(created_dates[ids], '%Y-%m-%dT%H:%M:%SZ'))
        datetime_objects.sort()
        time_deltas = []
        for i in range(len(datetime_objects) - 1):
            delta = datetime_objects[i + 1] - datetime_objects[i]
            time_deltas.append(delta.total_seconds())
        average_time = sum(time_deltas) / len(time_deltas)
        date_hours_mins = avg_time(average_time)
        intro = "The average time between pull requests for repo " + str(username) + "/" + str(repo) + " is: "
        display_text = intro + str(date_hours_mins[0]) + "days: " + str(date_hours_mins[1]) + " hours: " + str(date_hours_mins[2]) \
                        + " mins: "
    else:
        display_text = display_text
    return display_text


def events(offset: int = 10):
    """
    Observe all the events from https://api.github.com/events within a time frame
    :param offset: number of minutes for viz. events are being observed.
    :return: dictionary of events or int value of time difference needed
    """
    event_list = []
    event_json = requests.get('https://api.github.com/events')
    event_data = event_json.json()
    from_time = datetime.now() - timedelta(minutes=offset)
    for event in event_data:
        if datetime.strptime(event["created_at"], '%Y-%m-%dT%H:%M:%SZ') < from_time:
            event_list.append(event['type'])
        else:
            time_diff = datetime.strptime(event["created_at"], '%Y-%m-%dT%H:%M:%SZ') - from_time
            event_list = int(offset - (time_diff.seconds / 60)) # converting seconds to minutes
    return dict(Counter(event_list)) if not isinstance(event_list, int) else event_list


def avg_time(average_time: float):
    """
    convert a datetime float value to human readable format
    :param average_time: float value from datetime
    :return: number of days, hours and minutes in float.
    """
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60
    days = average_time // seconds_in_day
    hours = (average_time - (days * seconds_in_day)) // seconds_in_hour
    minutes = (average_time - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    return days, hours, minutes


def dict_to_list(dict_values: dict):
    """
    Converts a dictionary into list of keys and values
    :param dict_values: dictionary for viz. keys and values are to be expected
    :return: list of keys and list of values
    """
    keys = []
    values = []
    for key, value in dict_values.items():
        keys.append(key)
        values.append(value)
    return keys, values
