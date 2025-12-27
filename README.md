# Network-Enumeration-Tool

A comprehensive Python-based network enumeration tool that automates the discovery and documentation of network hosts, services, and vulnerabilities. This tool integrates multiple enumeration techniques and produces professional Markdown reports.

## Features

- **Flexible Target Specification**: Supports individual IPs, DNS hostnames, CIDR subnets, and comma-separated combinations
- **Host Exclusion**: Exclude out-of-scope hosts from enumeration
- **DNS Safety**: Confirmation prompt when DNS records are provided to prevent scope violations
- **Comprehensive Enumeration**:
  - Host discovery and availability verification
  - Operating system detection (Windows/Linux/Unix/Unknown)
  - Service discovery (ports, protocols, service names)
  - Windows-specific enumeration (SMB, NetBIOS, Active Directory)
- **Professional Reporting**: Generates detailed Markdown reports with verified and unverified information
- **Modular Design**: Object-oriented architecture with separate modules for each component

## Requirements

### Python Version
- **Python 3.12** (specifically version 3.12)

### External Tools
The following command-line tools must be installed and available in your PATH:

- **nmap** (required) - Network scanning and enumeration
- **enum4linux** (optional) - Windows SMB enumeration
- **smbclient** (optional) - SMB client for Windows enumeration
- **nmblookup** (optional) - NetBIOS name lookup
- **ldapsearch** (optional) - LDAP/Active Directory enumeration

### Installation of External Tools

#### Windows
```powershell
# Install nmap using Chocolatey
choco install nmap

# Or download from: https://nmap.org/download.html
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install nmap enum4linux smbclient samba-common-bin ldap-utils
```

#### macOS
```bash
brew install nmap
brew install enum4linux
```

## Installation

1. **Clone or download this repository**

2. **Create a Python 3.12 virtual environment**:
   ```bash
   python3.12 -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```powershell
     venv\Scripts\Activate.ps1
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Note: This project uses only Python standard library modules, so no additional Python packages are required.

5. **Verify nmap installation**:
   ```bash
   nmap --version
   ```

## Usage

### Basic Usage

```bash
# Enumerate a single host
python main.py 192.168.1.1

# Enumerate a subnet
python main.py 192.168.1.0/24

# Enumerate a DNS hostname
python main.py server.example.com

# Enumerate multiple targets
python main.py 192.168.1.1,192.168.1.2,192.168.1.3
```

### Advanced Usage

```bash
# Exclude specific hosts
python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254

# Custom output file
python main.py 192.168.1.1 -o ./reports/my_report.md

# Combined example
python main.py 10.0.0.0/16 --exclude 10.0.1.0/24,10.0.2.0/24 -o network_scan.md
```

### Command-Line Options

- `--help, -h`: Display comprehensive usage information
- `-o <path>, --output <path>`: Specify custom output file path
- `--exclude, -e`: Exclude hosts from enumeration (same format as targets)

### Target Specification Formats

The tool accepts targets in multiple formats:

- **Individual IPv4 addresses**: `192.168.1.1`
- **DNS hostnames**: `server.example.com`
- **CIDR notation**: `192.168.1.0/24`
- **Comma-separated lists**: `192.168.1.1,server.example.com,10.0.0.0/24`

## Output

The tool generates a Markdown report (`.md` file) in the current working directory with the default naming convention:

```
host_enumeration_report_YYYYMMDD_HHMM_UTC.md
```

The report includes:

1. **Verified Information Table**: IP address, hostname, domain, services, OS type, Windows-specific info
2. **Unverified Information Section**: Probable but unconfirmed details and potential vulnerabilities
3. **Command Outputs Section**: All commands executed with raw output in code blocks

## Project Structure

```
.
├── main.py              # Main entry point and CLI interface
├── models.py            # Data models (HostInfo, Service, etc.)
├── target_parser.py     # Target and exclusion parsing
├── dns_safety.py        # DNS safety checks and prompts
├── nmap_handler.py      # Nmap command execution
├── nmap_parser.py       # Nmap output parsing
├── windows_enum.py      # Windows-specific enumeration
├── report_builder.py    # Markdown report generation
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── USER_GUIDE.md        # Detailed user guide
├── contributions.md     # Individual contributions
├── limitations.md       # Known limitations and edge cases
└── samples/             # Sample output reports
```

## Important Notes

⚠️ **Authorization Required**: Only test against systems you own or have explicit written permission to test. Unauthorized scanning is illegal.

⚠️ **Scope Compliance**: Always verify your target scope before running enumeration. Use the DNS safety feature when enumerating DNS hostnames.

⚠️ **Detection**: Network enumeration activities may be detected by security systems. Ensure you have proper authorization.

## Testing

The tool has been tested against:
- Windows systems (various versions)
- Linux systems (Ubuntu, Debian, CentOS)
- Mixed network environments
- Various subnet sizes

See `samples/` directory for example output reports.

## Troubleshooting

### "nmap is not installed or not in PATH"
- Ensure nmap is installed and accessible from your command line
- Verify with: `nmap --version`
- Add nmap to your system PATH if needed

### "Could not resolve hostname"
- Check DNS configuration
- Verify hostname is correct
- Check network connectivity

### "Permission denied" errors
- Some scans require elevated privileges
- On Linux/macOS, you may need `sudo` for certain operations
- On Windows, run as Administrator if needed

## Contributing

This is a course project. See `contributions.md` for individual contributions.

## License

This project is for educational purposes as part of CSCI 4449/6658 Ethical Hacking course at University of New Haven.


## Acknowledgments

- University of New Haven - CSCI 4449/6658 Ethical Hacking
- Nmap Project (https://nmap.org)

