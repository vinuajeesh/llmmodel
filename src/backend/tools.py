import platform
import subprocess
import datetime
import mss
import os
import socket
import psutil
from duckduckgo_search import DDGS

class SystemTools:

    @staticmethod
    def get_current_time():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def execute_cmd(command):
        """
        Executes a shell command.
        WARNING: This is dangerous. In a real app, this should be heavily restricted.
        """
        try:
            # Using shell=True for flexibility, but it's a security risk.
            # Capturing output.
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    @staticmethod
    def take_screenshot(filename="screenshot.png"):
        try:
            with mss.mss() as sct:
                # Capture the first monitor
                monitor = sct.monitors[1]
                sct.shot(mon=monitor, output=filename)
            return f"Screenshot saved to {os.path.abspath(filename)}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    @staticmethod
    def scan_network():
        """
        Basic network scan using ARP or Ping would require root/admin usually.
        We will just list network interfaces and local IP for now to be safe and portable.
        """
        try:
            info = []
            info.append(f"Hostname: {socket.gethostname()}")

            # Interfaces
            stats = psutil.net_if_addrs()
            for intf, addrs in stats.items():
                info.append(f"Interface: {intf}")
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info.append(f"  IP Address: {addr.address}")
                        info.append(f"  Netmask: {addr.netmask}")
                        info.append(f"  Broadcast: {addr.broadcast}")

            return "\n".join(info)
        except Exception as e:
            return f"Error scanning network: {str(e)}"

    @staticmethod
    def search_web(query):
        try:
            results = DDGS().text(query, max_results=3)
            return str(results)
        except Exception as e:
            return f"Error searching web: {str(e)}"

    @staticmethod
    def get_system_specs():
        try:
            return f"""
            OS: {platform.system()} {platform.release()}
            CPU: {platform.processor()}
            RAM: {round(psutil.virtual_memory().total / (1024.0 **3))} GB
            """
        except Exception as e:
            return str(e)
