"""
Data models for storing enumeration results.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Service:
    """Represents a discovered service."""
    name: str
    port: int
    protocol: str
    version: Optional[str] = None
    state: str = "open"


@dataclass
class CommandOutput:
    """Stores command and its raw output."""
    command: str
    output: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_markdown(self) -> str:
        """Convert command output to markdown format."""
        return f"Command: `{self.command}`\n\n```\n{self.output}\n```\n"


@dataclass
class HostInfo:
    """Stores all information about an enumerated host."""
    ip_address: str
    hostname: Optional[str] = None
    domain: Optional[str] = None
    os_type: Optional[str] = None  # Windows, Linux, Unix, Unknown
    os_version: Optional[str] = None
    services: List[Service] = field(default_factory=list)
    windows_info: Dict[str, str] = field(default_factory=dict)
    command_outputs: List[CommandOutput] = field(default_factory=list)
    unverified_info: List[str] = field(default_factory=list)
    is_windows: bool = False

    def add_service(self, service: Service):
        """Add a service to the host."""
        self.services.append(service)

    def add_command_output(self, command: str, output: str):
        """Add a command output."""
        self.command_outputs.append(CommandOutput(command, output))

    def add_unverified_info(self, info: str):
        """Add unverified information."""
        self.unverified_info.append(info)

    def get_verified_table_markdown(self) -> str:
        """Generate verified information table in markdown."""
        lines = [
            "| Field | Value |",
            "|-------|-------|"
        ]
        
        lines.append(f"| IP Address | {self.ip_address} |")
        
        if self.hostname:
            lines.append(f"| Hostname | {self.hostname} |")
        
        if self.domain:
            lines.append(f"| Domain | {self.domain} |")
        
        if self.os_type:
            lines.append(f"| Operating System Type | {self.os_type} |")
        
        if self.services:
            service_list = ", ".join([f"{s.name} ({s.port}/{s.protocol})" for s in self.services])
            lines.append(f"| Active Services | {service_list} |")
        
        if self.is_windows and self.windows_info:
            for key, value in self.windows_info.items():
                lines.append(f"| {key} | {value} |")
        
        return "\n".join(lines)

    def get_unverified_section_markdown(self) -> str:
        """Generate unverified information section in markdown."""
        if not self.unverified_info:
            return "No unverified information available."
        
        lines = []
        for info in self.unverified_info:
            lines.append(f"- {info}")
        
        return "\n".join(lines)

    def get_command_outputs_markdown(self) -> str:
        """Generate command outputs section in markdown."""
        if not self.command_outputs:
            return "No command outputs available."
        
        return "\n\n".join([cmd.to_markdown() for cmd in self.command_outputs])


@dataclass
class EnumerationResults:
    """Container for all enumeration results."""
    hosts: Dict[str, HostInfo] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)

    def add_host(self, host: HostInfo):
        """Add a host to results."""
        self.hosts[host.ip_address] = host

    def get_host(self, ip: str) -> Optional[HostInfo]:
        """Get host information by IP."""
        return self.hosts.get(ip)

