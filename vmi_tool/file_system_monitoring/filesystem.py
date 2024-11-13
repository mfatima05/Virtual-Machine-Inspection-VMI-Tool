import os
import psutil

class FileSystemMonitoring:
    def __init__(self):
        pass
    
    def get_disk_usage(self, path='C:\\'):
        """
        Retrieve disk usage statistics for the specified path.
        :param path: Path to get disk usage information for (default is C:\).
        :return: Dictionary with disk usage statistics.
        """
        # Ensure the path is absolute and normalized
        path = os.path.abspath(path)
        
        # Check if path exists
        if not os.path.exists(path):
            return {'error': f"Path {path} does not exist."}
        
        try:
            # Try to get the disk usage statistics
            usage = psutil.disk_usage(path)
            return {
                'total': f"{usage.total / (1024 ** 3):.2f} GB",
                'used': f"{usage.used / (1024 ** 3):.2f} GB",
                'free': f"{usage.free / (1024 ** 3):.2f} GB",
                'percent': f"{usage.percent:.2f}%"
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_files_and_directories(self, path='.'):
        """
        List all files and directories in the specified path.
        :param path: Directory path to list files and directories from (default is current directory).
        :return: List of dictionaries with file and directory names.
        """
        # Ensure the path is absolute
        path = os.path.abspath(path)
        
        # Check if path exists
        if not os.path.exists(path):
            return {'error': f"Path {path} does not exist."}
        
        file_list = []
        for entry in os.scandir(path):
            file_list.append({
                'name': entry.name,
                'type': 'directory' if entry.is_dir() else 'file',
                'size': f"{entry.stat().st_size / (1024 ** 2):.2f} MB" if entry.is_file() else None
            })
        return file_list
    
    def get_file_system_stats(self):
        """
        Retrieve file system statistics including total, used, and free space.
        :return: Dictionary with file system statistics.
        """
        partitions = psutil.disk_partitions()
        stats = {}
        for partition in partitions:
            stats[partition.device] = self.get_disk_usage(partition.mountpoint)
        return stats
