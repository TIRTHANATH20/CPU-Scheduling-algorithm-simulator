import tkinter as tk
from tkinter import ttk, messagebox
import time

processes = []

# Function to add a process
def add_process():
    try:
        process_id = entry_process_id.get()
        arrival_time = int(entry_arrival_time.get())
        burst_time = int(entry_burst_time.get())
        priority = int(entry_priority.get()) if entry_priority.get() else None

        process = {
            'processId': process_id,
            'arrivalTime': arrival_time,
            'burstTime': burst_time,
            'priority': priority
        }

        processes.append(process)
        update_process_table()
        clear_form()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs for all fields.")

# Function to clear input fields
def clear_form():
    entry_process_id.delete(0, tk.END)
    entry_arrival_time.delete(0, tk.END)
    entry_burst_time.delete(0, tk.END)
    entry_priority.delete(0, tk.END)

# Function to update the process table
def update_process_table():
    for row in process_table.get_children():
        process_table.delete(row)
    
    for process in processes:
        process_table.insert("", "end", values=(
            process['processId'], 
            process['arrivalTime'], 
            process['burstTime'], 
            process['priority'] if process['priority'] is not None else "-"
        ))

# Function to clear the previous Gantt chart
def clear_gantt_chart():
    for widget in frame_gantt.winfo_children():
        widget.destroy()

# Function to animate scheduling and append Gantt chart
def append_gantt(gantt_chart):
    clear_gantt_chart()  # Clear previous Gantt chart
    for i, process in enumerate(gantt_chart):
        gantt_block = tk.Label(frame_gantt, text=process, bg="lightblue", relief="solid", width=5)
        gantt_block.grid(row=0, column=i, padx=2, pady=5)
        root.update()
        time.sleep(1)

# Function to simulate scheduling
def simulate():
    algorithm = combo_algorithm.get()
    quantum_time = entry_quantum_time.get()
    
    if algorithm == "Round Robin" and not quantum_time:
        messagebox.showerror("Input Error", "Please enter a time quantum for Round Robin.")
        return
    
    if not processes:
        messagebox.showerror("Input Error", "Please add at least one process before simulating.")
        return
    
    if algorithm == "FCFS":
        result = fcfs(processes)
    elif algorithm == "SJF":
        result = sjf(processes)
    elif algorithm == "Priority":
        result = priority_scheduling(processes)
    elif algorithm == "Round Robin":
        result = round_robin(processes, int(quantum_time))
    
    display_results(result, algorithm)
    append_gantt(result['gantt'])  # Append the new Gantt chart

# Function to display the results
def display_results(result, algorithm):
    result_label.config(text=f"Gantt Chart ({algorithm}): " + " ".join(result['gantt']))
    metrics_label.config(text=f"Average Waiting Time: {result['averageWaitingTime']:.2f}, "
                              f"Average Turnaround Time: {result['averageTurnaroundTime']:.2f}")

    detailed_results_text = "\n".join(
        [f"Process {p['processId']} - Waiting Time: {result['waitingTimes'][p['processId']]:.2f}, "
         f"Turnaround Time: {result['turnaroundTimes'][p['processId']]:.2f}"
         for p in processes]
    )
    detailed_results_label.config(text=detailed_results_text)

# Reset function to clear all the data and fields
def reset():
    global processes
    processes = []  # Reset the process list
    clear_form()  # Clear input fields
    update_process_table()  # Clear the process table
    clear_gantt_chart()  # Clear the Gantt chart
    result_label.config(text="Gantt Chart: ")  # Reset Gantt chart label
    metrics_label.config(text="Average Waiting Time: , Average Turnaround Time: ")  # Reset metrics label
    detailed_results_label.config(text="")  # Clear detailed results

# Scheduling Algorithms (Backend Logic)

def fcfs(processes):
    processes.sort(key=lambda x: x['arrivalTime'])
    current_time = 0
    gantt = []
    waiting_time = {}
    turnaround_time = {}
    
    for process in processes:
        if current_time < process['arrivalTime']:
            current_time = process['arrivalTime']
        gantt.append(process['processId'])
        waiting_time[process['processId']] = current_time - process['arrivalTime']
        turnaround_time[process['processId']] = waiting_time[process['processId']] + process['burstTime']
        current_time += process['burstTime']
    
    avg_waiting_time = sum(waiting_time.values()) / len(waiting_time)
    avg_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time)
    
    return {
        "gantt": gantt,
        "averageWaitingTime": avg_waiting_time,
        "averageTurnaroundTime": avg_turnaround_time,
        "waitingTimes": waiting_time,
        "turnaroundTimes": turnaround_time,
        "totalTime": current_time
    }

def sjf(processes):
    processes.sort(key=lambda x: (x['arrivalTime'], x['burstTime']))
    current_time = 0
    gantt = []
    waiting_time = {}
    turnaround_time = {}
    
    while processes:
        available_processes = [p for p in processes if p['arrivalTime'] <= current_time]
        if not available_processes:
            current_time += 1
            continue
        process = min(available_processes, key=lambda x: x['burstTime'])
        processes.remove(process)
        gantt.append(process['processId'])
        waiting_time[process['processId']] = current_time - process['arrivalTime']
        turnaround_time[process['processId']] = waiting_time[process['processId']] + process['burstTime']
        current_time += process['burstTime']
    
    avg_waiting_time = sum(waiting_time.values()) / len(waiting_time)
    avg_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time)
    
    return {
        "gantt": gantt,
        "averageWaitingTime": avg_waiting_time,
        "averageTurnaroundTime": avg_turnaround_time,
        "waitingTimes": waiting_time,
        "turnaroundTimes": turnaround_time,
        "totalTime": current_time
    }

def priority_scheduling(processes):
    processes.sort(key=lambda x: (x['arrivalTime'], x['priority']))
    current_time = 0
    gantt = []
    waiting_time = {}
    turnaround_time = {}
    
    while processes:
        available_processes = [p for p in processes if p['arrivalTime'] <= current_time]
        if not available_processes:
            current_time += 1
            continue
        process = min(available_processes, key=lambda x: x['priority'])
        processes.remove(process)
        gantt.append(process['processId'])
        waiting_time[process['processId']] = current_time - process['arrivalTime']
        turnaround_time[process['processId']] = waiting_time[process['processId']] + process['burstTime']
        current_time += process['burstTime']
    
    avg_waiting_time = sum(waiting_time.values()) / len(waiting_time)
    avg_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time)
    
    return {
        "gantt": gantt,
        "averageWaitingTime": avg_waiting_time,
        "averageTurnaroundTime": avg_turnaround_time,
        "waitingTimes": waiting_time,
        "turnaroundTimes": turnaround_time,
        "totalTime": current_time
    }

def round_robin(processes, quantum):
    processes = sorted(processes, key=lambda x: x['arrivalTime'])
    queue = []
    gantt = []
    current_time = 0
    waiting_time = {}
    remaining_burst_time = {}
    turnaround_time = {}
    completed_processes = set()

    for process in processes:
        waiting_time[process['processId']] = 0
        remaining_burst_time[process['processId']] = process['burstTime']
        turnaround_time[process['processId']] = 0

    while len(completed_processes) < len(processes):
        for process in processes:
            if process['arrivalTime'] <= current_time and process['processId'] not in completed_processes:
                queue.append(process)
        
        if not queue:
            current_time += 1
            continue

        process = queue.pop(0)
        if remaining_burst_time[process['processId']] <= quantum:
            current_time += remaining_burst_time[process['processId']]
            gantt.append(process['processId'])
            turnaround_time[process['processId']] = current_time - process['arrivalTime']
            completed_processes.add(process['processId'])
        else:
            current_time += quantum
            remaining_burst_time[process['processId']] -= quantum
            gantt.append(process['processId'])

    avg_waiting_time = sum(waiting_time.values()) / len(processes)
    avg_turnaround_time = sum(turnaround_time.values()) / len(processes)

    return {
        "gantt": gantt,
        "averageWaitingTime": avg_waiting_time,
        "averageTurnaroundTime": avg_turnaround_time,
        "waitingTimes": waiting_time,
        "turnaroundTimes": turnaround_time,
        "totalTime": current_time
    }

# Tkinter GUI Setup
root = tk.Tk()
root.title("CPU Scheduling Algorithms Simulator")

# Process Input Section
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_process_id = tk.Label(frame_input, text="Process ID:")
label_process_id.grid(row=0, column=0, padx=5, pady=5)
entry_process_id = tk.Entry(frame_input)
entry_process_id.grid(row=0, column=1, padx=5, pady=5)

label_arrival_time = tk.Label(frame_input, text="Arrival Time:")
label_arrival_time.grid(row=1, column=0, padx=5, pady=5)
entry_arrival_time = tk.Entry(frame_input)
entry_arrival_time.grid(row=1, column=1, padx=5, pady=5)

label_burst_time = tk.Label(frame_input, text="Burst Time:")
label_burst_time.grid(row=2, column=0, padx=5, pady=5)
entry_burst_time = tk.Entry(frame_input)
entry_burst_time.grid(row=2, column=1, padx=5, pady=5)

label_priority = tk.Label(frame_input, text="Priority (optional):")
label_priority.grid(row=3, column=0, padx=5, pady=5)
entry_priority = tk.Entry(frame_input)
entry_priority.grid(row=3, column=1, padx=5, pady=5)

button_add_process = tk.Button(frame_input, text="Add Process", command=add_process)
button_add_process.grid(row=4, columnspan=2, pady=10)

# Process Table
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

process_table = ttk.Treeview(frame_table, columns=("Process ID", "Arrival Time", "Burst Time", "Priority"), show="headings")
process_table.heading("Process ID", text="Process ID")
process_table.heading("Arrival Time", text="Arrival Time")
process_table.heading("Burst Time", text="Burst Time")
process_table.heading("Priority", text="Priority")
process_table.pack()

# Algorithm Selection Section
frame_algorithm = tk.Frame(root)
frame_algorithm.pack(pady=10)

label_algorithm = tk.Label(frame_algorithm, text="Select Algorithm:")
label_algorithm.grid(row=0, column=0, padx=5, pady=5)

combo_algorithm = ttk.Combobox(frame_algorithm, values=["FCFS", "SJF", "Priority", "Round Robin"])
combo_algorithm.grid(row=0, column=1, padx=5, pady=5)

label_quantum_time = tk.Label(frame_algorithm, text="Quantum Time (for Round Robin):")
label_quantum_time.grid(row=1, column=0, padx=5, pady=5)
entry_quantum_time = tk.Entry(frame_algorithm)
entry_quantum_time.grid(row=1, column=1, padx=5, pady=5)

button_simulate = tk.Button(frame_algorithm, text="Simulate", command=simulate)
button_simulate.grid(row=2, columnspan=2, pady=10)

# Reset Button
button_reset = tk.Button(frame_algorithm, text="Reset", command=reset)
button_reset.grid(row=3, columnspan=2, pady=10)

# Gantt Chart Frame (for animation)
frame_gantt = tk.Frame(root)
frame_gantt.pack(pady=10)

# Results Section
frame_results = tk.Frame(root)
frame_results.pack(pady=10)

result_label = tk.Label(frame_results, text="Gantt Chart: ")
result_label.pack()

metrics_label = tk.Label(frame_results, text="Average Waiting Time: , Average Turnaround Time: ")
metrics_label.pack()

detailed_results_label = tk.Label(frame_results, text="")
detailed_results_label.pack()

# Start the GUI main loop
root.mainloop()
