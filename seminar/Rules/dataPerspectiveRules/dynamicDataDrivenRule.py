from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY, DEFAULT_TRANSITION_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY, PARAMETER_CONSTANT_TRANSITION_KEY

# The value of event data type p1(wrt an event of type e1 for an activity of type a1) is calculated using the mathematical expression μ
# EXAMPLE: The value of insurance surcharges (wrt a complete event for an update insurance premium activity) is calculated using the mathematical expression insurance surcharges=current premium x 0,20
def arithmetic_derivation_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, mathematical_expression, parameters=None):
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    if not mathematical_expression(event[event_data_type_key], event):
                        return False
            else:
                continue
    return True

# The value of event data type p1(wrt an event of type e1for an activity of type a1) is determined using the expression
# EXAMPLE: The value of compulsory excess (wrt a complete event for a register car insurance policy activity) is determined using the expression (if age≤23 then 500 else 400)
# EIGENTLICH SELBE WIE FUNKTION DRÜBER => man kann lediglich eine EXPRESSION FESTLEGEN MIT DER MAN ABLEITET
def logical_derivation_rule(trace: Trace, event_data_type_key: str, activity: str, event_type: str, expression, parameters=None):
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    for event in trace:
        if event[activity_key] == activity:
            if event[transition_key] == event_type:
                if event.get(event_data_type_key) is not None:
                    if not expression(event[event_data_type_key], event):
                        return False
            else:
                continue
    return True

# The value of event data type p1(wrt an event of type e1for an activity of type a1) is equal to the value of event data type p2(wrt an event of type e2 for an activity of type a2)
def event_data_equality_rule(trace: Trace, event_data_type_key1: str, event_data_type_key2: str, activity1: str, activity2: str, event_type1: str, event_type2: str, parameters=None):
    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    activity1_event1_found = False
    activity2_event2_found = False
    activity1_event1_value = ""
    activity2_event2_value = ""

    for event in trace:
        if event[activity_key] == activity1:
            if event[transition_key] == event_type1:
                if event.get(event_data_type_key1) is not None:
                    activity1_event1_found = True
                    activity1_event1_value = event[event_data_type_key1]
        if event[activity_key] == activity2:
            if event[transition_key] == event_type2:
                if event.get(event_data_type_key2) is not None:
                    activity1_event2_found = True
                    activity2_event2_value = event[event_data_type_key2]
        if activity1_event1_found and activity1_event2_found:
            if activity1_event1_value == activity2_event2_value:
                return True
            else:
                return False
    return True


# The value of event data type p1(wrt an event of type e1for an activity of type a1) is not equal to the value of event data type p2(wrt an event of type e2 for an activity of type a2)
def event_data_exclusion_rule(trace: Trace, event_data_type_key1: str, event_data_type_key2: str, activity1: str, activity2: str, event_type1: str, event_type2: str, parameters=None):
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    transition_key = parameters[
        PARAMETER_CONSTANT_TRANSITION_KEY] if PARAMETER_CONSTANT_TRANSITION_KEY in parameters else DEFAULT_TRANSITION_KEY

    activity1_event1_found = False
    activity2_event2_found = False
    activity1_event1_value = ""
    activity2_event2_value = ""

    for event in trace:
        if event[activity_key] == activity1:
            if event[transition_key] == event_type1:
                if event.get(event_data_type_key1) is not None:
                    activity1_event1_found = True
                    activity1_event1_value = event[event_data_type_key1]
        if event[activity_key] == activity2:
            if event[transition_key] == event_type2:
                if event.get(event_data_type_key2) is not None:
                    activity1_event2_found = True
                    activity2_event2_value = event[event_data_type_key2]
        if activity1_event1_found and activity1_event2_found:
            if activity1_event1_value != activity2_event2_value:
                return True
            else:
                return False
    return True