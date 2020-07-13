from pm4py.objects.log.log import EventLog
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_RESOURCE_KEY, DEFAULT_TIMESTAMP_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY,PARAMETER_CONSTANT_RESOURCE_KEY, PARAMETER_CONSTANT_TIMESTAMP_KEY

import datetime
from dateutil.relativedelta import *
import math

# in month mm,yyyy
# in quarter q,yyyy
# in year yyyy

# TODO:ausbauen
# in day x
# within x days
# within x months
# within x years
# within x weeks


# TODO: vielleicht auch für ein Trace sinnvoll?
def originator_cardinality_rule(log:EventLog, activity:str, resource:str, count_of_performed_type:str, count_of_performed:int, target_time_span:str, target_time_span_operator:str, parameters=None):
    """
    An activity of type a1 must not be performed more/ less then n times by the same person (in period T0)

    :param log:
    :param activity:
    :param resource:
    :param count_of_performed_type:
    :param count_of_performed:
    :param target_time_span:
    :param target_time_span_operator:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    resource_key = parameters[PARAMETER_CONSTANT_RESOURCE_KEY] if PARAMETER_CONSTANT_RESOURCE_KEY in parameters else DEFAULT_RESOURCE_KEY
    timestamp_key = parameters[PARAMETER_CONSTANT_TIMESTAMP_KEY] if PARAMETER_CONSTANT_TIMESTAMP_KEY in parameters else DEFAULT_TIMESTAMP_KEY

    count_resource = 0

    if(target_time_span_operator == "in month"):
        time_split = target_time_span.split(",")
        target_month, target_year = int(time_split[0]), int(time_split[1])
    elif (target_time_span_operator == "in quarter"):
        time_split = target_time_span.split(",")
        target_quarter, target_year = int(time_split[0]), int(time_split[1])
    elif (target_time_span_operator == "in year"):
        target_year = int(target_time_span)

    for trace in log:
        for event in trace:
            if(event[activity_key] == activity):
                activity_timestamp = event[timestamp_key]
                year, quarter, month, day = activity_timestamp.year, math.ceil(activity_timestamp.month / 3.), activity_timestamp.month, activity_timestamp.day

                if(event[resource_key] == resource):
                    if (target_time_span_operator == "in month"):
                        if(target_year == year and target_month == month):
                            count_resource = count_resource + 1
                    elif (target_time_span_operator == "in quarter"):
                        if(target_year == year and target_quarter == quarter):
                            count_resource = count_resource + 1
                    elif (target_time_span_operator == "in year"):
                        if(target_year == year):
                            count_resource = count_resource + 1

    if (count_of_performed_type == "less"):
        if(count_resource <= count_of_performed):
            return True
        else:
            return False
    elif (count_of_performed_type == "more"):
        if(count_resource >= count_of_performed):
            return True
        else:
            return False






