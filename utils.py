"""
Utility functions for the enumeration tool.
"""
import re
import socket
import ipaddress
import platform
from typing import List, Set, Optional
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def resolve_dns(hostname: str) -> Optional[str]:
    """Resolve DNS hostname to IP address."""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror as e:
        logger.warning(f"Failed to resolve {hostname}: {e}")
        return None


def is_valid_ip(ip: str) -> bool:
    """Check if string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False


def expand_cidr(cidr: str) -> List[str]:
    """Expand CIDR notation to list of IP addresses."""
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError as e:
        logger.error(f"Invalid CIDR notation {cidr}: {e}")
        return []


def get_dns_server() -> str:
    """Get the currently configured DNS server."""
    try:
        system = platform.system()
        if system == "Windows":
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Parse DNS servers from ipconfig output
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if "DNS Servers" in line or "DNS Server" in line:
                    # Try to extract IP from next few lines
                    for j in range(i, min(i+5, len(lines))):
                        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', lines[j])
                        if match:
                            return match.group(1)
        else:
            # Linux/Mac
            result = subprocess.run(
                ["cat", "/etc/resolv.conf"],
                capture_output=True,
                text=True,
                timeout=10
            )
            match = re.search(r'nameserver\s+(\S+)', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        logger.warning(f"Could not determine DNS server: {e}")
    
    return "Unable to determine"


def run_command(command: List[str], timeout: int = 300) -> tuple[str, int]:
    """Run a shell command and return output and return code."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            errors='replace'
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(command)}")
        return "Command timed out", -1
    except Exception as e:
        logger.error(f"Error running command {' '.join(command)}: {e}")
        return str(e), -1


def extract_os_from_nmap(output: str) -> tuple[Optional[str], Optional[str]]:
    """Extract OS type and version from nmap output using regex."""
    os_type = None
    os_version = None
    
    # Patterns for OS detection
    windows_patterns = [
        r'Windows\s+(\d+\.?\d*|Server\s+\d{4}|XP|Vista|7|8|10|11)',
        r'Microsoft\s+Windows\s+(\d+\.?\d*|Server\s+\d{4}|XP|Vista|7|8|10|11)',
        r'Win32',
    ]
    
    linux_patterns = [
        r'Linux\s+(\d+\.\d+\.\d+)',
        r'Ubuntu\s+(\d+\.\d+)',
        r'Debian\s+(\d+)',
        r'CentOS\s+(\d+)',
        r'Red\s+Hat\s+(\d+)',
    ]
    
    unix_patterns = [
        r'Unix',
        r'FreeBSD',
        r'OpenBSD',
        r'NetBSD',
        r'Solaris',
    ]
    
    # Check for Windows
    for pattern in windows_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            os_type = "Windows"
            os_version = match.group(1) if match.groups() else None
            break
    
    # Check for Linux
    if not os_type:
        for pattern in linux_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                os_type = "Linux"
                os_version = match.group(1) if match.groups() else None
                break
    
    # Check for Unix
    if not os_type:
        for pattern in unix_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                os_type = "Unix"
                break
    
    return os_type, os_version


def extract_services_from_nmap(output: str) -> List[dict]:
    """Extract service information from nmap output using regex."""
    services = []
    
    # Pattern to match service lines: PORT STATE SERVICE VERSION
    # Example: 22/tcp   open  ssh     OpenSSH 8.2p1
    pattern = r'(\d+)/(tcp|udp)\s+(\w+)\s+(\S+)(?:\s+(.+))?'
    
    for line in output.split('\n'):
        match = re.search(pattern, line)
        if match:
            port = int(match.group(1))
            protocol = match.group(2)
            state = match.group(3)
            service_name = match.group(4)
            version = match.group(5).strip() if match.group(5) else None
            
            if state == "open":
                services.append({
                    'port': port,
                    'protocol': protocol,
                    'name': service_name,
                    'version': version
                })
    
    return services
