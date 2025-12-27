"""
Parse nmap output and extract information.
"""
import re
import logging
from typing import List, Optional, Tuple

from models import Service, HostInfo
from utils import extract_os_from_nmap, extract_services_from_nmap

logger = logging.getLogger(__name__)


class NmapParser:
    """Parses nmap output and creates result objects."""
    
    @staticmethod
    def parse_hostname(output: str) -> Optional[str]:
        """Extract hostname from nmap output."""
        # Pattern: Nmap scan report for hostname (ip)
        pattern = r'Nmap scan report for\s+([^\s(]+)'
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            hostname = match.group(1)
            # Remove IP if hostname contains it
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
                return None
            return hostname
        
        # Alternative pattern: hostname.domain (ip)
        pattern = r'([a-zA-Z0-9.-]+)\s+\((\d+\.\d+\.\d+\.\d+)\)'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        
        return None
    
    @staticmethod
    def parse_ip_address(output: str) -> Optional[str]:
        """Extract IP address from nmap output."""
        # Pattern: Nmap scan report for hostname (ip) or just (ip)
        pattern = r'\((\d+\.\d+\.\d+\.\d+)\)'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        
        # Alternative: IP at start of scan report
        pattern = r'^Nmap scan report for\s+(\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, output, re.MULTILINE)
        if match:
            return match.group(1)
        
        return None
    
    @staticmethod
    def parse_services(output: str) -> List[Service]:
        """Extract services from nmap output."""
        services = []
        service_data = extract_services_from_nmap(output)
        
        for svc in service_data:
            service = Service(
                name=svc['name'],
                port=svc['port'],
                protocol=svc['protocol'],
                version=svc.get('version'),
                state="open"
            )
            services.append(service)
        
        return services
    
    @staticmethod
    def parse_os_info(output: str) -> Tuple[Optional[str], Optional[str], List[str]]:
        """
        Parse OS information from nmap output.
        
        Returns:
            Tuple of (os_type, os_version, unverified_info)
        """
        os_type, os_version = extract_os_from_nmap(output)
        unverified_info = []
        
        # Look for OS details in nmap output
        os_lines = []
        in_os_section = False
        
        for line in output.split('\n'):
            if 'OS details:' in line or 'OS CPE:' in line:
                in_os_section = True
                continue
            
            if in_os_section:
                if line.strip() and not line.startswith(' '):
                    break
                if line.strip():
                    os_lines.append(line.strip())
        
        # Extract additional OS information
        if os_lines:
            for line in os_lines:
                # Look for version hints
                if 'Windows' in line:
                    # Try to extract version
                    version_match = re.search(r'Windows\s+(Server\s+)?(\d{4}|\d+\.\d+)', line, re.IGNORECASE)
                    if version_match:
                        unverified_info.append(f"OS version appears to be {line.strip()}")
                    else:
                        unverified_info.append(f"OS details: {line.strip()}")
                elif 'Linux' in line or 'Unix' in line:
                    unverified_info.append(f"OS details: {line.strip()}")
        
        # Look for OS CPE
        cpe_pattern = r'OS\s+CPE:\s+(.+)'
        cpe_match = re.search(cpe_pattern, output, re.IGNORECASE)
        if cpe_match:
            unverified_info.append(f"OS CPE: {cpe_match.group(1).strip()}")
        
        return os_type, os_version, unverified_info
    
    @staticmethod
    def parse_nmap_output(output: str, command: str) -> Optional[HostInfo]:
        """
        Parse complete nmap output and create HostInfo object.
        
        Args:
            output: Raw nmap output
            command: Command that generated the output
            
        Returns:
            HostInfo object or None if parsing fails
        """
        ip = NmapParser.parse_ip_address(output)
        if not ip:
            logger.warning("Could not extract IP address from nmap output")
            return None
        
        hostname = NmapParser.parse_hostname(output)
        services = NmapParser.parse_services(output)
        os_type, os_version, unverified_info = NmapParser.parse_os_info(output)
        
        host_info = HostInfo(
            ip_address=ip,
            hostname=hostname,
            os_type=os_type or "Unknown",
            os_version=os_version,
            services=services,
            is_windows=(os_type == "Windows")
        )
        
        # Add unverified information
        for info in unverified_info:
            host_info.add_unverified_info(info)
        
        # Add command output
        host_info.add_command_output(command, output)
        
        return host_info

