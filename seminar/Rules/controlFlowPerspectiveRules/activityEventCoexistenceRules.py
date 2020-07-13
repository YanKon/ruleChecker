from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY

def non_overlapping_activity_rule():
    return

def simple_response_activity_rule(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    If activity of type a1 is performed then an activity of type a2 must be performed afterwards

    :param trace:
        Trace to be checked
    :param activity1:
        Activity to be checked
    :param activity2:
        Activity to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log
    :return:
        True if activity a2 was performed after activity a1
        True if activity a2 was not performed after activity a1
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    for i, event in enumerate(trace):
        if (event[activity_key] == activity1):
            for nextEvent in enumerate(trace, start=i):
                if(nextEvent[activity_key] == activity2):
                    return True
            break
    return False


def simple_precedence_activity_rule(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    An activity of type a1 must be performed before an activity of type a2 can be performed

    :param trace:
        Trace to be checked
    :param activity1:
        Activity to be checked
    :param activity2:
        Activity to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log
    :return:
        True if activity a2 was performed, a1 was also performed before
        False if activity a2 was performed, a1 was not performed before
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    activity1_found = False
    activity2_found = False

    for event in trace:
        if(event[activity_key] == activity1):
            activity1_found = True
        elif(event[activity_key] == activity2):
            activity2_found = True
            # break hier, weil wenn activity2 gefunden wurde, muss activity1 schon ausgeführt worden sein
            break
    if(not activity1_found or not activity2_found):
        return False
    return True

# not implemented
def alternate_response_activity_rule(log, activity1, activity2, attribute_change_key, attribute_change_to_value, attribute_key):
    return

# not implemented
def alternate_precedence_activity_rule(log, activity1, activity2, attribute_change_key, attribute_change_to_value, attribute_key):
    return

def chain_response_activity_rule(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
    An activity of type a2 must be executed immediately after each execution of an activity of type a1

    :param trace:
        Trace to be checked
    :param activity1:
        Activity to be checked
    :param activity2:
        Activity to be checked
    :param parameters: Parameters of the algorithm, including:
        activity_key -> Attribute identifying the activity in the log
    :return:
        True if activity a2 was immediately performed after a1
        False if activity a2 was not immediately performed after a1
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    trace_size = len(trace)
    for i, event in enumerate(trace):
        if(event[activity_key] == activity1):
            if(i < (trace_size-1) and trace[i+1][activity_key] == activity2):
                return True
            else:
                return False


# Each execution of an activity of type a2 must be immediately preceded by the execution of an activity of type a1
def chain_precedence_activity_rule(trace:Trace, activity1:str, activity2:str, parameters=None):
    """
        Each execution of an activity of type a2 must be immediately preceded by the execution of an activity of type a1

        :param trace:
        Trace to be checked
        :param activity1:
            Activity to be checked
        :param activity2:
            Activity to be checked
        :param parameters: Parameters of the algorithm, including:
            activity_key -> Attribute identifying the activity in the log
        :return:
            True if activity a2 was immediately performed after a1
            False if activity a2 was not immediately performed after a1
        """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    for i, event in enumerate(trace):
        if(event[activity_key] == activity2):
                if(i > 0 and trace[i-1][activity_key] == activity1):
                    return True
                else:
                    return False
