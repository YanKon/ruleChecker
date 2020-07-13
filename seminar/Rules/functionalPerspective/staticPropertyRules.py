from pm4py.objects.log.log import Trace
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY

def activity_artifact_coexistence_rule(trace:Trace, activity:str, artifact:tuple, parameters=None):
    """
    If activity of type a1 is performed then an artifact of type Art1 must exist
    (hier wird geprüft, ob die Aktivität selber das Artifact hat --> möglich wären auch andere Varianten wie z.B.
     - anderes Event
     - Datenbankabfrage

    :param trace:
    :param activity:
    :param artifact:
    :param parameters:
    :return:
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY

    artifact_attribute_key, artifact_attribute_value = artifact

    for event in trace:
        if (event[activity_key] == activity):
            if(event.get(artifact_attribute_key) != None):
                if(event[artifact_attribute_key] != artifact_attribute_value):
                    return True
    return False

# TODO
# If an event of type e1 occurs then an artifact of type Art1 must exist
def non_activity_event_artifact_coexistence_rule():
    return
