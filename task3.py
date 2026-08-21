import copy
from jobs import JOBS

def round_robin(quantum):
    jobs = copy.deepcopy(JOBS)
    for j in jobs:
        j['rem_time'] = j['burst_time']
        
    jobs_to_arrive = sorted(jobs, key=lambda x: (x['arrival_time'], x['job_id']))
    ready_queue = []
    
    current_time = 0
    completed_jobs = []
    
    context_switches = 0
    dispatch_slices = 0
    last_job_id = None
    
    while jobs_to_arrive or ready_queue:
        if not ready_queue and jobs_to_arrive:
            if current_time < jobs_to_arrive[0]['arrival_time']:
                current_time = jobs_to_arrive[0]['arrival_time']
            while jobs_to_arrive and jobs_to_arrive[0]['arrival_time'] <= current_time:
                ready_queue.append(jobs_to_arrive.pop(0))
               
        job = ready_queue.pop(0)
        
        dispatch_slices += 1
        if last_job_id is not None and job['job_id'] != last_job_id:
            context_switches += 1
        last_job_id = job['job_id']
        
        run_time = min(quantum, job['rem_time'])
        new_time = current_time + run_time
       
        while jobs_to_arrive and jobs_to_arrive[0]['arrival_time'] <= new_time:
            ready_queue.append(jobs_to_arrive.pop(0))
            
        job['rem_time'] -= run_time
        current_time = new_time
        
        if job['rem_time'] > 0:
            ready_queue.append(job) # Put expired job at the back
        else:
            job['tat'] = current_time - job['arrival_time']
            job['wt'] = job['tat'] - job['burst_time']
            completed_jobs.append(job)
            
    print(f"\n--- Round Robin (Quantum = {quantum}) ---")
    print(f"{'Job ID':<10} | {'Wait Time':<10} | {'Turnaround Time'}")
    print("-" * 45)
    
    job_order = {j['job_id']: i for i, j in enumerate(JOBS)}
    completed_jobs.sort(key=lambda x: job_order[x['job_id']])
    
    total_wt = sum(j['wt'] for j in completed_jobs)
    total_tat = sum(j['tat'] for j in completed_jobs)
    n = len(completed_jobs)
    
    for r in completed_jobs:
        print(f"{r['job_id']:<10} | {r['wt']:<10} | {r['tat']}")
        
    print(f"Average Waiting Time: {total_wt/n:.2f}")
    print(f"Average Turnaround Time: {total_tat/n:.2f}")
    print(f"Context Switches: {context_switches} (across {dispatch_slices} dispatch slices)")

if __name__ == "__main__":
    round_robin(3)
    round_robin(6)
    
    print("\n--- Theoretical Justification ---")
    print("A real OS would experience more overhead running Quantum 3 because it forces 16 context switches compared to only 10 switches at Quantum 6, and in a physical system, each switch consumes non-zero CPU cycles.")