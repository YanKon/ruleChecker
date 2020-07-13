from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.simulation.tree_generator import factory as tree_gen_factory
from pm4py.visualization.process_tree import factory as pt_vis_factory

#
# parameters = {}
# tree = tree_gen_factory.apply(parameters=parameters)
# print(tree)
#
# gviz = pt_vis_factory.apply(tree, parameters={"format": "png"})
# pt_vis_factory.view(gviz)



log = xes_import_factory.apply('/Users/yannick/Downloads/event-logs-process-mining-book/Chapter_1/running-example-just-two-cases.xes')
#print(log[0][0].keys())

# from pm4py.objects.log.importer.xes import factory as xes_log_importer
# from pm4py.algo.discovery.inductive import factory as discovery_algorithm
# from pm4py.visualization.petrinet import factory as pm_visualizer

# event_data = xes_log_importer.apply("/Users/yannick/Downloads/event-logs-process-mining-book/Chapter_1/running-example-just-two-cases.xes")
# model, marking_i, marking_f = discovery_algorithm.apply(event_data)
# pm_visualizer.view(pm_visualizer.apply(model, marking_i, marking_f, parameters={"format":"png"}))

# from pm4py.statistics.attributes.log import get as get
# act = get.get_all_trace_attributes_from_log(log)
# act2 = get.get_all_event_attributes_from_log(log)
# v = get.get_attribute_values(log,"Activity")

from pm4py.algo.enhancement.roles import factory as roles_factory
# execute the roles detection factory
roles = roles_factory.apply(log)

# print the results (grouped activities) on the screen
#print(roles)
#print([x[1] for x in roles])

#print(act)
#print(act2)
#print(v)



# def activity_cardinality(log, value):
#    for case_index, case in enumerate(log):
#        print("\n case index: %d case id: %s" %(case_index, case.attributes["concept:name"]))
#       for event_index, event in enumerate(case):
#            print(type(event))
#            if (event == value):
#                print("true")
#            else:
#                print("false")
#            print("event index: %s event activity: %s" %(event_index, event["concept:name"]))

#activity_cardinality(log,"decide")

from pm4py.objects.log.log import Trace
def new_activity_cardinality(log, value, attribute_key):
    for trace in log:
        new_trace = Trace()
        found = False
        for j in range(len(trace)):
            if attribute_key in trace[j]:
                attribute_value = trace[j][attribute_key]
                if(attribute_value == value):
                    print()

new_activity_cardinality(log,"Sean","org:resource")

#print(log)




from pm4py.algo.filtering.log.attributes import attributes_filter
activities = attributes_filter.get_attribute_values(log, "concept:name")
resources = attributes_filter.get_attribute_values(log, "org:resource")

from pm4py.util import constants
tracefilter_log_pos = attributes_filter.apply(log, ["Sean"],
                                          parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "org:resource", "positive": True})
tracefilter_log_neg = attributes_filter.apply(log, ["Sean"],
                                          parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "org:resource", "positive": False})

#print(activities)
#print(resources)
#print(tracefilter_log_pos)
#print(tracefilter_log_neg)




from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as visualizer

net, initial_marking, final_marking = alpha_miner.apply(log)
gviz = visualizer.apply(net, initial_marking, final_marking)
visualizer.view(gviz)

places = net.places
transitions = net.transitions
arcs = net.arcs

for place in places:
 print("\nPLACE: "+place.name)
 for arc in place.in_arcs:
  print(arc.source.name, arc.source.label)