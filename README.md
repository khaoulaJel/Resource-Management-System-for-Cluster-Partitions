# Simlab Cluster Resource Manager

The **Simlab Cluster Resource Manager** is a web-based application designed to monitor and manage HPC (High-Performance Computing) resources efficiently. This tool provides real-time insights into CPU and GPU utilization, making it easier for users to track resource usage and optimize workloads.

---

## Features

1. **User Authentication**:
   - Secure login using UM6P credentials.
   - Ensures only authorized users can access the dashboard.

2. **Resource Monitoring**:
   - Real-time data visualization for CPU and GPU usage.
   - Partition-wise resource tracking for CPU and GPU nodes.
   - Dynamic graphs and data tables for efficient monitoring.

3. **Dynamic Dashboard**:
   - Modern, responsive interface using Dash and Plotly.
   - Interactive dropdowns for selecting resource partitions.
   - Automatic updates for resource usage data.

4. **Backend Integration**:
   - Uses Paramiko for SSH communication with the Simlab cluster.
   - Fetches real-time data using optimized shell commands.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- A valid UM6P email and cluster credentials

### Dependencies
Install required Python packages using `pip install -r requirements.txt`.

Required packages:
- `dash`
- `flask`
- `paramiko`
- `numpy`
- `pandas`

---

## Usage

### Running the Application
1. Clone the repository and navigate to the project directory.
2. Run the following command: python index.py
3. Access the application in your browser at http://127.0.0.1:8050.

---

## Project Structure

- **index.py**: Entry point for the application. Manages routing between login and main pages.
- **main.py**: Implements the dashboard for resource monitoring.
- **login.py**: Handles user authentication with the cluster.
- **Commander.py**: Contains functions for SSH communication and credential verification.
- **User.py**: Manages user-related data and session handling.
- **DataFetcher.py**: Fetches and processes resource usage data (CPU and GPU) from the cluster.
- **__init__.py**: Initializes modules for the project.

---

## Key Modules

### Authentication (`login.py`)
- Validates UM6P credentials.
- Manages user sessions and redirects to the main dashboard upon successful login.

### Resource Fetching (`DataFetcher.py`)
- Executes optimized SSH commands to gather data:
  - **CPU**: Fetches partition-specific CPU usage.
  - **GPU**: Tracks GPU availability and usage.

### Dashboard (`main.py`)
- Displays real-time graphs and statistics.
- Features a dropdown for selecting partitions and dynamically updates resource information.

### SSH Manager (`Commander.py`)
- Implements connection reuse to minimize SSH overhead.
- Provides utility functions for verifying credentials and executing commands.

---

## Security

- **Session Management**: Uses Flask sessions to track user authentication.
- **Secure SSH Commands**: All communication with the cluster is secured via SSH.
