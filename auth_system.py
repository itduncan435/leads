#!/usr/bin/env python3
"""
Phone Number Authentication System
Secure local login/registration using phone number + PIN.
"""

import os
import json
import time
import hashlib
import random
import string
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

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

# Base directory
BANK_DIR = Path(__file__).resolve().parent
USERS_FILE = BANK_DIR / "users.json"
SESSION_FILE = BANK_DIR / ".session"


class AuthUI:
    """UI for authentication screens."""
    
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
        os.system("clear" if os.name != "nt" else "cls")
    
    def print_header(self, title: str = "AUTHENTICATION"):
        self.clear()
        if RICH_AVAILABLE:
            self._refresh_terminal_size()
            header = Panel(
                Align.center(Text(f"[bold bright_cyan]{title}[/bold bright_cyan]\n[dim]Secure Phone Number Authentication[/dim]")),
                border_style="bright_cyan",
                padding=(0, 2),
                expand=False,
            )
            self.console.print(header)
            self.console.print()
        else:
            print("=" * self.width)
            print(f"  {title}")
            print("  Secure Phone Number Authentication")
            print("=" * self.width)
            print()
    
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


class UserDatabase:
    """Manages user storage and retrieval."""
    
    def __init__(self, users_file: Path = USERS_FILE):
        self.users_file = users_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not self.users_file.exists():
            self._save_users({})
    
    def _load_users(self) -> Dict[str, Any]:
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_users(self, users: Dict[str, Any]):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2, default=str)
    
    def user_exists(self, phone: str) -> bool:
        users = self._load_users()
        return phone in users
    
    def register_user(self, phone: str, pin_hash: str, salt: str, name: str = "") -> bool:
        users = self._load_users()
        if phone in users:
            return False
        
        users[phone] = {
            "phone": phone,
            "pin_hash": pin_hash,
            "salt": salt,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "login_count": 0,
        }
        self._save_users(users)
        return True
    
    def authenticate_user(self, phone: str, pin_hash: str) -> Optional[Dict[str, Any]]:
        users = self._load_users()
        user = users.get(phone)
        if not user:
            return None
        
        if user.get("pin_hash") == pin_hash:
            user["last_login"] = datetime.now().isoformat()
            user["login_count"] = user.get("login_count", 0) + 1
            self._save_users(users)
            return user
        return None
    
    def get_user(self, phone: str) -> Optional[Dict[str, Any]]:
        users = self._load_users()
        return users.get(phone)
    
    def update_user(self, phone: str, updates: Dict[str, Any]) -> bool:
        users = self._load_users()
        if phone not in users:
            return False
        
        users[phone].update(updates)
        self._save_users(users)
        return True
    
    def delete_user(self, phone: str) -> bool:
        users = self._load_users()
        if phone in users:
            del users[phone]
            self._save_users(users)
            return True
        return False
    
    def list_users(self) -> list:
        users = self._load_users()
        return list(users.values())


class SessionManager:
    """Manages user login sessions."""
    
    def __init__(self, session_file: Path = SESSION_FILE):
        self.session_file = session_file
    
    def save_session(self, phone: str, name: str = "") -> bool:
        try:
            session_data = {
                "phone": phone,
                "name": name,
                "logged_in_at": datetime.now().isoformat(),
            }
            with open(self.session_file, "w") as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_session(self) -> Optional[Dict[str, Any]]:
        try:
            if not self.session_file.exists():
                return None
            with open(self.session_file, "r") as f:
                return json.load(f)
        except Exception:
            return None
    
    def clear_session(self) -> bool:
        try:
            if self.session_file.exists():
                self.session_file.unlink()
            return True
        except Exception:
            return False
    
    def is_logged_in(self) -> bool:
        session = self.load_session()
        return session is not None and "phone" in session


class AuthSystem:
    """Main authentication controller."""
    
    def __init__(self):
        self.ui = AuthUI()
        self.db = UserDatabase()
        self.session = SessionManager()
        self.current_user: Optional[Dict[str, Any]] = None
        self._seed_default_user()
    
    def _seed_default_user(self):
        """Seed default user JOHN AMUZU with PIN 1234."""
        phone = "+0599613879"
        if not self.db.user_exists(phone):
            salt = self._generate_salt()
            pin_hash = self._hash_pin("1234", salt)
            self.db.register_user(phone, pin_hash, salt, "JOHN AMUZU")
    
    def _hash_pin(self, pin: str, salt: str) -> str:
        """Hash PIN with salt for secure storage."""
        return hashlib.sha256((pin + salt).encode()).hexdigest()
    
    def _generate_salt(self, length: int = 16) -> str:
        """Generate random salt for PIN hashing."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def _validate_phone(self, phone: str) -> Tuple[bool, str]:
        """Validate phone number format."""
        phone = phone.strip()
        if not phone:
            return False, "Phone number is required"
        
        if not phone.startswith("+"):
            phone = "+" + phone
        
        if PHONENUMBERS_AVAILABLE:
            try:
                parsed = phonenumbers.parse(phone, None)
                if phonenumbers.is_valid_number(parsed):
                    return True, phone
                return False, "Invalid phone number format"
            except Exception:
                return False, "Invalid phone number format"
        
        if not re.match(r'^\+?[\d\s\-\(\)]{10,15}$', phone):
            return False, "Invalid phone number format. Use format: +1234567890"
        
        return True, phone
    
    def _validate_pin(self, pin: str) -> Tuple[bool, str]:
        """Validate PIN format."""
        pin = pin.strip()
        if not pin:
            return False, "PIN is required"
        if not pin.isdigit():
            return False, "PIN must contain only digits"
        if len(pin) < 4:
            return False, "PIN must be at least 4 digits"
        if len(pin) > 6:
            return False, "PIN must be at most 6 digits"
        return True, pin
    
    def register(self) -> bool:
        """Handle user registration."""
        self.ui.print_header("REGISTER")
        
        # Get phone number
        if RICH_AVAILABLE:
            phone = Prompt.ask("[bold bright_cyan]Enter phone number[/bold bright_cyan]", default="")
        else:
            phone = input("Enter phone number: ").strip()
        
        valid, result = self._validate_phone(phone)
        if not valid:
            self.ui.print_error(result)
            time.sleep(2)
            return False
        phone = result
        
        if self.db.user_exists(phone):
            self.ui.print_error("Phone number already registered. Please login instead.")
            time.sleep(2)
            return False
        
        # Get PIN
        if RICH_AVAILABLE:
            pin = Prompt.ask("[bold bright_cyan]Create 4-6 digit PIN[/bold bright_cyan]", password=True, default="")
        else:
            pin = input("Create 4-6 digit PIN: ").strip()
        
        valid, result = self._validate_pin(pin)
        if not valid:
            self.ui.print_error(result)
            time.sleep(2)
            return False
        pin = result
        
        # Confirm PIN
        if RICH_AVAILABLE:
            pin_confirm = Prompt.ask("[bold bright_cyan]Confirm PIN[/bold bright_cyan]", password=True, default="")
        else:
            pin_confirm = input("Confirm PIN: ").strip()
        
        if pin != pin_confirm:
            self.ui.print_error("PINs do not match")
            time.sleep(2)
            return False
        
        # Optional name
        if RICH_AVAILABLE:
            name = Prompt.ask("[bold bright_cyan]Enter your name (optional)[/bold bright_cyan]", default="")
        else:
            name = input("Enter your name (optional): ").strip()
        
        # Create account
        salt = self._generate_salt()
        pin_hash = self._hash_pin(pin, salt)
        
        if self.db.register_user(phone, pin_hash, salt, name):
            self.ui.print_success(f"Registration successful! Welcome, {name or 'User'}")
            self.ui.print_info(f"Phone: {phone}")
            time.sleep(2)
            return True
        else:
            self.ui.print_error("Registration failed. Phone number may already exist.")
            time.sleep(2)
            return False
    
    def login(self) -> bool:
        """Handle user login."""
        self.ui.print_header("LOGIN")
        
        # Show default user hint
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_yellow]💡 Default user:[/bold bright_yellow] [bold bright_cyan]0599613879[/bold bright_cyan] / [bold bright_cyan]1234[/bold bright_cyan]")
            self.ui.console.print()
        
        # Get phone number
        if RICH_AVAILABLE:
            phone = Prompt.ask("[bold bright_cyan]Enter phone number[/bold bright_cyan]", default="0599613879")
        else:
            phone = input("Enter phone number (default: 0599613879): ").strip() or "0599613879"
        
        valid, result = self._validate_phone(phone)
        if not valid:
            self.ui.print_error(result)
            time.sleep(2)
            return False
        phone = result
        
        # Check if user exists
        user = self.db.get_user(phone)
        if not user:
            self.ui.print_error("Phone number not registered. Please register first.")
            time.sleep(2)
            return False
        
        # Get PIN
        if RICH_AVAILABLE:
            pin = Prompt.ask("[bold bright_cyan]Enter your PIN[/bold bright_cyan]", password=True, default="1234")
        else:
            pin = input("Enter your PIN (default: 1234): ").strip() or "1234"
        
        valid, result = self._validate_pin(pin)
        if not valid:
            self.ui.print_error(result)
            time.sleep(2)
            return False
        pin = result
        
        # Authenticate
        pin_hash = self._hash_pin(pin, user["salt"])
        authenticated_user = self.db.authenticate_user(phone, pin_hash)
        
        if authenticated_user:
            self.current_user = authenticated_user
            self.session.save_session(phone, authenticated_user.get("name", ""))
            self.ui.print_success(f"Login successful! Welcome back, {authenticated_user.get('name', 'User')}")
            time.sleep(1.5)
            return True
        else:
            self.ui.print_error("Invalid PIN")
            time.sleep(2)
            return False
    
    def logout(self) -> bool:
        """Handle user logout."""
        if self.current_user:
            phone = self.current_user.get("phone", "")
            self.current_user = None
            self.session.clear_session()
            self.ui.print_success(f"Logged out successfully from {phone}")
            time.sleep(1.5)
            return True
        return False
    
    def auto_login(self) -> bool:
        """Attempt automatic login from saved session."""
        if self.session.is_logged_in():
            session = self.session.load_session()
            phone = session.get("phone", "")
            if phone:
                user = self.db.get_user(phone)
                if user:
                    self.current_user = user
                    return True
        return False
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user."""
        return self.current_user
    
    def is_authenticated(self) -> bool:
        """Check if user is currently logged in."""
        return self.current_user is not None
    
    def show_profile(self) -> None:
        """Display current user profile."""
        if not self.current_user:
            self.ui.print_warning("No user logged in")
            time.sleep(1)
            return
        
        self.ui.print_header("USER PROFILE")
        
        user = self.current_user
        if RICH_AVAILABLE:
            table = Table(show_header=False, box=box.HEAVY, border_style="bright_cyan", padding=(0, 2))
            table.add_column("Field", style="bold bright_cyan")
            table.add_column("Value", style="bright_green")
            
            table.add_row("📱 Phone", user.get("phone", "N/A"))
            table.add_row("👤 Name", user.get("name", "Anonymous"))
            table.add_row("📅 Created", user.get("created_at", "N/A")[:19].replace("T", " "))
            table.add_row("🕒 Last Login", user.get("last_login", "N/A")[:19].replace("T", " "))
            table.add_row("🔢 Login Count", str(user.get("login_count", 0)))
            
            self.ui.console.print(table)
        else:
            print(f"Phone: {user.get('phone', 'N/A')}")
            print(f"Name: {user.get('name', 'Anonymous')}")
            print(f"Created: {user.get('created_at', 'N/A')[:19]}")
            print(f"Last Login: {user.get('last_login', 'N/A')[:19]}")
            print(f"Login Count: {user.get('login_count', 0)}")
        
        input("\nPress Enter to continue...")
    
    def auth_menu(self) -> None:
        """Show authentication menu."""
        while True:
            self.ui.print_header("AUTHENTICATION MENU")
            
            items = [
                ("1", "Login", "Login with phone number and PIN"),
                ("2", "Quick Login", "Quick login as JOHN AMUZU (0599613879 / 1234)"),
                ("3", "Register", "Create new account"),
                ("4", "Profile", "View your profile"),
                ("5", "Logout", "Logout from current session"),
                ("0", "Back", "Return to main terminal"),
            ]
            
            if RICH_AVAILABLE:
                table = Table(show_header=True, header_style="bold bright_yellow", box=box.HEAVY, border_style="bright_yellow", show_lines=True, padding=(0, 1))
                table.add_column("OPT", style="bold bright_cyan", width=6, justify="center")
                table.add_column("ACTION", style="bold white")
                table.add_column("DESCRIPTION", style="dim green", max_width=50)
                
                for opt, action, desc in items:
                    table.add_row(opt, action, desc)
                
                self.ui.console.print(table)
                self.ui.console.print()
            else:
                print("\nAuthentication Menu")
                print("-" * 60)
                for opt, action, desc in items:
                    print(f"  [{opt:>3}] {action:<15} {desc}")
                print()
            
            if RICH_AVAILABLE:
                choice = Prompt.ask("[bold bright_green]Select option[/bold bright_green]", choices=["0", "1", "2", "3", "4", "5"], default="0", show_choices=False)
            else:
                choice = input("Select option: ").strip()
            
            if choice == "0":
                return
            elif choice == "1":
                self.login()
            elif choice == "2":
                self.quick_login()
            elif choice == "3":
                self.register()
            elif choice == "4":
                self.show_profile()
            elif choice == "5":
                if self.is_authenticated():
                    self.logout()
                else:
                    self.ui.print_warning("No user is currently logged in")
                    time.sleep(1)
    
    def quick_login(self) -> bool:
        """Quick login for default user JOHN AMUZU."""
        phone = "+0599613879"
        pin_hash = self._hash_pin("1234", self.db.get_user(phone)["salt"])
        authenticated_user = self.db.authenticate_user(phone, pin_hash)
        
        if authenticated_user:
            self.current_user = authenticated_user
            self.session.save_session(phone, authenticated_user.get("name", ""))
            self.ui.print_success(f"Quick login successful! Welcome, {authenticated_user.get('name', 'User')}")
            time.sleep(1.5)
            return True
        else:
            self.ui.print_error("Quick login failed. Please use option 1 to login manually.")
            time.sleep(2)
            return False


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current authenticated user from global auth system."""
    return _auth_system.get_current_user() if _auth_system else None


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return _auth_system.is_authenticated() if _auth_system else False


def require_auth(func):
    """Decorator to require authentication for a function."""
    def wrapper(*args, **kwargs):
        if not _auth_system or not _auth_system.is_authenticated():
            print("[ERROR] Authentication required. Please login first.")
            return None
        return func(*args, **kwargs)
    return wrapper


# Global auth system instance
_auth_system: Optional[AuthSystem] = None

def init_auth_system() -> AuthSystem:
    """Initialize and return the global auth system."""
    global _auth_system
    if _auth_system is None:
        _auth_system = AuthSystem()
        _auth_system.auto_login()
    return _auth_system

def get_auth_system() -> Optional[AuthSystem]:
    """Get the global auth system instance."""
    return _auth_system
