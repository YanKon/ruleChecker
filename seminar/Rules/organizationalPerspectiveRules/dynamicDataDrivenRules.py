from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_RESOURCE_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_RESOURCE_KEY


def exogenous_authorization_rule(trace: Trace, activity: str, expression_function, parameters=None):
    """
    An activity of type a1 must be performed under μ
    EXAMPLE: An evaluate claim activity must be performed at the office during regular office hour

    :param trace:
    :param activity:
    :param expression_function:
    :param attribute_key:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    for event in trace:
        if event[activity_key] == activity:
            if not expression_function(trace, event):
                return False
    return True



def static_originator_attribute_rule(trace: Trace, activity: str, resource: str, expression_function, parameters=None):
    """
    An activity of type a1 must be performed by a person who has characteristic C when μ evaluates true
    EXAMPLE: A call customer activity must be performed by a person who has as mother tongue Dutch when the client is Dutch speaking

    :param trace:
    :param activity:
    :param resource:
    :param expression_function:
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
        if event[activity_key] == activity:
            if expression_function(trace, event, resource):
                if not event[resource_key] == resource:
                    return False
    return True


def dynamic_originator_attribute_rule(trace: Trace, activity: str, characteristic_function, parameters=None):
    """
    An activity of type a1must be performed by a person who has temporal characteristic

    EXAMPLE: Activity approve payment must be performed by person P who is not out of the office
    characteristic_function --> Funktion, die Eigenschaften einer Person prüft (Eigenschaften sind hier alles mögliche: wie z.B. im Office, etc.)
    ---> es geht also mehr darum, Zusammenhänge zu prüfen (

    :param trace:
    :param activity:
    :param characteristic_function:
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
        if (event[activity_key] == activity):
            person = event[resource_key]
            if (not characteristic_function(person)):
                return False
    return True
