import copy
from jobs import JOBS

def print_results(name, results):
    print(f"\n--- {name} Scheduling ---")
    print(f"{'Job ID':<10} | {'Wait Time':<10} | {'Turnaround Time'}")
    print("-" * 45)
    total_wt = 0
    total_tat = 0
    for r in results:
        print(f"{r['job_id']:<10} | {r['wt']:<10} | {r['tat']}")
        total_wt += r['wt']
        total_tat += r['tat']
    
    n = len(results)
    print(f"Average Waiting Time: {total_wt/n:.2f}")
    print(f"Average Turnaround Time: {total_tat/n:.2f}")

def fcfs():
    jobs = sorted(copy.deepcopy(JOBS), key=lambda x: (x['arrival_time'], x['job_id']))
    current_time = 0
    results = []
    
    for job in jobs:
        if current_time < job['arrival_time']:
            current_time = job['arrival_time']
        
        wt = current_time - job['arrival_time']
        tat = wt + job['burst_time']
        
        results.append({'job_id': job['job_id'], 'wt': wt, 'tat': tat})
        current_time += job['burst_time']
        
    print_results("FCFS", results)

def sjf():
    jobs = copy.deepcopy(JOBS)
    current_time = 0
    completed = 0
    n = len(jobs)
    results = []
    
    while completed < n:
        ready_queue = [j for j in jobs if j['arrival_time'] <= current_time and 'completed' not in j]
        
        if not ready_queue:
            current_time += 1
            continue
         
        ready_queue.sort(key=lambda x: (x['burst_time'], x['arrival_time'], x['job_id']))
        job = ready_queue[0]
        
        wt = current_time - job['arrival_time']
        tat = wt + job['burst_time']
        
        results.append({'job_id': job['job_id'], 'wt': wt, 'tat': tat})
        current_time += job['burst_time']
        
        for j in jobs:
            if j['job_id'] == job['job_id']:
                j['completed'] = True
                break
        completed += 1
        
    print_results("Non-Preemptive SJF", results)

def srtf():
    jobs = copy.deepcopy(JOBS)
    for j in jobs:
        j['remaining_time'] = j['burst_time']
        
    current_time = 0
    completed = 0
    n = len(jobs)
    results_dict = {}
    
    while completed < n:
        ready_queue = [j for j in jobs if j['arrival_time'] <= current_time and j['remaining_time'] > 0]
        
        if not ready_queue:
            current_time += 1
            continue
        
        ready_queue.sort(key=lambda x: (x['remaining_time'], x['arrival_time'], x['job_id']))
        job = ready_queue[0]
        
        job['remaining_time'] -= 1
        current_time += 1
        
        if job['remaining_time'] == 0:
            completed += 1
            tat = current_time - job['arrival_time']
            wt = tat - job['burst_time']
            results_dict[job['job_id']] = {'job_id': job['job_id'], 'wt': wt, 'tat': tat}
            
    results = [results_dict[j['job_id']] for j in JOBS]
    print_results("SRTF", results)

if __name__ == "__main__":
    fcfs()
    sjf()
    srtf()