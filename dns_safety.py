"""
DNS safety checks and confirmation prompts.
"""
import socket
import subprocess
import re
import platform
import logging

logger = logging.getLogger(__name__)


class DNSSafety:
    """Handles DNS safety checks and user confirmation."""
    
    @staticmethod
    def get_dns_server() -> str:
        """Get the currently configured DNS server."""
        try:
            if platform.system() == "Windows":
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
                try:
                    result = subprocess.run(
                        ["cat", "/etc/resolv.conf"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    match = re.search(r'nameserver\s+(\S+)', result.stdout)
                    if match:
                        return match.group(1)
                except:
                    # Try systemd-resolve for newer Linux systems
                    try:
                        result = subprocess.run(
                            ["systemd-resolve", "--status"],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        match = re.search(r'DNS Servers:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result.stdout)
                        if match:
                            return match.group(1)
                    except:
                        pass
        except Exception as e:
            logger.warning(f"Could not determine DNS server: {e}")
        
        return "Unable to determine"
    
    @staticmethod
    def prompt_confirmation(target_spec: str) -> bool:
        """
        Prompt user for confirmation when DNS records are provided.
        
        Args:
            target_spec: Target specification that contains DNS names
            
        Returns:
            True if user confirms, False otherwise
        """
        dns_server = DNSSafety.get_dns_server()
        
        print("\n" + "="*70)
        print("DNS SAFETY CHECK")
        print("="*70)
        print(f"Target specification contains DNS records: {target_spec}")
        print(f"Currently configured DNS server: {dns_server}")
        print("\nWARNING: DNS misconfiguration could lead to scope violations.")
        print("Please verify that the DNS server is correct before proceeding.")
        print("="*70)
        
        while True:
            response = input("\nProceed with enumeration? (y/N): ").strip().lower()
            
            if not response:
                return False  # Default to No
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no (or press Enter for No).")

