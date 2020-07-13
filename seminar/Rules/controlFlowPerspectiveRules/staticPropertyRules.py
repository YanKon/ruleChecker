from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

import datetime
from dateutil.relativedelta import *
import math
import re

def parse(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: int(val) for key, val in m.groupdict().items()}

# end of day
# end of month
# end of quarter
# end of year
# within days
# within months
# within years

def absolute_time_rule(trace:Trace, activity:str, target_time_span, target_time_span_operator, parameters=None):
    """
    If an activity of type a1 is performed, then it must be performed before t0 (based on exact timestamp)

    :param trace:
    :param activity:
    :param target_time_span:
    :param target_time_span_operator:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transitions_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    activity_start_found = False
    activity_complete_found = False

    activity_start_timestamp:datetime.datetime
    activity_complete_timestamp:datetime.datetime

    for i,event in enumerate(trace):
        if(event[activity_key] == activity and event[transitions_key] == "start"):
            activity_start_found = True
            activity_start_timestamp = event["time:timestamp"]
            if (i < len(trace)-1):
                for j, nextEvent in enumerate(trace, start=i+1):
                    if(nextEvent[activity_key] == activity and nextEvent[transitions_key] == "complete"):
                        activity_complete_found = True
                        activity_complete_timestamp = nextEvent["time:timestamp"]
                        break

        if(activity_start_found and activity_complete_found):
            start_year, start_quarter, start_month, start_day = activity_start_timestamp.year, math.ceil(activity_start_timestamp.month / 3.),  activity_start_timestamp.month, activity_start_timestamp.day
            complete_year, complete_quarter, complete_month, complete_day = activity_complete_timestamp.year, math.ceil(activity_complete_timestamp.month / 3.), activity_complete_timestamp.month, activity_complete_timestamp.day

            if (target_time_span_operator == "end of day"):
                if(start_year == complete_year and start_month == complete_month):
                    if(start_day == complete_day):
                        return True
                return False

            elif (target_time_span_operator == "end of month"):
                if (start_year == complete_year):
                    if(start_month == complete_month):
                        return True
                return False

            elif (target_time_span_operator == "end of quarter"):
                if (start_year == complete_year):
                    if(start_quarter == complete_quarter):
                        return True

            elif (target_time_span_operator == "end of year"):
                if (start_year == complete_year):
                    return True
                return False

            elif (target_time_span_operator == "within days"):
                target_complete_timestamp = activity_start_timestamp + relativedelta(days=+target_time_span)
                if(activity_complete_timestamp <= target_complete_timestamp):
                    return True
                return False

            elif (target_time_span_operator == "within months"):
                target_complete_timestamp = activity_start_timestamp + relativedelta(months=+target_time_span)
                if(activity_complete_timestamp <= target_complete_timestamp):
                    return True
                return False

            elif (target_time_span_operator == "within years"):
                target_complete_timestamp = activity_start_timestamp + relativedelta(years=+target_time_span)
                if(activity_complete_timestamp <= target_complete_timestamp):
                    return True
                return False
    return False