from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_RESOURCE_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_RESOURCE_KEY


# TODO: erst mal nicht interessant
# A person must not be a member of both role r1 and role r2(i.e. not perform both activities for role r1 and activities for role r2)
def conflicting_roles_rule():
    return


def dynamic_segregation_of_duties(trace: Trace, activity1: str, activity2: str, resource, parameters=None):
    """
    A person must not perform both an activity of type a1 and an activity of type a2

    :param trace:
    :param activity1:
    :param activity2:
    :param resource:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    resource_key = parameters[
        PARAMETER_CONSTANT_RESOURCE_KEY] if PARAMETER_CONSTANT_RESOURCE_KEY in parameters else DEFAULT_RESOURCE_KEY

    activity1_resource = ""
    activity2_resource = ""

    for event in trace:
        if event[activity_key] == activity1:
            if event[resource_key] == resource:
                activity1_resource = resource
        elif event[activity_key] == activity2:
            if event[resource_key] == resource:
                activity2_resource = resource
        if (activity1_resource == activity2_resource):
            return False
    return True


# A person must not perform all activities of the activity type set sA(with m activity types)
def operational_segregation_of_duties(trace: Trace, activities: list, resource, parameters=None):
    """
    A person must not perform all activities of the activity type set sA(with m activity types)

    :param trace:
    :param activities:
    :param resource:
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    resource_key = parameters[
        PARAMETER_CONSTANT_RESOURCE_KEY] if PARAMETER_CONSTANT_RESOURCE_KEY in parameters else DEFAULT_RESOURCE_KEY

    activity = ""
    activity_resource = ""

    for event in trace:
        if event[activity_key] in activities:
            if (activity != event[activity_key] and activity_resource == event[resource_key]):
                return False
            activity = event[activity_key]
            activity_resource = event[resource_key]
    return True


def history_based_segregation_of_duties(trace: Trace, resource: str, parameters=None):
    """
    A person must not perform all activities in a specific process instance of process type s1

    :param trace:
    :param resource:
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    resource_key = parameters[
        PARAMETER_CONSTANT_RESOURCE_KEY] if PARAMETER_CONSTANT_RESOURCE_KEY in parameters else DEFAULT_RESOURCE_KEY

    activities = []

    for event in trace:
        if event[resource_key] == resource:
            if not event[activity_key] in activities:
                activities.append(event[activity_key])
        if len(activities) > 1:
            return False
    return True


def binding_of_duties(trace: Trace, activities: list, resource: str, parameters=None):
    """
    A person must perform all activities in activity set sA(with m activity types)

    :param trace:
    :param activities:
    :param resource:
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    resource_key = parameters[
        PARAMETER_CONSTANT_RESOURCE_KEY] if PARAMETER_CONSTANT_RESOURCE_KEY in parameters else DEFAULT_RESOURCE_KEY

    for event in trace:
        if (event[activity_key] in activities):
            if (event[resource_key] != resource):
                return False
    return True


# Person o1 was a member of role r1 on time T (i.e.role delegation event happened before T and a role retraction event happened after T)
def temporal_engagement_rule():
    return
