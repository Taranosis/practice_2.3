import tkinter as tk
import psutil

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_memory():
    return psutil.virtual_memory().percent

def get_disk():
    return psutil.disk_usage("/").percent

def update_stats():
    cpu_label.config(text=f"CPU: {get_cpu()}%")
    memory_label.config(text=f"RAM: {get_memory()}%")
    disk_label.config(text=f"Disk: {get_disk()}%")
    root.after(1000, update_stats)

root = tk.Tk()
root.title("Системный монитор")
root.geometry("250x150")

cpu_label = tk.Label(root, text="CPU: ", font=("Arial", 14))
cpu_label.pack(pady=5)

memory_label = tk.Label(root, text="RAM: ", font=("Arial", 14))
memory_label.pack(pady=5)

disk_label = tk.Label(root, text="Disk: ", font=("Arial", 14))
disk_label.pack(pady=5)

update_stats()
root.mainloop()