from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

def mandatory_event_data_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, parameters=None):
    """
    The value for event data type p1(wrt an event of type e1 for an activity of type a1) must be specified

    :param trace:
    :param event_data_type:
    :param activity:
    :param event_type:
        "start" or "complete"
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
                    if event[event_data_type_key] != "":
                        return True
                    else:
                        return False
            else:
                continue
    return True


def event_data_multiplicity_constraint(trace: Trace, constraint_type: str, constraint_count: int, event_data_types: list, activity: str, event_type: str, parameters=None):
    """
    Atleast/exactly/atmost n values for event data type p1(wrt an event of event type e1for an activity of type a1) must be specifie

    Values? Kann man einem Attribut in einem Event mehrere Values übergeben? Nur als Liste oder? --> wenn nicht, dann ist die Funktion identisch zu "Disjunctive_event_data_rule()"

    Wenn Aktivität mehrmals vorkommt, wird es geprüft, ob die erste Aktivität alles erfüllt. Erfüllt sie es nicht wird direkt False geliefert
    TODO: Mögliche Optimierung: ausgeben welche Aktivitäten in einem Trace es nicht erfüllen


    :param trace:
    :param event_data_types:
    :param activity:
    :param event_type:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    event_data_types_counter = 0

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                for event_data_type_key in event_data_types:
                    if event.get(event_data_type_key) is not None:
                        if event[event_data_type_key] != "":
                            event_data_types_counter += 1
                if constraint_type == "atleast":
                    if not event_data_types_counter >= constraint_count:
                        return False
                elif constraint_type == "exactly":
                    if not event_data_types_counter == constraint_count:
                        return False
                elif constraint_type == "atmost":
                    if not event_data_types_counter <= constraint_count:
                        return False
    return True


