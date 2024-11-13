import psutil

class ProcessMonitoring:
    def __init__(self):
        pass
    
    def get_all_processes(self):
        """
        Retrieve a list of all running processes with basic details.
        :return: List of dictionaries with process details.
        """
        process_list = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                process_list.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_used': f"{proc.info['memory_info'].rss / (1024 ** 2):.2f} MB"  # Memory usage in MB
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        for i in process_list:
            print(i)
    
    def get_process_info(self, pid):
        """
        Retrieve detailed information about a specific process by PID.
        :param pid: Process ID.
        :return: Dictionary with detailed process information.
        """
        try:
            proc = psutil.Process(pid)
            process_info = {
                'pid': proc.pid,
                'name': proc.name(),
                'status': proc.status(),
                'cpu_percent': proc.cpu_percent(interval=1),
                'memory_info': f"{proc.memory_info().rss / (1024 ** 2):.2f} MB",  # Memory usage in MB
                'create_time': proc.create_time(),
                'exe_path': proc.exe()
            }
            for key, value in process_info.items():
                print(f"{key}: {value}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {'error': 'Process not found or access denied'}
    
    def get_top_cpu_memory_processes(self, count=5):
        """
        Retrieve top processes by CPU and memory usage.
        :param count: Number of top processes to return.
        :return: List of dictionaries with process details.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_used': f"{proc.info['memory_info'].rss / (1024 ** 2):.2f} MB"  # Memory usage in MB
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort processes by CPU and memory usage (descending) and return the top N
        processes_by_cpu = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
        processes_by_memory = sorted(processes, key=lambda p: float(p['memory_used'].replace(' MB', '')), reverse=True)
        
        top_cpu = processes_by_cpu[:count]
        top_memory = processes_by_memory[:count]
        
        return {
            'top_cpu': top_cpu,
            'top_memory': top_memory
        }


