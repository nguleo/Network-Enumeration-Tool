"""
Generate Markdown reports from enumeration results.
"""
import os
from datetime import datetime
from typing import Optional

from models import EnumerationResults, HostInfo


class ReportBuilder:
    """Builds Markdown reports from enumeration results."""
    
    @staticmethod
    def generate_default_filename() -> str:
        """Generate default report filename with UTC timestamp."""
        now = datetime.utcnow()
        timestamp = now.strftime("%Y%m%d_%H%M_UTC")
        return f"host_enumeration_report_{timestamp}.md"
    
    @staticmethod
    def build_report(results: EnumerationResults, output_path: Optional[str] = None) -> str:
        """
        Build complete Markdown report.
        
        Args:
            results: EnumerationResults object
            output_path: Optional custom output path
            
        Returns:
            Path to generated report file
        """
        if output_path:
            filepath = output_path
        else:
            filename = ReportBuilder.generate_default_filename()
            # Save to current working directory
            filepath = os.path.join(os.getcwd(), filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        # Build report content
        content = ReportBuilder._build_report_content(results)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    @staticmethod
    def _build_report_content(results: EnumerationResults) -> str:
        """Build the Markdown content for the report."""
        lines = []
        
        # Header
        lines.append("# Host Enumeration Report")
        lines.append("")
        start_time_utc = results.start_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        lines.append(f"**Enumeration Start Time:** {start_time_utc}")
        lines.append(f"**Total Hosts Enumerated:** {len(results.hosts)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Table of Contents
        if len(results.hosts) > 1:
            lines.append("## Table of Contents")
            lines.append("")
            for i, (ip, host) in enumerate(results.hosts.items(), 1):
                hostname_str = f" ({host.hostname})" if host.hostname else ""
                lines.append(f"{i}. [{ip}{hostname_str}](#host-{i}-{ip.replace('.', '-')})")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Host sections
        for i, (ip, host) in enumerate(results.hosts.items(), 1):
            lines.append(ReportBuilder._build_host_section(host, i))
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Footer
        end_time = datetime.utcnow()
        end_time_utc = end_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        duration = end_time - results.start_time
        lines.append("## Report Summary")
        lines.append("")
        lines.append(f"**Enumeration End Time:** {end_time_utc}")
        lines.append(f"**Total Duration:** {duration}")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def _build_host_section(host: HostInfo, host_number: int) -> str:
        """Build Markdown section for a single host."""
        lines = []
        
        # Section header
        hostname_str = f" ({host.hostname})" if host.hostname else ""
        lines.append(f"## Host {host_number}: {host.ip_address}{hostname_str}")
        lines.append("")
        
        # Verified Information Table
        lines.append("### Verified Information")
        lines.append("")
        lines.append(host.get_verified_table_markdown())
        lines.append("")
        
        # Unverified Information
        lines.append("### Unverified Information")
        lines.append("")
        lines.append(host.get_unverified_section_markdown())
        lines.append("")
        
        # Command Outputs
        lines.append("### Command Outputs")
        lines.append("")
        lines.append(host.get_command_outputs_markdown())
        lines.append("")
        
        return "\n".join(lines)

