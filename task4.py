import copy
from jobs import JOBS

def priority_scheduling(aging=False):
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
            
        for j in ready_queue:
            wait_ticks = current_time - j['arrival_time']
            if aging:
                j['eff_prio'] = max(1, j['priority'] - (wait_ticks // 3))
            else:
                j['eff_prio'] = j['priority']
                
        ready_queue.sort(key=lambda x: (x['eff_prio'], x['arrival_time'], x['job_id']))
        job = ready_queue[0]
        
        wt = current_time - job['arrival_time']
        tat = wt + job['burst_time']
        
        results.append({'job_id': job['job_id'], 'wt': wt, 'tat': tat, 'eff_prio': job['eff_prio']})
        
        current_time += job['burst_time']
        
        for j in jobs:
            if j['job_id'] == job['job_id']:
                j['completed'] = True
                break
        completed += 1
        
    mode_name = "With Aging" if aging else "Without Aging"
    print(f"\n--- Non-Preemptive Priority Scheduling ({mode_name}) ---")
    print(f"{'Job ID':<10} | {'Wait Time':<10} | {'Turnaround Time'}")
    print("-" * 45)
    
    longest_wait_job = None
    max_wait = -1
    
    output_order = []
    for orig_job in JOBS:
        for r in results:
            if r['job_id'] == orig_job['job_id']:
                output_order.append(r)
                if r['wt'] > max_wait:
                    max_wait = r['wt']
                    longest_wait_job = r['job_id']
                break
                
    for r in output_order:
        print(f"{r['job_id']:<10} | {r['wt']:<10} | {r['tat']}")
        
    print(f"\nSingle longest-waiting job: {longest_wait_job} (Wait Time: {max_wait})")

if __name__ == "__main__":
    priority_scheduling(aging=False)
    priority_scheduling(aging=True)