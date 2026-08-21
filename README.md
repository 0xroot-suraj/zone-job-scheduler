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

## Part 2: Cloud-IoT Deployment Blueprint

### 1. Architectural Overview
This architecture deploys the Python-based scheduling-and-safety engine (built in Part 1) as a secure, cloud-hosted "Cloud Platform Layer." The three city zones (Zone-A, Zone-B, Zone-C) act as IoT edge networks. Zone controllers submit sensor-processing jobs (e.g., traffic-camera triggers) to this centralized layer via a secured API Gateway.

### 2. VPC Design & Network Security
The deployment utilizes a standard Virtual Private Cloud (VPC) isolated from the public internet. 
*   **Public Subnets:** House the API Gateways and Load Balancers. These act as the ingress points for the Zone-A, B, and C controllers.
*   **Private Subnets:** House the actual compute layer where our `jobs.py` queueing logic and `task567.py` Deadlock-Safety Engine run. The compute instances have no public IP addresses. 
*   **Security Groups:** Ingress to the private compute subnets is strictly limited to traffic originating from the API Gateway's security group.

### 3. Compute Layer Integration
The engine built in Part 1 is packaged into a containerized microservice. 
*   **Job Ingestion:** As IoT payloads arrive from the zones, they are parsed and formatted into the dictionary structure defined in `jobs.py` (containing `job_id`, `zone`, `burst_time`, etc.).
*   **Execution:** The container utilizes the **SRTF algorithm** (selected in Task 8) to prioritize processing. 
*   **Safety & Synchronization:** As jobs execute, they consume shared resources (e.g., the Zone-B compute-credit counter). The exact Peterson's Algorithm and Banker's Algorithm logic from `task567.py` runs at the hypervisor level to ensure these concurrent updates remain arithmetically correct and absolutely deadlock-free across the shared IoT resource pools.

### 4. Reliability & Availability
While the algorithms in Part 1 handle concurrent processing safely, the cloud architecture ensures high availability. If a compute node fails (e.g., simulating a fatal page fault as seen in the address translator of Task 7), an Auto-Scaling Group immediately provisions a replacement node within the private subnet, pulling the current resource allocations (`ALLOCATION` and `AVAILABLE` matrices) from a highly available distributed cache like Redis to resume safe execution.