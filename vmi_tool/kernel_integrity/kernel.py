import hashlib

class KernelIntegrity:
    def __init__(self, kernel_file='kernel_file_path'):
        self.kernel_file = kernel_file

    def compute_checksum(self):
        """Compute the checksum of the kernel file."""
        try:
            with open(self.kernel_file, 'rb') as f:
                file_hash = hashlib.sha256()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
                return file_hash.hexdigest()
        except Exception as e:
            return {'error': str(e)}

    def check_integrity(self, known_checksum):
        """Check if the current kernel file matches the known checksum."""
        current_checksum = self.compute_checksum()
        if 'error' in current_checksum:
            return current_checksum
        return {'integrity': current_checksum == known_checksum}
