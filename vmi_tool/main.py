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
from help.help import Help
import argparse
import time
import tkinter as tk
import pyclamd

def print_intro():
    print("""
                 VIRTUAL MACHINE INTROSPECTION TOOL
                           Developed by
                             ~Maseera
 
      Happy Testing :)
    
    """)

def main():
     # Print intro text
    print_intro()
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Virtual Machine Introspection (VMI) Tool - Developed by Khyati and Maseera."
    )
    parser = argparse.ArgumentParser(description="Virtual Machine Introspection (VMI) Tool")
    parser.add_argument('--vm', type=str, required=True, help='Name of the virtual machine.')
    parser.add_argument('--action', type=str, required=True, choices=['info', 'reboot', 'memory', 'network', 'process', 'filesystem', 'cpu', 'anomaly', 'snapshot', 'kernel','alerts', 'gui', 'malware-analysis'], help='Action to perform on the virtual machine.')
    parser.add_argument('--remote', type=str, help='IP or hostname for the remote VM.')
    parser.add_argument('--snapshot', type=str, help='Snapshot name for restore action. (Only required if action is "snapshot" and sub-action is restore)')
    parser.add_argument('--user', type=str, help='Username for the remote VM.')
    parser.add_argument('--password', type=str, help='Password for the remote VM.')
    parser.add_argument('--pid', type=int, help='Process ID for detailed process information.')
    parser.add_argument('--path', type=str, default='.', help='Path for file system monitoring (default is current directory).')
    parser.add_argument('--visualize', type=str, choices=['usage', 'core', 'temperature'], help='Type of visualization for CPU monitoring.')
    args = parser.parse_args()

    if args.action == 'memory':
        # Perform memory analysis
        mem_analysis = MemoryAnalysis()

        memory_info = mem_analysis.get_memory_info()
        print("Memory Info:", memory_info)

        swap_info = mem_analysis.get_swap_memory_info()
        print("Swap Info:", swap_info)

        top_processes = mem_analysis.get_top_memory_consuming_processes()
        print("Top Memory-Consuming Processes:", top_processes)

    elif args.action == 'network':
        # Perform network monitoring
        net_monitor = NetworkMonitoring()

        interfaces = net_monitor.get_network_interfaces()
        print("Network Interfaces:", interfaces)

        active_connections = net_monitor.get_active_connections()
        print("Active Connections:", active_connections)

        io_stats = net_monitor.get_network_io_stats()
        print("Network I/O Stats:", io_stats)
    
    elif args.action == 'process':
        # Perform process monitoring
        proc_monitor = ProcessMonitoring()

        if args.pid:
            process_info = proc_monitor.get_process_info(args.pid)
            print("Process Info:", process_info)
        else:
            all_processes = proc_monitor.get_all_processes()
            print("All Processes:", all_processes)

            top_processes = proc_monitor.get_top_cpu_memory_processes()
            print("Top CPU-Consuming Processes:", top_processes['top_cpu'])
            print("Top Memory-Consuming Processes:", top_processes['top_memory'])

    elif args.action == 'filesystem':
        # Perform file system monitoring
        fs_monitor = FileSystemMonitoring()

        disk_usage = fs_monitor.get_disk_usage(args.path)
        print("Disk Usage:", disk_usage)

        files_and_dirs = fs_monitor.list_files_and_directories(args.path)
        print("Files and Directories:", files_and_dirs)

        fs_stats = fs_monitor.get_file_system_stats()
        print("File System Stats:", fs_stats)
    
    elif args.action == 'cpu':
        cpu_monitor = CPUMonitoring()

        cpu_usage = cpu_monitor.get_cpu_usage()
        print("CPU Usage:", cpu_usage)

        cpu_stats = cpu_monitor.get_cpu_stats()
        print("CPU Stats:", cpu_stats)

        core_usage = cpu_monitor.get_cpu_core_usage()
        print("CPU Core Usage:", core_usage)

        cpu_temperature = cpu_monitor.get_cpu_temperature()
        print("CPU Temperature:", cpu_temperature)

    elif args.action == 'anomaly':
        anomaly_detector = AnomalyDetection()
        anomaly_detector.start_detection()

        # Run detection for a specified amount of time
        try:
            time.sleep(60)  # Collect data and detect anomalies for 60 seconds
        finally:
            anomaly_detector.stop_detection()
            print("Final CPU Usage History:", anomaly_detector.get_cpu_usage_history())

    elif args.action == 'snapshot':
        snapshot_manager = SnapshotManager()
        if args.snapshot:
            # Restore snapshot
            result = snapshot_manager.restore_snapshot(args.snapshot, args.vm)
            print(result)
        else:
            # Create new snapshot
            snapshot_name = snapshot_manager.create_snapshot(args.vm)
            print(f"Snapshot created: {snapshot_name}")

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
            info = vmi.get_vm_info()
            print(info)
        elif args.action == 'reboot':
            vmi.reboot_vm()

        vmi.disconnect()

if __name__ == "__main__":
    main()
