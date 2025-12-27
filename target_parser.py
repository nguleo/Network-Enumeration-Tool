"""
Parse and expand target specifications (IPs, DNS, CIDR).
"""
import re
from typing import List, Set
import ipaddress
import socket
import logging

from utils import resolve_dns, is_valid_ip, expand_cidr

logger = logging.getLogger(__name__)


class TargetParser:
    """Handles parsing and expansion of target specifications."""
    
    def __init__(self):
        self.resolved_targets: Set[str] = set()
        self.excluded_ips: Set[str] = set()
    
    def parse_targets(self, target_spec: str) -> Set[str]:
        """
        Parse target specification into a set of IP addresses.
        
        Supports:
        - Individual IPv4 addresses (e.g., 192.168.1.1)
        - DNS records (e.g., server.example.com)
        - Subnets in CIDR notation (e.g., 192.168.1.0/24)
        - Comma-separated lists of any combination
        
        Args:
            target_spec: Target specification string
            
        Returns:
            Set of IP addresses
        """
        targets = set()
        
        # Split by comma
        parts = [part.strip() for part in target_spec.split(',')]
        
        for part in parts:
            if not part:
                continue
            
            # Check if it's a CIDR notation
            if '/' in part:
                try:
                    ips = expand_cidr(part)
                    targets.update(ips)
                    logger.info(f"Expanded CIDR {part} to {len(ips)} hosts")
                except Exception as e:
                    logger.error(f"Error expanding CIDR {part}: {e}")
            
            # Check if it's a valid IP
            elif is_valid_ip(part):
                targets.add(part)
            
            # Assume it's a DNS name
            else:
                ip = resolve_dns(part)
                if ip:
                    targets.add(ip)
                    logger.info(f"Resolved {part} to {ip}")
                else:
                    logger.warning(f"Could not resolve {part}")
        
        self.resolved_targets = targets
        return targets
    
    def parse_exclusions(self, exclusion_spec: str) -> Set[str]:
        """
        Parse exclusion specification into a set of IP addresses.
        
        Same format as parse_targets.
        
        Args:
            exclusion_spec: Exclusion specification string
            
        Returns:
            Set of excluded IP addresses
        """
        exclusions = set()
        
        if not exclusion_spec:
            return exclusions
        
        # Split by comma
        parts = [part.strip() for part in exclusion_spec.split(',')]
        
        for part in parts:
            if not part:
                continue
            
            # Check if it's a CIDR notation
            if '/' in part:
                try:
                    ips = expand_cidr(part)
                    exclusions.update(ips)
                    logger.info(f"Expanded exclusion CIDR {part} to {len(ips)} hosts")
                except Exception as e:
                    logger.error(f"Error expanding exclusion CIDR {part}: {e}")
            
            # Check if it's a valid IP
            elif is_valid_ip(part):
                exclusions.add(part)
            
            # Assume it's a DNS name
            else:
                ip = resolve_dns(part)
                if ip:
                    exclusions.add(ip)
                    logger.info(f"Resolved exclusion {part} to {ip}")
                else:
                    logger.warning(f"Could not resolve exclusion {part}")
        
        self.excluded_ips = exclusions
        return exclusions
    
    def get_final_targets(self) -> Set[str]:
        """Get final target list after applying exclusions."""
        return self.resolved_targets - self.excluded_ips
    
    def has_dns_targets(self, target_spec: str) -> bool:
        """Check if target specification contains DNS names."""
        parts = [part.strip() for part in target_spec.split(',')]
        
        for part in parts:
            if not part:
                continue
            
            # Skip CIDR and IP addresses
            if '/' in part or is_valid_ip(part):
                continue
            
            # If it's not an IP and not a CIDR, assume it's DNS
            return True
        
        return False

