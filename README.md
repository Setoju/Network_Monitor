# System Monitor

A simple graphical system monitor application built with Python and Tkinter. It displays real-time information about CPU usage and temperature, RAM usage, GPU usage and temperature (if available), and network interface statistics.

## Features

* **CPU Usage and Temperature:** Shows the current CPU utilization percentage and temperature.
* **RAM Usage:** Displays the percentage of RAM used, along with the used and total RAM in GB.
* **GPU Usage and Temperature:** If an NVIDIA GPU is detected, it shows the GPU utilization percentage and temperature.
* **Network Statistics:** Provides the total network sent and received speeds, as well as individual sent and received speeds for each network interface.

## Requirements

* Python 3.x
* `tkinter` (usually included with Python)
* `psutil` (for system information)
* `pynvml` (for NVIDIA GPU information - optional)
