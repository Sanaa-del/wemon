import json
import sys
import copy
import matplotlib.pyplot as plt
import numpy as np

# GET THE ENTIRE LIST OF METRICS COLLECTED
#initial_raw_metrics_data = open("rawMetrics_old_no_wifi_avail")

#initial_metrics_in_json_format = json.load(initial_raw_metrics_data)

#print("new lens metrics", len(initial_metrics_in_json_format))

#second_round_metrics = open("precombMetrics")
with open('/home/sghandi/Téléchargements/wemon-main/LWIP.Metrics.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


second_round_json_format = data
print("second round", len(second_round_json_format))


normal_count = 0
bandwidth_count = 0
packet_loss_count = 0
delay_count = 0
wifi_availability_count = 0
user_machine_count = 0

for metric in second_round_json_format:
    if "Normal" in metric.get("scenario"):
        normal_count +=1
    elif "Bandwidth" in metric.get("scenario"):
        bandwidth_count +=1

    elif "Delay" in metric.get("scenario"):
        delay_count +=1
    
    elif "Loss" in metric.get("scenario"):
        packet_loss_count +=1

    elif "Availability" in metric.get("scenario"):
            wifi_availability_count +=1

    elif "Machine" in metric.get("scenario"):
            user_machine_count +=1

    
print("normal", normal_count)
print("banswidth", bandwidth_count)
print("pkt loss", packet_loss_count)
print("delay", delay_count)
print("wifi avail", wifi_availability_count)
print("user_machine", user_machine_count)

# to_add_to_second_round_unfiltered = []
# for index in range(1822, 1896):
#     new_metric = initial_metrics_in_json_format[index]
#     if "machine" in new_metric.get("scenario"):
#         # print("before", new_metric["scenario"])
#         new_metric["scenario"] = "Server Overload 0.75"
#         to_add_to_second_round_unfiltered.append(new_metric)
#         print("after", new_metric["scenario"])

# for index in range(1896, 1970):
#     new_metric = initial_metrics_in_json_format[index]
#     if "machine" in new_metric.get("scenario"):
#         # print("before", new_metric["scenario"])
#         new_metric["scenario"] = "Server Overload 0.5"
#         to_add_to_second_round_unfiltered.append(new_metric)
#         print("after", new_metric["scenario"])
# for index in range(1970, 1978):
#     new_metric = initial_metrics_in_json_format[index]
#     if "machine" in new_metric.get("scenario"):
#         # print("before", new_metric["scenario"])
#         new_metric["scenario"] = "Server Overload 0.3"
#         to_add_to_second_round_unfiltered.append(new_metric)
#         print("after", new_metric["scenario"])



# combine the data sets and correct for the server overload labelling errors
to_add_to_second_round_unfiltered = []
for metric in initial_metrics_in_json_format:
     if "Interference" in metric.get("scenario"):
          to_add_to_second_round_unfiltered.append(metric)

for index in range(1822, 1896):
    new_metric = initial_metrics_in_json_format[index]
    if "machine" in new_metric.get("scenario").lower():
        # print("before", new_metric["scenario"])
        new_metric["scenario"] = "Server Overload 0.75"
        to_add_to_second_round_unfiltered.append(new_metric)
        print("after", new_metric["scenario"])

for index in range(1896, 1970):
    new_metric = initial_metrics_in_json_format[index]
    if "machine" in new_metric.get("scenario").lower():
        print("before", new_metric["scenario"])
        new_metric["scenario"] = "Server Overload 0.5"
        to_add_to_second_round_unfiltered.append(new_metric)
        print("after", new_metric["scenario"])
for index in range(1970, 1983):
    new_metric = initial_metrics_in_json_format[index]
    if "machine" in new_metric.get("scenario").lower():
        print("before", new_metric["scenario"])
        new_metric["scenario"] = "Server Overload 0.3"
        to_add_to_second_round_unfiltered.append(new_metric)
        print("after", new_metric["scenario"])

print("allserverlensunfiltered", len(to_add_to_second_round_unfiltered))
# Remove any metrics that were not written to local database correctly

# unedited_intial_metrics = copy.deepcopy(initial_metrics_in_json_format)
# removed_so_far = 0
# for index in range(len(unedited_intial_metrics)):
#     if ((not (unedited_intial_metrics[index].get("scenario"))) or
#         (not unedited_intial_metrics[index].get("networkInfo")) or 
#         (not unedited_intial_metrics[index].get("cpuInfo")) or
#         (not unedited_intial_metrics[index].get("systemInfo")) or
#         (not unedited_intial_metrics[index].get("webInfo") )):
#         initial_metrics_in_json_format.pop(index - removed_so_far)
#         removed_so_far +=1

unedited_second_metrics = copy.deepcopy(second_round_json_format)
removed_so_far = 0
for index in range(len(unedited_second_metrics)):
    if ((not (unedited_second_metrics[index].get("scenario"))) or
        (not unedited_second_metrics[index].get("networkInfo")) or 
        (not unedited_second_metrics[index].get("cpuInfo")) or
        (not unedited_second_metrics[index].get("systemInfo")) or
        (not unedited_second_metrics[index].get("webInfo") )):
        second_round_json_format.pop(index - removed_so_far)
        removed_so_far +=1

removed_so_far = 0
to_add_to_second_round = copy.deepcopy(to_add_to_second_round_unfiltered)
for index in range(len(to_add_to_second_round_unfiltered)):
    if ((not (to_add_to_second_round_unfiltered[index].get("scenario"))) or
        (not to_add_to_second_round_unfiltered[index].get("networkInfo")) or 
        (not to_add_to_second_round_unfiltered[index].get("cpuInfo")) or
        (not to_add_to_second_round_unfiltered[index].get("systemInfo")) or
        (not to_add_to_second_round_unfiltered[index].get("webInfo") )):
        to_add_to_second_round.pop(index - removed_so_far)
        removed_so_far +=1

# print("to_add_second", to_add_to_second_round)
#remove the correlated data and change it to user load

print("lenofsecond", len(second_round_json_format))
print("len0ffilteredadditiins", len(to_add_to_second_round))
all_metrics_before_cpu_delta = second_round_json_format + to_add_to_second_round
print("lenafteradding", len(all_metrics_before_cpu_delta))
metrics_after_cpu_data = copy.deepcopy(all_metrics_before_cpu_delta)



# The labels are not yet updated to reflect the ML model
for data_sample_index in range(0, len(all_metrics_before_cpu_delta)):
    previous_data_point = all_metrics_before_cpu_delta[data_sample_index - 1].get("cpuInfo")["cpuProcessors"][0]["usage"]
    data_point1_usage = all_metrics_before_cpu_delta[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]

    idle_delta = data_point1_usage["idle"] - previous_data_point["idle"]
    kernel_delta = data_point1_usage["kernel"] - previous_data_point["kernel"]
    total_delta = data_point1_usage["total"] - previous_data_point["total"]
    user_delta = data_point1_usage["user"] - previous_data_point["user"]
    
   
    # print("load computed", all_metrics_before_cpu_delta[data_sample_index]["scenario"], ":" , load)

    if (user_delta>=0) and (kernel_delta >=0)  and total_delta >0:
        data_point1_usage["kernel"] = kernel_delta
        data_point1_usage["total"] = total_delta
        data_point1_usage["user"] = user_delta
        load = (user_delta + kernel_delta)/total_delta
        data_point1_usage["load"] = load
        metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"] = data_point1_usage
        # print("disovered", user_delta, kernel_delta)
        # print("\n after", metrics_after_cpu_data[data_sample_index]["scenario"], 
        #     metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["idle"],
        #                         metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["kernel"],
        #                         metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["total"],
        #                         metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["user"],
        #                         metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])
    
    else:
        # print("previos data point",all_metrics_before_cpu_delta[data_sample_index - 1]["scenario"], data_point1_usage["idle"],
        #                         data_point1_usage["kernel"],
        #                         data_point1_usage["total"],
        #                         data_point1_usage["user"] )
        # print("before change-current", all_metrics_before_cpu_delta[data_sample_index]["scenario"], data_point1_usage["idle"],
        #                         data_point1_usage["kernel"],
        #                         data_point1_usage["total"],
        #                         data_point1_usage["user"])
        # print("declined:", kernel_delta, user_delta, total_delta)
        # print("declined bool:", kernel_delta>=0, user_delta>=0, total_delta>0)
        load = (data_point1_usage["user"]  + data_point1_usage["kernel"] )/data_point1_usage["total"] 
        data_point1_usage["load"] = load
        metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"] = data_point1_usage

    # print("load error0", metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

for data_sample_index in range(1, len(all_metrics_before_cpu_delta)):
    previous_data_point = all_metrics_before_cpu_delta[data_sample_index - 1].get("cpuInfo")["cpuProcessors"][1]["usage"]
    data_point1_usage = all_metrics_before_cpu_delta[data_sample_index]["cpuInfo"]["cpuProcessors"][1]["usage"]
    
    idle_delta = data_point1_usage["idle"] - previous_data_point["idle"]
    kernel_delta = data_point1_usage["kernel"] - previous_data_point["kernel"]
    total_delta = data_point1_usage["total"] - previous_data_point["total"]
    user_delta = data_point1_usage["user"] - previous_data_point["user"]
    load = (user_delta + kernel_delta)/total_delta
    # load_points.append(load)

    if (user_delta>=0) and (kernel_delta >=0)  and total_delta >0:
        data_point1_usage["kernel"] = kernel_delta
        data_point1_usage["total"] = total_delta
        data_point1_usage["user"] = user_delta
        data_point1_usage["load"] = load
        metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][1]["usage"] = data_point1_usage
    else:
        load = (data_point1_usage["user"]  + data_point1_usage["kernel"] )/data_point1_usage["total"] 
        data_point1_usage["load"] = load
        metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][1]["usage"] = data_point1_usage

    # print("load error1", metrics_after_cpu_data[data_sample_index]["cpuInfo"]["cpuProcessors"][1]["usage"]["load"])

removed_so_far = 0
metrics_to_edit = copy.deepcopy(metrics_after_cpu_data)

for index in range(len(metrics_to_edit)):
    if ((not (metrics_to_edit[index].get("scenario"))) or
        (not metrics_to_edit[index].get("networkInfo")) or 
        (not metrics_to_edit[index].get("cpuInfo")) or
        (not metrics_to_edit[index].get("systemInfo")) or
        (not metrics_to_edit[index].get("webInfo") )):
        metrics_after_cpu_data.pop(index - removed_so_far)
        removed_so_far +=1

print("lenmetricsweeedingcupu data", len(metrics_after_cpu_data))
# TODO: Change the labels in metrics after cpu_data
load_points = dict()
load_points["Network Bandwidth"] = []
load_points["Network Delay"] = []
load_points["Network Loss"] = []
load_points["Wi-Fi Interference"] = []
load_points["User's Machine Overload"] = []
load_points["Server Overload"] = []
load_points["Normal"] = []
load_points["Wi-Fi Availability"] = []


for metric in metrics_after_cpu_data:
    if "normal" in metric.get("scenario").lower():
        metric["scenario"] = "Normal Scenario"
        # print("load error", metric["cpuInfo"]["cpuProcessors"][0]["usage"])
        load_points["Normal"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])
    
    elif "bandwidth" in metric.get("scenario").lower():
        metric["scenario"] = "Network Bandwidth"
        load_points["Network Bandwidth"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])
    
    elif "delay" in metric.get("scenario").lower():
        metric["scenario"] = "Network Delay"
        load_points["Network Delay"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

    elif "loss" in metric.get("scenario").lower():
        metric["scenario"] = "Network Loss"
        load_points["Network Loss"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

    elif "interference" in metric.get("scenario").lower():
        metric["scenario"] = "Wi-Fi Interference"
        load_points["Wi-Fi Interference"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

    
    elif "availability" in metric.get("scenario").lower():
        metric["scenario"] = "Wi-Fi Availability"
        load_points["Wi-Fi Availability"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

    elif "user" in metric.get("scenario").lower():
        metric["scenario"] = "User's Machine Overload"
        load_points["User's Machine Overload"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

    elif "server" in metric.get("scenario").lower():
        metric["scenario"] = "Server Overload"
        load_points["Server Overload"].append(metric["cpuInfo"]["cpuProcessors"][0]["usage"]["load"])

        print("got to final server edit")


# start_normal_index = 0
end_normal_index = 0
next_scenario = False
while not next_scenario:
    if metrics_after_cpu_data[end_normal_index]["scenario"] == "Normal Scenario":
       end_normal_index +=1
    else:
       next_scenario = True
#filters
# FILTER Functions for the rumsi threshold metrics
def rumsi_value_0_filter(json_object):
    rumsi_index_threshold = 0
    if json_object["webInfo"]["RUMSpeedIndex"] >= rumsi_index_threshold:
        return True

def rumsi_value_1_filter(json_object):
    rumsi_index_threshold = 1
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True

def rumsi_value_2_filter(json_object):
    rumsi_index_threshold = 2
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True


# def rumsi_value_2_5_filter(json_object):
#     rumsi_index_threshold = 2.5
#     if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
#         return True
    
def rumsi_value_3_filter(json_object):
    rumsi_index_threshold = 3
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True

def rumsi_value_4_filter(json_object):
    rumsi_index_threshold = 4
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True
    
def rumsi_value_5_filter(json_object):
    rumsi_index_threshold = 5
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True
    
def rumsi_value_10_filter(json_object):
    rumsi_index_threshold = 10
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True

def rumsi_value_20_filter(json_object):
    rumsi_index_threshold = 20
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True

def rumsi_value_30_filter(json_object):
    rumsi_index_threshold = 30
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True
    
def rumsi_value_40_filter(json_object):
    rumsi_index_threshold = 40
    if json_object["webInfo"]["RUMSpeedIndex"] > rumsi_index_threshold:
        return True
    
rumsi_greater_0_metrics = list(filter(rumsi_value_0_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_1_metrics = list(filter(rumsi_value_1_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_2_metrics = list(filter(rumsi_value_2_filter, metrics_after_cpu_data[end_normal_index:]))
# rumsi_greater_2_5_metrics = list(filter(rumsi_value_2_5_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_3_metrics = list(filter(rumsi_value_3_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_4_metrics = list(filter(rumsi_value_4_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_5_metrics = list(filter(rumsi_value_5_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_10_metrics = list(filter(rumsi_value_10_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_20_metrics = list(filter(rumsi_value_20_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_30_metrics = list(filter(rumsi_value_30_filter, metrics_after_cpu_data[end_normal_index:]))
rumsi_greater_40_metrics = list(filter(rumsi_value_40_filter, metrics_after_cpu_data[end_normal_index:]))

print("lens of ommitted", len(rumsi_greater_0_metrics)) #1233
# less than 5 rumsi 
# TODO INCLUDE 0 - 1,2,3
print("rumsi0", len(rumsi_greater_0_metrics)) #2416
print("rumsi1", len(rumsi_greater_1_metrics)) #2372
print("rumsi2", len(rumsi_greater_2_metrics)) #2047
# print("rumsi2.5", len(rumsi_greater_2_5_metrics)) #2047
print("rumsi3", len(rumsi_greater_3_metrics)) #1583
print("rumsi4", len(rumsi_greater_4_metrics)) #1157
print("rumsi5", len(rumsi_greater_5_metrics)) # 842 894
print("rumsi10", len(rumsi_greater_10_metrics)) #157 172
print("rumsi20", len(rumsi_greater_20_metrics)) #20 25
print("rumsi30", len(rumsi_greater_30_metrics)) #11 14
print("rumsi40", len(rumsi_greater_40_metrics)) #9 10

def count_metrics_speed_threshold (metrics):
    normal_count = 0
    bandwidth_count = 0
    packet_loss_count = 0
    delay_count = 0
    wifi_availability_count = 0
    user_machine_count = 0
    server_count = 0
    interference_count = 0

    for metric in metrics:
        if "Normal" in metric.get("scenario"):
            normal_count +=1
        elif "Bandwidth" in metric.get("scenario"):
            bandwidth_count +=1

        elif "Delay" in metric.get("scenario"):
            delay_count +=1
        
        elif "Loss" in metric.get("scenario"):
            packet_loss_count +=1

        elif "Availability" in metric.get("scenario"):
                wifi_availability_count +=1

        elif "Machine" in metric.get("scenario"):
                user_machine_count +=1
        
        elif "Server" in metric.get("scenario"):
                server_count +=1

        elif "Interference" in metric.get("scenario"):
                interference_count +=1
    
    counts_dict = dict()  
    counts_dict["normal_count"] = normal_count
    counts_dict["bandwidth_count"] = bandwidth_count
    counts_dict["packet_loss_count"] = packet_loss_count
    counts_dict["delay_count"] = delay_count
    counts_dict["wifi_availability_count"] = wifi_availability_count
    counts_dict["user_machine_count"] = user_machine_count
    counts_dict["server_count"] = server_count
    counts_dict["interference_count"] = interference_count

    return counts_dict

def metric_per_anomaly(metrics):
    metrics_dict = dict()
    metrics_dict["normal_domparse"] = []
    metrics_dict["normal_response"] = []
    metrics_dict["normal_domscripts"]= []
    metrics_dict["normal_dom"]= []
    metrics_dict["normal_downlink"]= []
    metrics_dict["normal_cpuload"]= []
    metrics_dict["normal_RUMSI"]= []
    metrics_dict["normal_pageloadtime"]= []
    metrics_dict["normal_rtt"]= []
    
    metrics_dict["bandwidth_domparse"]= []
    metrics_dict["bandwidth_response"]= []
    metrics_dict["bandwidth_domscripts"]= []
    metrics_dict["bandwidth_dom"]= []
    metrics_dict["bandwidth_downlink"]= []
    metrics_dict["bandwidth_cpuload"]= []
    metrics_dict["bandwidth_RUMSI"]= []
    metrics_dict["bandwidth_pageloadtime"]= []
    metrics_dict["bandwidth_rtt"]= []

    metrics_dict["packetloss_domparse"]= []
    metrics_dict["packetloss_response"]= []
    metrics_dict["packetloss_domscripts"]= []
    metrics_dict["packetloss_dom"]= []
    metrics_dict["packetloss_downlink"]= []
    metrics_dict["packetloss_cpuload"]= []
    metrics_dict["packetloss_RUMSI"]= []
    metrics_dict["packetloss_pageloadtime"]= []
    metrics_dict["packetloss_rtt"]= []

    metrics_dict["packetdelay_domparse"]= []
    metrics_dict["packetdelay_response"]= []
    metrics_dict["packetdelay_domscripts"]= []
    metrics_dict["packetdelay_dom"]= []
    metrics_dict["packetdelay_downlink"]= []
    metrics_dict["packetdelay_cpuload"]= []
    metrics_dict["packetdelay_RUMSI"]= []
    metrics_dict["packetdelay_pageloadtime"]= []
    metrics_dict["packetdelay_rtt"]= []

    metrics_dict["wifi_availability_domparse"]= []
    metrics_dict["wifi_availability_response"]= []
    metrics_dict["wifi_availability_domscripts"]= []
    metrics_dict["wifi_availability_dom"]= []
    metrics_dict["wifi_availability_downlink"] = []
    metrics_dict["wifi_availability_cpuload"]= []
    metrics_dict["wifi_availability_RUMSI"]= []
    metrics_dict["wifi_availability_pageloadtime"] = []
    metrics_dict["wifi_availability_rtt"]= []

    metrics_dict["interference_domparse"] = []
    metrics_dict["interference_response"]= []
    metrics_dict["interference_domscripts"]= []
    metrics_dict["interference_dom"]= []
    metrics_dict["interference_downlink"]= []
    metrics_dict["interference_cpuload"]= []
    metrics_dict["interference_RUMSI"]= []
    metrics_dict["interference_pageloadtime"]= []
    metrics_dict["interference_rtt"]= []

    metrics_dict["user_domparse"]= []
    metrics_dict["user_response"]= []
    metrics_dict["user_domscripts"]= []
    metrics_dict["user_dom"]= []
    metrics_dict["user_downlink"]= []
    metrics_dict["user_cpuload"]= []
    metrics_dict["user_RUMSI"]= []
    metrics_dict["user_pageloadtime"]= []
    metrics_dict["user_rtt"]= []

    metrics_dict["cpu_domparse"]= []
    metrics_dict["cpu_response"]= []
    metrics_dict["cpu_domscripts"]= []
    metrics_dict["cpu_dom"]= []
    metrics_dict["cpu_downlink"]= []
    metrics_dict["cpu_cpuload"]= []
    metrics_dict["cpu_RUMSI"]= []
    metrics_dict["cpu_pageloadtime"]= []
    metrics_dict["cpu_rtt"]= []

    domparse_list = []
    response_list= []
    domscripts_list= []
    dom_list= []
    downlink_list= []
    cpuload_list= []
    pageloadtime_list= []
    rtt_list= []
    for metric in metrics:
        # domparse_list.append(tuple(metric.get("webInfo").get("domParse"),metric.get("webInfo").get("RUMSpeedIndex")))
        # response_list.append(tuple(metric.get("webInfo").get("response"), metric.get("webInfo").get("RUMSpeedIndex")))
        # domscripts_list.append(tuple(metric.get("webInfo").get("domScripts"), metric.get("webInfo").get("RUMSpeedIndex")))
        # dom_list.append(metric.get("webInfo").get("dom"), metric.get("webInfo").get("RUMSpeedIndex"))
        # downlink_list.append(tuple(metric.get("networkInfo").get("downlink"), metric.get("webInfo").get("RUMSpeedIndex")))
        # cpuload_list.append(tuple(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"], metric.get("webInfo").get("RUMSpeedIndex")))
        # pageloadtime_list.append(tuple(metric.get("webInfo").get("pageloadtime"), metric.get("webInfo").get("RUMSpeedIndex")))
        # rtt_list.append(metric.get("networkInfo").get("rtt"), metric.get("webInfo").get("RUMSpeedIndex"))

        if "Normal" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["normal_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["normal_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["normal_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["normal_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["normal_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["normal_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["normal_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["normal_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["normal_rtt"].append(metric.get("networkInfo").get("rtt"))

        elif "Bandwidth" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["bandwidth_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["bandwidth_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["bandwidth_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["bandwidth_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["bandwidth_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["bandwidth_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["bandwidth_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["bandwidth_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["bandwidth_rtt"].append(metric.get("networkInfo").get("rtt"))          

        elif "Delay" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["packetdelay_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["packetdelay_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["packetdelay_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["packetdelay_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["packetdelay_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["packetdelay_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["packetdelay_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["packetdelay_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["packetdelay_rtt"].append(metric.get("networkInfo").get("rtt"))          
        
        elif "Loss" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["packetloss_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["packetloss_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["packetloss_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):   
                metrics_dict["packetloss_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["packetloss_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["packetloss_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["packetloss_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["packetloss_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["packetloss_rtt"].append(metric.get("networkInfo").get("rtt"))
            

        elif "Availability" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["wifi_availability_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["wifi_availability_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["wifi_availability_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["wifi_availability_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["wifi_availability_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["wifi_availability_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["wifi_availability_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["wifi_availability_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["wifi_availability_rtt"].append(metric.get("networkInfo").get("rtt"))               

        elif "Machine" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["cpu_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["cpu_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["cpu_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["cpu_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["cpu_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["cpu_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["cpu_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["cpu_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["cpu_rtt"].append(metric.get("networkInfo").get("rtt"))        
        
        elif "Server" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["user_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["user_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["user_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["user_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["user_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["user_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["user_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["user_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["user_rtt"].append(metric.get("networkInfo").get("rtt"))             

        elif "Interference" in metric.get("scenario"):
            if metric.get("webInfo").get("domParse"):
                metrics_dict["interference_domparse"].append(metric.get("webInfo").get("domParse"))
            if metric.get("webInfo").get("response"):
                metrics_dict["interference_response"].append(metric.get("webInfo").get("response"))
            if metric.get("webInfo").get("domScripts"):
                metrics_dict["interference_domscripts"].append(metric.get("webInfo").get("domScripts"))
            if metric.get("webInfo").get("dom"):
                metrics_dict["interference_dom"].append(metric.get("webInfo").get("dom"))
            if metric.get("networkInfo").get("downlink"):
                metrics_dict["interference_downlink"].append(metric.get("networkInfo").get("downlink"))
            if metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"]:
                metrics_dict["interference_cpuload"].append(metric.get("cpuInfo")["cpuProcessors"][0]["usage"]["load"])
            if metric.get("webInfo").get("RUMSpeedIndex"):
                metrics_dict["interference_RUMSI"].append(metric.get("webInfo").get("RUMSpeedIndex"))
            if metric.get("webInfo").get("pageloadtime"):
                metrics_dict["interference_pageloadtime"].append(metric.get("webInfo").get("pageloadtime"))
            if metric.get("networkInfo").get("rtt"):
                metrics_dict["interference_rtt"].append(metric.get("networkInfo").get("rtt"))              

    return (metrics_dict, domparse_list, response_list, 
    domscripts_list, 
    dom_list,downlink_list, cpuload_list, pageloadtime_list, rtt_list)

# TODO: Count number of scenarios in each of the speed index

# speed_2_5_statistics = count_metrics_speed_threshold(rumsi_greater_2_5_metrics)
speed_0_statistics = count_metrics_speed_threshold(rumsi_greater_0_metrics)
speed_1_statistics = count_metrics_speed_threshold(rumsi_greater_1_metrics)
speed_2_statistics = count_metrics_speed_threshold(rumsi_greater_2_metrics)
speed_3_statistics = count_metrics_speed_threshold(rumsi_greater_3_metrics)
speed_4_statistics = count_metrics_speed_threshold(rumsi_greater_4_metrics)
speed_5_statistics = count_metrics_speed_threshold(rumsi_greater_5_metrics)
speed_10_statistics = count_metrics_speed_threshold(rumsi_greater_10_metrics)
speed_20_statistics = count_metrics_speed_threshold(rumsi_greater_20_metrics)
speed_30_statistics = count_metrics_speed_threshold(rumsi_greater_30_metrics)
speed_40_statistics = count_metrics_speed_threshold(rumsi_greater_40_metrics)

print("speed0 statistics", speed_0_statistics)
print("speed1 statistics", speed_1_statistics)
print("speed2 statistics", speed_2_statistics)
# print("speed2_5 statistics", speed_2_5_statistics)
print("speed3 statistics", speed_3_statistics)
print("speed4 statistics", speed_4_statistics)
print("speed5 statistics", speed_5_statistics)
print("speed10 statistics", speed_10_statistics)
print("speed20 statistics", speed_20_statistics)
print("speed30 statistics", speed_40_statistics)
print("speed40 statistics", speed_40_statistics)

# speed0 statistics {'normal_count': 0, 'bandwidth_count': 372, 'packet_loss_count': 450, 'delay_count': 376, 'wifi_availability_count': 374, 'user_machine_count': 300, 'server_count': 155, 'interference_count': 389}
# speed1 statistics {'normal_count': 0, 'bandwidth_count': 366, 'packet_loss_count': 443, 'delay_count': 364, 'wifi_availability_count': 370, 'user_machine_count': 292, 'server_count': 154, 'interference_count': 383}
# speed2 statistics {'normal_count': 0, 'bandwidth_count': 315, 'packet_loss_count': 371, 'delay_count': 295, 'wifi_availability_count': 330, 'user_machine_count': 255, 'server_count': 139, 'interference_count': 342}
# speed3 statistics {'normal_count': 0, 'bandwidth_count': 230, 'packet_loss_count': 266, 'delay_count': 210, 'wifi_availability_count': 288, 'user_machine_count': 204, 'server_count': 113, 'interference_count': 272}
# speed4 statistics {'normal_count': 0, 'bandwidth_count': 151, 'packet_loss_count': 183, 'delay_count': 138, 'wifi_availability_count': 254, 'user_machine_count': 152, 'server_count': 88, 'interference_count': 191}
# speed5 statistics {'normal_count': 0, 'bandwidth_count': 104, 'packet_loss_count': 128, 'delay_count': 89, 'wifi_availability_count': 237, 'user_machine_count': 113, 'server_count': 77, 'interference_count': 146}
# speed10 statistics {'normal_count': 0, 'bandwidth_count': 18, 'packet_loss_count': 20, 'delay_count': 7, 'wifi_availability_count': 33, 'user_machine_count': 29, 'server_count': 17, 'interference_count': 48}
# speed20 statistics {'normal_count': 0, 'bandwidth_count': 2, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 2, 'user_machine_count': 7, 'server_count': 5, 'interference_count': 6}
# speed30 statistics {'normal_count': 0, 'bandwidth_count': 0, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 0, 'user_machine_count': 3, 'server_count': 1, 'interference_count': 3}
# speed40 statistics {'normal_count': 0, 'bandwidth_count': 0, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 0, 'user_machine_count': 3, 'server_count': 1, 'interference_count': 3}


# OLD AND OBSOLETE
# speed2_5 statistics {'normal_count': 0, 'bandwidth_count': 315, 'packet_loss_count': 371, 'delay_count': 295, 'wifi_availability_count': 330, 'user_machine_count': 255, 'server_count': 139, 'interference_count': 342}
# speed3 statistics {'normal_count': 0, 'bandwidth_count': 230, 'packet_loss_count': 266, 'delay_count': 210, 'wifi_availability_count': 288, 'user_machine_count': 204, 'server_count': 113, 'interference_count': 272}
# speed4 statistics {'normal_count': 0, 'bandwidth_count': 151, 'packet_loss_count': 183, 'delay_count': 138, 'wifi_availability_count': 254, 'user_machine_count': 152, 'server_count': 88, 'interference_count': 191}

#speed5 statistics {'normal_count': 25, 'bandwidth_count': 104, 'packet_loss_count': 128, 'delay_count': 89, 'wifi_availability_count': 237, 'user_machine_count': 113, 'server_count': 5}
# speed10 statistics {'normal_count': 2, 'bandwidth_count': 18, 'packet_loss_count': 20, 'delay_count': 7, 'wifi_availability_count': 33, 'user_machine_count': 29, 'server_count': 3}
# speed20 statistics {'normal_count': 0, 'bandwidth_count': 2, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 2, 'user_machine_count': 7, 'server_count': 1}
# speed30 statistics {'normal_count': 0, 'bandwidth_count': 0, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 0, 'user_machine_count': 3, 'server_count': 0}
# speed40 statistics {'normal_count': 0, 'bandwidth_count': 0, 'packet_loss_count': 2, 'delay_count': 1, 'wifi_availability_count': 0, 'user_machine_count': 3, 'server_count': 0}

metrics_dict, domparse_list, response_list, domscripts_list, dom_list,downlink_list, cpuload_list, pageloadtime_list, rtt_list = metric_per_anomaly(metrics_after_cpu_data)

normal_domparse, normal_bins_domparse = np.histogram(np.array(metrics_dict["normal_domparse"]))
normal_pdf = normal_domparse/sum(normal_domparse)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_domparse[1:], normal_cdf, marker = 'o', label="normal domparse CDF")

bandwidth_domparse, bandwidth_bins_domparse = np.histogram(np.array(metrics_dict["bandwidth_domparse"]))
print(len(metrics_dict["bandwidth_domparse"]))
bandwidth_pdf = bandwidth_domparse/sum(bandwidth_domparse)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_domparse[1:], bandwidth_cdf, marker = 'v', label="bandwidth domparse CDF")

packetdelay_domparse, packetdelay_bins_domparse = np.histogram(np.array(metrics_dict["packetdelay_domparse"]))
packetdelay_pdf = packetdelay_domparse/sum(packetdelay_domparse)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_domparse[1:], packetdelay_cdf, marker = 's', label="packetdelay domparse CDF")

packetloss_domparse, packetloss_bins_domparse = np.histogram(np.array(metrics_dict["packetloss_domparse"]))
packetloss_pdf = packetloss_domparse/sum(packetloss_domparse)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_domparse[1:], packetloss_cdf, marker = 'P', label="packetloss domparse CDF")

wifi_availability_domparse, wifi_availability_bins_domparse = np.histogram(np.array(metrics_dict["wifi_availability_domparse"]))
wifi_availability_pdf = wifi_availability_domparse/sum(wifi_availability_domparse)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_domparse[1:], wifi_availability_cdf, marker = '*', label="wifi_availability domparse CDF")

interference_domparse, interference_bins_domparse = np.histogram(np.array(metrics_dict["interference_domparse"]), bins=10)
interference_pdf = interference_domparse/sum(interference_domparse)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_domparse[1:], interference_cdf, marker = '_', label="interference domparse CDF")

cpu_domparse, cpu_bins_domparse = np.histogram(np.array(metrics_dict["cpu_domparse"]), bins=10)
cpu_pdf = cpu_domparse/sum(cpu_domparse)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_domparse[1:], cpu_cdf, marker = '+', label="cpu domparse CDF")

user_domparse, user_bins_domparse = np.histogram(np.array(metrics_dict["user_domparse"]), bins=10)
user_pdf = user_domparse/sum(user_domparse)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_domparse[1:], user_cdf, marker = 'X', label="user domparse CDF")

plt.xlabel("webInfo domParse")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# response print
normal_response, normal_bins_response = np.histogram(np.sort(np.array(metrics_dict["normal_response"])), bins=10)
normal_pdf = normal_response/sum(normal_response)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_response[1:], normal_cdf, marker = 'o', label="normal response CDF")

bandwidth_response, bandwidth_bins_response = np.histogram(np.array(metrics_dict["bandwidth_response"]), bins=10)
bandwidth_pdf = bandwidth_response/sum(bandwidth_response)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_response[1:], bandwidth_cdf, marker = 'v', label="bandwidth response CDF")

packetdelay_response, packetdelay_bins_response = np.histogram(np.array(metrics_dict["packetdelay_response"]), bins=10)
packetdelay_pdf = packetdelay_response/sum(packetdelay_response)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_response[1:], packetdelay_cdf, marker = 's', label="packetdelay response CDF")

packetloss_response, packetloss_bins_response = np.histogram(np.array(metrics_dict["packetloss_response"]), bins=10)
packetloss_pdf = packetloss_response/sum(packetloss_response)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_response[1:], packetloss_cdf, marker = 'P', label="packetloss response CDF")

wifi_availability_response, wifi_availability_bins_response = np.histogram(np.array(metrics_dict["wifi_availability_response"]), bins=10)
wifi_availability_pdf = wifi_availability_response/sum(wifi_availability_response)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_response[1:], wifi_availability_cdf, marker = '*', label="wifi_availability response CDF")

interference_response, interference_bins_response = np.histogram(np.array(metrics_dict["interference_response"]), bins=10)
interference_pdf = interference_response/sum(interference_response)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_response[1:], interference_cdf, marker = '_', label="interference response CDF")

cpu_response, cpu_bins_response = np.histogram(np.array(metrics_dict["cpu_response"]), bins=10)
cpu_pdf = cpu_response/sum(cpu_response)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_response[1:], cpu_cdf, marker = '+', label="cpu response CDF")

user_response, user_bins_response = np.histogram(np.array(metrics_dict["user_response"]), bins=10)
user_pdf = user_response/sum(user_response)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_response[1:], user_cdf, marker = 'X', label="user response CDF")

plt.xlabel("webInfo.response")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# domScripts print
normal_domscripts, normal_bins_domscripts = np.histogram(np.array(metrics_dict["normal_domscripts"]), bins=10)
normal_pdf = normal_domscripts/sum(normal_domscripts)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_domscripts[1:], normal_cdf, marker = 'o', label="normal domscripts CDF")

bandwidth_domscripts, bandwidth_bins_domscripts = np.histogram(np.array(metrics_dict["bandwidth_domscripts"]), bins=10)
bandwidth_pdf = bandwidth_domscripts/sum(bandwidth_domscripts)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_domscripts[1:], bandwidth_cdf, marker = 'v', label="bandwidth domscripts CDF")

packetdelay_domscripts, packetdelay_bins_domscripts = np.histogram(np.array(metrics_dict["packetdelay_domscripts"]), bins=10)
packetdelay_pdf = packetdelay_domscripts/sum(packetdelay_domscripts)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_domscripts[1:], packetdelay_cdf, marker = 's', label="packetdelay domscripts CDF")

packetloss_domscripts, packetloss_bins_domscripts = np.histogram(np.array(metrics_dict["packetloss_domscripts"]), bins=10)
packetloss_pdf = packetloss_domscripts/sum(packetloss_domscripts)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_domscripts[1:], packetloss_cdf, marker = 'P', label="packetloss domscripts CDF")

wifi_availability_domscripts, wifi_availability_bins_domscripts = np.histogram(np.array(metrics_dict["wifi_availability_domscripts"]), bins=10)
wifi_availability_pdf = wifi_availability_domscripts/sum(wifi_availability_domscripts)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_domscripts[1:], wifi_availability_cdf, marker = '*', label="wifi_availability domscripts CDF")

interference_domscripts, interference_bins_domscripts = np.histogram(np.array(metrics_dict["interference_domscripts"]), bins=10)
interference_pdf = interference_domscripts/sum(interference_domscripts)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_domscripts[1:], interference_cdf, marker = '_', label="interference domscripts CDF")

cpu_domscripts, cpu_bins_domscripts = np.histogram(np.array(metrics_dict["cpu_domscripts"]), bins=10)
cpu_pdf = cpu_domscripts/sum(cpu_domscripts)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_domscripts[1:], cpu_cdf, marker = '+', label="cpu domscripts CDF")

user_domscripts, user_bins_domscripts = np.histogram(np.array(metrics_dict["user_domscripts"]), bins=10)
user_pdf = user_domscripts/sum(user_domscripts)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_domscripts[1:], user_cdf, marker = 'X', label="user domscripts CDF")

plt.xlabel("webInfo.domscripts")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# dom print
normal_dom, normal_bins_dom = np.histogram(np.array(metrics_dict["normal_dom"]), bins=10)
normal_pdf = normal_dom/sum(normal_dom)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_dom[1:], normal_cdf, marker = 'o', label="normal dom CDF")

bandwidth_dom, bandwidth_bins_dom = np.histogram(np.array(metrics_dict["bandwidth_dom"]), bins=10)
bandwidth_pdf = bandwidth_dom/sum(bandwidth_dom)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_dom[1:], bandwidth_cdf, marker = 'v', label="bandwidth dom CDF")

packetdelay_dom, packetdelay_bins_dom = np.histogram(np.array(metrics_dict["packetdelay_dom"]), bins=10)
packetdelay_pdf = packetdelay_dom/sum(packetdelay_dom)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_dom[1:], packetdelay_cdf, marker = 's', label="packetdelay dom CDF")

packetloss_dom, packetloss_bins_dom = np.histogram(np.array(metrics_dict["packetloss_dom"]), bins=10)
packetloss_pdf = packetloss_dom/sum(packetloss_dom)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_dom[1:], packetloss_cdf, marker = 'P', label="packetloss dom CDF")

wifi_availability_dom, wifi_availability_bins_dom = np.histogram(np.array(metrics_dict["wifi_availability_dom"]), bins=10)
wifi_availability_pdf = wifi_availability_dom/sum(wifi_availability_dom)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_dom[1:], wifi_availability_cdf, marker = '*', label="wifi_availability dom CDF")

interference_dom, interference_bins_dom = np.histogram(np.array(metrics_dict["interference_dom"]), bins=10)
interference_pdf = interference_dom/sum(interference_dom)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_dom[1:], interference_cdf, marker = '_', label="interference dom CDF")

cpu_dom, cpu_bins_dom = np.histogram(np.array(metrics_dict["cpu_dom"]), bins=10)
cpu_pdf = cpu_dom/sum(cpu_dom)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_dom[1:], cpu_cdf, marker = '+', label="cpu dom CDF")

user_dom, user_bins_dom = np.histogram(np.array(metrics_dict["user_dom"]), bins=10)
user_pdf = user_dom/sum(user_dom)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_dom[1:], user_cdf, marker = 'X', label="user dom CDF")

plt.xlabel("webInfo.dom")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# print downlink
normal_downlink, normal_bins_downlink = np.histogram(np.array(metrics_dict["normal_downlink"]), bins=10)
normal_pdf = normal_downlink/sum(normal_downlink)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_downlink[1:], normal_cdf, marker = 'o', label="normal downlink CDF")

bandwidth_downlink, bandwidth_bins_downlink = np.histogram(np.array(metrics_dict["bandwidth_downlink"]), bins=10)
bandwidth_pdf = bandwidth_downlink/sum(bandwidth_downlink)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_downlink[1:], bandwidth_cdf, marker = 'v', label="bandwidth downlink CDF")

packetdelay_downlink, packetdelay_bins_downlink = np.histogram(np.array(metrics_dict["packetdelay_downlink"]), bins=10)
packetdelay_pdf = packetdelay_downlink/sum(packetdelay_downlink)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_downlink[1:], packetdelay_cdf, marker = 's', label="packetdelay downlink CDF")

packetloss_downlink, packetloss_bins_downlink = np.histogram(np.array(metrics_dict["packetloss_downlink"]), bins=10)
packetloss_pdf = packetloss_downlink/sum(packetloss_downlink)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_downlink[1:], packetloss_cdf, marker = 'P', label="packetloss downlink CDF")

wifi_availability_downlink, wifi_availability_bins_downlink = np.histogram(np.array(metrics_dict["wifi_availability_downlink"]), bins=10)
wifi_availability_pdf = wifi_availability_downlink/sum(wifi_availability_downlink)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_downlink[1:], wifi_availability_cdf, marker = '*', label="wifi_availability downlink CDF")

interference_downlink, interference_bins_downlink = np.histogram(np.array(metrics_dict["interference_downlink"]), bins=10)
interference_pdf = interference_downlink/sum(interference_downlink)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_downlink[1:], interference_cdf, marker = '_', label="interference downlink CDF")

cpu_downlink, cpu_bins_downlink = np.histogram(np.array(metrics_dict["cpu_downlink"]), bins=10)
cpu_pdf = cpu_downlink/sum(cpu_downlink)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_downlink[1:], cpu_cdf, marker = '+', label="cpu downlink CDF")

user_downlink, user_bins_downlink = np.histogram(np.array(metrics_dict["user_downlink"]), bins=10)
user_pdf = user_downlink/sum(user_downlink)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_downlink[1:], user_cdf, marker = 'X', label="user downlink CDF")

plt.xlabel("networkInfo.downlink")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# cpu load print
normal_cpuload, normal_bins_cpuload = np.histogram(np.array(metrics_dict["normal_cpuload"]), bins=10)
normal_pdf = normal_cpuload/sum(normal_cpuload)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_cpuload[1:], normal_cdf, marker = 'o', label="normal cpuload CDF")

bandwidth_cpuload, bandwidth_bins_cpuload = np.histogram(np.array(metrics_dict["bandwidth_cpuload"]), bins=10)
bandwidth_pdf = bandwidth_cpuload/sum(bandwidth_cpuload)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_cpuload[1:], bandwidth_cdf, marker = 'v', label="bandwidth cpuload CDF")

packetdelay_cpuload, packetdelay_bins_cpuload = np.histogram(np.array(metrics_dict["packetdelay_cpuload"]), bins=10)
packetdelay_pdf = packetdelay_cpuload/sum(packetdelay_cpuload)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_cpuload[1:], packetdelay_cdf, marker = 's', label="packetdelay cpuload CDF")

packetloss_cpuload, packetloss_bins_cpuload = np.histogram(np.array(metrics_dict["packetloss_cpuload"]), bins=10)
packetloss_pdf = packetloss_cpuload/sum(packetloss_cpuload)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_cpuload[1:], packetloss_cdf, marker = 'P', label="packetloss cpuload CDF")

wifi_availability_cpuload, wifi_availability_bins_cpuload = np.histogram(np.array(metrics_dict["wifi_availability_cpuload"]), bins=10)
wifi_availability_pdf = wifi_availability_cpuload/sum(wifi_availability_cpuload)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_cpuload[1:], wifi_availability_cdf, marker = '*', label="wifi_availability cpuload CDF")

interference_cpuload, interference_bins_cpuload = np.histogram(np.array(metrics_dict["interference_cpuload"]), bins=10)
interference_pdf = interference_cpuload/sum(interference_cpuload)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_cpuload[1:], interference_cdf, marker = '_', label="interference cpuload CDF")

cpu_cpuload, cpu_bins_cpuload = np.histogram(np.array(metrics_dict["cpu_cpuload"]), bins=10)
cpu_pdf = cpu_cpuload/sum(cpu_cpuload)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_cpuload[1:], cpu_cdf, marker = '+', label="cpu cpuload CDF")

user_cpuload, user_bins_cpuload = np.histogram(np.array(metrics_dict["user_cpuload"]), bins=10)
user_pdf = user_cpuload/sum(user_cpuload)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_cpuload[1:], user_cdf, marker = 'X', label="user cpuload CDF")

plt.xlabel("CPU Load")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

# speedindex print
normal_RUMSI, normal_bins_RUMSI = np.histogram(np.array(metrics_dict["normal_RUMSI"]), bins=10)
normal_pdf = normal_RUMSI/sum(normal_RUMSI)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_RUMSI[1:], normal_cdf, marker = 'o', label="normal RUMSI CDF")

bandwidth_RUMSI, bandwidth_bins_RUMSI = np.histogram(np.array(metrics_dict["bandwidth_RUMSI"]), bins=10)
bandwidth_pdf = bandwidth_RUMSI/sum(bandwidth_RUMSI)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_RUMSI[1:], bandwidth_cdf, marker = 'v', label="bandwidth RUMSI CDF")

packetdelay_RUMSI, packetdelay_bins_RUMSI = np.histogram(np.array(metrics_dict["packetdelay_RUMSI"]), bins=10)
packetdelay_pdf = packetdelay_RUMSI/sum(packetdelay_RUMSI)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_RUMSI[1:], packetdelay_cdf, marker = 's', label="packetdelay RUMSI CDF")

packetloss_RUMSI, packetloss_bins_RUMSI = np.histogram(np.array(metrics_dict["packetloss_RUMSI"]), bins=10)
packetloss_pdf = packetloss_RUMSI/sum(packetloss_RUMSI)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_RUMSI[1:], packetloss_cdf, marker = 'P', label="packetloss RUMSI CDF")

wifi_availability_RUMSI, wifi_availability_bins_RUMSI = np.histogram(np.array(metrics_dict["wifi_availability_RUMSI"]), bins=10)
wifi_availability_pdf = wifi_availability_RUMSI/sum(wifi_availability_RUMSI)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_RUMSI[1:], wifi_availability_cdf, marker = '*', label="wifi_availability RUMSI CDF")

interference_RUMSI, interference_bins_RUMSI = np.histogram(np.array(metrics_dict["interference_RUMSI"]), bins=10)
interference_pdf = interference_RUMSI/sum(interference_RUMSI)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_RUMSI[1:], interference_cdf, marker = '_', label="interference RUMSI CDF")

cpu_RUMSI, cpu_bins_RUMSI = np.histogram(np.array(metrics_dict["cpu_RUMSI"]), bins=10)
cpu_pdf = cpu_RUMSI/sum(cpu_RUMSI)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_RUMSI[1:], cpu_cdf, marker = '+', label="cpu RUMSI CDF")

user_RUMSI, user_bins_RUMSI = np.histogram(np.array(metrics_dict["user_RUMSI"]), bins=10)
user_pdf = user_RUMSI/sum(user_RUMSI)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_RUMSI[1:], user_cdf, marker = 'X', label="user RUMSI CDF")

plt.xlabel("webInfo RUMSI")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()

#pageloadtime print
normal_pageloadtime, normal_bins_pageloadtime = np.histogram(np.array(metrics_dict["normal_pageloadtime"]), bins=10)
normal_pdf = normal_pageloadtime/sum(normal_pageloadtime)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_pageloadtime[1:], normal_cdf, marker = 'o', label="normal pageloadtime CDF")

bandwidth_pageloadtime, bandwidth_bins_pageloadtime = np.histogram(np.array(metrics_dict["bandwidth_pageloadtime"]), bins=10)
bandwidth_pdf = bandwidth_pageloadtime/sum(bandwidth_pageloadtime)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_pageloadtime[1:], bandwidth_cdf, marker = 'v', label="bandwidth pageloadtime CDF")

packetdelay_pageloadtime, packetdelay_bins_pageloadtime = np.histogram(np.array(metrics_dict["packetdelay_pageloadtime"]), bins=10)
packetdelay_pdf = packetdelay_pageloadtime/sum(packetdelay_pageloadtime)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_pageloadtime[1:], packetdelay_cdf, marker = 's', label="packetdelay pageloadtime CDF")

packetloss_pageloadtime, packetloss_bins_pageloadtime = np.histogram(np.array(metrics_dict["packetloss_pageloadtime"]), bins=10)
packetloss_pdf = packetloss_pageloadtime/sum(packetloss_pageloadtime)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_pageloadtime[1:], packetloss_cdf, marker = 'P', label="packetloss pageloadtime CDF")

wifi_availability_pageloadtime, wifi_availability_bins_pageloadtime = np.histogram(np.array(metrics_dict["wifi_availability_pageloadtime"]), bins=10)
wifi_availability_pdf = wifi_availability_pageloadtime/sum(wifi_availability_pageloadtime)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_pageloadtime[1:], wifi_availability_cdf, marker = '*', label="wifi_availability pageloadtime CDF")

interference_pageloadtime, interference_bins_pageloadtime = np.histogram(np.array(metrics_dict["interference_pageloadtime"]), bins=10)
interference_pdf = interference_pageloadtime/sum(interference_pageloadtime)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_pageloadtime[1:], interference_cdf, marker = '_', label="interference pageloadtime CDF")

cpu_pageloadtime, cpu_bins_pageloadtime = np.histogram(np.array(metrics_dict["cpu_pageloadtime"]), bins=10)
cpu_pdf = cpu_pageloadtime/sum(cpu_pageloadtime)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_pageloadtime[1:], cpu_cdf, marker = '+', label="cpu pageloadtime CDF")

user_pageloadtime, user_bins_pageloadtime = np.histogram(np.array(metrics_dict["user_pageloadtime"]), bins=10)
user_pdf = user_pageloadtime/sum(user_pageloadtime)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_pageloadtime[1:], user_cdf, marker = 'X', label="user pageloadtime CDF")

plt.xlabel("webInfo pageloadtime")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()


# rtt print
normal_rtt, normal_bins_rtt = np.histogram(np.array(metrics_dict["normal_rtt"]), bins=10)
normal_pdf = normal_rtt/sum(normal_rtt)
normal_cdf = np.cumsum(normal_pdf)
plt.plot(normal_bins_rtt[1:], normal_cdf, marker = 'o', label="normal rtt CDF")

bandwidth_rtt, bandwidth_bins_rtt = np.histogram(np.array(metrics_dict["bandwidth_rtt"]), bins=10)
bandwidth_pdf = bandwidth_rtt/sum(bandwidth_rtt)
bandwidth_cdf = np.cumsum(bandwidth_pdf)
plt.plot(bandwidth_bins_rtt[1:], bandwidth_cdf, marker = 'v', label="bandwidth rtt CDF")

packetdelay_rtt, packetdelay_bins_rtt = np.histogram(np.array(metrics_dict["packetdelay_rtt"]), bins=10)
packetdelay_pdf = packetdelay_rtt/sum(packetdelay_rtt)
packetdelay_cdf = np.cumsum(packetdelay_pdf)
plt.plot(packetdelay_bins_rtt[1:], packetdelay_cdf, marker = 's', label="packetdelay rtt CDF")

packetloss_rtt, packetloss_bins_rtt = np.histogram(np.array(metrics_dict["packetloss_rtt"]), bins=10)
packetloss_pdf = packetloss_rtt/sum(packetloss_rtt)
packetloss_cdf = np.cumsum(packetloss_pdf)
plt.plot(packetloss_bins_rtt[1:], packetloss_cdf, marker = 'P', label="packetloss rtt CDF")

wifi_availability_rtt, wifi_availability_bins_rtt = np.histogram(np.array(metrics_dict["wifi_availability_rtt"]), bins=10)
wifi_availability_pdf = wifi_availability_rtt/sum(wifi_availability_rtt)
wifi_availability_cdf = np.cumsum(wifi_availability_pdf)
plt.plot(wifi_availability_bins_rtt[1:], wifi_availability_cdf, marker = '*', label="wifi_availability rtt CDF")

interference_rtt, interference_bins_rtt = np.histogram(np.array(metrics_dict["interference_rtt"]), bins=10)
interference_pdf = interference_rtt/sum(interference_rtt)
interference_cdf = np.cumsum(interference_pdf)
plt.plot(interference_bins_rtt[1:], interference_cdf, marker = '_', label="interference rtt CDF")

cpu_rtt, cpu_bins_rtt = np.histogram(np.array(metrics_dict["cpu_rtt"]), bins=10)
cpu_pdf = cpu_rtt/sum(cpu_rtt)
cpu_cdf = np.cumsum(cpu_pdf)
plt.plot(cpu_bins_rtt[1:], cpu_cdf, marker = '+', label="cpu rtt CDF")

user_rtt, user_bins_rtt = np.histogram(np.array(metrics_dict["user_rtt"]), bins=10)
user_pdf = user_rtt/sum(user_rtt)
user_cdf = np.cumsum(user_pdf)
plt.plot(user_bins_rtt[1:], user_cdf, marker = 'X', label="user rtt CDF")

plt.xlabel("webInfo rtt")
plt.ylabel("Probability", color="red")
plt.legend()
plt.show()


# protocol_count_dict = dict()
# protocol_count_dict["http/1.1"] = 0
# protocol_count_dict["h2"] = 0
# protocol_count_dict["h3"] = 0
# for metric in metrics_after_cpu_data[end_normal_index:]:
#     # print("failing metric", metric)
#     if metric["webInfo"].get("protocol") =="http/1.1":
#         protocol_count_dict["http/1.1"] +=1

#     elif metric["webInfo"].get("protocol") =="h2":
#         print(metric["webInfo"].get("RUMSpeedIndex"))
#         protocol_count_dict["h2"] +=1

#     elif metric["webInfo"].get("protocol") =="h3":
#             protocol_count_dict["h3"] +=1

#     else:
#         continue

# print("protocol_count in anomalies data", protocol_count_dict)
# # protocol_count in anomalies data {'http/1.1': 2376, 'h2': 31, 'h3': 0}

# Write anomaly_metrics to a file

print(type(metrics_after_cpu_data))
anomalies_metrics_file = open("Info_load.json", "w")
# rumsi_2_5_file=open("RUMSI-2_5_load.json", "w")
rumsi_1_file = open("RUMSI-1_load.json", "w")
rumsi_2_file = open("RUMSI-2_load.json", "w")
rumsi_3_file = open("RUMSI-3_load.json", "w")
rumsi_4_file = open("RUMSI-4_load.json", "w")
rumsi_5_file = open("RUMSI-5_load.json", "w")
# rumsi_10_file = open("RUMSI-10_load.json", "w")
# rumsi_20_file = open("RUMSI-20_load.json", "w")
# rumsi_30_file = open("RUMSI-30_load.json", "w")
# rumsi_40_file = open("RUMSI-40_load.json", "w")
json.dump(metrics_after_cpu_data[end_normal_index:], anomalies_metrics_file)
# json.dump(rumsi_greater_2_5_metrics, rumsi_2_5_file)
json.dump(rumsi_greater_1_metrics, rumsi_1_file)
json.dump(rumsi_greater_2_metrics, rumsi_2_file)
json.dump(rumsi_greater_3_metrics, rumsi_3_file)
json.dump(rumsi_greater_4_metrics, rumsi_4_file)
json.dump(rumsi_greater_5_metrics, rumsi_5_file)
# json.dump(rumsi_greater_10_metrics, rumsi_10_file)
# json.dump(rumsi_greater_20_metrics, rumsi_20_file)
# json.dump(rumsi_greater_30_metrics, rumsi_30_file)
# json.dump(rumsi_greater_40_metrics, rumsi_40_file)




# # PRINTING CDFs
# normal_count, normal_bins_count = np.histogram(np.array(load_points["Normal"]), bins=10)
# normal_pdf = normal_count/sum(normal_count)
# normal_cdf = np.cumsum(normal_pdf)

# bandwidth_count, bandwidth_bins_count = np.histogram(np.array(load_points["Network Bandwidth"]), bins=10)
# bandwidth_pdf = bandwidth_count/sum(bandwidth_count)
# bandwidth_cdf = np.cumsum(bandwidth_pdf)

# delay_count, delay_bins_count = np.histogram(np.array(load_points["Network Delay"]), bins=10)
# delay_pdf = delay_count/sum(delay_count)
# delay_cdf = np.cumsum(delay_pdf)

# loss_count, loss_bins_count = np.histogram(np.array(load_points["Network Loss"]), bins=10)
# loss_pdf = loss_count/sum(loss_count)
# loss_cdf = np.cumsum(loss_pdf)

# server_count, server_bins_count = np.histogram(np.array(load_points["Server Overload"]), bins=10)
# server_pdf = server_count/sum(server_count)
# server_cdf = np.cumsum(server_pdf)

# machine_count, machine_bins_count = np.histogram(np.array(load_points["User's Machine Overload"]), bins=10)
# machine_pdf = machine_count/sum(machine_count)
# machine_cdf = np.cumsum(machine_pdf)

# wifi_avail_count, wifi_avail_bins_count = np.histogram(np.array(load_points["Wi-Fi Availability"]), bins=10)
# wifi_avail_pdf = wifi_avail_count/sum(wifi_avail_count)
# wifi_avail_cdf = np.cumsum(wifi_avail_pdf)

# interference_count, interference_bins_count = np.histogram(np.array(load_points["Wi-Fi Interference"]), bins=10)
# interference_pdf = interference_count/sum(interference_count)
# interference_cdf = np.cumsum(interference_pdf)

# # USE THE LINE BELOW TO plot CDF AND PDF GRAPHS
# # plt.plot(normal_bins_count[1:], normal_pdf, color="red", label="normal PDF")

# # UNCOMMENT THE LINES BELOW TO PLOT THE CDFFS
# # plt.plot(normal_bins_count[1:], normal_cdf, marker = 'o', label="normal CDF")
# # plt.plot(bandwidth_bins_count[1:], bandwidth_cdf, marker = 'v', label="network bandwidth CDF")
# # plt.plot(delay_bins_count[1:], delay_cdf, marker = 's', label="network delay CDF")
# # plt.plot(loss_bins_count[1:], loss_cdf, marker = 'P', label="network loss CDF")
# # plt.plot(server_bins_count[1:], server_cdf, marker = '*', label="server overload CDF")
# # plt.plot(machine_bins_count[1:], machine_cdf, marker = '_', label="user machine overload CDF")
# # plt.plot(wifi_avail_bins_count[1:], wifi_avail_cdf, marker = '+', label="wifi medium availability CDF")
# # plt.plot(interference_bins_count[1:], interference_cdf, marker = 'X', label="wifi interference CDF")
# # # plt.xlim([0.173, 0.33])
# # plt.xlabel("load value")
# # plt.ylabel("Probability", color="red")
# # plt.legend()
# # plt.show()

# # OBSOLETE
# # USE THE LINES BELOW TO PLOT CDF on HISTOGRAM old and obsolete
# # plt.hist(np.array(load_points["Normal"]),bins=normal_bins_count,density=True)
# # plt.hist(np.array(load_points["Normal"]),bins=normal_bins_count, density=True, cumulative=True, label='CDF', color="red")

# # plt.xlabel("load value")
# # # plt.ylabel("Probability", color="red")
# # plt.legend()
# # plt.xlim([0.173, 0.33])
# # plt.show()
