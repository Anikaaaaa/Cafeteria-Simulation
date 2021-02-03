import heapq
import random
from builtins import print
import matplotlib.pyplot as plt
import numpy as np

MAX_TIME = 5400
MAX_SERVED = 0
MIN_DELAY = 100
SEQ1 = 0
SEQ2 = 0



class Params:
    def __init__(self):
        self.group_size = []
        self.group_size_probablity = []
        self.interarrival_time_between_groups = 0
        self.routing_probablity = []
        self.hotfood_ST = []
        self.hotfood_ACT = []
        self.sandwich_ST = []
        self.sandwich_ACT = []
        self.drinks_ST = []
        self.drinks_ACT = []
        self.cashiers = 0
        self.hotfood_server = 0
        self.sandwich_server = 0
        self.route_array = []


def taking_input(params):
    f = open('input2')
    lines = f.readlines()
    total_lines = len(lines)
    i = 0
    for word in lines[0].split():
        params.group_size.append(int(word))
        # print(params.group_size[i])
        i += 1

    i = 0
    for word in lines[1].split():
        params.group_size_probablity.append(float(word))
        # print(params.group_size_probablity[i])
        i += 1

    params.interarrival_time_between_groups = int(lines[2])
    # print(params.interarrival_time_between_groups)

    i = 0
    for word in lines[3].split():
        params.routing_probablity.append(float(word))
        params.route_array.append((i + 1))
        # print(params.routing_probablity[i])
        i += 1

    i = 0
    for word in lines[4].split():
        params.hotfood_ST.append(int(word))
        # print(params.hotfood_ST[i])
        i += 1

    i = 0
    for word in lines[5].split():
        params.hotfood_ACT.append(int(word))
        # print(params.hotfood_ACT[i])
        i += 1

    i = 0
    for word in lines[6].split():
        params.sandwich_ST.append(int(word))
        # print(params.sandwich_ST[i])
        i += 1
    i = 0
    for word in lines[7].split():
        params.sandwich_ACT.append(int(word))
        # print(params.sandwich_ACT[i])
        i += 1
    i = 0
    for word in lines[8].split():
        params.drinks_ST.append(int(word))
        # print(params.drinks_ST[i])
        i += 1
    i = 0
    for word in lines[9].split():
        params.drinks_ACT.append(int(word))
        # print(params.drinks_ACT[i])
        i += 1


class States:
    def __init__(self):
        # States
        self.hotfood_queue = []
        self.sandwich_queue = []
        self.cashier_queue = []
        self.cashier_queue_ACT = []
        self.server_state_hotfood = 0
        self.server_state_sandwich = 0
        self.total_served_cashier = []
        self.total_served_hotfood = 0
        self.total_served_sandwich = 0
        self.total_served_drinks = 0
        self.total_served = 0
        self.server_state_cashier = []
        self.delay_hotfood = 0.0
        self.delay_sandwich = 0.0
        self.delay_cashier = []
        self.total_arrival_this_group_type = []
        self.total_delay_this_group_type = []
        self.group_length_for_hotfood_queue = []
        self.group_length_for_sandwich_queue = []
        self.group_length_for_cashier_queue = []
        self.number_of_total_customer_in_system = 0
        self.max_number_customer_any_moment = 0
        self.average_customer_in_system = 0.0
        self.max_length_queue_hotfood = 0
        self.max_length_queue_sandwich = 0
        self.max_length_queue_cashier = []
        self.avg_queue_len_hotfood = 0.0
        self.avg_queue_len_sandwich = 0.0
        self.avg_queue_len_cashier = 0.0
        self.total_queue_len_cashier = 0
        self.avg_queue_delay_hotfood = 0.0
        self.avg_queue_delay_sandwich = 0.0
        self.avg_queue_delay_cashier = []
        self.avg_queue_delay_grouptype = []
        self.overall_avg_delay = 0.0
        self.area_num_in_hotfood_q = 0.0
        self.area_num_in_sandwich_q = 0.0
        self.avg_queue_length_hotfood = 0.0
        self.avg_queue_length_sandwich = 0.0
        self.avg_queue_length_cashier = 0.0
        self.area_num_in_cashier_q = 0.0
        self.total_served_this_group_type = []
        self.delay_route_type = []
        self.Avg_delay_route_type = []
        self.served_route_type = []
        self.area_num_route_type = []
        self.current_num = 0
        self.overall_route_type_delay = 0.0
        self.avg_num_route = 0.0
        self.area_num_route_typ = 0.0
        self.total_arrived = 0
        self.group_no = []
        self.ttl_srvd = 0
        self.overall_cashier_delay = 0.0

        self.queue = []
        # Declare other states variables that might be needed
        self.server_status = 0
        self.delay = 0.0
        self.length = 0
        self.time_since_last_event = 0.0
        self.time_of_last_event = 0.0
        self.total_time_served = 0.0
        self.service_time = 0.0
        self.no_of_cust_delayed = 0
        self.num_in_queue = 0
        self.area_num_in_queue = 0.0
        self.num_waited = 0
        self.servers_status = []
        # self.service_time = 0
        self.wait_time = 0
        # self.busy=1
        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0
        self.QueueLimit = 1000
        self.num_in_q = 0
        self.no_of_q_avilable = 0

    def update(self, sim, event):
        # Complete this function
        if self.number_of_total_customer_in_system > self.max_number_customer_any_moment:
            self.max_number_customer_any_moment = self.number_of_total_customer_in_system
        if len(self.hotfood_queue) > self.max_length_queue_hotfood:
            self.max_length_queue_hotfood = len(self.hotfood_queue)
        if len(self.sandwich_queue) > self.max_length_queue_sandwich:
            self.max_length_queue_sandwich = len(self.sandwich_queue)
        i = 0
        while i < sim.params.cashiers:
            if len(self.cashier_queue[i]) > self.max_length_queue_cashier[i]:
                self.max_length_queue_cashier[i] = len(self.cashier_queue[i])
            i += 1

        self.time_since_last_event = event.eventTime - self.time_of_last_event
        self.time_of_last_event = event.eventTime

        self.avg_queue_len_hotfood += len(self.hotfood_queue) * self.time_since_last_event
        self.avg_queue_len_sandwich += len(self.sandwich_queue) * self.time_since_last_event
        i = 0
        while i < sim.params.cashiers:
            self.total_queue_len_cashier += len(self.cashier_queue[i])
            i += 1
        self.avg_queue_len_cashier += (self.total_queue_len_cashier / sim.params.cashiers) * self.time_since_last_event

        self.average_customer_in_system += self.time_since_last_event * self.number_of_total_customer_in_system
        # print("len hotfood q %d" %(len(self.hotfood_queue)))
        # print("len sandwich q %d" %(len(self.sandwich_queue)))
        ########################## updating ####################
        self.area_num_in_hotfood_q += len(self.hotfood_queue) * self.time_since_last_event
        self.area_num_in_sandwich_q += len(self.sandwich_queue) * self.time_since_last_event
        self.area_num_in_cashier_q += (self.total_queue_len_cashier * self.time_since_last_event) / sim.params.cashiers
        ###########self.total_time_served += ( self.server_status * self.time_since_last_event )
        # self.total_time_served =
        ############self.area_num_in_queue += ( self.num_in_q * self.time_since_last_event)

        # i = 0
        # while i < len(sim.params.route_array):
        #   self.area_num_route_type[i] += self.current_num * self.time_since_last_event
        #  i+=1
        self.area_num_route_typ += self.current_num * self.time_since_last_event

    def finish(self, sim):
        self.avg_queue_delay_hotfood = self.delay_hotfood / self.total_served_hotfood
        self.avg_queue_delay_sandwich = self.delay_sandwich / self.total_served_sandwich
        i = 0
        while i < sim.params.cashiers:
            self.avg_queue_delay_cashier[i] = self.delay_cashier[i] / self.total_served_cashier[i]
            i += 1

        i = 0
        while i < sim.params.cashiers:
            self.overall_cashier_delay += self.avg_queue_delay_cashier[i]
            i += 1

        self.overall_cashier_delay = self.overall_cashier_delay / sim.params.cashiers

        i = 0
        while i < len(sim.params.group_size):
            # self.avg_queue_delay_grouptype[i] = self.total_delay_this_group_type[i]/self.total_arrival_this_group_type[i]
            self.avg_queue_delay_grouptype[i] = self.total_delay_this_group_type[i] / self.total_served_this_group_type[
                i]
            i += 1

        i = 0
        while i < len(sim.params.group_size):
            self.overall_avg_delay += sim.params.group_size_probablity[i] * self.avg_queue_delay_grouptype[i]
            i += 1

        ############################### updating ##########################
        self.avg_queue_length_hotfood = self.area_num_in_hotfood_q / sim.simclock
        self.avg_queue_length_sandwich = self.area_num_in_sandwich_q / sim.simclock
        self.avg_queue_length_cashier = self.area_num_in_cashier_q / sim.simclock

        i = 0
        while i < len(sim.params.route_array):
            if self.served_route_type[i] > 0:
                self.Avg_delay_route_type[i] = self.delay_route_type[i] / self.served_route_type[i]
                # print("Avg delay for route type %d is %lf" %((i+1),self.Avg_delay_route_type[i]/60))
            i += 1
        i = 0
        while i < len(sim.params.route_array):
            self.overall_route_type_delay += self.Avg_delay_route_type[i] * sim.params.routing_probablity[i]
            i += 1
        # print("overall route type delay %lf" %(self.overall_route_type_delay/60))
        self.avg_num_route = self.area_num_route_typ / sim.simclock
        # print("Avg num route type %lf" %(self.avg_num_route))

        #####################Average customer = sum of area of customer / total simulation time
        #####################Average q length = sum of area of q / total simulation time

        ###self.avgQdelay = self.delay / self.served
        ###self.avgQlength = self.area_num_in_queue / sim.simclock
        ###self.util = self.total_time_served / sim.simclock

    def printResults(self, sim):
        print("Average queue delay hotfood =  %lf" % (self.avg_queue_delay_hotfood / 60))
        print("Average queue delay sandwich =  %lf" % (self.avg_queue_delay_sandwich / 60))
        i = 0
        #while i < sim.params.cashiers:
           # print("Average queue delay cashier %d  =  %lf" % (i + 1, (self.avg_queue_delay_cashier[i] / 60)))
            #i += 1
        print("Overall Avg cashier delay %lf" %(self.overall_cashier_delay/60))

        i = 0

        while i < len(sim.params.group_size):
            print("Average queue delay grouptype %d  =  %lf" % (i + 1, (self.avg_queue_delay_grouptype[i]) / 60))
            i += 1
        print('overall queue delay groups %lf' % (self.overall_avg_delay / 60))
        ################## updating ###############
        print("Avg queue length for hotfood %lf" % (self.avg_queue_length_hotfood))
        print("Avg queue length for sandwich %lf" % (self.avg_queue_length_sandwich))
        print("Avg queue length for cashier %lf" % (self.avg_queue_length_cashier))

        i = 0
        while i < len(sim.params.route_array):
            print("Avg delay for route type %d is %lf" % ((i + 1), self.Avg_delay_route_type[i] / 60))
            i += 1
        i = 0

        print("overall route type delay %lf" % (self.overall_route_type_delay / 60))
        # self.avg_num_route = self.area_num_route_typ / sim.simclock
        print("Avg num route type %lf" % (self.avg_num_route))

    def printResults1(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)

    def AnalyticalResults(self, sim):
        print(
            'MMk AnalyticalResults  : lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        # print('MMk Total customer served: %d' % (self.served))
        aql = 0
        adq = 0
        if sim.params.mu != sim.params.lambd:
            aql = float((sim.params.lambd ** 2) / (sim.params.mu * (sim.params.mu - sim.params.lambd)))
            adq = float(sim.params.lambd / (sim.params.mu * (sim.params.mu - sim.params.lambd)))
        uf = float(sim.params.lambd / sim.params.mu)
        print('MMk Average queue length: %lf' % (aql))
        print('MMk Average customer delay in queue: %lf' % (adq))
        print('MMk Time-average server utility: %lf' % (uf))

    # Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        self.group_no = None
        self.route_type = None
        self.current_counter = None
        self.Queue_no = None
        self.ACT = None
        self.isMarked = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __lt__(self, other):
        return True

    def __repr__(self):
        return self.eventType


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        Time = sim.simclock + random.expovariate(1 / sim.params.interarrival_time_between_groups)
        # print(Time)
        group_type = int(np.random.choice(sim.params.group_size, 1, sim.params.group_size_probablity))
        sim.states.total_arrival_this_group_type[group_type - 1] += 1
        queue_no = 0
        current_counter = 0
        ACT = 0.0

        i = 0
        while i < group_type:
            if (i + 1) == group_type:
                isMarked = 1
            else:
                isMarked = 0
            # print("in start")
            # print("group no %d" %(group_type))
            # print("Is marked %d" %(isMarked))
            #route_type = int(np.random.choice(sim.params.route_array, 1, sim.params.routing_probablity))  # 1 hotfood,2 sand,3 drinks
            route_type = int(
                np.random.choice(sim.params.route_array, 1, p=[.8,.15,.05]))  # 1 hotfood,2 sand,3 drinks

            sim.scheduleEvent(ArrivalEvent(Time, sim, group_type, queue_no, current_counter, route_type, ACT, isMarked))
            i += 1
        # print('Scheduling Arrival event at start event at %f' %self.eventTime)
        # sim.scheduleEvent(ArrivalEvent ( Time,sim ))
        sim.scheduleEvent(ExitEvent(MAX_TIME, sim))


class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        # Complete this function
        None


class ArrivalEvent(Event):
    def __init__(self, eventTime, sim, group_no, Queue_no, current_counter, route_type, ACT, isMarked):
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.group_no = group_no
        self.Queue_no = Queue_no
        self.current_counter = current_counter
        self.route_type = route_type
        self.ACT = ACT
        self.isMarked = isMarked

    def process(self, sim):
        sim.states.current_num += 1
        if self.isMarked == 1:
            sim.states.total_arrived += 1
            # print("calling new arrival")
            Time = sim.simclock + random.expovariate(1 / sim.params.interarrival_time_between_groups)
            # print(Time)
            group_type = int(np.random.choice(sim.params.group_size, 1, sim.params.group_size_probablity))
            sim.states.total_arrival_this_group_type[group_type - 1] += 1
            queue_no = 0
            current_counter = 0
            ACT = 0.0

            i = 0
            while i < group_type:
                if (i + 1) == group_type:
                    isMarked = 1
                else:
                    isMarked = 0
                # print("group type %d" %(group_type))
                # print("Is marked %d" %(isMarked))
                #route_type = int(np.random.choice(sim.params.route_array, 1,sim.params.routing_probablity))  # 1 hotfood,2 sand,3 drinks
                route_type = int(
                    np.random.choice(sim.params.route_array, 1, p=[.8, .15, .05]))  # 1 hotfood,2 sand,3 drinks

                # print("route type %d" %(route_type))

                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, group_type, queue_no, current_counter, route_type, ACT, isMarked))
                i += 1

        if self.current_counter == 0:
            self.isMarked = 0
            # sim.states.total_served += 1
            sim.states.number_of_total_customer_in_system += 1
            if self.route_type == 1:
                if sim.states.server_state_hotfood == 0:
                    ######################## served kothay rakhbo decision nite hbe
                    sim.states.total_served_hotfood += 1
                    sim.states.server_state_hotfood = 1
                    lo = sim.params.hotfood_ST[0]
                    hi = sim.params.hotfood_ST[1]
                    lo_ACT = sim.params.hotfood_ACT[0]
                    hi_ACT = sim.params.hotfood_ACT[1]
                    self.ACT += np.random.uniform(lo_ACT, hi_ACT)
                    departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
                    counter_current = 1
                    sim.states.delay_hotfood += 0.0
                    sim.scheduleEvent(DepartureEvent(departure_time, sim, self.group_no, self.Queue_no, counter_current,
                                                     self.route_type, self.ACT, self.isMarked))
                else:
                    sim.states.hotfood_queue.append(sim.simclock)
                    sim.states.group_length_for_hotfood_queue.append(self.group_no)

            elif self.route_type == 2:
                self.isMarked = 0
                if sim.states.server_state_sandwich == 0:
                    sim.states.total_served_sandwich += 1
                    sim.states.server_state_sandwich = 1
                    lo = sim.params.sandwich_ST[0]
                    hi = sim.params.sandwich_ST[1]
                    lo_ACT = sim.params.sandwich_ACT[0]
                    hi_ACT = sim.params.sandwich_ACT[1]
                    self.ACT += np.random.uniform(lo_ACT, hi_ACT)
                    departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
                    counter_current = 1
                    sim.states.delay_sandwich += 0.0
                    sim.scheduleEvent(DepartureEvent(departure_time, sim, self.group_no, self.Queue_no, counter_current,
                                                     self.route_type, self.ACT, self.isMarked))
                else:
                    sim.states.sandwich_queue.append(sim.simclock)
                    sim.states.group_length_for_sandwich_queue.append(self.group_no)
            elif self.route_type == 3:
                self.isMarked = 0
                sim.states.total_served_drinks += 1
                lo = sim.params.drinks_ST[0]
                hi = sim.params.drinks_ST[1]
                lo_ACT = sim.params.drinks_ACT[0]
                hi_ACT = sim.params.drinks_ACT[1]
                self.ACT += np.random.uniform(lo_ACT, hi_ACT)
                isMarked = 0
                departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
                counter_current = 2
                sim.scheduleEvent(
                    DepartureEvent(departure_time, sim, self.group_no, self.Queue_no, counter_current, self.route_type,
                                   self.ACT, isMarked))

        elif self.current_counter == 1:
            self.isMarked = 0
            sim.states.total_served_drinks += 1
            lo = sim.params.drinks_ST[0]
            hi = sim.params.drinks_ST[1]
            lo_ACT = sim.params.drinks_ACT[0]
            hi_ACT = sim.params.drinks_ACT[1]
            self.ACT += np.random.uniform(lo_ACT, hi_ACT)
            departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
            counter_current = 2
            sim.scheduleEvent(
                DepartureEvent(departure_time, sim, self.group_no, self.Queue_no, counter_current, self.route_type,
                               self.ACT, self.isMarked))

        elif self.current_counter == 2:
            self.isMarked = 0
            index = 100
            i = 0
            while i < sim.params.cashiers:
                if sim.states.server_state_cashier[i] == 0:
                    index = i
                i += 1
            if index != 100:
                sim.states.server_state_cashier[index] = 1
                sim.states.total_served_cashier[index] += 1
                departure_time = sim.simclock + self.ACT
                counter_current = 3
                self.Queue_no = index + 1
                sim.scheduleEvent(
                    DepartureEvent(departure_time, sim, self.group_no, self.Queue_no, counter_current, self.route_type,
                                   self.ACT, self.isMarked))
            else:
                shortest_len = len(sim.states.cashier_queue[0])
                index = 0
                i = 0
                while i < sim.params.cashiers:
                    if len(sim.states.cashier_queue[i]) < shortest_len:
                        shortest_len = len(sim.states.cashier_queue[i])
                        index = i
                    i += 1
                sim.states.cashier_queue[index].append(sim.simclock)
                sim.states.cashier_queue_ACT[index].append(self.ACT)
                sim.states.group_length_for_cashier_queue[index].append(self.group_no)
                ############### cashier er queue te kon group er koto delay setao lagbe taina?


class DepartureEvent(Event):
    def __init__(self, eventTime, sim, group_no, Queue_no, current_counter, route_type, ACT, isMarked):
        self.eventTime = eventTime
        self.eventType = 'DEPARTURE'
        self.sim = sim
        self.group_no = group_no
        self.Queue_no = Queue_no
        self.current_counter = current_counter
        self.route_type = route_type
        self.ACT = ACT
        self.isMarked = 0

    def process(self, sim):
        sim.states.current_num -= 1
        sim.states.total_served_this_group_type[self.group_no - 1] += 1
        sim.states.served_route_type[self.route_type - 1] += 1

        self.isMarked = 0
        if self.route_type == 1:
            if self.current_counter == 1:
                # self.current_counter  = 2
                Time = sim.simclock
                ### As drinks have no queue
                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, self.group_no, self.Queue_no, self.current_counter, self.route_type,
                                 self.ACT, self.isMarked))
                if len(sim.states.hotfood_queue) > 0:
                    time = sim.states.hotfood_queue.pop(0)
                    group_length = sim.states.group_length_for_hotfood_queue.pop(0)
                    delay = sim.simclock - time
                    lo = sim.params.hotfood_ST[0]
                    hi = sim.params.hotfood_ST[1]
                    lo_ACT = sim.params.hotfood_ACT[0]
                    hi_ACT = sim.params.hotfood_ACT[1]
                    ACT = np.random.uniform(lo_ACT, hi_ACT)
                    departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
                    sim.states.total_served_hotfood += 1
                    sim.states.delay_hotfood += delay
                    sim.states.total_delay_this_group_type[group_length - 1] += delay
                    sim.states.delay_route_type[self.route_type - 1] += delay
                    isMarked = 0  ##################### korbo kina
                    # group_no = 0 #################
                    route_type = 1
                    current_counter = 1
                    # ACT = 0.0
                    sim.scheduleEvent(
                        DepartureEvent(departure_time, sim, group_length, self.Queue_no, current_counter, route_type,
                                       ACT, isMarked))
                else:
                    sim.states.server_state_hotfood = 0
            elif self.current_counter == 2:
                # self.current_counter = 3
                Time = sim.simclock
                ### As drinks have no queue
                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, self.group_no, self.Queue_no, self.current_counter, self.route_type,
                                 self.ACT, self.isMarked))
            elif self.current_counter == 3:
                # print('this is final departure')
                sim.states.number_of_total_customer_in_system -= 1

                cashier_index = self.Queue_no - 1
                if len(sim.states.cashier_queue[cashier_index]) > 0:
                    sim.states.total_served_cashier[cashier_index] += 1
                    time = sim.states.cashier_queue[cashier_index].pop(0)
                    total_ACT = sim.states.cashier_queue_ACT[cashier_index].pop(0)
                    delay = sim.simclock - time
                    sim.states.delay_cashier[cashier_index] += delay
                    current_counter = 3
                    group_no = sim.states.group_length_for_cashier_queue[cashier_index].pop(0)
                    sim.states.total_delay_this_group_type[group_no - 1] += delay
                    sim.states.delay_route_type[self.route_type - 1] += delay
                    isMarked = 0
                    Queue_no = self.Queue_no
                    departure_time = sim.simclock + total_ACT
                    sim.scheduleEvent(
                        DepartureEvent(departure_time, sim, group_no, Queue_no, current_counter, self.route_type,
                                       total_ACT, isMarked))
                else:
                    sim.states.server_state_cashier[cashier_index] = 0

        elif self.route_type == 2:
            if self.current_counter == 1:
                # self.current_counter  = 2
                Time = sim.simclock
                ### As drinks have no queue
                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, self.group_no, self.Queue_no, self.current_counter, self.route_type,
                                 self.ACT, self.isMarked))
                if len(sim.states.sandwich_queue) > 0:
                    time = sim.states.sandwich_queue.pop(0)
                    delay = sim.simclock - time
                    group_length = sim.states.group_length_for_sandwich_queue.pop(0)
                    lo = sim.params.sandwich_ST[0]
                    hi = sim.params.sandwich_ST[1]
                    lo_ACT = sim.params.sandwich_ACT[0]
                    hi_ACT = sim.params.sandwich_ACT[1]
                    ACT = np.random.uniform(lo_ACT, hi_ACT)
                    departure_time = sim.simclock + np.random.uniform(lo, hi)  ########################### thik ache?
                    sim.states.total_served_sandwich += 1
                    sim.states.delay_sandwich += delay
                    sim.states.delay_route_type[self.route_type - 1] += delay
                    sim.states.total_delay_this_group_type[group_length - 1] += delay
                    isMarked = 0  ##################### korbo kina
                    # group_no = 0 #################
                    route_type = 2
                    current_counter = 1
                    # ACT = 0.0
                    sim.scheduleEvent(
                        DepartureEvent(departure_time, sim, group_length, self.Queue_no, current_counter, route_type,
                                       ACT, isMarked))
                else:
                    sim.states.server_state_sandwich = 0
            elif self.current_counter == 2:
                # self.current_counter = 3
                Time = sim.simclock
                ### As drinks have no queue
                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, self.group_no, self.Queue_no, self.current_counter, self.route_type,
                                 self.ACT, self.isMarked))
            elif self.current_counter == 3:
                # print('this is final departure')
                sim.states.ttl_srvd += 1
                cashier_index = self.Queue_no - 1
                if len(sim.states.cashier_queue[cashier_index]) > 0:
                    time = sim.states.cashier_queue[cashier_index].pop(0)
                    total_ACT = sim.states.cashier_queue_ACT[cashier_index].pop(0)
                    delay = sim.simclock - time
                    sim.states.delay_route_type[self.route_type - 1] += delay
                    sim.states.delay_cashier[cashier_index] += delay
                    current_counter = 3
                    group_no = sim.states.group_length_for_cashier_queue[cashier_index].pop(0)
                    sim.states.total_delay_this_group_type[group_no - 1] += delay
                    isMarked = 0
                    Queue_no = self.Queue_no
                    departure_time = sim.simclock + total_ACT
                    sim.scheduleEvent(
                        DepartureEvent(departure_time, sim, group_no, Queue_no, current_counter, self.route_type,
                                       total_ACT, isMarked))
                else:
                    sim.states.server_state_cashier[cashier_index] = 0

        elif self.route_type == 3:
            if self.current_counter == 2:
                # self.current_counter = 3
                Time = sim.simclock
                ### As drinks have no queue
                sim.scheduleEvent(
                    ArrivalEvent(Time, sim, self.group_no, self.Queue_no, self.current_counter, self.route_type,
                                 self.ACT, self.isMarked))
            elif self.current_counter == 3:
                # print('this is final departure')
                cashier_index = self.Queue_no - 1
                if len(sim.states.cashier_queue[cashier_index]) > 0:
                    time = sim.states.cashier_queue[cashier_index].pop(0)
                    total_ACT = sim.states.cashier_queue_ACT[cashier_index].pop(0)
                    delay = sim.simclock - time
                    sim.states.delay_cashier[cashier_index] += delay
                    sim.states.delay_route_type[self.route_type - 1] += delay
                    current_counter = 3
                    group_no = sim.states.group_length_for_cashier_queue[cashier_index].pop(0)
                    sim.states.total_delay_this_group_type[group_no - 1] += delay
                    isMarked = 0
                    Queue_no = self.Queue_no
                    departure_time = sim.simclock + total_ACT
                    sim.scheduleEvent(
                        DepartureEvent(departure_time, sim, group_no, Queue_no, current_counter, self.route_type,
                                       total_ACT, isMarked))
                else:
                    sim.states.server_state_cashier[cashier_index] = 0


class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        self.simclock = 0
        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        self.params = params
        self.states = states

    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    # np.random.seed(101)
    def run(self):
        random.seed(self.seed)
        self.initialize()
        i = 0
        while i < self.params.cashiers:
            self.states.cashier_queue.append([])
            self.states.cashier_queue_ACT.append([])
            self.states.server_state_cashier.append(0)
            self.states.total_served_cashier.append(0)
            self.states.group_length_for_cashier_queue.append([])
            self.states.max_length_queue_cashier.append(0)
            self.states.delay_cashier.append(0.0)
            self.states.avg_queue_delay_cashier.append(0.0)
            i += 1

        i = 0
        while i < len(self.params.group_size):
            self.states.total_arrival_this_group_type.append(0)
            self.states.total_delay_this_group_type.append(0.0)
            self.states.avg_queue_delay_grouptype.append(0.0)
            self.states.total_served_this_group_type.append(0)
            i += 1
        i = 0
        while i < len(self.params.route_array):
            self.states.delay_route_type.append(0.0)
            self.states.served_route_type.append(0)
            self.states.Avg_delay_route_type.append(0.0)
            i += 1

        while len(self.eventQ) > 0:

            time, event = heapq.heappop(self.eventQ)
            if event.eventType == 'EXIT':
                break

            if self.states != None:
                self.states.update(self, event)

            # print(event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)
        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)
        # self.states.AnalyticalResults(self)

    def getResults(self):
        return self.states.getResults(self)


def task1():
    params = Params()
    taking_input(params)
    params.cashiers = 2
    params.hotfood_server = 1
    params.sandwich_server = 1
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()
    print()
    print()
    print("Result 1st case 1,1,2")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED :
        MAX_SERVED =max_served
        SEQ1 = 112
    #min_delay = sim.states.
    sim.printResults()


def task2():
    params = Params()
    taking_input(params)
    params.cashiers = 3
    params.hotfood_server = 1
    params.sandwich_server = 1
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()
    print()
    print()
    print("Result 2nd case 1,1,3")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 113

    sim.printResults()


def task2_1():
    params = Params()
    taking_input(params)
    params.cashiers = 2
    params.hotfood_server = 2
    params.sandwich_server = 1
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 3rd case 2,1,2")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 212

    sim.printResults()


def task2_2():
    params = Params()
    taking_input(params)
    params.cashiers = 2
    params.hotfood_server = 1
    params.sandwich_server = 2
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 4th case 1,2,2")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 122

    sim.printResults()


def task3():
    params = Params()
    taking_input(params)
    params.cashiers = 2
    params.hotfood_server = 2
    params.sandwich_server = 2
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 5th case 2,2,2")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 222

    sim.printResults()


def task4():
    params = Params()
    taking_input(params)
    params.cashiers = 2
    params.hotfood_server = 1
    params.sandwich_server = 3
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 6th case 2,1,3")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 213

    sim.printResults()


def task5():
    params = Params()
    taking_input(params)
    params.cashiers = 1
    params.hotfood_server = 2
    params.sandwich_server = 3
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 7th case 1,2,3")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 123

    sim.printResults()


def task8():
    params = Params()
    taking_input(params)
    params.cashiers = 3
    params.hotfood_server = 2
    params.sandwich_server = 2
    ######################## ACT o divide korbo kina sure nah
    i = 0
    while i < 2:
        params.hotfood_ST[i] = params.hotfood_ST[i] / params.hotfood_server
        params.hotfood_ACT[i] = params.hotfood_ACT[i] / params.hotfood_server
        params.sandwich_ST[i] = params.sandwich_ST[i] / params.sandwich_server
        params.sandwich_ACT[i] = params.sandwich_ACT[i] / params.sandwich_server
        # print(params.hotfood_ST[i])
        i += 1
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())
    sim.run()

    print()
    print()
    print("Result 8th case 2,2,3")
    print("total %d" % (sim.states.ttl_srvd))
    global MAX_SERVED
    global SEQ1
    global MIN_DELAY
    max_served = sim.states.ttl_srvd
    if max_served > MAX_SERVED:
        MAX_SERVED = max_served
        SEQ1 = 223

    sim.printResults()


def main():
    max_served = 0
    min_delay = 100
    srvd = 0
    delay = 100
    task1()
    task2()
    task2_1()
    task2_2()
    task3()
    task4()
    task5()
    task8()
    print("Max served %d"%(MAX_SERVED))
    print("At Sequence %d"%(SEQ1))


main()

