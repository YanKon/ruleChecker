from Rules.functionalPerspective.activityEventCoexistenceRules import *
from Rules.functionalPerspective.cardinalityBasedRules import *
from Rules.functionalPerspective.dynamicDataDrivenRules import *
from Rules.functionalPerspective.relativeTimeOrientedRules import *
from Rules.functionalPerspective.staticPropertyRules import *

from Rules.controlFlowPerspectiveRules.activityEventCoexistenceRules import *
from Rules.controlFlowPerspectiveRules.dynamicDataDrivenRules import *
from Rules.controlFlowPerspectiveRules.relativeTimeOrientedRules import *
from Rules.controlFlowPerspectiveRules.staticPropertyRules import *

from Rules.dataPerspectiveRules.activityEventCoexistenceRules import *
from Rules.dataPerspectiveRules.cardinalityBasedRules import *
from Rules.dataPerspectiveRules.dynamicDataDrivenRule import *
from Rules.dataPerspectiveRules.relativeTimeOrientedRules import *
from Rules.dataPerspectiveRules.staticPropertyRules import *

from Rules.organizationalPerspectiveRules.activityEventCoexistenceRules import *
from Rules.organizationalPerspectiveRules.cardinalityBasedRules import *
from Rules.organizationalPerspectiveRules.dynamicDataDrivenRules import *
from Rules.organizationalPerspectiveRules.relativeTimeOrientedRules import *
from Rules.organizationalPerspectiveRules.staticPropertyRules import *

from pm4py.objects.log.importer.xes import factory as xes_import_factory

############ Grafische Darstellung eines Event Logs ############
#from pm4py.algo.discovery.alpha import factory as alpha_miner
#from pm4py.visualization.petrinet import factory as visualizer
#from pm4py.objects.petri.common.final_marking import discover_final_marking
#from pm4py.objects.petri.common.initial_marking import discover_initial_marking
#path= *****
#log = xes_import_factory.apply(path)
#net, initial_marking, final_marking = alpha_miner.apply(log)
#gviz = visualizer.apply(net, initial_marking, final_marking)
#visualizer.view(gviz)
#for place in net.places:
#   if len(place.out_arcs) == 0:
#        for arc in place.in_arcs:
#            print(arc.source)

#log = xes_import_factory.apply('./Log/running-example.xes')

############### Beispiele ###################
#print(activity_existence(log[0], "register request"))
#print(multiple_activity_existence(log[0], ["register request", "reject request"]))
#print(activity_absence(log[0], "register request"))
#print(multiple_activity_absence(log[0], ["register request", "reject request"]))
#print(activity_range(log[0], "register request", 2, 2))
#print(event_activity_responded_existence(log[0], "register request", [("Activity", "check ticket"), ("Costs", "100")]))
#print(activity_inclusion(log, "check ticket", "decide", "concept:name"))

#log = xes_import_factory.apply('./Log/repairExample.xes')
#print(originator_cardinality_rule(log, "Analyze Defect", "Tester3", "more", 3, "01,1970", "in month", "concept:name"))
