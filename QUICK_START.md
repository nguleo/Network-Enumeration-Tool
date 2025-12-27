# Quick Start Guide

## Installation (5 minutes)

1. **Install Python 3.12** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version` should show 3.12.x

2. **Install nmap**
   - Windows: `choco install nmap` or download from https://nmap.org
   - Linux: `sudo apt-get install nmap`
   - macOS: `brew install nmap`
   - Verify: `nmap --version`

3. **Set up virtual environment**
   ```bash
   python3.12 -m venv venv
   venv\Scripts\Activate.ps1  # Windows PowerShell
   # OR
   source venv/bin/activate   # Linux/macOS
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

```bash
# Enumerate a single host
python main.py 192.168.1.1

# View help
python main.py --help

# Enumerate subnet with exclusions
python main.py 192.168.1.0/24 --exclude 192.168.1.1,192.168.1.254

# Custom output file
python main.py 192.168.1.1 -o my_report.md
```

## What You Get

A Markdown report (`host_enumeration_report_YYYYMMDD_HHMM_UTC.md`) containing:
- Verified information (IP, hostname, services, OS)
- Unverified information (probable details)
- Raw command outputs

## Next Steps

- Read `README.md` for detailed installation
- Read `USER_GUIDE.md` for comprehensive usage
- Check `samples/` for example reports
- Review `limitations.md` for known issues

## Troubleshooting

**"nmap not found"**: Install nmap and ensure it's in PATH

**"Permission denied"**: Some scans may need sudo/Administrator

**"DNS resolution failed"**: Check network connectivity and DNS config

## Important

⚠️ **Only scan authorized targets!** Unauthorized scanning is illegal.

