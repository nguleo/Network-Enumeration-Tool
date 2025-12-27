"""
Windows-specific enumeration tools.
"""
import subprocess
import re
import logging
from typing import Dict, List, Tuple

from models import HostInfo, Service
from utils import run_command

logger = logging.getLogger(__name__)


class WindowsEnumeration:
    """Handles Windows-specific enumeration."""
    
    @staticmethod
    def check_smb_available() -> bool:
        """Check if SMB enumeration tools are available."""
        # Check for smbclient, enum4linux, or similar tools
        tools = ['smbclient', 'enum4linux', 'rpcclient']
        for tool in tools:
            try:
                result = subprocess.run(
                    [tool, "--version"] if tool != "smbclient" else [tool, "-V"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0 or tool == "smbclient":
                    return True
            except FileNotFoundError:
                continue
            except Exception:
                continue
        return False
    
    @staticmethod
    def enumerate_smb(target: str) -> Tuple[str, int]:
        """
        Enumerate SMB shares and information.
        
        Args:
            target: Target IP address
            
        Returns:
            Tuple of (output, return_code)
        """
        # Try enum4linux first
        cmd = ["enum4linux", "-a", target]
        output, return_code = run_command(cmd, timeout=300)
        
        if return_code == 0 or "DOMAIN" in output or "WORKGROUP" in output:
            return output, return_code
        
        # Fallback to smbclient
        logger.info("enum4linux not available or failed, trying smbclient")
        cmd = ["smbclient", "-L", target, "-N"]
        output2, return_code2 = run_command(cmd, timeout=60)
        
        # Combine outputs
        combined = f"=== enum4linux output ===\n{output}\n\n=== smbclient output ===\n{output2}"
        return combined, return_code2 if return_code != 0 else return_code
    
    @staticmethod
    def enumerate_netbios(target: str) -> Tuple[str, int]:
        """
        Enumerate NetBIOS information.
        
        Args:
            target: Target IP address
            
        Returns:
            Tuple of (output, return_code)
        """
        # Try nmblookup
        cmd = ["nmblookup", "-A", target]
        output, return_code = run_command(cmd, timeout=30)
        
        if return_code == 0:
            return output, return_code
        
        # Fallback to nbtscan if available
        cmd = ["nbtscan", target]
        output2, return_code2 = run_command(cmd, timeout=30)
        
        combined = f"=== nmblookup output ===\n{output}\n\n=== nbtscan output ===\n{output2}"
        return combined, return_code2 if return_code != 0 else return_code
    
    @staticmethod
    def enumerate_ldap(target: str) -> Tuple[str, int]:
        """
        Enumerate LDAP/Active Directory information.
        
        Args:
            target: Target IP address
            
        Returns:
            Tuple of (output, return_code)
        """
        # Try ldapsearch
        cmd = ["ldapsearch", "-x", "-H", f"ldap://{target}", "-s", "base"]
        output, return_code = run_command(cmd, timeout=60)
        
        if return_code == 0:
            return output, return_code
        
        # Try with common base DN
        base_dns = [
            "dc=example,dc=com",
            "dc=domain,dc=local",
            "dc=corp,dc=local"
        ]
        
        for base_dn in base_dns:
            cmd = ["ldapsearch", "-x", "-H", f"ldap://{target}", "-b", base_dn, "-s", "base"]
            output2, return_code2 = run_command(cmd, timeout=60)
            if return_code2 == 0:
                return output2, return_code2
        
        return output, return_code
    
    @staticmethod
    def parse_smb_output(output: str) -> Dict[str, str]:
        """Parse SMB enumeration output and extract information."""
        info = {}
        
        # Extract domain/workgroup
        domain_match = re.search(r'Domain/Workgroup:\s*(.+)', output, re.IGNORECASE)
        if domain_match:
            info["Domain/Workgroup"] = domain_match.group(1).strip()
        
        # Extract computer name
        name_match = re.search(r'Computer name:\s*(.+)', output, re.IGNORECASE)
        if name_match:
            info["Computer Name"] = name_match.group(1).strip()
        
        # Extract OS version
        os_match = re.search(r'OS version:\s*(.+)', output, re.IGNORECASE)
        if os_match:
            info["OS Version"] = os_match.group(1).strip()
        
        # Extract shares
        share_pattern = r'Share\s+Type\s+Comment\s+---+\s+([^\n]+(?:\n[^\n]+)*)'
        share_match = re.search(share_pattern, output, re.IGNORECASE | re.MULTILINE)
        if share_match:
            shares = share_match.group(1)
            info["SMB Shares"] = shares.strip()
        
        # Extract users (if available)
        user_pattern = r'user:\[([^\]]+)\]'
        user_matches = re.findall(user_pattern, output, re.IGNORECASE)
        if user_matches:
            info["Users"] = ", ".join(user_matches)
        
        return info
    
    @staticmethod
    def parse_netbios_output(output: str) -> Dict[str, str]:
        """Parse NetBIOS enumeration output."""
        info = {}
        
        # Extract NetBIOS name
        name_pattern = r'(\S+)\s+<00>\s+UNIQUE'
        name_match = re.search(name_pattern, output)
        if name_match:
            info["NetBIOS Name"] = name_match.group(1)
        
        # Extract domain
        domain_pattern = r'(\S+)\s+<00>\s+GROUP'
        domain_match = re.search(domain_pattern, output)
        if domain_match:
            info["NetBIOS Domain"] = domain_match.group(1)
        
        # Extract MAC address
        mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
        mac_match = re.search(mac_pattern, output)
        if mac_match:
            info["MAC Address"] = mac_match.group(0)
        
        return info
    
    @staticmethod
    def parse_ldap_output(output: str) -> Dict[str, str]:
        """Parse LDAP/AD enumeration output."""
        info = {}
        
        # Extract domain
        domain_pattern = r'dc=([^,]+)'
        domain_matches = re.findall(domain_pattern, output)
        if domain_matches:
            info["LDAP Domain"] = ".".join(domain_matches)
        
        # Extract naming contexts
        context_pattern = r'namingContexts:\s*(.+)'
        context_match = re.search(context_pattern, output, re.IGNORECASE)
        if context_match:
            info["Naming Contexts"] = context_match.group(1).strip()
        
        return info
    
    @staticmethod
    def enumerate_windows_host(target: str, host_info: HostInfo) -> HostInfo:
        """
        Perform comprehensive Windows enumeration.
        
        Args:
            target: Target IP address
            host_info: Existing HostInfo object to update
            
        Returns:
            Updated HostInfo object
        """
        logger.info(f"Starting Windows-specific enumeration for {target}")
        
        # SMB Enumeration
        smb_output, _ = WindowsEnumeration.enumerate_smb(target)
        host_info.add_command_output(f"enum4linux -a {target}", smb_output)
        smb_info = WindowsEnumeration.parse_smb_output(smb_output)
        host_info.windows_info.update(smb_info)
        
        # Extract domain from SMB if available
        if "Domain/Workgroup" in smb_info:
            domain = smb_info["Domain/Workgroup"]
            if domain and domain != "WORKGROUP":
                host_info.domain = domain
        
        # NetBIOS Enumeration
        netbios_output, _ = WindowsEnumeration.enumerate_netbios(target)
        host_info.add_command_output(f"nmblookup -A {target}", netbios_output)
        netbios_info = WindowsEnumeration.parse_netbios_output(netbios_output)
        host_info.windows_info.update(netbios_info)
        
        # LDAP/AD Enumeration (if LDAP port is open)
        ldap_ports = [389, 636]
        has_ldap = any(svc.port in ldap_ports and svc.protocol == "tcp" 
                      for svc in host_info.services)
        
        if has_ldap:
            ldap_output, _ = WindowsEnumeration.enumerate_ldap(target)
            host_info.add_command_output(f"ldapsearch -x -H ldap://{target}", ldap_output)
            ldap_info = WindowsEnumeration.parse_ldap_output(ldap_output)
            host_info.windows_info.update(ldap_info)
            
            if "LDAP Domain" in ldap_info:
                host_info.domain = ldap_info["LDAP Domain"]
        
        # Add unverified information based on SMB output
        if "OS Version" in smb_info:
            os_version = smb_info["OS Version"]
            host_info.add_unverified_info(f"OS Version is at least {os_version}")
        
        return host_info

