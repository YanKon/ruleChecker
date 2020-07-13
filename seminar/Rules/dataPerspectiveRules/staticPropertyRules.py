import re

from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

def event_data_value_set_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, value_set: list, parameters=None):
    """
    The value of event data type p1(wrt an event of type e1 for an activity of type a1) must be included in set of values sV

    :param trace:
    :param event_data_type_key:
    :param activity:
    :param event_type:
    :param value_set:
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    if not event[event_data_type_key] in value_set:
                        return False
    return True

def event_data_value_range_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, range_type: str, lower_bound: int, upper_bound: int, parameters=None):
    """
    The value of event data type p1(wrt an event of type e1for an activity of type a1) must be included in value range range

    :param trace:
    :param event_data_type_key:
    :param activity:
    :param event_type:
    :param range_type:
    :param lower_bound:
    :param upper_bound:
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[
        PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    if range_type == "int":
                        event_data_type_value = int(event[event_data_type_key])
                        if not event_data_type_value >= lower_bound and event_data_type_value <= upper_bound:
                            return False
                    elif range_type == "float":
                        event_data_type_value = float(event[event_data_type_key])
                        if not event_data_type_value >= lower_bound and event_data_type_value <= upper_bound:
                            return False
    return True

def event_data_uniqueness_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, parameters=None):
    """
    The value of event data type p1(wrt an event of type e1 for an activity of type a1) must be unique

    :param trace:
    :param event_data_type_key:
    :param activity:
    :param event_type:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[
        PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    event_data_type_values = []

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    if event[event_data_type_key] in event_data_type_values:
                        return False
                    event_data_type_values.append(event[event_data_type_key])
    return True

# TODO: exisitiert doch schon? --> Event data exclusion rule
# The value of event data type p1(wrt an event of type e1for an activity of type a1) is not equal to the value of event data type p2(wrt an event of type e1 for an activity of type a1)
def irreflexive_event_data_rule():
    return

def event_data_format_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, data_format: str, parameters=None):
    """
    The value of event data type p1(wrt an event of type e1for an activity of type a1) must conform to data format f

    :param trace:
    :param event_data_type_key:
    :param activity:
    :param event_type:
    :param data_format:
        "^[A-Z][a-z]{2}[0-9]{3}$" siehe (https://stackoverflow.com/a/35686691)
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[
        PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    rex = re.compile(data_format)
                    if not rex.match(event[event_data_type_key]):
                        return False
    return True
