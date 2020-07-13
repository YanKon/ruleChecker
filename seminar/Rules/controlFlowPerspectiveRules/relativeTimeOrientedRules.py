from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

import datetime
import re

def parse(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: int(val) for key, val in m.groupdict().items()}

def time_span_within(time_delta:datetime, parsed_target_time_delta:dict, timespan_operator:str):
    days, hours, minutes = time_delta.days, time_delta.seconds // 3600, time_delta.seconds % 3600 // 60
    seconds = time_delta.seconds - hours * 3600 - minutes * 60

    parsed_days = parsed_target_time_delta.get("days")
    parsed_hours = parsed_target_time_delta.get("hours")
    parsed_minutes = parsed_target_time_delta.get("minutes")
    parsed_seconds = parsed_target_time_delta.get("seconds")

    # at_least
    if (timespan_operator == "<="):
        if (days >= parsed_days):
            return True
        elif (days <= parsed_days):
            return False
        else:
            if (hours >= parsed_hours):
                return True
            elif (hours <= parsed_hours):
                return False
            else:
                if (minutes >= parsed_minutes):
                    return True
                elif (minutes <= parsed_minutes):
                    return False
                else:
                    if (seconds >= parsed_seconds):
                        return True
                    elif (seconds <= parsed_seconds):
                        return False

    elif (timespan_operator == ">="):
        if (days <= parsed_days):
            return True
        elif (days >= parsed_days):
            return False
        else:
            if (hours <= parsed_hours):
                return True
            elif (hours >= parsed_hours):
                return False
            else:
                if (minutes <= parsed_minutes):
                    return True
                elif (minutes >= parsed_minutes):
                    return False
                else:
                    if (seconds <= parsed_seconds):
                        return True
                    elif (seconds >= parsed_seconds):
                        return False

    elif (timespan_operator == "="):
        if (days == parsed_days):
            if (hours == parsed_hours):
                if (minutes == parsed_hours):
                    if (seconds == parsed_minutes):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False



def activity_time_rule(trace:Trace, activity:str, time_unit, time_status:str, parameters=None):
    """
    An activity of type a1 must be performed in at most/exactly at most/exactly/at least t time units

    :param trace:
    :param activity:
    :param time_unit:
    :param time_status:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transitions_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    activity_start_found = False
    activity_complete_found = False

    activity_start_timestamp: datetime
    activity_complete_timestamp: datetime

    for i, event in enumerate(trace):
        if(event[activity_key] == activity and event[transitions_key] == "start"):
            activity_start_found = True
            activity_start_timestamp = event["time:timestamp"]
            for event in enumerate(trace, start=i+1):
                if(event[activity_key] == activity and event[transitions_key] == "complete"):
                    activity_complete_found = True
                    activity_complete_timestamp = event["time:timestamp"]
                    break
            if(activity_complete_found):
                time_delta = activity_complete_timestamp - activity_start_timestamp
                parsed_time_unit = parse(time_unit)
                if (time_span_within(time_delta, parsed_time_unit, time_status)):
                    return True
                else:
                    return False
    return False

def inter_activity_time_rule(trace:Trace, activity1:str, activity2:str, target_time_span, time_span_operator, parameters=None):
    """
    Between the execution of an activity of type a1 and of an activity of type a2 there are at most/ exactly/at least t time units

    :param trace:
    :param activity1:
    :param activity2:
    :param target_time_span:
    :param time_span_operator:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity1_found = False
    activity2_found = False

    activity1_timestamp:datetime
    activity2_timestamp:datetime

    for i, event in enumerate(trace):
        if(event[activity_key] == activity1):
            activity1_found = True
            activity1_timestamp = event["time:timestamp"];
            if(i < len(trace)-1):
                for nextEvent in enumerate(trace, start=i+1):
                    if(nextEvent[activity_key] == activity2):
                        activity2_found = True
                        activity2_timestamp = nextEvent["time:timestamp"]
                        break
                if(activity2_found):
                    time_delta = activity2_timestamp - activity1_timestamp
                    parsed_target_time_span = parse(target_time_span)
                    if(time_span_within(time_delta,parsed_target_time_span,time_span_operator)):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
    if(not activity1_found or not activity2_found):
        return False
    return False