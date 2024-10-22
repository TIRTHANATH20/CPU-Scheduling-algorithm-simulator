# CPU scheduling algorithm simulator-
This project is a CPU Scheduling Algorithms Simulator built using Python's tkinter library for the graphical user interface (GUI). The simulator implements four CPU scheduling algorithms:

First-Come, First-Served (FCFS)
Shortest Job First (SJF)
Priority Scheduling
Round Robin (with customizable time quantum)
The application allows users to add processes with their respective parameters and simulate the scheduling process. It also displays the Gantt Chart for visualizing the scheduling order and calculates key metrics such as Average Waiting Time and Average Turnaround Time for each algorithm.

Features
Add processes with:
Process ID
Arrival Time
Burst Time
(Optional) Priority
Select the scheduling algorithm to simulate:
FCFS
SJF
Priority Scheduling
Round Robin (with customizable time quantum)
View the Gantt Chart for each algorithm.
See metrics such as:
Average Waiting Time
Average Turnaround Time
Detailed Waiting and Turnaround times for each process.
Reset functionality to clear the inputs, table, and simulation results.
Algorithms Implemented
First-Come, First-Served (FCFS):

Processes are executed in the order they arrive.
Shortest Job First (SJF):

The process with the shortest burst time is selected next, among the available processes.
Priority Scheduling:

Processes are scheduled based on their priority (lower values indicate higher priority).
Round Robin:

Each process is assigned a time quantum, and they are executed in a cyclic manner.
GUI Layout
The GUI is built using the tkinter library. It is divided into the following sections:

Input Form: Enter the details of processes such as Process ID, Arrival Time, Burst Time, and Priority (optional).
Process Table: Displays all the added processes.
Algorithm Selection: Choose an algorithm and set the quantum time for Round Robin.
Gantt Chart: Visualizes the order in which processes are executed.
Metrics: Shows the calculated metrics (Average Waiting Time and Average Turnaround Time).
Reset Button: Clear all inputs and results to start a new simulation.
