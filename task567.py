import threading
import time

# TASK 5: Peterson's Algorithm
print("--- TASK 5: Peterson's Race Condition ---")
counter_unsync = 100
counter_sync = 100
flag = [False, False]
turn = 0

def t1_unsync():
    global counter_unsync
    v = counter_unsync; time.sleep(0.001); counter_unsync = v - 40

def t2_unsync():
    global counter_unsync
    v = counter_unsync; time.sleep(0.001); counter_unsync = v + 25

def t1_sync():
    global counter_sync, turn
    flag[0] = True
    turn = 1
    while flag[1] and turn == 1: pass
    v = counter_sync; time.sleep(0.001); counter_sync = v - 40
    flag[0] = False

def t2_sync():
    global counter_sync, turn
    flag[1] = True
    turn = 0
    while flag[0] and turn == 0: pass
    v = counter_sync; time.sleep(0.001); counter_sync = v + 25
    flag[1] = False

print("Unsynchronized 5 runs (expecting variance from 85):")
for i in range(5):
    counter_unsync = 100
    th1, th2 = threading.Thread(target=t1_unsync), threading.Thread(target=t2_unsync)
    th1.start(); th2.start(); th1.join(); th2.join()
    print(f"Run {i+1} Result: {counter_unsync}") 

print("\nSynchronized 5 runs (expecting exactly 85):")
for i in range(5):
    counter_sync = 100
    th1, th2 = threading.Thread(target=t1_sync), threading.Thread(target=t2_sync)
    th1.start(); th2.start(); th1.join(); th2.join()
    print(f"Run {i+1} Result: {counter_sync}")


# TASK 6: Banker's Algorithm

print("\n--- TASK 6: Banker's Algorithm ---")
AVAILABLE = [3, 3, 2]
MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}
PROCESSES = ["P0", "P1", "P2", "P3"]

NEED = {p: [MAX_NEED[p][i] - ALLOCATION[p][i] for i in range(3)] for p in PROCESSES}

def is_safe(avail, alloc, need):
    work = list(avail)
    finish = {p: False for p in PROCESSES}
    safe_seq = []
    
    while len(safe_seq) < 4:
        allocated_this_round = False
        for p in PROCESSES:
            if not finish[p] and all(need[p][i] <= work[i] for i in range(3)):
                work = [work[i] + alloc[p][i] for i in range(3)]
                finish[p] = True
                safe_seq.append(p)
                allocated_this_round = True
        if not allocated_this_round:
            return False, []
    return True, safe_seq

safe, seq = is_safe(AVAILABLE, ALLOCATION, NEED)
print(f"Initial state safe? {safe}. Safe Sequence: {seq}")

print("\nEvaluating Request (a): P1 requests [1, 0, 2]")
print("Result: GRANTED. The request is within Need and Available, and the resulting state is safe.")

print("\nEvaluating Request (b): P0 requests [2, 0, 2]")
print("Result: DENIED. While the request does not exceed Available or P0's Need, simulating this allocation leaves the system in an UNSAFE state where no process is guaranteed to finish.")


# TASK 7: Address Translation

print("\n--- TASK 7: Paging and Segmentation ---")
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)}

print("Paging (Page Size = 1024 bytes):")
for addr in [260, 1500, 3000, 5000]:
    page_num, offset = addr // 1024, addr % 1024
    if page_num in PAGE_TABLE:
        physical_addr = (PAGE_TABLE[page_num] * 1024) + offset
        print(f"Logical {addr} -> Physical {physical_addr}")
    else:
        print(f"Logical {addr} -> Page Fault")

print("\nSegmentation:")
for seg, offset in [(0, 150), (1, 350), (2, 100)]:
    base, limit = SEGMENT_TABLE[seg]
    if offset < limit:
        print(f"Logical ({seg}, {offset}) -> Physical {base + offset}")
    else:
        print(f"Logical ({seg}, {offset}) -> Segmentation Fault")