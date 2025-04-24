import tkinter as tk
from tkinter import ttk
import psutil
import time

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground="#66ccff")
        self.style.configure("TFrame", background="#1e1e1e")

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.cpu_label = ttk.Label(self.main_frame, text="CPU Usage: --% | Temp: --°C", style="Header.TLabel")
        self.cpu_label.pack(anchor=tk.W, pady=5)

        self.gpu_label = ttk.Label(self.main_frame, text="GPU Usage: --% | Temp: --°C", style="Header.TLabel")
        self.ram_label = ttk.Label(self.main_frame, text="RAM Usage: --%", style="Header.TLabel")
        self.ram_label.pack(anchor=tk.W, pady=5)
        self.gpu_label.pack(anchor=tk.W, pady=5)

        self.net_summary_label = ttk.Label(self.main_frame, text="Total Net: Sent -- KB/s | Recv -- KB/s", style="Header.TLabel")
        self.net_summary_label.pack(anchor=tk.W, pady=5)

        self.interfaces_frame = ttk.LabelFrame(self.main_frame, text="Per Interface Stats", style="TFrame")
        self.interfaces_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.interface_labels = {}

        self.prev_net_io = psutil.net_io_counters(pernic=True)
        self.last_update = time.time()

        self.update_stats()

    def update_stats(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_temp = "--"
        try:
            temps = psutil.sensors_temperatures()
            if "coretemp" in temps:
                cpu_temp = round(temps["coretemp"][0].current, 1)
            elif "k10temp" in temps:
                cpu_temp = round(temps["k10temp"][0].current, 1)
            elif "cpu_thermal" in temps:
                cpu_temp = round(temps["cpu_thermal"][0].current, 1)
        except:
            pass
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage:.1f}% | Temp: {cpu_temp}°C")

        gpu_usage = "--"
        gpu_temp = "--"
        if GPU_AVAILABLE:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
                gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            except:
                gpu_usage = "N/A"
                gpu_temp = "N/A"
        self.gpu_label.config(text=f"GPU Usage: {gpu_usage}% | Temp: {gpu_temp}°C")

        ram = psutil.virtual_memory()
        ram_usage_percent = ram.percent
        ram_used_gb = ram.used / (1024 ** 3)
        ram_total_gb = ram.total / (1024 ** 3)
        self.ram_label.config(
            text=f"RAM Usage: {ram_usage_percent:.1f}% ({ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB)")

        now = time.time()
        elapsed = now - self.last_update
        current_net_io = psutil.net_io_counters(pernic=True)

        total_sent = 0
        total_recv = 0

        for iface, stats in current_net_io.items():
            prev_stats = self.prev_net_io.get(iface)
            if not prev_stats:
                continue

            sent_bytes = stats.bytes_sent - prev_stats.bytes_sent
            recv_bytes = stats.bytes_recv - prev_stats.bytes_recv

            sent_kbps = (sent_bytes / 1024) / elapsed
            recv_kbps = (recv_bytes / 1024) / elapsed

            total_sent += sent_kbps
            total_recv += recv_kbps

            label_text = f"{iface}: Sent {sent_kbps:.2f} KB/s | Recv {recv_kbps:.2f} KB/s"
            if iface not in self.interface_labels:
                self.interface_labels[iface] = ttk.Label(self.interfaces_frame, text=label_text)
                self.interface_labels[iface].pack(anchor=tk.W, pady=2)
            else:
                self.interface_labels[iface].config(text=label_text)

        self.net_summary_label.config(text=f"Total Net: Sent {total_sent:.2f} KB/s | Recv {total_recv:.2f} KB/s")

        self.prev_net_io = current_net_io
        self.last_update = now
        self.root.after(1000, self.update_stats)

    def __del__(self):
        if GPU_AVAILABLE:
            pynvml.nvmlShutdown()