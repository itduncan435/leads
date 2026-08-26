#!/usr/bin/env python3
"""
Security Suite Integration Module
Merges AllHackingTools and SpyHunt into the main AIO V18.0 application.
"""

import os
import sys
import subprocess
import platform
import time
import json
import random
import string
import socket
import requests
import urllib.parse
import threading
import queue
import re
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Callable

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt
    from rich import box
    from rich.align import Align
    from rich.style import Style
    from rich.markup import escape
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Base directories
BANK_DIR = Path(__file__).resolve().parent.parent
ALLHACKING_DIR = BANK_DIR / "AllHackingTools"
SPYHUNT_DIR = BANK_DIR / "spyhunt-main"


class SecuritySuiteUI:
    """UI handler for Security Suite menus."""
    
    def __init__(self):
        self.width = 80
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None
    
    def _refresh_terminal_size(self):
        try:
            self.width = os.get_terminal_size().columns
        except Exception:
            self.width = 80
    
    def clear(self):
        os.system("clear" if platform.system() != "Windows" else "cls")
    
    def print_header(self, title: str = "SECURITY SUITE"):
        self.clear()
        if RICH_AVAILABLE:
            self._refresh_terminal_size()
            header = Panel(
                Align.center(Text(f"[bold bright_red]{title}[/bold bright_red]\n[dim]AllHackingTools + SpyHunt Integration[/dim]")),
                border_style="bright_red",
                padding=(0, 2),
                expand=False,
            )
            self.console.print(header)
            self.console.print()
        else:
            print("=" * self.width)
            print(f"  {title}")
            print("  AllHackingTools + SpyHunt Integration")
            print("=" * self.width)
            print()
    
    def print_menu(self, items: List[Tuple[str, str, str]], title: str = "MENU"):
        if RICH_AVAILABLE:
            self._refresh_terminal_size()
            table = Table(
                show_header=True,
                header_style="bold bright_yellow",
                box=box.HEAVY,
                border_style="bright_yellow",
                show_lines=True,
                padding=(0, 1),
                title=f"[bold bright_yellow]{title}[/bold bright_yellow]",
                title_style="bold bright_yellow",
            )
            table.add_column("OPT", style="bold bright_cyan", width=6, justify="center")
            table.add_column("TOOL", style="bold white")
            table.add_column("DESCRIPTION", style="dim green", max_width=50)
            
            for opt, tool, desc in items:
                table.add_row(opt, tool, desc)
            
            self.console.print(table)
            self.console.print()
        else:
            print(f"\n{title}")
            print("-" * self.width)
            for opt, tool, desc in items:
                print(f"  [{opt:>3}] {tool:<30} {desc}")
            print()
    
    def prompt_choice(self, prompt_text: str = "Select option", choices: Optional[List[str]] = None) -> str:
        if RICH_AVAILABLE:
            if choices:
                return Prompt.ask(f"[bold bright_green]{prompt_text}[/bold bright_green]", choices=choices, default=choices[0] if choices else "0", show_choices=False)
            return Prompt.ask(f"[bold bright_green]{prompt_text}[/bold bright_green]", default="0")
        else:
            return input(f"{prompt_text}: ").strip()
    
    def print_success(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_green][OK] {escape(message)}[/bold bright_green]")
        else:
            print(f"[OK] {message}")
    
    def print_error(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_red][ERROR] {escape(message)}[/bold bright_red]")
        else:
            print(f"[ERROR] {message}")
    
    def print_info(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_cyan][INFO] {escape(message)}[/bold bright_cyan]")
        else:
            print(f"[INFO] {message}")
    
    def print_warning(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_yellow][WARN] {escape(message)}[/bold bright_yellow]")
        else:
            print(f"[WARN] {message}")


class ToolLauncher:
    """Launches external tools safely."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.ui = SecuritySuiteUI()
    
    def _run_command(self, cmd: str, cwd: Optional[Path] = None, capture: bool = False) -> Tuple[int, str, str]:
        """Run a shell command safely."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(cwd or self.base_dir),
                capture_output=capture,
                text=True,
                timeout=300,
            )
            return result.returncode, result.stdout or "", result.stderr or ""
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def launch_script(self, script_path: Path, args: str = "", cwd: Optional[Path] = None) -> bool:
        """Launch a bash/python script."""
        if not script_path.exists():
            self.ui.print_error(f"Tool not found: {script_path}")
            return False
        
        self.ui.print_info(f"Launching: {script_path.name}")
        cmd = f"{script_path} {args}".strip()
        try:
            if platform.system() == "Windows":
                subprocess.Popen(cmd, cwd=str(cwd or self.base_dir), creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd, shell=True, cwd=str(cwd or self.base_dir))
            return True
        except Exception as e:
            self.ui.print_error(f"Failed to launch: {e}")
            return False
    
    def run_python_module(self, module_path: Path, func_name: str = "main", *args, **kwargs) -> Any:
        """Import and run a Python module function."""
        if not module_path.exists():
            self.ui.print_error(f"Module not found: {module_path}")
            return None
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, func_name):
                return getattr(mod, func_name)(*args, **kwargs)
            else:
                self.ui.print_error(f"Function {func_name} not found in {module_path.name}")
                return None
        except Exception as e:
            self.ui.print_error(f"Module execution failed: {e}")
            return None


class AllHackingToolsSuite:
    """AllHackingTools integration."""
    
    CATEGORIES = {
        "1": ("IP Hacking", "IpHack.py"),
        "2": ("Router Hacking", "RouterMenu.py"),
        "3": ("Mail Hacking", "MailMenu.py"),
        "4": ("Web Hacking", "WebMenu.py"),
        "5": ("Cam Hacking", "CamHackMenu.py"),
        "6": ("Android Hacking", "AndroidMenu.py"),
        "7": ("SQL Injection", "SQLinjectionMenu.py"),
        "8": ("Social Engineering", "SocialMenu.py"),
        "9": ("Spam Tools", "SpamMenu.py"),
        "10": ("Analytics", "AnalistickMenu.py"),
        "11": ("Dark Search", "DarkSearchMenu.py"),
        "12": ("Phishing", "PhishingMenu.py"),
        "13": ("Password Tools", "PassworldMenu.py"),
        "14": ("Wordlist Generator", "WordlistGeneratorMenu.py"),
        "15": ("XSS Attacks", "XSSAttackMenu.py"),
        "16": ("Discord Tools", "discordMenu.py"),
        "17": ("Telegram Tools", "telegramMenu.py"),
        "18": ("Other Tools", "Other.py"),
        "19": ("Termux Tools", "TermuxS.py"),
    }
    
    def __init__(self):
        self.ui = SecuritySuiteUI()
        self.launcher = ToolLauncher(ALLHACKING_DIR)
    
    def show_menu(self) -> None:
        self.ui.print_header("ALLHACKINGTOOLS SUITE")
        items = [
            (k, v[0], f"AllHackingTools - {v[0]} module") 
            for k, v in self.CATEGORIES.items()
        ]
        items.append(("0", "BACK", "Return to main menu"))
        self.ui.print_menu(items, "ALLHACKINGTOOLS CATEGORIES")
        
        choice = self.ui.prompt_choice("Select category", [k for k, _ in items])
        if choice == "0":
            return
        
        if choice in self.CATEGORIES:
            _, script_name = self.CATEGORIES[choice]
            script_path = ALLHACKING_DIR / "Files" / script_name
            self.launcher.launch_script(script_path, "", cwd=ALLHACKING_DIR)
            input("\nPress Enter to continue...")
        else:
            self.ui.print_error("Invalid option")
            time.sleep(1)


class SpyHuntSuite:
    """SpyHunt security scanner integration."""
    
    def __init__(self):
        self.ui = SecuritySuiteUI()
        self.launcher = ToolLauncher(SPYHUNT_DIR)
    
    def show_menu(self) -> None:
        self.ui.print_header("SPYHUNT SECURITY SUITE")
        items = [
            ("1", "Target Intelligence", "Domain/URL analysis and pentest suggestions"),
            ("2", "Subdomain Enumeration", "Discover subdomains with multiple tools"),
            ("3", "Port Scanning", "Nmap-based port and service scanning"),
            ("4", "Web Vulnerability Scan", "Comprehensive web app vulnerability scanner"),
            ("5", "JWT Analyzer", "JSON Web Token security analysis"),
            ("6", "S3 Security Scanner", "AWS S3 bucket misconfiguration scanner"),
            ("7", "SSL/TLS Analyzer", "SSL certificate and configuration analysis"),
            ("8", "Heap Dump Analyzer", "Java heap dump security analysis"),
            ("9", "Advanced Scanners", "XXE, SSRF, SSTI, NoSQL, CRLF scanners"),
            ("10", "Wayback Machine", "Historical URL and endpoint discovery"),
            ("11", "Shodan Search", "Shodan IoT/exposed service search"),
            ("12", "Certificate Transparency", "CT log search for domains"),
            ("13", "Asset Finder", "Domain asset discovery tool"),
            ("14", "Path Hunter", "Directory and file path enumeration"),
            ("15", "WAF Detector", "Web Application Firewall detection"),
            ("16", "Smuggler", "HTTP request smuggling detector"),
            ("17", "F5 BigIP Scanner", "F5 BigIP vulnerability scanner"),
            ("0", "BACK", "Return to main menu"),
        ]
        self.ui.print_menu(items, "SPYHUNT SECURITY TOOLS")
        
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in items])
        if choice == "0":
            return
        
        self._run_spyhunt_tool(choice)
    
    def _run_spyhunt_tool(self, choice: str) -> None:
        """Execute selected SpyHunt tool."""
        try:
            if choice == "1":
                self._run_target_intel()
            elif choice == "2":
                self._run_subdomain_enum()
            elif choice == "3":
                self._run_port_scan()
            elif choice == "4":
                self._run_web_vuln_scan()
            elif choice == "5":
                self._run_jwt_analyzer()
            elif choice == "6":
                self._run_s3_scanner()
            elif choice == "7":
                self._run_ssl_analyzer()
            elif choice == "8":
                self._run_heap_dump()
            elif choice == "9":
                self._run_advanced_scanners()
            elif choice == "10":
                self._run_wayback()
            elif choice == "11":
                self._run_shodan_search()
            elif choice == "12":
                self._run_cert_search()
            elif choice == "13":
                self._run_assetfinder()
            elif choice == "14":
                self._run_pathhunt()
            elif choice == "15":
                self._run_waf_detector()
            elif choice == "16":
                self._run_smuggler()
            elif choice == "17":
                self._run_f5_scanner()
            else:
                self.ui.print_error("Invalid option")
                time.sleep(1)
        except Exception as e:
            self.ui.print_error(f"Tool execution failed: {e}")
            input("\nPress Enter to continue...")
    
    def _get_target(self) -> Optional[str]:
        """Get target URL/IP from user."""
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            target = Prompt.ask("[bold bright_green]Enter target URL/IP[/bold bright_green]", default="")
        else:
            target = input("Enter target URL/IP: ").strip()
        return target if target else None
    
    def _run_target_intel(self) -> None:
        self.ui.print_info("Starting Target Intelligence scan...")
        target = self._get_target()
        if not target:
            return
        self.ui.print_info(f"Analyzing: {target}")
        try:
            from spyhunt_main.modules.target_intel import analyze_target
            result = analyze_target(target)
            self.ui.print_success("Analysis complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(result), title="Target Intel", border_style="green"))
            else:
                print(result)
        except ImportError:
            self.ui.print_warning("Direct module import not available, launching SpyHunt CLI...")
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--target-intel {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_subdomain_enum(self) -> None:
        self.ui.print_info("Starting Subdomain Enumeration...")
        target = self._get_target()
        if not target:
            return
        self.ui.print_info(f"Enumerating subdomains for: {target}")
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.subdomain_enum import SubdomainEnumerator
            enum = SubdomainEnumerator(target)
            results = enum.enumerate()
            self.ui.print_success(f"Found {len(results)} subdomains")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel("\n".join(results[:20]), title=f"Subdomains ({len(results)})", border_style="green"))
            else:
                for sub in results[:20]:
                    print(sub)
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--subdomains {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_port_scan(self) -> None:
        self.ui.print_info("Starting Port Scan...")
        target = self._get_target()
        if not target:
            return
        self.ui.print_info(f"Scanning ports on: {target}")
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.port_scanner import PortScanner
            scanner = PortScanner(target)
            results = scanner.scan()
            self.ui.print_success("Port scan complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="Port Scan Results", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--ports {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_web_vuln_scan(self) -> None:
        self.ui.print_info("Starting Web Vulnerability Scan...")
        target = self._get_target()
        if not target:
            return
        self.ui.print_info(f"Scanning vulnerabilities for: {target}")
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.web_scanner import WebScanner
            scanner = WebScanner(target)
            results = scanner.scan()
            self.ui.print_success("Vulnerability scan complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="Vulnerability Results", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--web-scan {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_jwt_analyzer(self) -> None:
        self.ui.print_info("Starting JWT Analyzer...")
        token = ""
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            token = Prompt.ask("[bold bright_green]Enter JWT token[/bold bright_green]", default="")
        else:
            token = input("Enter JWT token: ").strip()
        if not token:
            self.ui.print_error("No token provided")
            return
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.jwt_analyzer import JWTAnalyzer
            analyzer = JWTAnalyzer(token)
            results = analyzer.analyze()
            self.ui.print_success("JWT analysis complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="JWT Analysis", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.ui.print_warning("JWT analyzer module not available")
        input("\nPress Enter to continue...")
    
    def _run_s3_scanner(self) -> None:
        self.ui.print_info("Starting S3 Security Scanner...")
        target = self._get_target()
        if not target:
            return
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.ss3sec import S3Scanner
            scanner = S3Scanner(target)
            results = scanner.scan()
            self.ui.print_success("S3 scan complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="S3 Security Results", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--s3-scan {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_ssl_analyzer(self) -> None:
        self.ui.print_info("Starting SSL/TLS Analyzer...")
        target = self._get_target()
        if not target:
            return
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.ssl_sec import SSLAnalyzer
            analyzer = SSLAnalyzer(target)
            results = analyzer.analyze()
            self.ui.print_success("SSL analysis complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="SSL/TLS Analysis", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--ssl {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_heap_dump(self) -> None:
        self.ui.print_info("Starting Heap Dump Analyzer...")
        dump_path = ""
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            dump_path = Prompt.ask("[bold bright_green]Enter heap dump file path[/bold bright_green]", default="")
        else:
            dump_path = input("Enter heap dump file path: ").strip()
        if not dump_path or not os.path.exists(dump_path):
            self.ui.print_error("Invalid file path")
            return
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.heap_dump import HeapdumpAnalyzer
            analyzer = HeapdumpAnalyzer(dump_path)
            results = analyzer.analyze()
            self.ui.print_success("Heap dump analysis complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(results), title="Heap Dump Analysis", border_style="green"))
            else:
                print(results)
        except ImportError:
            self.ui.print_warning("Heap dump analyzer module not available")
        input("\nPress Enter to continue...")
    
    def _run_advanced_scanners(self) -> None:
        self.ui.print_info("Starting Advanced Vulnerability Scanners...")
        target = self._get_target()
        if not target:
            return
        scanners = ["XXE", "SSRF", "SSTI", "NoSQL Injection", "CRLF"]
        self.ui.print_info(f"Running scanners for: {target}")
        try:
            sys.path.insert(0, str(SPYHUNT_DIR))
            from modules.advanced_scanners import (
                XXEScanner, SSRFScanner, SSTIScanner, NoSQLInjectionScanner, CRLFScanner
            )
            results = {}
            for scanner_class, name in [
                (XXEScanner, "XXE"),
                (SSRFScanner, "SSRF"),
                (SSTIScanner, "SSTI"),
                (NoSQLInjectionScanner, "NoSQLi"),
                (CRLFScanner, "CRLF"),
            ]:
                try:
                    scanner = scanner_class(target)
                    results[name] = scanner.scan()
                except Exception as e:
                    results[name] = f"Scan failed: {e}"
            self.ui.print_success("Advanced scanning complete")
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(json.dumps(results, indent=2), title="Advanced Scan Results", border_style="green"))
            else:
                print(json.dumps(results, indent=2))
        except ImportError:
            self.launcher.launch_script(SPYHUNT_DIR / "spyhunt.py", f"--advanced-scan {target}", cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_wayback(self) -> None:
        self.ui.print_info("Starting Wayback Machine lookup...")
        target = self._get_target()
        if not target:
            return
        try:
            self.launcher.run_python_module(
                SPYHUNT_DIR / "scripts" / "waybackmachina.py",
                "main", target
            )
        except Exception as e:
            self.ui.print_error(f"Wayback lookup failed: {e}")
        input("\nPress Enter to continue...")
    
    def _run_shodan_search(self) -> None:
        self.ui.print_info("Starting Shodan Search...")
        query = ""
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            query = Prompt.ask("[bold bright_green]Enter Shodan search query[/bold bright_green]", default="")
        else:
            query = input("Enter Shodan search query: ").strip()
        if not query:
            self.ui.print_error("No query provided")
            return
        self.launcher.launch_script(SPYHUNT_DIR / "scripts" / "shodanscan.sh", query, cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_cert_search(self) -> None:
        self.ui.print_info("Starting Certificate Transparency search...")
        target = self._get_target()
        if not target:
            return
        self.launcher.launch_script(SPYHUNT_DIR / "scripts" / "certsh.sh", target, cwd=SPYHUNT_DIR)
        input("\nPress Enter to continue...")
    
    def _run_assetfinder(self) -> None:
        self.ui.print_info("Starting Asset Finder...")
        target = self._get_target()
        if not target:
            return
        assetfinder_path = SPYHUNT_DIR / "tools" / "assetfinder"
        if assetfinder_path.exists():
            self.launcher.launch_script(assetfinder_path, target, cwd=SPYHUNT_DIR)
        else:
            self.ui.print_warning("Assetfinder not found. Install it first.")
        input("\nPress Enter to continue...")
    
    def _run_pathhunt(self) -> None:
        self.ui.print_info("Starting Path Hunter...")
        target = self._get_target()
        if not target:
            return
        try:
            self.launcher.run_python_module(SPYHUNT_DIR / "tools" / "pathhunt.py", "main", target)
        except Exception as e:
            self.ui.print_error(f"Path hunter failed: {e}")
        input("\nPress Enter to continue...")
    
    def _run_waf_detector(self) -> None:
        self.ui.print_info("Starting WAF Detector...")
        target = self._get_target()
        if not target:
            return
        waf_path = SPYHUNT_DIR / "tools" / "whatwaf"
        if waf_path.exists():
            self.launcher.launch_script(waf_path / "whatwaf.py", f"--url {target}", cwd=waf_path)
        else:
            self.ui.print_warning("WhatWaf not found.")
        input("\nPress Enter to continue...")
    
    def _run_smuggler(self) -> None:
        self.ui.print_info("Starting HTTP Smuggler...")
        target = self._get_target()
        if not target:
            return
        smuggler_path = SPYHUNT_DIR / "tools" / "smuggler"
        if smuggler_path.exists():
            self.launcher.launch_script(smuggler_path / "smuggler.py", f"-u {target}", cwd=smuggler_path)
        else:
            self.ui.print_warning("Smuggler not found.")
        input("\nPress Enter to continue...")
    
    def _run_f5_scanner(self) -> None:
        self.ui.print_info("Starting F5 BigIP Scanner...")
        target = self._get_target()
        if not target:
            return
        try:
            self.launcher.run_python_module(SPYHUNT_DIR / "tools" / "f5bigip_scanner.py", "main", target)
        except Exception as e:
            self.ui.print_error(f"F5 scanner failed: {e}")
        input("\nPress Enter to continue...")


class QuickReconSuite:
    """Quick reconnaissance tools."""
    
    def __init__(self):
        self.ui = SecuritySuiteUI()
    
    def show_menu(self) -> None:
        self.ui.print_header("QUICK RECON SUITE")
        items = [
            ("1", "DNS Lookup", "Resolve DNS records for a domain"),
            ("2", "WHOIS Lookup", "WHOIS information for domain/IP"),
            ("3", "IP Geolocation", "Geolocate an IP address"),
            ("4", "Port Scanner", "Basic TCP port scanner"),
            ("5", "HTTP Headers", "Analyze HTTP response headers"),
            ("6", "Robots.txt", "Check robots.txt for hidden paths"),
            ("7", "SSL Certificate Info", "Get SSL certificate details"),
            ("8", "Subdomain Brute", "Brute-force subdomains (wordlist)"),
            ("9", "Technology Detector", "Detect web technologies"),
            ("10", "Email Harvester", "Extract emails from website"),
            ("0", "BACK", "Return to main menu"),
        ]
        self.ui.print_menu(items, "QUICK RECON TOOLS")
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in items])
        if choice == "0":
            return
        self._run_recon_tool(choice)
    
    def _get_target(self) -> Optional[str]:
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            return Prompt.ask("[bold bright_green]Enter target URL/IP[/bold bright_green]", default="")
        return input("Enter target URL/IP: ").strip()
    
    def _run_recon_tool(self, choice: str) -> None:
        target = self._get_target()
        if not target and choice != "0":
            self.ui.print_error("No target specified")
            time.sleep(1)
            return
        
        try:
            if choice == "1":
                self._dns_lookup(target)
            elif choice == "2":
                self._whois_lookup(target)
            elif choice == "3":
                self._ip_geolocation(target)
            elif choice == "4":
                self._port_scan(target)
            elif choice == "5":
                self._http_headers(target)
            elif choice == "6":
                self._robots_txt(target)
            elif choice == "7":
                self._ssl_info(target)
            elif choice == "8":
                self._subdomain_brute(target)
            elif choice == "9":
                self._tech_detect(target)
            elif choice == "10":
                self._email_harvest(target)
        except Exception as e:
            self.ui.print_error(f"Recon tool failed: {e}")
        input("\nPress Enter to continue...")
    
    def _dns_lookup(self, target: str) -> None:
        import dns.resolver
        self.ui.print_info(f"DNS lookup for: {target}")
        try:
            for record_type in ["A", "AAAA", "MX", "NS", "TXT", "SOA"]:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    self.ui.print_success(f"{record_type} Records:")
                    for rdata in answers:
                        print(f"  {rdata}")
                except dns.resolver.NoAnswer:
                    pass
                except dns.resolver.NXDOMAIN:
                    self.ui.print_error(f"Domain {target} does not exist")
                    break
        except ImportError:
            self.ui.print_warning("dnspython not installed. Install with: pip install dnspython")
    
    def _whois_lookup(self, target: str) -> None:
        self.ui.print_info(f"WHOIS lookup for: {target}")
        try:
            import whois
            w = whois.whois(target)
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(str(w), title="WHOIS Info", border_style="green"))
            else:
                print(w)
        except ImportError:
            self.ui.print_warning("python-whois not installed. Install with: pip install python-whois")
        except Exception as e:
            self.ui.print_error(f"WHOIS lookup failed: {e}")
    
    def _ip_geolocation(self, target: str) -> None:
        self.ui.print_info(f"Geolocating IP: {target}")
        try:
            resp = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
            data = resp.json()
            if data.get("status") == "success":
                if RICH_AVAILABLE:
                    from rich.panel import Panel
                    self.console.print(Panel(json.dumps(data, indent=2), title="IP Geolocation", border_style="green"))
                else:
                    print(json.dumps(data, indent=2))
            else:
                self.ui.print_error("Geolocation failed")
        except Exception as e:
            self.ui.print_error(f"Geolocation failed: {e}")
    
    def _port_scan(self, target: str) -> None:
        self.ui.print_info(f"Port scanning: {target}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 5432, 5900, 8080, 8443]
        open_ports = []
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    service = "unknown"
                    try:
                        service = socket.getservbyport(port)
                    except Exception:
                        pass
                    open_ports.append(f"{port} ({service})")
                    self.ui.print_success(f"Port {port} ({service}) is OPEN")
                sock.close()
            except Exception:
                pass
        if not open_ports:
            self.ui.print_warning("No common ports found open")
    
    def _http_headers(self, target: str) -> None:
        self.ui.print_info(f"Analyzing headers for: {target}")
        try:
            if not target.startswith("http"):
                target = f"https://{target}"
            resp = requests.get(target, timeout=10, allow_redirects=False)
            headers = dict(resp.headers)
            if RICH_AVAILABLE:
                from rich.panel import Panel
                self.console.print(Panel(json.dumps(headers, indent=2), title="HTTP Headers", border_style="green"))
            else:
                print(json.dumps(headers, indent=2))
        except Exception as e:
            self.ui.print_error(f"Headers fetch failed: {e}")
    
    def _robots_txt(self, target: str) -> None:
        self.ui.print_info(f"Checking robots.txt for: {target}")
        try:
            if not target.startswith("http"):
                target = f"https://{target}"
            resp = requests.get(f"{target}/robots.txt", timeout=10)
            if resp.status_code == 200:
                self.ui.print_success("robots.txt found:")
                print(resp.text[:2000])
            else:
                self.ui.print_warning("robots.txt not found")
        except Exception as e:
            self.ui.print_error(f"robots.txt fetch failed: {e}")
    
    def _ssl_info(self, target: str) -> None:
        self.ui.print_info(f"Getting SSL info for: {target}")
        try:
            import ssl
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    if RICH_AVAILABLE:
                        from rich.panel import Panel
                        self.console.print(Panel(json.dumps(cert, indent=2), title="SSL Certificate", border_style="green"))
                    else:
                        print(json.dumps(cert, indent=2))
        except Exception as e:
            self.ui.print_error(f"SSL info fetch failed: {e}")
    
    def _subdomain_brute(self, target: str) -> None:
        self.ui.print_info(f"Brute-forcing subdomains for: {target}")
        common_subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2", "admin", "blog", "api", "dev", "staging", "test"]
        found = []
        for sub in common_subdomains:
            domain = f"{sub}.{target}"
            try:
                socket.gethostbyname(domain)
                found.append(domain)
                self.ui.print_success(f"Found: {domain}")
            except socket.gaierror:
                pass
        if not found:
            self.ui.print_warning("No subdomains found")
    
    def _tech_detect(self, target: str) -> None:
        self.ui.print_info(f"Detecting technologies for: {target}")
        try:
            if not target.startswith("http"):
                target = f"https://{target}"
            resp = requests.get(target, timeout=10)
            headers = dict(resp.headers)
            tech = []
            if "X-Powered-By" in headers:
                tech.append(f"Server: {headers['X-Powered-By']}")
            if "Server" in headers:
                tech.append(f"Server: {headers['Server']}")
            if "X-Generator" in headers:
                tech.append(f"Generator: {headers['X-Generator']}")
            if tech:
                self.ui.print_success("Detected technologies:")
                for t in tech:
                    print(f"  {t}")
            else:
                self.ui.print_warning("No obvious technology headers found")
        except Exception as e:
            self.ui.print_error(f"Technology detection failed: {e}")
    
    def _email_harvest(self, target: str) -> None:
        self.ui.print_info(f"Harvesting emails from: {target}")
        try:
            if not target.startswith("http"):
                target = f"https://{target}"
            resp = requests.get(target, timeout=10)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resp.text)
            if emails:
                self.ui.print_success(f"Found {len(set(emails))} unique emails:")
                for email in set(emails):
                    print(f"  {email}")
            else:
                self.ui.print_warning("No emails found")
        except Exception as e:
            self.ui.print_error(f"Email harvest failed: {e}")


class SecuritySuite:
    """Main Security Suite controller."""
    
    def __init__(self):
        self.ui = SecuritySuiteUI()
        self.all_hacking = AllHackingToolsSuite()
        self.spyhunt = SpyHuntSuite()
        self.quick_recon = QuickReconSuite()
    
    def show_main_menu(self) -> None:
        """Show the main Security Suite menu."""
        while True:
            self.ui.print_header("SECURITY SUITE - MAIN MENU")
            items = [
                ("1", "AllHackingTools Suite", "Full hacking toolkit with 19 categories"),
                ("2", "SpyHunt Security Scanner", "Advanced security reconnaissance toolkit"),
                ("3", "Quick Recon", "Fast reconnaissance utilities"),
                ("4", "Phishing Tools", "Phishing and social engineering tools"),
                ("5", "Network Tools", "Network scanning and analysis"),
                ("0", "BACK", "Return to main application"),
            ]
            self.ui.print_menu(items, "SECURITY TOOLS")
            
            choice = self.ui.prompt_choice("Select suite", [k for k, _, _ in items])
            if choice == "0":
                return
            
            if choice == "1":
                self.all_hacking.show_menu()
            elif choice == "2":
                self.spyhunt.show_menu()
            elif choice == "3":
                self.quick_recon.show_menu()
            elif choice == "4":
                self._phishing_tools_menu()
            elif choice == "5":
                self._network_tools_menu()
            else:
                self.ui.print_error("Invalid option")
                time.sleep(1)
    
    def _phishing_tools_menu(self) -> None:
        self.ui.print_header("PHISHING TOOLS")
        items = [
            ("1", "Zphisher", "Automated phishing tool with 30+ templates"),
            ("2", "ShellPhish", "Modded shellphish tool"),
            ("3", "SayCheese", "Webcam grabber by link"),
            ("4", "BlackPhish", "Easy phishing tool"),
            ("5", "Mask Phish", "URL masking tool"),
            ("6", "Seeker", "Smartphone location tool"),
            ("7", "AIOPhish", "Social phishing toolkit"),
            ("8", "I-See-You", "User location finder"),
            ("0", "BACK", "Return to security suite"),
        ]
        self.ui.print_menu(items, "PHISHING TOOLS")
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in items])
        if choice == "0":
            return
        
        phishing_launcher = ToolLauncher(ALLHACKING_DIR)
        phishing_tools = {
            "1": ("zphisher", "zphisher.sh"),
            "2": ("ShellPhish", "ShellPhish/shellphish.sh"),
            "3": ("saycheese", "saycheese/saycheese.sh"),
            "4": ("BlackPhish", "BlackPhish/blackphish.py"),
            "5": ("Mask-Phish", "Mask-Phish.Termux/Mask-Phish.sh"),
            "6": ("seeker", "seeker/seeker.py"),
            "7": ("AIOPhish", "AIOPhish/aiophish.sh"),
            "8": ("I-See-You", "I-See-You/ISeeYou.sh"),
        }
        
        if choice in phishing_tools:
            name, path = phishing_tools[choice]
            tool_path = ALLHACKING_DIR / path
            phishing_launcher.launch_script(tool_path, "", cwd=ALLHACKING_DIR)
            input("\nPress Enter to continue...")
    
    def _network_tools_menu(self) -> None:
        self.ui.print_header("NETWORK TOOLS")
        items = [
            ("1", "Nmap Scanner", "Network mapper and port scanner"),
            ("2", "Network Sniffer", "Packet capture and analysis"),
            ("3", "ARP Scanner", "Local network ARP discovery"),
            ("4", "Ping Sweep", "ICMP ping sweep"),
            ("5", "DNS Enumeration", "DNS record enumeration"),
            ("6", "SMB Enumeration", "SMB share enumeration"),
            ("7", "SNMP Walk", "SNMP community string walker"),
            ("0", "BACK", "Return to security suite"),
        ]
        self.ui.print_menu(items, "NETWORK TOOLS")
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in items])
        if choice == "0":
            return
        
        self.ui.print_info("Network tool launching...")
        # Network tools can be integrated here
        if choice in ["1", "3", "4", "5"]:
            target = self._get_target()
            if target:
                self.ui.print_info(f"Scanning: {target}")
                # Launch nmap if available
                if choice == "1":
                    self.ui.print_info("Running nmap scan...")
                    os.system(f"nmap -sV -sC {target}")
        input("\nPress Enter to continue...")


def launch_security_suite() -> None:
    """Entry point for Security Suite from main application."""
    suite = SecuritySuite()
    suite.show_main_menu()


if __name__ == "__main__":
    launch_security_suite()
