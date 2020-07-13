from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

def activity_start_precondition_rule(trace:Trace, activity:str, expression_func, parameters=None):
    """
    An activity of type a1 can only be executed if expression μ holds
    Example: An update provisions activity can only be executed if the current provisions are lower than a recent estimate of the expected cost

    :param trace:
        Trace to be checked
    :param activity:
        Activity to be checked
    :param expression_func:
        Function that returns true or false -> The trace and the activity are transferred to her -> Any attributes can be tested
    :param parameters:
    :return:

    True if activity a2 was immediately performed after a1
    False if activity a2 was not immediately performed after a1
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    #if(not callable(expression_function)):
    #    return error

    for event in trace:
        if(event[activity_key] == activity):
            if(expression_func(trace, activity)):
                return True
            else:
                return False
    return True

# An activity of type a1 can only be completed if expression μ hold
def activity_end_precondition_rule(trace:Trace, activity:str, expression_func, parameters=None):
    """
    An activity of type a1 can only be completed if expression μ holds

    :param trace:
        Trace to be checked
    :param activity:
        Activity to be checked
    :param expression_func:
        Function that returns true or false -> The trace and the activity are transferred to her -> Any attributes can be tested
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transitions_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if(event[activity_key] == activity and event[transitions_key] == "complete"):
            if(expression_func(trace, activity)):
                return True
            else:
                return False
    return True
