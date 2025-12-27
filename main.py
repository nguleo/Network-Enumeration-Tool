#!/usr/bin/env python3
"""
Network Enumeration Tool - Final Project
CSCI 4449/6658 Ethical Hacking - Fall 2025

A comprehensive network enumeration tool that automates discovery and
documentation of network hosts, services, and vulnerabilities.
"""
import argparse
import sys
import logging
from typing import Set

from target_parser import TargetParser
from dns_safety import DNSSafety
from nmap_handler import NmapHandler
from nmap_parser import NmapParser
from windows_enum import WindowsEnumeration
from report_builder import ReportBuilder
from models import EnumerationResults, HostInfo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_help():
    """Print comprehensive help information."""
    help_text = """
Network Enumeration Tool - Comprehensive Usage Guide
====================================================

SYNOPSIS
    python main.py [OPTIONS] <targets>

DESCRIPTION
    This tool performs comprehensive network enumeration including host discovery,
    service enumeration, OS detection, and Windows-specific enumeration when applicable.
    Results are output in a professional Markdown report.

TARGET SPECIFICATION
    The tool accepts targets in multiple formats:
    
    • Individual IPv4 addresses:
        python main.py (e.g 192.168.1.1)
        python main.py (e.g 10.0.0.5)
    
    • DNS hostnames:
        python main.py (e.gserver.example.com)
        python main.py (e.g www.google.com)
    
    • CIDR notation (subnets):
        python main.py 192.168.1.0/24
        python main.py 10.0.0.0/16
    
    • Comma-separated lists (any combination):
        python main.py 192.168.1.1,192.168.1.2,192.168.1.3
        python main.py server.example.com,192.168.1.0/24,10.0.0.5
        python main.py 192.168.1.1-10,example.com,10.0.0.0/24

EXCLUSION SPECIFICATION
    Use --exclude to specify hosts that should be excluded from enumeration:
    
    • Exclude individual IPs:
        python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254
    
    • Exclude DNS hosts:
        python main.py 192.168.1.0/24 --exclude gateway.example.com
    
    • Exclude subnets:
        python main.py 10.0.0.0/16 --exclude 10.0.1.0/24

REQUIRED OPTIONS
    --help, -h
        Display this help message and exit.

    -o <path>, --output <path>
        Specify custom output file path and name.
        Default: host_enumeration_report_YYYYMMDD_HHMM_UTC.md in current directory
        
        Examples:
            python main.py 192.168.1.1 -o ./reports/my_report.md
            python main.py 192.168.1.0/24 -o /tmp/enum_report.md

DNS SAFETY FEATURE
    When DNS records are provided in the target specification, the tool will:
    1. Display the currently configured DNS server
    2. Prompt for confirmation before proceeding (y/N)
    3. Default to "No" if no input is provided
    
    This prevents accidental scope violations due to DNS misconfiguration.

ENUMERATION CAPABILITIES
    The tool performs the following enumeration:
    
    General Host Enumeration:
    • Host discovery and availability verification
    • Operating system detection (Windows/Linux/Unix/Unknown)
    • Service discovery (ports, protocols, service names)
    • Network topology mapping
    
    Windows-Specific Enumeration (when Windows host detected):
    • SMB enumeration (shares, users, domain information)
    • NetBIOS enumeration
    • Active Directory information gathering (if domain-joined)
    • Windows-specific service enumeration

OUTPUT FORMAT
    The tool generates a Markdown report (.md) containing:
    
    For each host:
    1. Verified Information Table
       - IP Address
       - Hostname
       - Domain (if applicable)
       - Active Services
       - Operating System Type
       - Windows-specific information (if applicable)
    
    2. Unverified Information Section
       - Probable but unconfirmed details
       - Potential vulnerabilities based on service versions
    
    3. Command Outputs Section
       - Each command executed with raw output
       - Formatted in code blocks for readability

EXAMPLES
    # Enumerate a single host
    python main.py 192.168.1.1
    
    # Enumerate a subnet with exclusions
    python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254
    
    # Enumerate multiple targets with custom output
    python main.py server1.example.com,server2.example.com,192.168.1.5 -o ./report.md
    
    # Enumerate a DNS hostname (will prompt for DNS confirmation)
    python main.py www.example.com
    
    # Enumerate large network with exclusions
    python main.py 10.0.0.0/16 --exclude 10.0.1.0/24,10.0.2.0/24 -o network_scan.md

REQUIREMENTS
    • Python 3.12
    • nmap (must be installed and in PATH)
    • Optional: enum4linux, smbclient, nmblookup, ldapsearch (for Windows enumeration)

NOTES
    • Only test against authorized targets
    • Never run this tool against systems you don't own or have explicit permission to test
    • Some enumeration techniques may be detected by security systems
    • Full port scans can take significant time for large networks
    • Review generated reports carefully for sensitive information
    • Use responsibly and ethically

FOR MORE INFORMATION
    Refer to the project documentation or contact the author.

"""
    print(help_text)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Network Enumeration Tool - Comprehensive host and service enumeration',
        add_help=False  # We'll handle --help manually for better formatting
    )
    
    parser.add_argument(
        'targets',
        nargs='?',
        help='Target specification (IPs, DNS, CIDR, or comma-separated list)'
    )
    
    parser.add_argument(
        '--exclude',
        '-e',
        type=str,
        default='',
        help='Exclude hosts from enumeration (same format as targets)'
    )
    
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=None,
        help='Custom output file path (default: host_enumeration_report_YYYYMMDD_HHMM_UTC.md)'
    )
    
    parser.add_argument(
        '--help',
        '-h',
        action='store_true',
        help='Show comprehensive help message'
    )
    
    return parser.parse_args()


def enumerate_host(target_ip: str, results: EnumerationResults) -> HostInfo:
    """
    Enumerate a single host.
    
    Args:
        target_ip: IP address to enumerate
        results: EnumerationResults object to store results
        
    Returns:
        HostInfo object
    """
    logger.info(f"Starting enumeration of {target_ip}")
    
    # Check if nmap is available
    if not NmapHandler.check_nmap_installed():
        logger.error("nmap is not installed or not in PATH")
        raise RuntimeError("nmap is required but not found")
    
    # Perform TCP scan with service detection
    nmap_output, _ = NmapHandler.nmap_tcp_quick(target_ip)
    
    # Parse nmap output
    host_info = NmapParser.parse_nmap_output(nmap_output, f"nmap -sV -sC -F {target_ip}")
    
    if not host_info:
        # Create minimal host info if parsing fails
        host_info = HostInfo(ip_address=target_ip)
        host_info.add_command_output(f"nmap -sV -sC -F {target_ip}", nmap_output)
    
    # Perform OS detection
    os_output, _ = NmapHandler.nmap_os_detection(target_ip)
    host_info.add_command_output(f"nmap -O --osscan-guess {target_ip}", os_output)
    
    # Update OS info from OS detection scan
    os_type, os_version, unverified = NmapParser.parse_os_info(os_output)
    if os_type:
        host_info.os_type = os_type
        if os_version:
            host_info.os_version = os_version
        host_info.is_windows = (os_type == "Windows")
    
    for info in unverified:
        host_info.add_unverified_info(info)
    
    # Windows-specific enumeration
    if host_info.is_windows:
        logger.info(f"Windows host detected, performing Windows-specific enumeration")
        host_info = WindowsEnumeration.enumerate_windows_host(target_ip, host_info)
    
    # Add to results
    results.add_host(host_info)
    
    return host_info


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Handle --help
    if args.help or not args.targets:
        print_help()
        sys.exit(0)
    
    # Parse targets
    parser = TargetParser()
    targets = parser.parse_targets(args.targets)
    
    if not targets:
        logger.error("No valid targets found")
        print("Error: No valid targets could be parsed from the specification.")
        sys.exit(1)
    
    # Check for DNS targets and prompt if needed
    if parser.has_dns_targets(args.targets):
        if not DNSSafety.prompt_confirmation(args.targets):
            print("Enumeration cancelled by user.")
            sys.exit(0)
    
    # Parse exclusions
    excluded = set()
    if args.exclude:
        excluded = parser.parse_exclusions(args.exclude)
        targets = targets - excluded
        logger.info(f"Excluded {len(excluded)} hosts")
    
    if not targets:
        logger.error("No targets remaining after exclusions")
        print("Error: All targets were excluded.")
        sys.exit(1)
    
    logger.info(f"Starting enumeration of {len(targets)} target(s)")
    
    # Initialize results
    results = EnumerationResults()
    
    # Enumerate each target
    for target_ip in sorted(targets):
        try:
            enumerate_host(target_ip, results)
            logger.info(f"Completed enumeration of {target_ip}")
        except Exception as e:
            logger.error(f"Error enumerating {target_ip}: {e}")
            # Create error entry
            error_host = HostInfo(ip_address=target_ip)
            error_host.add_unverified_info(f"Enumeration error: {str(e)}")
            results.add_host(error_host)
    
    # Generate report
    try:
        report_path = ReportBuilder.build_report(results, args.output)
        print(f"\nEnumeration complete! Report saved to: {report_path}")
        print(f"Total hosts enumerated: {len(results.hosts)}")
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        print(f"Error generating report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

