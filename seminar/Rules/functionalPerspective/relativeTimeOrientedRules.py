from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY

import datetime
import re

def parse(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: int(val) for key, val in m.groupdict().items()}

def started_to_late(time_delta, parsed_delta_time):
    days, hours, minutes = time_delta.days, time_delta.seconds // 3600, time_delta.seconds % 3600 // 60
    seconds = time_delta.seconds - hours * 3600 - minutes * 60

    if (parsed_delta_time.get("days") < days):
        return True
    elif (parsed_delta_time.get("days") > days):
        return False
    else:
        if (parsed_delta_time.get("hours") < hours):
            return True
        elif (parsed_delta_time.get("hours") > hours):
            return False
        else:
            if (parsed_delta_time.get("minutes") < minutes):
                return True
            elif (parsed_delta_time.get("minutes") > minutes):
                return False
            else:
                if (parsed_delta_time.get("seconds") < seconds):
                    return True
                elif (parsed_delta_time.get("seconds") > seconds):
                    return False
    return True

def timed_activity_existence_rule(trace:Trace, activity1:str, activity2:str, time_status:str, time_unit:str, parameters=None):
    """
    An activity of type a1 must be started/ completed before/ after/on t time units (relative to t0)

    :param trace:
    :param activity1:
    :param activity2:
    :param time_status:
    :param time_unit:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    parsed_delta_time:dict = parse(time_unit)
    activity1_found = False
    activity2_found = False
    activity1_timestamp:datetime
    activity2_timestamp:datetime

    for event in trace:
        if (not activity1_found and event[activity_key] == activity1):
            activity1_found = True
            activity1_timestamp = event["time:timestamp"]
        elif (not activity2_found and event[activity_key] == activity2):
            activity2_found = True
            activity2_timestamp = event["time:timestamp"]

    if(activity1_found and activity2_found):
        if (time_status == "started before"):
            # activity1 startet nach activity2
            if(activity1_timestamp > activity2_timestamp):
                return False
            elif(started_to_late(activity2_timestamp-activity1_timestamp,parsed_delta_time)):
                return False
        elif (time_status == "started after"):
            # activity1 startet vor activity2
            if (activity1_timestamp < activity2_timestamp):
                return False
            if (started_to_late(activity1_timestamp - activity2_timestamp, parsed_delta_time)):
                return False
        elif (time_status == "started on"):
            first_activity_timestamp = trace[0]["time:timestamp"]
            if (started_to_late(activity1_timestamp - first_activity_timestamp)):
                return False

        # wenn oben nichts zutrifft, passt alles
        return True
        # TODO: completed before/after/on
        # completed möglich, wenn kein status über start oder completed als Attribut geführt wird?

    # activity1 oder activity2 nicht vorhanden
    else:
        return False

    return True

#TODO: vielleicht so implementieren wie pm4py -> Parameter mit absence oder existence -> funktionsname time-oriented_activity_existence_rule()
def timed_activity_absence_rule():
    return