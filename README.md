# Cafeteria-Simulation
The cafeteria at your university is trying to improve its service during the lunch rush
from 1PM to 2:30PM. Customers arrive together in groups of size 1, 2, 3, and 4, with respective
probabilities 0.5, 0.3, 0.1, and 0.1. Inter-arrival times between groups are exponentially distributed
with mean 30 seconds. Initially, the system is empty and idle, and is to run for the 90-minute period.
Each arriving customer, whether alone or part of a group, takes one of three routes through the
cafeteria (groups in general split up after they arrive):

• Hot-food service, then drinks, then cashier

• Specialty-sandwich bar, then drinks, then cashier

• Drinks (only), then cashier

The probabilities of these routes are respectively 0.80, 0.15, and 0.05; see Figure 2. At the hotfood counter and the specialty-sandwich bar, customers are served one at a time (although there
might actually be one or two workers present, as discussed below). The drinks stand is self-service,
and assume that nobody ever has to queue up here; this is equivalent to thinking of the drinks
stand as having infinitely many servers. There are either two or three cashiers (see below), each
having his own queue, and there is no jockeying; customers arriving to the cashiers simply choose
the shortest queue. All queues in the model are FIFO.
In Figure 2, ST stands for service time at a station, and ACT stands for the accumulated (future)
cashier time due to having visited a station; the notation U(a, b) means that the corresponding
quantity is distributed uniformly between a and b seconds. For example, a route 1 customer
goes first to the hot-food station, joins the queue there if necessary, receives service there that is
uniformly distributed between 50 and 120 seconds, “stores away” part of a (future) cashier time
that is uniformly distributed between 20 and 40 seconds, then spends an amount of time uniformly
distributed between 5 seconds and 20 seconds getting a drink, and accumulates an additional
amount of (future) cashier time distributed uniformly between 5 seconds and 10 seconds. Thus, his service requirement at a cashier will be the sum of the U(20, 40) and U(5, 10) random variates he
“picked up” at the hot-food and drinks stations.

Report the following measures of system performance:

• The average and maximum delays in queue for hot food, specialty sandwiches, and cashiers
(regardless of which cashier)

• The time-average and maximum number in queue for hot food and specialty sandwiches
(separately), and the time-average and maximum total number in all cashier queues

• The average and maximum total delay in all the queues for each of the three types of customers
(separately)

• The overall average total delay for all customers, found by weighting their individual average
total delays by their respective probabilities of occurrence

• The time-average and maximum total number of customers in the entire system

The minimum number of employees is 4; run this as the “base-case” model. Then, consider
adding employees, in several ways:

1. Five employees, with the additional person used in one of the following ways:

• As a third cashier

• To help at the hot-food station. In this case, customers are still served one at a time,
but their service time is cut in half, being distributed uniformly between 25 seconds and
60 seconds.

• To help at the specialty-sandwich bar, meaning that service is still one at a time, but
distributed uniformly between 30 seconds and 90 seconds


2. Six employees, in one of the following configurations:

• Two cashiers, and two each at the hot-food and specialty-sandwich stations

• Three cashiers, two at hot food, and one at specialty sandwiches

• Three cashiers, one at hot food, and two at specialty sandwiches


3. Seven employees, with three cashiers, and two each at the hot-food and specialty-sandwich
stations

![Figure 1](https://drive.google.com/uc?export=view&id=1dbZkDfgdXF_dIaHdS8Ovkx8d70bfdr5y)

