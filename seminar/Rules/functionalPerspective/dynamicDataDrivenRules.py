from pm4py.objects.petri.petrinet import PetriNet
from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY


# If expression μ becomes true before the process instance ends, then an activity of type a1 must be executed at least once
def data_driven_activity_inclusion(trace:Trace, final_marking_place:PetriNet.Place, activity:str, expression, parameters=None):

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    in_arcs = final_marking_place.in_arcs
    activity_found = False

    for event in trace:
        if(event[activity_key] == activity):
            activity_found = True
        # Prozess ist schon beendet --> Expression erfüllt?
        if(event[activity_key] in in_arcs):
            if(expression() and activity_found):
                return True
            else:
                return False


#TODO: diese Methode wäre interessant, um aufzuzeigen ob eine Activity unnötigerweise ausgeführt wurde
# If expression μ becomes true before the process instance ends, then activity a1 must not be executed
def data_driven_activity_exclusion(log, expression, activity, attribute_key):
    return