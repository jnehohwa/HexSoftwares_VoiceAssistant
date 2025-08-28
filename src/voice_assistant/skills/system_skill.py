import psutil
import platform
from datetime import datetime
from .base import Skill

class SystemSkill(Skill):
    def names(self):
        return ["system", "sys", "status", "stats", "info"]

    def handle(self, cmd: str, args: str) -> str:
        try:
            if not args or args.lower() in ["info", "status", "stats"]:
                return self._get_system_info()
            elif args.lower() in ["cpu", "processor"]:
                return self._get_cpu_info()
            elif args.lower() in ["memory", "ram"]:
                return self._get_memory_info()
            elif args.lower() in ["disk", "storage"]:
                return self._get_disk_info()
            elif args.lower() in ["network", "net"]:
                return self._get_network_info()
            elif args.lower() in ["processes", "ps"]:
                return self._get_process_info()
            else:
                return f"Unknown system command: {args}. Try: info, cpu, memory, disk, network, processes"
        except Exception as e:
            return f"System error: {e}"

    def _get_system_info(self):
        """Get comprehensive system information"""
        try:
            # Basic system info
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk info
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            info = f"""System Information:
• OS: {system} {release} ({machine})
• Processor: {processor} ({cpu_count} cores)
• CPU Usage: {cpu_percent}%
• Memory Usage: {memory_percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
• Disk Usage: {disk_percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
• Uptime: {uptime.days} days, {uptime.seconds // 3600} hours"""
            
            return info
        except Exception as e:
            return f"Error getting system info: {e}"

    def _get_cpu_info(self):
        """Get detailed CPU information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = f"""CPU Information:
• Usage: {cpu_percent}%
• Cores: {cpu_count}
• Frequency: {cpu_freq.current:.0f} MHz (max: {cpu_freq.max:.0f} MHz)"""
            
            return info
        except Exception as e:
            return f"Error getting CPU info: {e}"

    def _get_memory_info(self):
        """Get detailed memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            info = f"""Memory Information:
• RAM Usage: {memory.percent}%
• RAM Used: {memory.used // (1024**3)} GB
• RAM Total: {memory.total // (1024**3)} GB
• RAM Available: {memory.available // (1024**3)} GB
• Swap Usage: {swap.percent}%
• Swap Used: {swap.used // (1024**3)} GB"""
            
            return info
        except Exception as e:
            return f"Error getting memory info: {e}"

    def _get_disk_info(self):
        """Get disk usage information"""
        try:
            partitions = psutil.disk_partitions()
            info = "Disk Information:\n"
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info += f"• {partition.device}: {usage.percent}% used ({usage.used // (1024**3)}GB / {usage.total // (1024**3)}GB)\n"
                except Exception:
                    continue
            
            return info.strip()
        except Exception as e:
            return f"Error getting disk info: {e}"

    def _get_network_info(self):
        """Get network information"""
        try:
            # Network interfaces
            interfaces = psutil.net_if_addrs()
            info = "Network Information:\n"
            
            for interface, addresses in interfaces.items():
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        info += f"• {interface}: {addr.address}\n"
            
            # Network usage
            net_io = psutil.net_io_counters()
            info += f"• Bytes sent: {net_io.bytes_sent // (1024**2)} MB\n"
            info += f"• Bytes received: {net_io.bytes_recv // (1024**2)} MB"
            
            return info
        except Exception as e:
            return f"Error getting network info: {e}"

    def _get_process_info(self):
        """Get top processes by CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            info = "Top 5 Processes by CPU Usage:\n"
            for i, proc in enumerate(processes[:5]):
                info += f"• {proc['name']}: {proc['cpu_percent']:.1f}% CPU, {proc['memory_percent']:.1f}% RAM\n"
            
            return info.strip()
        except Exception as e:
            return f"Error getting process info: {e}"
