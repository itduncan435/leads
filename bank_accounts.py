#!/usr/bin/env python3
"""
Bank Accounts Module
Manages user bank accounts with name, phone, and balance.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

BANK_DIR = Path(__file__).resolve().parent
ACCOUNTS_FILE = BANK_DIR / "bank_accounts.json"


class BankAccountManager:
    """Manages bank accounts."""
    
    def __init__(self, accounts_file: Path = ACCOUNTS_FILE):
        self.accounts_file = accounts_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not self.accounts_file.exists():
            self._save_accounts({})
    
    def _load_accounts(self) -> Dict[str, Any]:
        try:
            with open(self.accounts_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_accounts(self, accounts: Dict[str, Any]):
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f, indent=2, default=str)
    
    def add_account(self, phone: str, name: str, balance: float = 0.0) -> bool:
        """Add a new bank account."""
        accounts = self._load_accounts()
        phone = self._normalize_phone(phone)
        
        if phone in accounts:
            return False
        
        accounts[phone] = {
            "phone": phone,
            "name": name.upper(),
            "balance": float(balance),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self._save_accounts(accounts)
        return True
    
    def get_account(self, phone: str) -> Optional[Dict[str, Any]]:
        """Get account by phone number."""
        accounts = self._load_accounts()
        phone = self._normalize_phone(phone)
        return accounts.get(phone)
    
    def update_balance(self, phone: str, new_balance: float) -> bool:
        """Update account balance."""
        accounts = self._load_accounts()
        phone = self._normalize_phone(phone)
        
        if phone not in accounts:
            return False
        
        accounts[phone]["balance"] = float(new_balance)
        accounts[phone]["updated_at"] = datetime.now().isoformat()
        self._save_accounts(accounts)
        return True
    
    def deposit(self, phone: str, amount: float) -> bool:
        """Deposit money into account."""
        account = self.get_account(phone)
        if not account:
            return False
        
        new_balance = account["balance"] + amount
        return self.update_balance(phone, new_balance)
    
    def withdraw(self, phone: str, amount: float) -> bool:
        """Withdraw money from account."""
        account = self.get_account(phone)
        if not account:
            return False
        
        if account["balance"] < amount:
            return False
        
        new_balance = account["balance"] - amount
        return self.update_balance(phone, new_balance)
    
    def delete_account(self, phone: str) -> bool:
        """Delete an account."""
        accounts = self._load_accounts()
        phone = self._normalize_phone(phone)
        
        if phone in accounts:
            del accounts[phone]
            self._save_accounts(accounts)
            return True
        return False
    
    def list_accounts(self) -> List[Dict[str, Any]]:
        """List all accounts."""
        accounts = self._load_accounts()
        return list(accounts.values())
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number to +XXXXXXXXXXX format."""
        phone = phone.strip()
        if not phone.startswith("+"):
            phone = "+" + phone
        return phone
    
    def seed_default_users(self) -> None:
        """Seed default users for testing."""
        default_users = [
            {"phone": "0599613879", "name": "JOHN AMUZU", "balance": 12.82},
        ]
        
        for user in default_users:
            phone = self._normalize_phone(user["phone"])
            if not self.get_account(phone):
                self.add_account(phone, user["name"], user["balance"])
                print(f"Seeded user: {user['name']} ({phone}) - Balance: ${user['balance']}")


# Global instance
_bank_accounts: Optional[BankAccountManager] = None

def get_bank_account_manager() -> BankAccountManager:
    """Get the global bank account manager instance."""
    global _bank_accounts
    if _bank_accounts is None:
        _bank_accounts = BankAccountManager()
        _bank_accounts.seed_default_users()
    return _bank_accounts
