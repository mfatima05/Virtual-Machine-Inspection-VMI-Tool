from vmi_core.core import VMICore
from memory_analysis.memory import MemoryAnalysis
from network_monitoring.network import NetworkMonitoring
from process_monitoring.process import ProcessMonitoring
from file_system_monitoring.filesystem import FileSystemMonitoring
from anomaly_detection.anomaly import AnomalyDetection
from snapshot_manager.snapshot import SnapshotManager
from hypervisor_monitoring.hypervisor import HypervisorMonitor
from kernel_integrity.kernel import KernelIntegrity
from alerts.alert import Alerts
from gui_dashboard.gui import GUIInterface
import argparse
import time
import tkinter as tk
import subprocess
import sys

def print_intro():
    print("""
                 VIRTUAL MACHINE INTROSPECTION TOOL
                           Developed by
                             ~Maseera
      Happy Testing :)
    """)

def check_vm_exists(vm_name):
    try:
        # Check if VM with given name exists in VirtualBox
        output = subprocess.check_output(["VBoxManage", "list", "vms"]).decode()
        return f'"{vm_name}"' in output
    except Exception as e:
        print(f"Error checking VM existence: {e}")
        return False

def main():
    # Print intro text
    print_intro()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Virtual Machine Introspection (VMI) Tool - Developed by Maseera."
    )
    parser.add_argument('--vm', type=str, required=True, help='Name of the virtual machine.')
    parser.add_argument('--action', type=str, required=True, choices=[
        'info', 'reboot', 'memory', 'network', 'process', 'filesystem', 
        'cpu', 'anomaly', 'snapshot', 'kernel', 'alerts', 'gui', 'malware-analysis'], 
        help='Action to perform on the virtual machine.'
    )
    parser.add_argument('--remote', type=str, help='IP or hostname for the remote VM.')
    parser.add_argument('--snapshot', type=str, help='Snapshot name for restore action.')
    parser.add_argument('--user', type=str, help='Username for the remote VM.')
    parser.add_argument('--password', type=str, help='Password for the remote VM.')
    parser.add_argument('--pid', type=int, help='Process ID for detailed process information.')
    parser.add_argument('--path', type=str, default='.', help='Path for file system monitoring.')
    parser.add_argument('--visualize', type=str, choices=['usage', 'core', 'temperature'], 
                        help='Type of visualization for CPU monitoring.')
    args = parser.parse_args()

    # Check if the specified VM exists
    if not check_vm_exists(args.vm):
        print(f"Error: VM '{args.vm}' does not exist.")
        sys.exit(1)

    if args.action == 'memory':
        mem_analysis = MemoryAnalysis()
        print("Memory Info:", mem_analysis.get_memory_info())
        print("Swap Info:", mem_analysis.get_swap_memory_info())
        print("Top Memory-Consuming Processes:", mem_analysis.get_top_memory_consuming_processes())

    elif args.action == 'network':
        net_monitor = NetworkMonitoring()
        print("Network Interfaces:", net_monitor.get_network_interfaces())
        print("Active Connections:", net_monitor.get_active_connections())
        print("Network I/O Stats:", net_monitor.get_network_io_stats())
    
    elif args.action == 'process':
        proc_monitor = ProcessMonitoring()
        if args.pid:
            print("Process Info:", proc_monitor.get_process_info(args.pid))
        else:
            print("All Processes:", proc_monitor.get_all_processes())
            top_processes = proc_monitor.get_top_cpu_memory_processes()
            print("Top CPU-Consuming Processes:", top_processes['top_cpu'])
            print("Top Memory-Consuming Processes:", top_processes['top_memory'])

    elif args.action == 'filesystem':
        fs_monitor = FileSystemMonitoring()
        print("Disk Usage:", fs_monitor.get_disk_usage(args.path))
        print("Files and Directories:", fs_monitor.list_files_and_directories(args.path))
        print("File System Stats:", fs_monitor.get_file_system_stats())
    
    elif args.action == 'cpu':
        cpu_monitor = CPUMonitoring()
        print("CPU Usage:", cpu_monitor.get_cpu_usage())
        print("CPU Stats:", cpu_monitor.get_cpu_stats())
        print("CPU Core Usage:", cpu_monitor.get_cpu_core_usage())
        print("CPU Temperature:", cpu_monitor.get_cpu_temperature())

    elif args.action == 'anomaly':
        anomaly_detector = AnomalyDetection()
        anomaly_detector.start_detection()
        try:
            time.sleep(60)  # Run for 60 seconds
        finally:
            anomaly_detector.stop_detection()
            print("Final CPU Usage History:", anomaly_detector.get_cpu_usage_history())

    elif args.action == 'snapshot':
        snapshot_manager = SnapshotManager()
        if args.snapshot:
            print(snapshot_manager.restore_snapshot(args.snapshot, args.vm))
        else:
            print(f"Snapshot created: {snapshot_manager.create_snapshot(args.vm)}")

    elif args.action == 'kernel':
        kernel_integrity = KernelIntegrity('path_to_kernel_file')
        print(kernel_integrity.check_integrity('known_checksum'))

    elif args.action == 'alerts':
        alert_manager = Alerts()
        alert_manager.send_alert('recipient@example.com', 'Test Alert', 'This is a test alert.')

    elif args.action == 'gui':
        root = tk.Tk()
        app = GUIInterface(root)
        root.mainloop()

    else:
        vmi = VMICore(args.vm, remote_host=args.remote, username=args.user, password=args.password)
        vmi.connect()
        if args.action == 'info':
            print(vmi.get_vm_info())
        elif args.action == 'reboot':
            vmi.reboot_vm()
        vmi.disconnect()

if __name__ == "__main__":
    main()
