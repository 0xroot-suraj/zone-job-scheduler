# Part 2: Cloud, Security & IoT Deployment Blueprint

## Task 9: Distributed Architecture & Communication
I have selected a **Hybrid architecture** for coordinating the three zone controllers with the central Smart City Operations dashboard. 
*   **Justification:** A hybrid model offers high **scalability** as new zones are added, provides strong **fault tolerance** (zones can continue processing local jobs via edge computing if the center goes down), and eliminates the **single point of failure** inherent in a strict client-server model.

**Data Flows:**
*   **(a) Zone controller pushing a real-time public-safety alert to the dashboard:** This flow will be **Asynchronous** using **MQTT**. MQTT's lightweight publish/subscribe model is ideal for real-time, low-latency alerts where the controller doesn't need to wait for a dashboard response to keep functioning.
*   **(b) Zone controller uploading its full day's sensor log for archival:** This flow will be **Synchronous** using **HTTPS**. A synchronous connection ensures the massive log file is fully and securely received by the central archive before the local controller deletes its copy to free up storage.

## Task 10: VPC-Based Network Boundary
The deployment utilizes a **single VPC with three logically isolated private subnets** (Subnet-A, Subnet-B, Subnet-C). 
*   **Justification:** A single VPC provides logical isolation while allowing unified centralized management. The customizability of the VPC allows us to assign non-overlapping CIDR blocks to each zone's subnet, ensuring clean IP management.
*   **Enforcement Control:** The cross-zone boundary is enforced via **Security Group rules**. The security group attached to Subnet-A explicitly denies all inbound traffic originating from the CIDR blocks of Subnet-B and Subnet-C, physically preventing direct peer-to-peer compromise between zones.

## Task 11: Network-Security Objectives
1.  **Protect Sensitive Data:** *Encryption at Rest (AES-256).* Defends the platform by ensuring that even if physical storage drives are compromised, the historical sensor logs remain unreadable without the decryption key.
2.  **Authentication:** *Multi-Factor Authentication (MFA).* Defends against credential stuffing by requiring a secondary physical token before any admin can access the zone controller interfaces.
3.  **Authorization:** *Role-Based Access Control (RBAC).* Defends against privilege escalation by ensuring a user can only perform actions explicitly granted to their assigned role.
4.  **Prevent Cyber Attacks:** *Network Firewall.* Defends the platform by inspecting packet headers and blocking malicious IP addresses from initiating DDoS or port-scanning attacks against the API gateway.
5.  **Secure Communication:** *TLS 1.3.* Defends data in transit by creating an encrypted tunnel, preventing Man-in-the-Middle (MitM) attackers from snooping on sensor payloads.
6.  **Ensure Availability:** *Auto-Scaling Groups.* Defends the system against sudden traffic spikes (like a city-wide emergency triggering thousands of sensors) by automatically provisioning additional compute instances.

## Task 12: IAM and Data-Protection Map

**IAM Role Table:**
| Role Name | Permission Set |
| :--- | :--- |
| **Zone Operator** | Read/Write access limited only to their specific assigned zone controller. Cannot alter global routing. |
| **City Dashboard Admin** | Global Read/Write access across all zones, permission to modify VPC routing and update scheduler logic. |
| **Auditor** | Strict Read-only access to historical logs and job execution times for compliance checks. |

**Data-Protection Map:**
*   **At Rest:** Protected using *AES-256 Encryption*. Example: The raw `JOBS` list and historical completion logs stored on a zone controller's hard drive.
*   **In Transit:** Protected using *TLS 1.3 Encryption*. Example: A real-time public-safety alert payload traveling from Zone-A to the central dashboard.
*   **In Use:** Protected using *Confidential Computing (Secure Enclaves)*. Example: The Banker's-Algorithm safety check engine from Part 1 running inside active memory, protecting the `AVAILABLE` and `ALLOCATION` matrices from being scraped by malware on the host machine.

## Task 13: IoT Connectivity & Architecture Mapping

**IoT Sensor/Device Connectivity:**
1.  **Traffic-Camera Trigger:** *5G*. Justified by the need for high-bandwidth, low-latency transmission of heavy image/video data from intersections.
2.  **Environmental Sensor (Air Quality):** *LoRaWAN*. Justified by its low-power draw (can run on batteries for years) and long-range capabilities across wide city parks.
3.  **Wearable Public-Safety Device (for City Workers):** *Wi-Fi*. Justified by moderate range and ability to connect seamlessly to existing city-deployed municipal network nodes.

**IoT Architecture Layers:**
1.  **Physical Environment:** The city infrastructure (intersections, parks, utility stations) where events occur.
2.  **Perception/Device:** The physical traffic cameras, environmental sensors, and wearables capturing data.
3.  **Gateway:** The local zone controllers (Zone-A, B, C) aggregating and filtering the raw sensor data.
4.  **Network Communication:** The 5G, LoRaWAN, and Wi-Fi networks transmitting data back to the central hub.
5.  **Cloud Platform:** **The scheduler and Banker's-Algorithm engine from Part 1**, handling all compute, concurrency logic, and resource-allocation safety.
6.  **Application:** The Smart City Operations dashboard where human operators view alerts and insights.

## Task 14: Threats and Mitigations
1.  **Threat:** *Distributed Denial of Service (DDoS).* Malicious actors flood the API gateway with fake job requests to crash the scheduler.
    *   **Mitigation:** Implement edge-level Rate Limiting to block traffic bursts exceeding normal threshold patterns.
2.  **Threat:** *Man-in-the-Middle (MitM) Attack.* An attacker intercepts the network traffic to alter a public-safety alert.
    *   **Mitigation:** Enforce strict TLS 1.3 encryption for all data flowing between the Gateways and the Cloud Platform.
3.  **Threat:** *Device Spoofing.* A malicious device connects to the network pretending to be a legitimate city traffic camera to send false triggers.
    *   **Mitigation:** Require Mutual TLS (mTLS) where each approved IoT device holds a cryptographic certificate that must be verified before the gateway accepts its data.