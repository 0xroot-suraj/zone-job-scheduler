# Zone Job-Scheduler & Secure Cloud-IoT Deployment Blueprint

This repository contains the complete end-to-end compute layer and deployment blueprint for the multi-zone monitoring platform. It is divided into the runnable Python scheduling-and-safety engine (Part 1) and the cloud deployment architecture (Part 2).

## Part 1: How to Run the Scripts
All code is written in plain Python using only the standard library. No external dependencies are required. Execute the following commands in your terminal from the root directory of this repository:

*   **Task 2 (FCFS, SJF, SRTF):** `python task2.py`
*   **Task 3 (Round Robin):** `python task3.py`
*   **Task 4 (Priority & Aging):** `python task4.py`
*   **Tasks 5, 6, & 7 (Synchronization & Memory):** `python task567.py`

---

## Task 8: Algorithm Selection Justification

Based on the measured simulation data in Tasks 2-4, **SRTF (Shortest Remaining Time First)** is the optimal algorithm family for production deployment to handle the zone-controller jobs. It delivered the lowest average waiting time (11.50) and turnaround time (17.00), ensuring critical sensor data is processed rapidly.

The other algorithm families are less suitable for the following reasons:
1.  **FCFS:** Suffers from the "convoy effect." By running blindly in arrival order, its average waiting time was **17.12**, significantly higher than the SJF/SRTF family.
2.  **Round Robin:** Incurs excessive context-switching overhead. The simulation demonstrated exactly **16 context switches at Quantum 3** and **10 switches at Quantum 6**. In a physical OS environment, these constant interruptions consume valuable CPU cycles compared to burst-based methods.
3.  **Priority Scheduling:** Introduces the risk of strict starvation. Without aging, job **Z3-J02** suffered the longest wait time in the queue (33 ticks). While aging mitigates this, it requires constant dynamic recalculation of effective priorities, an overhead that SRTF avoids while still delivering superior overall wait times.

---

## Part 2: Cloud, Security & IoT Deployment Blueprint
The complete architectural design, network boundary planning, and IoT mapping can be found in the documentation folder:

[View Architecture Blueprint (docs/architecture_blueprint.md)](docs/architecture_blueprint.md)