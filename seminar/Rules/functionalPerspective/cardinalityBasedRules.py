from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY

def activity_existence(trace:Trace, activity:str, parameters=None) -> bool:
    """
    Check if an activity performed at least once

    :param trace:
        Trace to be checked
    :param activity:
        Activity to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log

    :return:
        True if the activity performed at least once
        False if the activity is not performed at least once
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY


    for event in trace:
        if (event[activity_key] == activity):
            return True
    return False

def multiple_activity_existence(trace:Trace, activities:list, parameters=None):
    """
    Check if activities performed at least once.

    :param trace:
        Trace to be checked
    :param activities:
        Activities to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log

    :return:
        List of activities that were not performed at least once
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    missed_activities = []
    for activity in activities:
        if(not activity_existence(trace, activity, activity_key)):
            missed_activities.append(activity)
    return missed_activities

def activity_absence(trace:Trace, activity:str, parameters=None):
    """
    Checks whether an activity has been performed that must not be performed

    :param trace:
        Trace to be checked
    :param activity:
        Activities to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log

    :return:
        True if the activity has not been performed (Rule fulfilled)
        False, if the activity has been performed although it should not be performed (Rule not fulfilled)
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    for event in trace:
        if(event[activity_key] == activity):
            return False
    return False

def multiple_activity_absence(trace:Trace, activities:str, parameters=None):
    """
    Checks whether activities have been performed that are not allowed to be performed

    :param trace:
        Trace to be checked
    :param activities:
        Activities to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log

    :return:
        List of activities that were performed although they were not allowed to be performed
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    existing_activities = []
    for activity in activities:
        if(activity_existence(trace, activity, activity_key)):
            existing_activities.append(activity)
    return existing_activities


def activity_range(trace:Trace, activity:str, lower_bound:int, upper_bound:int, parameters=None):
    """
    Check if an activity be executed at least i times and at most j times

    :param trace:
        Trace to be checked
    :param activity:
        Activity to be checked
    :param lower_bound:
        Minimum number of times the activity should be performed
    :param upper_bound:
        Maximum number of times the activity should be performed
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log

    :return:
        True if the activity be executed at least i times and at most j times\n
        False if the activity be not executed at least i times and at most j times
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    if lower_bound < 0:
        raise Exception('lower_bound is negative')
    if upper_bound < 0:
        raise Exception('upper_bound is negative')
    if (lower_bound > upper_bound):
        raise Exception('lower_bound is larger then upper_bound')

    activity_counter = 0
    for event in trace:
        if event[activity_key] == activity:
            activity_counter += 1
    if(activity_counter >= lower_bound and activity_counter <= upper_bound):
        return True
    else: return False