from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY

def activity_inclusion(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    Activity type a1 and Activity of type a2 are mutually inclusive

    :param trace:
    :param activity1:
    :param activity2:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity1_found = False
    activity2_found = False

    for event in trace:
        if(not activity1_found and event[activity_key] == activity1):
            activity1_found = True
        elif(not activity2_found and event[activity_key] == activity2):
            activity2_found = True

        if(activity1_found and activity2_found):
            return True

    return False

# TODO: über activities iterieren und dann nochmal über alle events iterieren (n^2 time cost) ineffizient -> gibt es eine Alternative?
# vielleicht erst über events iterieren und speichern welche aktivitäten schon gesehen und dann erst über activities --> drüber nachdenken!
def activity_inclusion_multiple(trace:Trace, activites:list, parameters=None):
    """
    Check if Activtiies(Activity type a1, Activity type a2) are mutually inclusive

    :param trace:
    :param activites:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    not_fulfilled_activities = []
    for activity1, activity2 in activites:
        if(not activity_inclusion(trace, activity1, activity2, activity_key)):
            not_fulfilled_activities.append((activity1,activity2))

    return not_fulfilled_activities


def activity_substitution(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    Activity type a1 and activity type a2 are mutually exclusive

    :param trace:
    :param activity1:
    :param activity2:
    :param parameters:

    :return:
        True, if activity1 and activity2 are mutually exclusive (not together in a trace)
        False, otherwise
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity1_found = False
    activity2_found = False

    for event in trace:
        if(not activity1_found and event[activity_key] == activity1):
            activity1_found = True
        elif(not activity2_found and event[activity_key] == activity2):
            activity2_found = True

        if(activity1_found and activity2_found):
            return False
        else: return True

def activity_substitution_multiple(trace:Trace, activites:list, parameters=None):
    """

    :param trace:
    :param activites:
    :param parameters:

    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    not_fulfilled_activities = []
    for activity1, activity2 in activites:
        if (not activity_inclusion(trace, activity1, activity2, activity_key)):
            not_fulfilled_activities.append((activity1, activity2))

    return not_fulfilled_activities


def responded_existence(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    If an activity of type a1 is performed then an activity of type activity a2 must be performed
    Ativity1 muss vor Activity2 ausgeführt werden. Tritt Activity2 vor Activity1 auf, sofern Activity2 nicht nochmal nach Activity1 auftreten--> False

    :param trace:
    :param activity1:
    :param activity2:
    :param parameters:

    :return:
        True, if Activity1 is performed and activity2 is performed sometime after activity1
        False, otherwise
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity1_found = False

    for event in trace:
        if(not activity1_found and event[activity_key] == activity1):
            activity1_found = True
        elif(activity1_found):
            if(event[activity_key] == activity2):
                return True
    return False

# TODO: parameter mit dem eingestellt wird, ob eine activity nur einmal vorkommen darf
def activity_choice(trace:Trace, activities:list, at_least_performed:int, parameters=None):
    """
    At least n activities of activity type set sA (with m activity types) must be performed

    :param trace:
    :param activities:
    :param at_least_performed:
    :param parameters:
    :return:
        True,
        False,
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    at_least_performed = at_least_performed
    for event in trace:
        if(event[activity_key] in activities):
            at_least_performed -= 1
        if(at_least_performed == 0):
            return True

    return False


# TODO: was ist ein Event in diesem Fall?
# TODO: Event vielleicht als Liste mit Tupel (Attribute_key, attribute_value)
# An activity of type a1 must be performed if an event of type e1 occurred
def event_activity_responded_existence(trace:Trace, activity:str, check_event:list, parameters=None):
    """

    :param trace:
            Trace to be checked
    :param activity:
            Activity to be checked
    :param check_event:
            Event to be checked [(attribute_key, attribute_value), ... ]
    :param parameters:
    :return:
    """
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity_found = False
    check_event_found = False
    check_event_size = len(check_event)
    for event in trace:
        if event[activity_key] == activity:
            activity_found = True
        for index, (check_event_attribute_key, check_event_attribute_value) in enumerate(check_event):
            if event.get(check_event_attribute_key) != None:
                if event[check_event_attribute_key] == check_event_attribute_value:
                    if index == check_event_size - 1:
                        check_event_found = True
                        break
                    continue
                else:
                    break
        if activity_found and check_event_found:
            return True
    return False

# TODO:
# An activity of type a1 must not be performed if an event of type e1 occurre
def event_activity_responded_absence():
    return

# TODO:
# At least n activities of activity type set sA (with m activity types) must be performed if an event of type e1 occurred
def event_activity_responded_choice():
    return
