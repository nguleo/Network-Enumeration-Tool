# Individual Contributions

This document outlines the contributions of each team member to the Network Enumeration Tool project.

## Project Overview

The Network Enumeration Tool is a comprehensive Python-based tool for network reconnaissance and enumeration, developed as the final project for CSCI 4449/6658 Ethical Hacking.

## Team Members

- **Student 1**: Leonel Mainsah Ngu, 00983692
- **Student 2**: Mantazedul Quaderi, 00862236

---

## Contribution Breakdown

### Core Architecture and Design

**Contributor**: Leonel Mainsah Ngu

- Designed overall modular architecture
- Created object-oriented class structure
- Implemented data models (`models.py`)
- Designed report structure and formatting

### Target Parsing and DNS Safety

**Contributor**: Leonel Mainsah Ngu

- Implemented `target_parser.py` for parsing IPs, DNS, CIDR, and comma-separated lists
- Developed exclusion feature logic
- Created `dns_safety.py` with DNS server detection and confirmation prompts
- Implemented DNS resolution and validation

### Nmap Integration

**Contributor**: Leonel Mainsah Ngu

- Developed `nmap_handler.py` with multiple scan types (TCP quick, TCP full, UDP, OS detection)
- Created `nmap_parser.py` with regex-based output parsing
- Implemented service extraction and OS detection from nmap output
- Added error handling and timeout management

### Windows Enumeration

**Contributor**: Leonel Mainsah Ngu

- Implemented `windows_enum.py` for Windows-specific enumeration
- Developed SMB enumeration integration
- Created NetBIOS enumeration functionality
- Implemented LDAP/Active Directory enumeration
- Built parsing functions for Windows-specific output

### Report Generation

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Developed `report_builder.py` for Markdown report generation
- Implemented UTC timestamp handling
- Created report structure with verified/unverified information sections
- Built command output formatting
- Implemented custom output path support

### CLI Interface and Main Logic

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Created `main.py` with comprehensive CLI argument parsing
- Implemented `--help` documentation
- Developed main enumeration workflow
- Integrated all modules into cohesive tool
- Added error handling and logging

### Utility Functions

**Contributor**: Leonel Mainsah Ngu 

- Implemented `utils.py` with helper functions
- Created DNS resolution utilities
- Developed regex patterns for information extraction
- Added command execution wrappers

### Documentation

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Wrote `README.md` with installation and usage instructions
- Created comprehensive `USER_GUIDE.md`
- Documented limitations in `limitations.md`
- Added inline code comments and docstrings
- Created sample reports

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Wrote `contributions.md` (this file)
- Created `requirements.txt`
- Added code documentation and comments
- Reviewed and edited documentation

### Testing and Validation

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Tested against Windows systems
- Tested against Linux systems
- Created sample reports in `samples/` directory
- Documented edge cases and limitations
- Performed integration testing

**Contributor**: Leonel Mainsah Ngu and Mantazedul Quaderi

- Tested target parsing with various formats
- Validated exclusion feature
- Tested DNS safety feature
- Performed error handling validation
- Tested report generation

---

## Code Statistics

### Lines of Code by Module

- `main.py`: ~200 lines
- `models.py`: ~150 lines
- `target_parser.py`: ~120 lines
- `dns_safety.py`: ~80 lines
- `nmap_handler.py`: ~150 lines
- `nmap_parser.py`: ~180 lines
- `windows_enum.py`: ~250 lines
- `report_builder.py`: ~150 lines
- `utils.py`: ~120 lines

**Total**: ~1,400 lines of Python code

### Documentation

- `README.md`: ~300 lines
- `USER_GUIDE.md`: ~500 lines
- `contributions.md`: ~150 lines
- `limitations.md`: ~100 lines
- Inline comments and docstrings: Throughout codebase

---

## Design Decisions

### Modular Architecture

**Decision**: Break tool into separate modules rather than monolithic file

**Rationale**: 
- Easier to maintain and test
- Follows object-oriented best practices
- Allows for individual component development
- Meets project requirements for modular design

**Contributors**: Both team members collaborated on architecture design

### Regex-Based Parsing

**Decision**: Use regex patterns to extract information from command outputs

**Rationale**:
- Required by project specifications
- Flexible and extensible
- Works with various command output formats
- Allows extraction of actionable information

**Contributors**: [Student Name] implemented parsing logic

### UTC Timestamps

**Decision**: Use UTC for all timestamps in reports

**Rationale**:
- Standard practice for network tools
- Avoids timezone confusion
- Required by project specifications
- Consistent across different systems

**Contributors**: [Student Name] implemented timestamp handling

---

## Challenges and Solutions

### Challenge 1: DNS Safety Implementation

**Problem**: Implementing cross-platform DNS server detection

**Solution**: Created platform-specific detection for Windows, Linux, and macOS

**Contributor**: [Student Name]

### Challenge 2: Windows Enumeration Tool Availability

**Problem**: Different systems have different Windows enumeration tools available

**Solution**: Implemented fallback mechanisms to try multiple tools

**Contributor**: [Student Name]

### Challenge 3: Large Network Performance

**Problem**: Scanning large networks can be very slow

**Solution**: Implemented efficient target parsing and exclusion, added progress logging

**Contributor**: [Student Name]

---

## Future Enhancements (Not Implemented)

The following features were considered but not implemented due to time constraints:

- Parallel host enumeration
- Resume functionality for interrupted scans
- JSON output format option
- Vulnerability database integration
- Web-based report viewer

---

## Notes

- All team members reviewed and tested the complete codebase
- Each member is prepared to discuss any part of the project
- Code follows PEP 8 style guidelines
- All external code snippets are properly cited

---



