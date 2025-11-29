
import matplotlib.pyplot as plt
from copy import deepcopy

# -----------------------------
# داده‌های پردازه‌ها
# -----------------------------
processes = ["P1", "P2", "P3", "P4"]
arrival_times = [0, 2, 4, 6]
burst_times = [5, 3, 1, 2]
priorities = [2, 1, 3, 4]  # اولویت کمتر = بالاتر
quantum = 2  # برای Round Robin

# -----------------------------
# تابع رسم گانت چارت
# -----------------------------
def draw_gantt_chart(processes, start_times, end_times, colors=None, title="Gantt Chart"):
    n = len(processes)
    if colors is None:
        colors = ['skyblue','lightgreen','salmon','orange','violet','pink','yellow','cyan','gray','lightcoral']
    
    # ایجاد نگاشت برای پیدا کردن ایندکس فرآیند بر اساس نام
    process_map = {p: i for i, p in enumerate(processes)}

    plt.figure(figsize=(12,5))
    for i in range(len(start_times)):
        # پیدا کردن ایندکس فرآیند برای انتخاب رنگ صحیح
        process_idx = process_map[start_times[i][0]] # استفاده از نام فرآیند برای پیدا کردن ایندکس
        
        plt.barh(start_times[i][0], end_times[i]-start_times[i][1], left=start_times[i][1], 
                 color=colors[process_idx % len(colors)], height=0.6) # ارتفاع کمتر برای تفکیک بهتر
        plt.text((start_times[i][1]+end_times[i])/2, process_idx, f"{start_times[i][1]}-{end_times[i]}", 
                 va='center', ha='center', color='black', fontweight='bold')
    
    plt.xlabel("Time")
    plt.ylabel("Processes")
    plt.title(title)
    plt.yticks(range(len(processes)), processes) # تنظیم دقیق برچسب‌های محور y
    plt.xlim(0, max(end_times)+1)
    plt.grid(axis='x', linestyle='--')
    plt.show()

# -----------------------------
# FCFS
# -----------------------------
def fcfs(processes, arrival_times, burst_times):
    n = len(processes)
    start_times = [0]*n
    end_times = [0]*n
    waiting_times = [0]*n
    turnaround_times = [0]*n

    start_times[0] = arrival_times[0]
    end_times[0] = start_times[0] + burst_times[0]
    waiting_times[0] = start_times[0] - arrival_times[0]
    turnaround_times[0] = end_times[0] - arrival_times[0]

    for i in range(1,n):
        start_times[i] = max(arrival_times[i], end_times[i-1])
        end_times[i] = start_times[i] + burst_times[i]
        waiting_times[i] = start_times[i] - arrival_times[i]
        turnaround_times[i] = end_times[i] - arrival_times[i]

    print("\n=== FCFS ===")
    print("Process\tArrival\tBurst\tStart\tEnd\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{start_times[i]}\t{end_times[i]}\t{waiting_times[i]}\t{turnaround_times[i]}")
    print(f"Avg Waiting: {sum(waiting_times)/n:.2f}, Avg Turnaround: {sum(turnaround_times)/n:.2f}")
    
    # آماده‌سازی داده‌ها برای تابع رسم
    gantt_data = [(processes[i], start_times[i]) for i in range(n)]
    draw_gantt_chart(processes, gantt_data, end_times, title="Gantt Chart - FCFS")

# -----------------------------
# SJF Non-preemptive
# -----------------------------
def sjf_np(processes, arrival_times, burst_times):
    n = len(processes)
    completed = [False]*n
    start_times = [0]*n
    end_times = [0]*n
    waiting_times = [0]*n
    turnaround_times = [0]*n
    time = 0
    count = 0

    while count < n:
        idx = -1
        min_burst = float('inf')
        for i in range(n):
            if arrival_times[i] <= time and not completed[i] and burst_times[i] < min_burst:
                min_burst = burst_times[i]
                idx = i
        if idx == -1:
            time +=1
            continue
        start_times[idx] = time
        end_times[idx] = time + burst_times[idx]
        waiting_times[idx] = start_times[idx] - arrival_times[idx]
        turnaround_times[idx] = end_times[idx] - arrival_times[idx]
        time = end_times[idx]
        completed[idx] = True
        count +=1

    print("\n=== SJF Non-preemptive ===")
    print("Process\tArrival\tBurst\tStart\tEnd\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{start_times[i]}\t{end_times[i]}\t{waiting_times[i]}\t{turnaround_times[i]}")
    print(f"Avg Waiting: {sum(waiting_times)/n:.2f}, Avg Turnaround: {sum(turnaround_times)/n:.2f}")

    gantt_data = [(processes[i], start_times[i]) for i in range(n)]
    draw_gantt_chart(processes, gantt_data, end_times, title="Gantt Chart - SJF Non-preemptive")

# -----------------------------
# SRT (Shortest Remaining Time) - Preemptive
# -----------------------------
def srt(processes, arrival_times, burst_times):
    n = len(processes)
    completed = [False]*n
    remaining_times = burst_times.copy()
    waiting_times = [0]*n
    turnaround_times = [0]*n
    time = 0
    count = 0
    current_process = -1
    
    # برای رسم گانت چارت
    gantt_processes = []
    gantt_start_times = []
    gantt_end_times = []
    
    while count < n:
        idx = -1
        min_remaining = float('inf')
        for i in range(n):
            if arrival_times[i] <= time and not completed[i] and remaining_times[i] < min_remaining:
                min_remaining = remaining_times[i]
                idx = i
        
        if idx == -1:
            time += 1
            continue
        
        if current_process != idx:
            gantt_processes.append(processes[idx])
            gantt_start_times.append(time)
            current_process = idx
        
        time += 1
        remaining_times[idx] -= 1
        gantt_end_times.append(time)
        
        if remaining_times[idx] == 0:
            completed[idx] = True
            count += 1
            turnaround_times[idx] = time - arrival_times[idx]
            waiting_times[idx] = turnaround_times[idx] - burst_times[idx]
            current_process = -1 # بازنشانی فرآیند فعلی
    
    print("\n=== SRT (Shortest Remaining Time) ===")
    print("Process\tArrival\tBurst\tStart\tEnd\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t--\t--\t{waiting_times[i]}\t{turnaround_times[i]}")
    print(f"Avg Waiting: {sum(waiting_times)/n:.2f}, Avg Turnaround: {sum(turnaround_times)/n:.2f}")
    
    # آماده‌سازی داده‌ها برای رسم
    gantt_data = [(gantt_processes[i], gantt_start_times[i]) for i in range(len(gantt_processes))]
    draw_gantt_chart(processes, gantt_data, gantt_end_times, title="Gantt Chart - SRT")

# -----------------------------
# Round Robin (RR)
# -----------------------------
def rr(processes, arrival_times, burst_times, quantum):
    n = len(processes)
    remaining_times = burst_times.copy()
    completed = [False] * n
    waiting_times = [0] * n
    turnaround_times = [0] * n
    
    time = 0
    completed_count = 0
    ready_queue = []
    in_queue = [False] * n # برای جلوگیری از اضافه شدن تکراری به صف

    # برای رسم گانت چارت
    gantt_processes = []
    gantt_start_times = []
    gantt_end_times = []

    while completed_count < n:
        # 1. افزودن فرآیندهای جدید به صف آماده
        for i in range(n):
            if arrival_times[i] <= time and not completed[i] and not in_queue[i]:
                ready_queue.append(i)
                in_queue[i] = True

        # 2. اگر صف خالی است، CPU بیکار است
        if not ready_queue:
            time += 1
            continue

        # 3. خارج کردن فرآیند از صف برای اجرا
        current_idx = ready_queue.pop(0)
        in_queue[current_idx] = False

        # 4. ثبت اطلاعات برای گانت چارت
        gantt_processes.append(processes[current_idx])
        gantt_start_times.append(time)

        # 5. اجرای فرآیند برای یک کوانتم یا تا زمان اتمام
        exec_time = min(quantum, remaining_times[current_idx])
        time += exec_time
        remaining_times[current_idx] -= exec_time
        
        gantt_end_times.append(time)

        # 6. بررسی اتمام فرآیند
        if remaining_times[current_idx] == 0:
            completed[current_idx] = True
            completed_count += 1
            turnaround_times[current_idx] = time - arrival_times[current_idx]
            waiting_times[current_idx] = turnaround_times[current_idx] - burst_times[current_idx]

    print("\n=== Round Robin (Quantum = {}) ===".format(quantum))
    print("Process\tArrival\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{waiting_times[i]}\t{turnaround_times[i]}")
    print(f"Avg Waiting: {sum(waiting_times)/n:.2f}, Avg Turnaround: {sum(turnaround_times)/n:.2f}")

    # آماده‌سازی داده‌ها برای رسم
    gantt_data = [(gantt_processes[i], gantt_start_times[i]) for i in range(len(gantt_processes))]
    draw_gantt_chart(processes, gantt_data, gantt_end_times, title=f"Gantt Chart - Round Robin (Q={quantum})")

# -----------------------------
# Priority Non-preemptive
# -----------------------------
def priority_np(processes, arrival_times, burst_times, priorities):
    n = len(processes)
    completed = [False]*n
    start_times = [0]*n
    end_times = [0]*n
    waiting_times = [0]*n
    turnaround_times = [0]*n
    time = 0
    count = 0

    while count < n:
        idx = -1
        highest_priority = float('inf')
        for i in range(n):
            if arrival_times[i] <= time and not completed[i] and priorities[i]<highest_priority:
                highest_priority = priorities[i]
                idx = i
        if idx==-1:
            time +=1
            continue
        start_times[idx] = time
        end_times[idx] = time + burst_times[idx]
        waiting_times[idx] = start_times[idx] - arrival_times[idx]
        turnaround_times[idx] = end_times[idx] - arrival_times[idx]
        time = end_times[idx]
        completed[idx]=True
        count +=1

    print("\n=== Priority Scheduling Non-preemptive ===")
    print("Process\tArrival\tBurst\tPriority\tStart\tEnd\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{arrival_times[i]}\t{burst_times[i]}\t{priorities[i]}\t{start_times[i]}\t{end_times[i]}\t{waiting_times[i]}\t{turnaround_times[i]}")
    print(f"Avg Waiting: {sum(waiting_times)/n:.2f}, Avg Turnaround: {sum(turnaround_times)/n:.2f}")
    
    gantt_data = [(processes[i], start_times[i]) for i in range(n)]
    draw_gantt_chart(processes, gantt_data, end_times, title="Gantt Chart - Priority Non-preemptive")

# -----------------------------
# اجرای تمام الگوریتم‌ها
# -----------------------------
fcfs(processes, arrival_times, burst_times)
sjf_np(processes, arrival_times, burst_times)
srt(processes, arrival_times, burst_times)
rr(processes, arrival_times, burst_times, quantum)
priority_np(processes, arrival_times, burst_times, priorities)
