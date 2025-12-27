# User Guide - Network Enumeration Tool

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Target Specification](#target-specification)
4. [Exclusion Feature](#exclusion-feature)
5. [DNS Safety Feature](#dns-safety-feature)
6. [Output and Reports](#output-and-reports)
7. [Enumeration Process](#enumeration-process)
8. [Examples](#examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Introduction

The Network Enumeration Tool is a comprehensive Python-based tool designed to automate network reconnaissance and enumeration. It integrates multiple enumeration techniques learned throughout the Ethical Hacking course and produces professional Markdown reports.

## Getting Started

### Prerequisites

Before using the tool, ensure you have:

1. Python 3.12 installed
2. nmap installed and in your PATH
3. (Optional) Windows enumeration tools: enum4linux, smbclient, nmblookup, ldapsearch

### Running the Tool

Basic command structure:
```bash
python main.py [OPTIONS] <targets>
```

### Getting Help

To view comprehensive help information:
```bash
python main.py --help
```

## Target Specification

The tool accepts targets in multiple formats, allowing flexibility in how you specify what to enumerate.

### Individual IPv4 Addresses

```bash
python main.py 192.168.1.1
python main.py 10.0.0.5
```

### DNS Hostnames

```bash
python main.py server.example.com
python main.py www.google.com
```

**Note**: When DNS hostnames are provided, the DNS safety feature will prompt for confirmation.

### CIDR Notation (Subnets)

```bash
# Single subnet
python main.py 192.168.1.0/24

# Larger network
python main.py 10.0.0.0/16
```

### Comma-Separated Lists

You can combine any of the above formats:

```bash
# Multiple IPs
python main.py 192.168.1.1,192.168.1.2,192.168.1.3

# Mixed formats
python main.py server.example.com,192.168.1.0/24,10.0.0.5

# Complex example
python main.py 192.168.1.1,server.example.com,10.0.0.0/24,192.168.2.5
```

## Exclusion Feature

The exclusion feature allows you to exclude out-of-scope hosts that fall within your target specification.

### Use Cases

- Excluding gateway and broadcast addresses from subnet scans
- Excluding specific servers that are out of scope
- Excluding entire subnets from larger network scans

### Syntax

The exclusion format is identical to target specification:

```bash
# Exclude individual IPs
python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254

# Exclude DNS hosts
python main.py 192.168.1.0/24 --exclude gateway.example.com

# Exclude subnets
python main.py 10.0.0.0/16 --exclude 10.0.1.0/24,10.0.2.0/24

# Complex exclusion
python main.py 192.168.0.0/16 --exclude 192.168.1.0/24,192.168.2.1,server.example.com
```

### How It Works

1. The tool first parses and expands all targets
2. Then it parses and expands all exclusions
3. Finally, it removes excluded hosts from the target list
4. Enumeration proceeds only on the remaining hosts

## DNS Safety Feature

When DNS hostnames are included in your target specification, the tool implements a safety check to prevent accidental scope violations.

### What Happens

1. **DNS Server Display**: The tool displays your currently configured DNS server
2. **Confirmation Prompt**: You are prompted to confirm before proceeding
3. **Default Behavior**: If you press Enter without input, the default is "No" (cancellation)

### Example Interaction

```
======================================================================
DNS SAFETY CHECK
======================================================================
Target specification contains DNS records: server.example.com
Currently configured DNS server: 8.8.8.8

WARNING: DNS misconfiguration could lead to scope violations.
Please verify that the DNS server is correct before proceeding.
======================================================================

Proceed with enumeration? (y/N): 
```

### Why This Matters

DNS misconfiguration could cause:
- Resolving to wrong IP addresses
- Enumerating systems outside your authorized scope
- Legal and ethical violations

Always verify your DNS server configuration before proceeding.

## Output and Reports

### Default Output

By default, reports are saved in the current working directory with the naming convention:

```
host_enumeration_report_YYYYMMDD_HHMM_UTC.md
```

Example: `host_enumeration_report_20251117_143022_UTC.md`

### Custom Output Location

Use the `-o` or `--output` option to specify a custom path:

```bash
# Custom filename in current directory
python main.py 192.168.1.1 -o my_report.md

# Custom path
python main.py 192.168.1.1 -o ./reports/scan_2025.md

# Absolute path
python main.py 192.168.1.1 -o /tmp/enumeration_report.md
```

### Report Structure

Each report contains:

#### Header Section
- Enumeration start time (UTC)
- Total hosts enumerated

#### Table of Contents
- Links to each host section (for multi-host reports)

#### Host Sections
Each enumerated host has its own section with:

1. **Verified Information Table**
   - IP Address
   - Hostname (if discovered)
   - Domain (if domain-joined)
   - Active Services (port, protocol, service name)
   - Operating System Type
   - Windows-specific information (if applicable)

2. **Unverified Information Section**
   - Probable but unconfirmed details
   - Example: "OS Version is at least Windows Server 2008 R2"
   - Potential vulnerabilities based on service versions

3. **Command Outputs Section**
   - Each command executed in single-line code blocks
   - Raw output in multi-line code blocks
   - Includes all commands used to generate the report

#### Footer
- Enumeration end time (UTC)
- Total duration

## Enumeration Process

### General Host Enumeration

For every host, the tool performs:

1. **TCP Port Scan**: Quick scan with service version detection
2. **OS Detection**: Operating system fingerprinting
3. **Service Enumeration**: Identifies open ports, protocols, and services

### Windows-Specific Enumeration

When a Windows host is detected, additional enumeration includes:

1. **SMB Enumeration**: 
   - Share discovery
   - User enumeration
   - Domain/workgroup information
   - OS version details

2. **NetBIOS Enumeration**:
   - NetBIOS name resolution
   - Domain information
   - MAC address discovery

3. **Active Directory Enumeration** (if domain-joined):
   - LDAP queries
   - Domain information
   - Naming contexts

### Information Extraction

The tool uses regex patterns to extract actionable information from command outputs:

- OS type and version detection
- Service identification
- Port and protocol extraction
- Windows-specific details

## Examples

### Example 1: Single Host Enumeration

```bash
python main.py 192.168.1.100
```

This will:
- Scan 192.168.1.100
- Detect OS and services
- Perform Windows enumeration if Windows is detected
- Generate a report in the current directory

### Example 2: Subnet Scan with Exclusions

```bash
python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254
```

This will:
- Scan all hosts in 192.168.1.0/24 (254 hosts)
- Exclude the gateway (192.168.1.1) and broadcast (192.168.1.254)
- Enumerate remaining 252 hosts
- Generate a comprehensive report

### Example 3: Multiple Targets with Custom Output

```bash
python main.py server1.example.com,server2.example.com,192.168.1.5 -o ./reports/multi_host_scan.md
```

This will:
- Prompt for DNS confirmation (DNS safety feature)
- Enumerate three hosts
- Save report to custom location

### Example 4: Large Network with Multiple Exclusions

```bash
python main.py 10.0.0.0/16 --exclude 10.0.1.0/24,10.0.2.0/24,10.0.3.1 -o network_scan.md
```

This will:
- Scan 10.0.0.0/16 (65,534 hosts)
- Exclude three subnets and one specific IP
- Generate a large comprehensive report

## Best Practices

### 1. Scope Verification
- Always verify your target scope before enumeration
- Use exclusion feature for out-of-scope hosts
- Double-check DNS resolution when using hostnames

### 2. Performance Considerations
- Large subnet scans can take significant time
- Consider scanning during off-peak hours
- Use exclusions to reduce scan time

### 3. Documentation
- Save reports with descriptive names using `-o` option
- Organize reports in directories by date or project
- Review reports for accuracy

### 4. Security
- Only scan authorized targets
- Be aware that enumeration may be detected
- Follow responsible disclosure practices

### 5. Testing
- Test against your own lab environment first
- Verify tool functionality before production use
- Review sample reports in `samples/` directory

## Troubleshooting

### Issue: "nmap is not installed or not in PATH"

**Solution**:
- Install nmap for your operating system
- Verify installation: `nmap --version`
- Add nmap to system PATH if needed

### Issue: "Could not resolve hostname"

**Solution**:
- Check DNS configuration
- Verify hostname spelling
- Test DNS resolution manually: `nslookup hostname`
- Check network connectivity

### Issue: "Permission denied" errors

**Solution**:
- Some operations may require elevated privileges
- On Linux/macOS: Try `sudo python main.py ...`
- On Windows: Run as Administrator
- Note: Most scans don't require root/admin, but OS detection might

### Issue: Slow enumeration

**Solution**:
- Large networks take time - this is expected
- Consider scanning smaller subnets
- Use exclusions to reduce target count
- Check network connectivity and latency

### Issue: Missing Windows enumeration data

**Solution**:
- Ensure Windows enumeration tools are installed
- Check that SMB ports (445, 139) are accessible
- Verify firewall rules allow enumeration traffic
- Some Windows features require specific tools (enum4linux, smbclient)

### Issue: Report not generated

**Solution**:
- Check write permissions in output directory
- Verify disk space is available
- Check for error messages in console output
- Try specifying custom output path with `-o`

## Additional Resources

- See `README.md` for installation and setup
- See `limitations.md` for known limitations
- See `samples/` directory for example reports
- Contact instructor for course-specific questions

