"""
Nmap command execution handler.
"""
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class NmapHandler:
    """Handles execution of nmap commands."""
    
    @staticmethod
    def check_nmap_installed() -> bool:
        """Check if nmap is installed and available."""
        try:
            result = subprocess.run(
                ["nmap", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error checking nmap: {e}")
            return False
    
    @staticmethod
    def nmap_tcp_quick(target: str, ports: Optional[str] = None) -> tuple[str, int]:
        """
        Quick TCP scan with service version detection.
        
        Args:
            target: Target IP address
            ports: Port specification (e.g., "80,443" or "1-1000"), None for default
            
        Returns:
            Tuple of (output, return_code)
        """
        cmd = ["nmap", "-sV", "-sC", "-T4", "--open", "-Pn"]  # -Pn: Skip ping, assume host is up
        
        if ports:
            cmd.extend(["-p", ports])
        else:
            cmd.append("-F")  # Fast scan (top 100 ports)
        
        cmd.append(target)
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                errors='replace'
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Nmap scan timed out for {target}")
            return "Nmap scan timed out", -1
        except Exception as e:
            logger.error(f"Error running nmap: {e}")
            return str(e), -1
    
    @staticmethod
    def nmap_tcp_full(target: str) -> tuple[str, int]:
        """
        Full TCP port scan with service version detection.
        
        Args:
            target: Target IP address
            
        Returns:
            Tuple of (output, return_code)
        """
        cmd = ["nmap", "-sV", "-sC", "-p-", "-T4", "--open", "-Pn", target]  # -Pn: Skip ping
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800,  # 30 minutes for full scan
                errors='replace'
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Nmap full scan timed out for {target}")
            return "Nmap full scan timed out", -1
        except Exception as e:
            logger.error(f"Error running nmap full scan: {e}")
            return str(e), -1
    
    @staticmethod
    def nmap_udp(target: str, ports: Optional[str] = None) -> tuple[str, int]:
        """
        UDP port scan.
        
        Args:
            target: Target IP address
            ports: Port specification, None for common UDP ports
            
        Returns:
            Tuple of (output, return_code)
        """
        cmd = ["nmap", "-sU", "-T4", "--open", "-Pn"]  # -Pn: Skip ping
        
        if ports:
            cmd.extend(["-p", ports])
        else:
            cmd.append("--top-ports", "100")  # Top 100 UDP ports
        
        cmd.append(target)
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                errors='replace'
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Nmap UDP scan timed out for {target}")
            return "Nmap UDP scan timed out", -1
        except Exception as e:
            logger.error(f"Error running nmap UDP scan: {e}")
            return str(e), -1
    
    @staticmethod
    def nmap_os_detection(target: str) -> tuple[str, int]:
        """
        OS detection scan.
        
        Args:
            target: Target IP address
            
        Returns:
            Tuple of (output, return_code)
        """
        cmd = ["nmap", "-O", "--osscan-guess", "-T4", "-Pn", target]  # -Pn: Skip ping
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                errors='replace'
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            logger.error(f"Nmap OS detection timed out for {target}")
            return "Nmap OS detection timed out", -1
        except Exception as e:
            logger.error(f"Error running nmap OS detection: {e}")
            return str(e), -1

