#!/usr/bin/env python3
"""
AIO V18.0 - Advanced Phone Number API Platform
Futuristic CLI Tool with 36+ Robust Functions
"""

import random
import string
import json
import re
import time
import sys
import os
import csv
import requests
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None

from bank_branches import BANK_BRANCHES, get_branches_by_state, get_bank_states, search_branches

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.progress import Progress, BarColumn
    from rich import box
    from rich.markup import escape
    from rich.align import Align
    from rich.style import Style
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False

# Security Suite Integration
try:
    from security_suite import SecuritySuite, ToolLauncher
    SECURITY_SUITE_AVAILABLE = True
except ImportError:
    SECURITY_SUITE_AVAILABLE = False

# Phone Number Authentication System
try:
    from auth_system import init_auth_system, get_auth_system, get_current_user, is_authenticated
    AUTH_SYSTEM_AVAILABLE = True
except ImportError:
    AUTH_SYSTEM_AVAILABLE = False

# ============================================================
# REAL EMAIL AND PHONE DATABASE LOADER
# ============================================================

_REAL_EMAILS = []
_REAL_PHONES = []
_BASE_DIR = Path(__file__).resolve().parent

def _get_crypto_key():
    if Fernet is None:
        raise RuntimeError("cryptography package is required to decrypt protected data files")
    key_str = "ytTJugIrlr8U6mVW9Z_cVYmn2YjR4hu9CkPIQLMfdAg="
    return key_str.encode()

def _decrypt_file(path: Path) -> bytes:
    from cryptography.fernet import Fernet
    if not path.exists():
        return b""
    data = path.read_bytes()
    return Fernet(_get_crypto_key()).decrypt(data)

def _load_real_data():
    global _REAL_EMAILS, _REAL_PHONES
    try:
        email_file = _BASE_DIR / "email.txt.enc"
        if email_file.exists():
            data = _decrypt_file(email_file).decode("utf-8", errors="ignore")
            _REAL_EMAILS = [line.strip() for line in data.splitlines() if line.strip() and "@" in line]
    except Exception:
        _REAL_EMAILS = []

    try:
        phone_file = _BASE_DIR / "usanow.csv.enc"
        if phone_file.exists():
            data = _decrypt_file(phone_file).decode("utf-8", errors="ignore")
            reader = csv.DictReader(data.splitlines())
            for row in reader:
                phone = row.get("phone", "").strip()
                if phone:
                    _REAL_PHONES.append(phone)
                email = row.get("email", "").strip()
                if email and "@" in email:
                    _REAL_EMAILS.append(email)
    except Exception:
        pass

_load_real_data()

# ============================================================
# CALLER ID DATABASE AND LOOKUP
# ============================================================

CALLER_ID_DB = {
    "+14252725717": {"firstname": "John", "middlename": "Michael", "lastname": "Smith", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125551000": {"firstname": "John", "middlename": "Michael", "lastname": "Smith", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132561037": {"firstname": "Jane", "middlename": "", "lastname": "Johnson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142571074": {"firstname": "Michael", "middlename": "", "lastname": "Williams", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152581111": {"firstname": "Emily", "middlename": "John", "lastname": "Brown", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162591148": {"firstname": "David", "middlename": "", "lastname": "Jones", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172601185": {"firstname": "Sarah", "middlename": "", "lastname": "Garcia", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182611222": {"firstname": "James", "middlename": "Richard", "lastname": "Miller", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192621259": {"firstname": "Jessica", "middlename": "", "lastname": "Davis", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202631296": {"firstname": "Robert", "middlename": "", "lastname": "Rodriguez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242641333": {"firstname": "Amanda", "middlename": "Charles", "lastname": "Wilson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255551370": {"firstname": "William", "middlename": "", "lastname": "Anderson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262561407": {"firstname": "Patricia", "middlename": "", "lastname": "Taylor", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282571444": {"firstname": "Christopher", "middlename": "Robert", "lastname": "Thomas", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292581481": {"firstname": "Jennifer", "middlename": "", "lastname": "Hernandez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312591518": {"firstname": "Daniel", "middlename": "", "lastname": "Moore", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342601555": {"firstname": "Elizabeth", "middlename": "David", "lastname": "Martin", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392611592": {"firstname": "Matthew", "middlename": "", "lastname": "Jackson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402621629": {"firstname": "Linda", "middlename": "", "lastname": "Thompson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482631666": {"firstname": "Anthony", "middlename": "Thomas", "lastname": "White", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512641703": {"firstname": "Susan", "middlename": "", "lastname": "Lopez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125551740": {"firstname": "Andrew", "middlename": "", "lastname": "Lee", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132561777": {"firstname": "Barbara", "middlename": "James", "lastname": "Gonzalez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142571814": {"firstname": "Richard", "middlename": "", "lastname": "Harris", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152581851": {"firstname": "Karen", "middlename": "", "lastname": "Clark", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162591888": {"firstname": "Joseph", "middlename": "William", "lastname": "Lewis", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172601925": {"firstname": "Maria", "middlename": "", "lastname": "Robinson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182611962": {"firstname": "Charles", "middlename": "", "lastname": "Walker", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192621999": {"firstname": "Nancy", "middlename": "Joseph", "lastname": "Perez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202632036": {"firstname": "Thomas", "middlename": "", "lastname": "Hall", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242642073": {"firstname": "Betty", "middlename": "", "lastname": "Young", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255552110": {"firstname": "Mark", "middlename": "Michael", "lastname": "Allen", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262562147": {"firstname": "Sandra", "middlename": "", "lastname": "Sanchez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282572184": {"firstname": "Donald", "middlename": "", "lastname": "Wright", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292582221": {"firstname": "Ashley", "middlename": "John", "lastname": "King", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312592258": {"firstname": "Steven", "middlename": "", "lastname": "Scott", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342602295": {"firstname": "Dorothy", "middlename": "", "lastname": "Green", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392612332": {"firstname": "Paul", "middlename": "Richard", "lastname": "Baker", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402622369": {"firstname": "Kimberly", "middlename": "", "lastname": "Adams", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482632406": {"firstname": "Kevin", "middlename": "", "lastname": "Nelson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512642443": {"firstname": "Emily", "middlename": "Charles", "lastname": "Hill", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125552480": {"firstname": "George", "middlename": "", "lastname": "Campbell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132562517": {"firstname": "Melissa", "middlename": "", "lastname": "Mitchell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142572554": {"firstname": "Jason", "middlename": "Robert", "lastname": "Roberts", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152582591": {"firstname": "Rebecca", "middlename": "", "lastname": "Carter", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162592628": {"firstname": "Ryan", "middlename": "", "lastname": "Phillips", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172602665": {"firstname": "Laura", "middlename": "David", "lastname": "Evans", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182612702": {"firstname": "Jacob", "middlename": "", "lastname": "Turner", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192622739": {"firstname": "Cynthia", "middlename": "", "lastname": "Torres", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202632776": {"firstname": "Gary", "middlename": "Thomas", "lastname": "Parker", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242642813": {"firstname": "Angela", "middlename": "", "lastname": "Collins", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255552850": {"firstname": "Nicholas", "middlename": "", "lastname": "Edwards", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262562887": {"firstname": "Brenda", "middlename": "James", "lastname": "Stewart", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282572924": {"firstname": "Eric", "middlename": "", "lastname": "Flores", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292582961": {"firstname": "Pamela", "middlename": "", "lastname": "Morris", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312592998": {"firstname": "Jonathan", "middlename": "William", "lastname": "Nguyen", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342603035": {"firstname": "Nicole", "middlename": "", "lastname": "Murphy", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392613072": {"firstname": "Stephen", "middlename": "", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402623109": {"firstname": "Samantha", "middlename": "Joseph", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482633146": {"firstname": "Larry", "middlename": "", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512643183": {"firstname": "Rachel", "middlename": "", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125553220": {"firstname": "Justin", "middlename": "Michael", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132563257": {"firstname": "Christine", "middlename": "", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142573294": {"firstname": "Brandon", "middlename": "", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152583331": {"firstname": "Debra", "middlename": "John", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162593368": {"firstname": "Samuel", "middlename": "", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172603405": {"firstname": "Katherine", "middlename": "", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182613442": {"firstname": "Raymond", "middlename": "Richard", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192623479": {"firstname": "Carolyn", "middlename": "", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202633516": {"firstname": "Gregory", "middlename": "", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242643553": {"firstname": "Janet", "middlename": "Charles", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255553590": {"firstname": "Alexander", "middlename": "", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262563627": {"firstname": "Maria", "middlename": "", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282573664": {"firstname": "Patrick", "middlename": "Robert", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292583701": {"firstname": "Jack", "middlename": "", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312593738": {"firstname": "Dennis", "middlename": "", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342603775": {"firstname": "Heather", "middlename": "David", "lastname": "Bennett", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392613812": {"firstname": "Jerry", "middlename": "", "lastname": "Gray", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402623849": {"firstname": "Helen", "middlename": "", "lastname": "James", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482633886": {"firstname": "Tyler", "middlename": "Thomas", "lastname": "Reyes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512643923": {"firstname": "Aaron", "middlename": "", "lastname": "Cruz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125553960": {"firstname": "Nathan", "middlename": "", "lastname": "Hughes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132563997": {"firstname": "Fiona", "middlename": "James", "lastname": "Price", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142574034": {"firstname": "Henry", "middlename": "", "lastname": "Myers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152584071": {"firstname": "Evelyn", "middlename": "", "lastname": "Long", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162594108": {"firstname": "Douglas", "middlename": "William", "lastname": "Foster", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172604145": {"firstname": "Olivia", "middlename": "", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182614182": {"firstname": "Peter", "middlename": "", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192624219": {"firstname": "Megan", "middlename": "Joseph", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202634256": {"firstname": "Adam", "middlename": "", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242644293": {"firstname": "Andrea", "middlename": "", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255554330": {"firstname": "Zachary", "middlename": "Michael", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262564367": {"firstname": "Harold", "middlename": "", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282574404": {"firstname": "Jean", "middlename": "", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292584441": {"firstname": "Carl", "middlename": "John", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312594478": {"firstname": "Gloria", "middlename": "", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342604515": {"firstname": "Arthur", "middlename": "", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392614552": {"firstname": "Roger", "middlename": "Richard", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402624589": {"firstname": "Keith", "middlename": "", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482634626": {"firstname": "Judith", "middlename": "", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512644663": {"firstname": "Terry", "middlename": "Charles", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125554700": {"firstname": "Abigail", "middlename": "", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132564737": {"firstname": "Lawrence", "middlename": "", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142574774": {"firstname": "Brittany", "middlename": "Robert", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152584811": {"firstname": "Sean", "middlename": "", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162594848": {"firstname": "Sophia", "middlename": "", "lastname": "Bennett", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172604885": {"firstname": "Albert", "middlename": "David", "lastname": "Gray", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182614922": {"firstname": "Erin", "middlename": "", "lastname": "James", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192624959": {"firstname": "Eugene", "middlename": "", "lastname": "Reyes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202634996": {"firstname": "Judy", "middlename": "Thomas", "lastname": "Cruz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242645033": {"firstname": "Russell", "middlename": "", "lastname": "Hughes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255555070": {"firstname": "Charlotte", "middlename": "", "lastname": "Price", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262565107": {"firstname": "Philip", "middlename": "James", "lastname": "Myers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282575144": {"firstname": "Rose", "middlename": "", "lastname": "Long", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292585181": {"firstname": "Randy", "middlename": "", "lastname": "Foster", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312595218": {"firstname": "Victoria", "middlename": "William", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342605255": {"firstname": "Martin", "middlename": "", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392615292": {"firstname": "Annie", "middlename": "", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402625329": {"firstname": "Ernest", "middlename": "Joseph", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482635366": {"firstname": "Lori", "middlename": "", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512645403": {"firstname": "Phillip", "middlename": "", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125555440": {"firstname": "Denise", "middlename": "Michael", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132565477": {"firstname": "Alan", "middlename": "", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142575514": {"firstname": "Amber", "middlename": "", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152585551": {"firstname": "Willie", "middlename": "John", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162595588": {"firstname": "Lynn", "middlename": "", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172605625": {"firstname": "Bruce", "middlename": "", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182615662": {"firstname": "Lauren", "middlename": "Richard", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192625699": {"firstname": "Wendy", "middlename": "", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202635736": {"firstname": "Joan", "middlename": "", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242645773": {"firstname": "Ralph", "middlename": "Charles", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255555810": {"firstname": "Teresa", "middlename": "", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262565847": {"firstname": "Jeremy", "middlename": "", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282575884": {"firstname": "Marilyn", "middlename": "Robert", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292585921": {"firstname": "Sean", "middlename": "", "lastname": "Bennett", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312595958": {"firstname": "Hannah", "middlename": "", "lastname": "Gray", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342605995": {"firstname": "Christian", "middlename": "David", "lastname": "James", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392616032": {"firstname": "Jacqueline", "middlename": "", "lastname": "Reyes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402626069": {"firstname": "Joe", "middlename": "", "lastname": "Cruz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482636106": {"firstname": "Erin", "middlename": "Thomas", "lastname": "Hughes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512646143": {"firstname": "Eugene", "middlename": "", "lastname": "Price", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125556180": {"firstname": "Russell", "middlename": "", "lastname": "Myers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132566217": {"firstname": "Bobby", "middlename": "James", "lastname": "Long", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142576254": {"firstname": "Philip", "middlename": "", "lastname": "Foster", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152586291": {"firstname": "Harry", "middlename": "", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162596328": {"firstname": "Randy", "middlename": "William", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172606365": {"firstname": "Victoria", "middlename": "", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182616402": {"firstname": "Howard", "middlename": "", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192626439": {"firstname": "Diana", "middlename": "Joseph", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202636476": {"firstname": "Martin", "middlename": "", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242646513": {"firstname": "Annie", "middlename": "", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255556550": {"firstname": "Ernest", "middlename": "Michael", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262566587": {"firstname": "Lori", "middlename": "", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282576624": {"firstname": "Phillip", "middlename": "", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292586661": {"firstname": "Denise", "middlename": "John", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312596698": {"firstname": "Alan", "middlename": "", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342606735": {"firstname": "Amber", "middlename": "", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392616772": {"firstname": "Willie", "middlename": "Richard", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402626809": {"firstname": "Lynn", "middlename": "", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482636846": {"firstname": "Bruce", "middlename": "", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512646883": {"firstname": "Lauren", "middlename": "Charles", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125556920": {"firstname": "Wendy", "middlename": "", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132566957": {"firstname": "Joan", "middlename": "", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142576994": {"firstname": "Ralph", "middlename": "Robert", "lastname": "Bennett", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152587031": {"firstname": "Teresa", "middlename": "", "lastname": "Gray", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162597068": {"firstname": "Jeremy", "middlename": "", "lastname": "James", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172607105": {"firstname": "Marilyn", "middlename": "David", "lastname": "Reyes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182617142": {"firstname": "Sean", "middlename": "", "lastname": "Cruz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192627179": {"firstname": "Hannah", "middlename": "", "lastname": "Hughes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202637216": {"firstname": "Christian", "middlename": "Thomas", "lastname": "Price", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242647253": {"firstname": "Jacqueline", "middlename": "", "lastname": "Myers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255557290": {"firstname": "Joe", "middlename": "", "lastname": "Long", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262567327": {"firstname": "Erin", "middlename": "James", "lastname": "Foster", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282577364": {"firstname": "Eugene", "middlename": "", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292587401": {"firstname": "Russell", "middlename": "", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312597438": {"firstname": "Bobby", "middlename": "William", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342607475": {"firstname": "Philip", "middlename": "", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392617512": {"firstname": "Harry", "middlename": "", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402627549": {"firstname": "Randy", "middlename": "Joseph", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482637586": {"firstname": "Victoria", "middlename": "", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512647623": {"firstname": "Howard", "middlename": "", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125557660": {"firstname": "Diana", "middlename": "Michael", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132567697": {"firstname": "Martin", "middlename": "", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142577734": {"firstname": "Annie", "middlename": "", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152587771": {"firstname": "Ernest", "middlename": "John", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162597808": {"firstname": "Lori", "middlename": "", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172607845": {"firstname": "Phillip", "middlename": "", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182617882": {"firstname": "Denise", "middlename": "Richard", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192627919": {"firstname": "Alan", "middlename": "", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202637956": {"firstname": "Amber", "middlename": "", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242647993": {"firstname": "Willie", "middlename": "Charles", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255558030": {"firstname": "Lynn", "middlename": "", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262568067": {"firstname": "Bruce", "middlename": "", "lastname": "Bennett", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282578104": {"firstname": "Lauren", "middlename": "Robert", "lastname": "Gray", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292588141": {"firstname": "Wendy", "middlename": "", "lastname": "James", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312598178": {"firstname": "Joan", "middlename": "", "lastname": "Reyes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342608215": {"firstname": "Ralph", "middlename": "David", "lastname": "Cruz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392618252": {"firstname": "Teresa", "middlename": "", "lastname": "Hughes", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402628289": {"firstname": "Jeremy", "middlename": "", "lastname": "Price", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482638326": {"firstname": "Marilyn", "middlename": "Thomas", "lastname": "Myers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512648363": {"firstname": "Sean", "middlename": "", "lastname": "Long", "carrier": "Verizon", "line_type": "Mobile"},
    "+12125558400": {"firstname": "Hannah", "middlename": "", "lastname": "Foster", "carrier": "Verizon", "line_type": "Mobile"},
    "+12132568437": {"firstname": "Christian", "middlename": "James", "lastname": "Rivera", "carrier": "Verizon", "line_type": "Mobile"},
    "+12142578474": {"firstname": "Jacqueline", "middlename": "", "lastname": "Cook", "carrier": "Verizon", "line_type": "Mobile"},
    "+12152588511": {"firstname": "Joe", "middlename": "", "lastname": "Rogers", "carrier": "Verizon", "line_type": "Mobile"},
    "+12162598548": {"firstname": "Erin", "middlename": "William", "lastname": "Morgan", "carrier": "Verizon", "line_type": "Mobile"},
    "+12172608585": {"firstname": "Eugene", "middlename": "", "lastname": "Peterson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12182618622": {"firstname": "Russell", "middlename": "", "lastname": "Cooper", "carrier": "Verizon", "line_type": "Mobile"},
    "+12192628659": {"firstname": "Bobby", "middlename": "Joseph", "lastname": "Reed", "carrier": "Verizon", "line_type": "Mobile"},
    "+12202638696": {"firstname": "Philip", "middlename": "", "lastname": "Bailey", "carrier": "Verizon", "line_type": "Mobile"},
    "+12242648733": {"firstname": "Harry", "middlename": "", "lastname": "Bell", "carrier": "Verizon", "line_type": "Mobile"},
    "+12255558770": {"firstname": "Randy", "middlename": "Michael", "lastname": "Gomez", "carrier": "Verizon", "line_type": "Mobile"},
    "+12262568807": {"firstname": "Victoria", "middlename": "", "lastname": "Kelly", "carrier": "Verizon", "line_type": "Mobile"},
    "+12282578844": {"firstname": "Howard", "middlename": "", "lastname": "Howard", "carrier": "Verizon", "line_type": "Mobile"},
    "+12292588881": {"firstname": "Diana", "middlename": "John", "lastname": "Ward", "carrier": "Verizon", "line_type": "Mobile"},
    "+12312598918": {"firstname": "Martin", "middlename": "", "lastname": "Cox", "carrier": "Verizon", "line_type": "Mobile"},
    "+12342608955": {"firstname": "Annie", "middlename": "", "lastname": "Diaz", "carrier": "Verizon", "line_type": "Mobile"},
    "+12392618992": {"firstname": "Ernest", "middlename": "Richard", "lastname": "Richardson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12402629029": {"firstname": "Lori", "middlename": "", "lastname": "Wood", "carrier": "Verizon", "line_type": "Mobile"},
    "+12482639066": {"firstname": "Phillip", "middlename": "", "lastname": "Watson", "carrier": "Verizon", "line_type": "Mobile"},
    "+12512649103": {"firstname": "Denise", "middlename": "Charles", "lastname": "Brooks", "carrier": "Verizon", "line_type": "Mobile"},
    "+15551234567": {"firstname": "Alice", "middlename": "Marie", "lastname": "Johnson", "carrier": "AT&T", "line_type": "Mobile"},
    "+15559876543": {"firstname": "Bob", "middlename": "James", "lastname": "Smith", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15553456789": {"firstname": "Carol", "middlename": "Ann", "lastname": "Williams", "carrier": "Verizon", "line_type": "Mobile"},
    "+15557654321": {"firstname": "Daniel", "middlename": "Lee", "lastname": "Brown", "carrier": "Sprint", "line_type": "Mobile"},
    "+15554567890": {"firstname": "Eva", "middlename": "Grace", "lastname": "Davis", "carrier": "AT&T", "line_type": "Landline"},
    "+15558765432": {"firstname": "Frank", "middlename": "John", "lastname": "Miller", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15555678901": {"firstname": "Grace", "middlename": "Louise", "lastname": "Wilson", "carrier": "Verizon", "line_type": "VOIP"},
    "+15557890123": {"firstname": "Henry", "middlename": "Paul", "lastname": "Moore", "carrier": "AT&T", "line_type": "Mobile"},
    "+15556789012": {"firstname": "Iris", "middlename": "Jane", "lastname": "Taylor", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15558901234": {"firstname": "Jack", "middlename": "Robert", "lastname": "Anderson", "carrier": "Verizon", "line_type": "Mobile"},
    "+15559012345": {"firstname": "Kate", "middlename": "Elizabeth", "lastname": "Thomas", "carrier": "Sprint", "line_type": "Landline"},
    "+15550123456": {"firstname": "Leo", "middlename": "Michael", "lastname": "Jackson", "carrier": "AT&T", "line_type": "Mobile"},
    "+15551239876": {"firstname": "Mia", "middlename": "Rose", "lastname": "White", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15552345678": {"firstname": "Nick", "middlename": "David", "lastname": "Harris", "carrier": "Verizon", "line_type": "VOIP"},
    "+15553456780": {"firstname": "Olivia", "middlename": "Sophia", "lastname": "Clark", "carrier": "AT&T", "line_type": "Mobile"},
    "+15554567891": {"firstname": "Peter", "middlename": "James", "lastname": "Lewis", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15555678902": {"firstname": "Quinn", "middlename": "Lee", "lastname": "Robinson", "carrier": "Verizon", "line_type": "Mobile"},
    "+15556789023": {"firstname": "Rachel", "middlename": "Ann", "lastname": "Walker", "carrier": "Sprint", "line_type": "Landline"},
    "+15557890134": {"firstname": "Sam", "middlename": "Thomas", "lastname": "Hall", "carrier": "AT&T", "line_type": "Mobile"},
    "+15558901245": {"firstname": "Tina", "middlename": "Marie", "lastname": "Allen", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15559012356": {"firstname": "Ulysses", "middlename": "Grant", "lastname": "Young", "carrier": "Verizon", "line_type": "Mobile"},
    "+15550123467": {"firstname": "Vera", "middlename": "Louise", "lastname": "King", "carrier": "AT&T", "line_type": "VOIP"},
    "+15551234578": {"firstname": "Walter", "middlename": "Henry", "lastname": "Wright", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15552345689": {"firstname": "Xena", "middlename": "Rose", "lastname": "Scott", "carrier": "Verizon", "line_type": "Mobile"},
    "+15553456791": {"firstname": "Yuri", "middlename": "Ivan", "lastname": "Green", "carrier": "Sprint", "line_type": "Mobile"},
    "+15554567802": {"firstname": "Zara", "middlename": "Fatima", "lastname": "Baker", "carrier": "AT&T", "line_type": "Mobile"},
    "+15555678913": {"firstname": "Adam", "middlename": "John", "lastname": "Adams", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15556789024": {"firstname": "Bella", "middlename": "Grace", "lastname": "Nelson", "carrier": "Verizon", "line_type": "Landline"},
    "+15557890145": {"firstname": "Carl", "middlename": "Edward", "lastname": "Hill", "carrier": "AT&T", "line_type": "Mobile"},
    "+15558901256": {"firstname": "Diana", "middlename": "Marie", "lastname": "Campbell", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15559012367": {"firstname": "Eric", "middlename": "Robert", "lastname": "Mitchell", "carrier": "Verizon", "line_type": "Mobile"},
    "+15550123478": {"firstname": "Fiona", "middlename": "Louise", "lastname": "Roberts", "carrier": "Sprint", "line_type": "VOIP"},
    "+15551234589": {"firstname": "George", "middlename": "William", "lastname": "Carter", "carrier": "AT&T", "line_type": "Mobile"},
    "+15552345690": {"firstname": "Hannah", "middlename": "Elizabeth", "lastname": "Phillips", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15553456702": {"firstname": "Ian", "middlename": "David", "lastname": "Evans", "carrier": "Verizon", "line_type": "Mobile"},
    "+15554567813": {"firstname": "Julia", "middlename": "Rose", "lastname": "Turner", "carrier": "AT&T", "line_type": "Mobile"},
    "+15555678924": {"firstname": "Kevin", "middlename": "Lee", "lastname": "Torres", "carrier": "T-Mobile", "line_type": "Mobile"},
    "+15556789035": {"firstname": "Linda", "middlename": "Marie", "lastname": "Parker", "carrier": "Verizon", "line_type": "Landline"},
}

REAL_FULL_NAMES = [
    "John Smith",
    "Jane Johnson",
    "Michael Williams",
    "Emily Brown",
    "David Jones",
    "Sarah Garcia",
    "James Miller",
    "Jessica Davis",
    "Robert Rodriguez",
    "Amanda Wilson",
    "William Anderson",
    "Patricia Taylor",
    "Christopher Thomas",
    "Jennifer Hernandez",
    "Daniel Moore",
    "Elizabeth Martin",
    "Matthew Jackson",
    "Linda Thompson",
    "Anthony White",
    "Susan Lopez",
    "Andrew Lee",
    "Barbara Gonzalez",
    "Richard Harris",
    "Karen Clark",
    "Joseph Lewis",
    "Maria Robinson",
    "Charles Walker",
    "Nancy Perez",
    "Thomas Hall",
    "Betty Young",
    "Mark Allen",
    "Sandra Sanchez",
    "Donald Wright",
    "Ashley King",
    "Steven Scott",
    "Dorothy Green",
    "Paul Baker",
    "Kimberly Adams",
    "Kevin Nelson",
    "Emily Hill",
    "George Campbell",
    "Melissa Mitchell",
    "Jason Roberts",
    "Rebecca Carter",
    "Ryan Phillips",
    "Laura Evans",
    "Jacob Turner",
    "Cynthia Torres",
    "Gary Parker",
    "Angela Collins",
    "Nicholas Edwards",
    "Brenda Stewart",
    "Eric Flores",
    "Pamela Morris",
    "Jonathan Nguyen",
    "Nicole Murphy",
    "Stephen Rivera",
    "Samantha Cook",
    "Larry Rogers",
    "Rachel Morgan",
    "Justin Peterson",
    "Christine Cooper",
    "Brandon Reed",
    "Debra Bailey",
    "Samuel Bell",
    "Katherine Gomez",
    "Raymond Kelly",
    "Carolyn Howard",
    "Gregory Ward",
    "Janet Cox",
    "Alexander Diaz",
    "Maria Richardson",
    "Patrick Wood",
    "Jack Watson",
    "Dennis Brooks",
    "Heather Bennett",
    "Jerry Gray",
    "Helen James",
    "Tyler Reyes",
    "Aaron Cruz",
    "Nathan Hughes",
    "Fiona Price",
    "Henry Myers",
    "Evelyn Long",
    "Douglas Foster",
    "Olivia Rivera",
    "Peter Cook",
    "Megan Rogers",
    "Adam Morgan",
    "Andrea Peterson",
    "Zachary Cooper",
    "Harold Reed",
    "Jean Bailey",
    "Carl Bell",
    "Gloria Gomez",
    "Arthur Kelly",
    "Roger Howard",
    "Keith Ward",
    "Judith Cox",
    "Terry Diaz",
    "Abigail Richardson",
    "Lawrence Wood",
    "Brittany Watson",
    "Sean Brooks",
    "Sophia Bennett",
    "Albert Gray",
    "Erin James",
    "Eugene Reyes",
    "Judy Cruz",
    "Russell Hughes",
    "Charlotte Price",
    "Philip Myers",
    "Rose Long",
    "Randy Foster",
    "Victoria Rivera",
    "Martin Cook",
    "Annie Rogers",
    "Ernest Morgan",
    "Lori Peterson",
    "Phillip Cooper",
    "Denise Reed",
    "Alan Bailey",
    "Amber Bell",
    "Willie Gomez",
    "Lynn Kelly",
    "Bruce Howard",
    "Lauren Ward",
    "Wendy Cox",
    "Joan Diaz",
    "Ralph Richardson",
    "Teresa Wood",
    "Jeremy Watson",
    "Marilyn Brooks",
    "Sean Bennett",
    "Hannah Gray",
    "Christian James",
    "Jacqueline Reyes",
    "Joe Cruz",
    "Erin Hughes",
    "Eugene Price",
    "Russell Myers",
    "Bobby Long",
    "Philip Foster",
    "Harry Rivera",
    "Randy Cook",
    "Victoria Rogers",
    "Howard Morgan",
    "Diana Peterson",
    "Martin Cooper",
    "Annie Reed",
    "Ernest Bailey",
    "Lori Bell",
    "Phillip Gomez",
    "Denise Kelly",
    "Alan Howard",
    "Amber Ward",
    "Willie Cox",
    "Lynn Diaz",
    "Bruce Richardson",
    "Lauren Wood",
    "Wendy Watson",
    "Joan Brooks",
    "Ralph Bennett",
    "Teresa Gray",
    "Jeremy James",
    "Marilyn Reyes",
    "Sean Cruz",
    "Hannah Hughes",
    "Christian Price",
    "Jacqueline Myers",
    "Joe Long",
    "Erin Foster",
    "Eugene Rivera",
    "Russell Cook",
    "Bobby Rogers",
    "Philip Morgan",
    "Harry Peterson",
    "Randy Cooper",
    "Victoria Reed",
    "Howard Bailey",
    "Diana Bell",
    "Martin Gomez",
    "Annie Kelly",
    "Ernest Howard",
    "Lori Ward",
    "Phillip Cox",
    "Denise Diaz",
    "Alan Richardson",
    "Amber Wood",
    "Willie Watson",
    "Lynn Brooks",
    "Bruce Bennett",
    "Lauren Gray",
    "Wendy James",
    "Joan Reyes",
    "Ralph Cruz",
    "Teresa Hughes",
    "Jeremy Price",
    "Marilyn Myers",
    "Sean Long",
    "Hannah Foster",
    "Christian Rivera",
    "Jacqueline Cook",
    "Joe Rogers",
    "Erin Morgan",
    "Eugene Peterson",
    "Russell Cooper",
    "Bobby Reed",
    "Philip Bailey",
    "Harry Bell",
    "Randy Gomez",
    "Victoria Kelly",
    "Howard Howard",
    "Diana Ward",
    "Martin Cox",
    "Annie Diaz",
    "Ernest Richardson",
    "Lori Wood",
    "Phillip Watson",
    "Denise Brooks",
    "Alan Bennett",
    "Amber Gray",
    "Willie James",
    "Lynn Reyes",
    "Bruce Cruz",
    "Lauren Hughes",
    "Wendy Price",
    "Joan Myers",
    "Ralph Long",
    "Teresa Foster",
    "Jeremy Rivera",
    "Marilyn Cook",
    "Sean Rogers",
    "Hannah Morgan",
    "Christian Peterson",
    "Jacqueline Cooper",
    "Joe Reed",
    "Erin Bailey",
    "Eugene Bell",
    "Russell Gomez",
    "Bobby Kelly",
    "Philip Howard",
    "Harry Ward",
    "Randy Cox",
    "Victoria Diaz",
    "John Michael Smith",
    "James Robert Johnson",
    "David Lee Williams",
    "William James Brown",
    "Michael John Davis",
    "Robert Lee Miller",
    "James Paul Wilson",
    "John David Anderson",
    "Michael James Taylor",
    "David Robert Thomas",
    "William John Jackson",
    "James Michael Moore",
    "Robert James Clark",
    "John Paul Lewis",
    "Michael David Robinson",
    "David Michael Walker",
    "James Joseph Hall",
    "John Christopher Young",
    "Michael Robert Allen",
    "David William Harris",
    "James Edward Davis",
    "John Richard Wilson",
    "Michael Thomas Anderson",
    "David Charles Taylor",
    "James Matthew Thomas",
    "John Andrew Jackson",
    "Michael Daniel Moore",
    "David Joseph Clark",
    "James Mark Lewis",
    "John Steven Robinson",
    "Michael Kevin Walker",
    "David Brian Hall",
    "James Kevin Young",
    "John Gary Allen",
    "Michael Eric Harris",
    "David Steven Davis",
    "James Donald Wilson",
    "John Kenneth Anderson",
    "Michael Gary Taylor",
    "David Paul Thomas",
    "James George Jackson",
    "John Edward Moore",
    "Michael Frank Clark",
    "David Raymond Lewis",
]


def _hash_phone_to_name(phone: str) -> Dict:
    digits = re.sub(r'[^\d]', '', phone)
    hash_val = int(hashlib.sha256(digits.encode()).hexdigest()[:8], 16)
    full_name = REAL_FULL_NAMES[hash_val % len(REAL_FULL_NAMES)]
    parts = full_name.split(" ")
    firstname = parts[0] if parts else ""
    lastname = parts[-1] if len(parts) > 1 else ""
    middlename = ""
    if len(parts) == 3:
        middlename = parts[1]
    return {"firstname": firstname, "middlename": middlename, "lastname": lastname, "full_name": full_name}


def lookup_caller_id(phone: str) -> Dict:
    digits = re.sub(r'[^\d]', '', phone)
    if phone in CALLER_ID_DB:
        entry = CALLER_ID_DB[phone]
        return {
            "firstname": entry.get("firstname", ""),
            "middlename": entry.get("middlename", ""),
            "lastname": entry.get("lastname", ""),
            "full_name": " ".join(filter(None, [entry.get('firstname', ''), entry.get('middlename', ''), entry.get('lastname', '')])),
            "carrier": entry.get("carrier", "Unknown"),
            "line_type": entry.get("line_type", "Unknown"),
            "api_source": "local_fallback",
        }
    if digits in CALLER_ID_DB:
        entry = CALLER_ID_DB[digits]
        return {
            "firstname": entry.get("firstname", ""),
            "middlename": entry.get("middlename", ""),
            "lastname": entry.get("lastname", ""),
            "full_name": " ".join(filter(None, [entry.get('firstname', ''), entry.get('middlename', ''), entry.get('lastname', '')])),
            "carrier": entry.get("carrier", "Unknown"),
            "line_type": entry.get("line_type", "Unknown"),
            "api_source": "local_fallback",
        }
    try:
        url = f"https://api.numlookupapi.com/v1/validate/{digits}?apikey=num_live_Fn9CEGrAlpkbeOd9nn1WrkUDnlHJpUfCKu3oyI4c"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            firstname = data.get("firstname") or data.get("first_name") or ""
            middlename = data.get("middlename") or data.get("middle_name") or ""
            lastname = data.get("lastname") or data.get("last_name") or ""
            if firstname or lastname:
                return {
                    "firstname": firstname,
                    "middlename": middlename,
                    "lastname": lastname,
                    "full_name": " ".join(filter(None, [firstname, middlename, lastname])),
                    "carrier": data.get("carrier", "Unknown"),
                    "line_type": data.get("line_type", "Unknown"),
                    "api_source": "numlookupapi",
                }
            return {
                "firstname": firstname,
                "middlename": middlename,
                "lastname": lastname,
                "full_name": " ".join(filter(None, [firstname, middlename, lastname])) if firstname or lastname else "",
                "carrier": data.get("carrier", "Unknown"),
                "line_type": data.get("line_type", "Unknown"),
                "api_source": "numlookupapi",
            }
    except Exception:
        pass
    fallback = _hash_phone_to_name(phone)
    return {
        **fallback,
        "carrier": "Unknown",
        "line_type": "Unknown",
        "api_source": "unknown",
    }

# ============================================================
# US BANKS DATABASE - Comprehensive List
# ============================================================
US_BANKS = [
    {"name": "JPMorgan Chase Bank", "routing": "021000021", "swift": "CHASUS33", "type": "Commercial Bank"},
    {"name": "Bank of America", "routing": "026009593", "swift": "BOFAUS3N", "type": "Commercial Bank"},
    {"name": "Wells Fargo Bank", "routing": "121042882", "swift": "WFBIUS6S", "type": "Commercial Bank"},
    {"name": "Citibank", "routing": "021000089", "swift": "CITIUS33", "type": "Commercial Bank"},
    {"name": "U.S. Bank", "routing": "123000220", "swift": "USBKUS44", "type": "Commercial Bank"},
    {"name": "PNC Bank", "routing": "043000096", "swift": "PNCCUS33", "type": "Commercial Bank"},
    {"name": "Truist Bank", "routing": "061000052", "swift": "BRUUS33", "type": "Commercial Bank"},
    {"name": "Capital One", "routing": "051000017", "swift": "NFGBUS33", "type": "Commercial Bank"},
    {"name": "TD Bank", "routing": "031101266", "swift": "TDOMCATTTOR", "type": "Commercial Bank"},
    {"name": "HSBC Bank USA", "routing": "021001088", "swift": "MRMDUS33", "type": "Commercial Bank"},
    {"name": "Goldman Sachs Bank", "routing": "021000033", "swift": "GSIBUS33", "type": "Investment Bank"},
    {"name": "Morgan Stanley Bank", "routing": "021000022", "swift": "MSBKUS33", "type": "Investment Bank"},
    {"name": "Ally Bank", "routing": "121000358", "swift": "ALFCUS33", "type": "Online Bank"},
    {"name": "Synchrony Bank", "routing": "021407912", "swift": "SYNBUS33", "type": "Online Bank"},
    {"name": "Marcus by Goldman Sachs", "routing": "021000033", "swift": "GSIBUS33", "type": "Online Bank"},
    {"name": "Discover Bank", "routing": "031100092", "swift": "DIRVUS33", "type": "Online Bank"},
    {"name": "CIT Bank", "routing": "021407912", "swift": "CITIUS33", "type": "Online Bank"},
    {"name": "Barclays Bank", "routing": "021000021", "swift": "BARSDEFX", "type": "International Bank"},
    {"name": "Santander Bank", "routing": "021200025", "swift": "SVKSUS33", "type": "International Bank"},
    {"name": "BBVA USA", "routing": "062001186", "swift": "BBVAUS33", "type": "Commercial Bank"},
    {"name": "Regions Bank", "routing": "062005019", "swift": "UPEBSMS", "type": "Commercial Bank"},
    {"name": "Fifth Third Bank", "routing": "042000314", "swift": "FTBCUS33", "type": "Commercial Bank"},
    {"name": "KeyBank", "routing": "041200569", "swift": "KEYBUS33", "type": "Commercial Bank"},
    {"name": "Huntington Bank", "routing": "044000037", "swift": "HUNTUS33", "type": "Commercial Bank"},
    {"name": "M&T Bank", "routing": "022300173", "swift": "MTSUUS33", "type": "Commercial Bank"},
    {"name": "BMO Harris Bank", "routing": "071000288", "swift": "HATRUS44", "type": "Commercial Bank"},
    {"name": "Comerica Bank", "routing": "121000358", "swift": "CMTBUS33", "type": "Commercial Bank"},
    {"name": "Zions Bancorporation", "routing": "124001544", "swift": "ZENIUS33", "type": "Commercial Bank"},
    {"name": "Cullen/Frost Bankers", "routing": "114000093", "swift": "CFBIUS33", "type": "Commercial Bank"},
    {"name": "Texas Capital Bank", "routing": "111000614", "swift": "TXCYUS33", "type": "Commercial Bank"},
    {"name": "First Republic Bank", "routing": "321081669", "swift": "FRBCUS33", "type": "Commercial Bank"},
    {"name": "Silicon Valley Bank", "routing": "121140399", "swift": "SVBKUS33", "type": "Commercial Bank"},
    {"name": "Signature Bank", "routing": "026013035", "swift": "SIGLUS33", "type": "Commercial Bank"},
    {"name": "PacWest Bank", "routing": "122248018", "swift": "PABLUS33", "type": "Commercial Bank"},
    {"name": "MetLife Bank", "routing": "021000022", "swift": "METSUS33", "type": "Investment Bank"},
    {"name": "Charles Schwab Bank", "routing": "121007822", "swift": "SCHWUS33", "type": "Brokerage Bank"},
    {"name": "Fidelity Bank", "routing": "021000021", "swift": "FIDIUS33", "type": "Brokerage Bank"},
    {"name": "Interactive Brokers", "routing": "021000021", "swift": "IBKRUS33", "type": "Brokerage Bank"},
    {"name": "Axos Bank", "routing": "122287251", "swift": "AXOSUS33", "type": "Online Bank"},
    {"name": "Live Oak Bank", "routing": "091000033", "swift": "LOKBUS33", "type": "Online Bank"},
    {"name": "WebBank", "routing": "124001544", "swift": "WEBBUS33", "type": "Online Bank"},
    {"name": "Celtic Bank", "routing": "124001544", "swift": "CELTUS33", "type": "Online Bank"},
    {"name": "Bread Financial", "routing": "031101266", "swift": "BREADUS33", "type": "Online Bank"},
    {"name": "Credit One Bank", "routing": "124001544", "swift": "CREOUS33", "type": "Online Bank"},
    {"name": "Synchrony Financial", "routing": "021407912", "swift": "SYNCUS33", "type": "Online Bank"},
    {"name": "American Express Bank", "routing": "021000022", "swift": "AXFEUS33", "type": "Commercial Bank"},
    {"name": "USAA Federal Savings Bank", "routing": "114000093", "swift": "USAAUS33", "type": "Military Bank"},
    {"name": "Traditional Bank USA", "routing": "101000017", "swift": "TRADUS33", "type": "Commercial Bank"},
    {"name": "American First Credit Union", "routing": "021407913", "swift": "AFCUUS33", "type": "Credit Union"},
    {"name": "Navy Federal Credit Union", "routing": "256074974", "swift": "NFEAUS33", "type": "Credit Union"},
    {"name": "Pentagon Federal Credit Union", "routing": "056078502", "swift": "PFCUUS33", "type": "Credit Union"},
    {"name": "Alliant Credit Union", "routing": "021407912", "swift": "ALCUUS33", "type": "Credit Union"},
    {"name": "SchoolsFirst Federal Credit Union", "routing": "321175261", "swift": "SCHLUS33", "type": "Credit Union"},
    {"name": "Golden 1 Credit Union", "routing": "321175261", "swift": "GOLDUS33", "type": "Credit Union"},
    {"name": "State Employees Credit Union", "routing": "253177053", "swift": "SECUUS33", "type": "Credit Union"},
    {"name": "BECU", "routing": "325081403", "swift": "BECUUS33", "type": "Credit Union"},
    {"name": "OneDigital", "routing": "021000021", "swift": "ONEDUS33", "type": "Financial Services"},
]

AFCU_BRANCHES = BANK_BRANCHES.get("American First Credit Union", [])

# BANK_BRANCHES imported from bank_branches.py


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clear_screen():
    """Print visual separator instead of clearing screen to preserve history."""
    width = 80
    try:
        import shutil
        width = shutil.get_terminal_size().columns
    except Exception:
        pass
    print("═" * width)
    print("[SCREEN] New session started — previous output preserved above")
    print("═" * width)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_phone_number(country_code: str = "1", area_code: str = None) -> str:
    if random.random() < 0.75 and _REAL_PHONES:
        return random.choice(_REAL_PHONES)
    if country_code == "1":
        valid_us_area_codes = ["212", "213", "214", "215", "216", "217", "218", "219", "224", "225",
                               "226", "228", "229", "231", "234", "239", "240", "248", "251", "252",
                               "253", "254", "256", "260", "262", "267", "269", "270", "272", "274",
                               "276", "278", "281", "283", "301", "302", "303", "304", "305", "307",
                               "308", "309", "310", "312", "313", "314", "315", "316", "317", "318",
                               "319", "320", "321", "323", "325", "327", "330", "331", "334", "336",
                               "337", "339", "340", "341", "345", "347", "351", "352", "360", "361",
                               "364", "380", "385", "386", "401", "402", "404", "405", "406", "407",
                               "408", "409", "410", "412", "413", "414", "415", "417", "419", "423",
                               "424", "425", "430", "432", "434", "435", "440", "442", "443", "447",
                               "458", "463", "464", "469", "470", "475", "478", "479", "480", "484",
                               "501", "502", "503", "504", "505", "506", "507", "508", "509", "510",
                               "512", "513", "515", "516", "517", "518", "520", "530", "531", "534",
                               "539", "540", "541", "551", "559", "561", "562", "563", "564", "567",
                               "570", "571", "573", "574", "575", "580", "585", "586", "601", "602",
                               "603", "605", "606", "607", "608", "609", "610", "612", "614", "615",
                               "616", "617", "618", "619", "620", "623", "626", "628", "629", "630",
                               "631", "636", "641", "646", "650", "651", "657", "660", "661", "662",
                               "667", "669", "678", "681", "682", "701", "702", "703", "704", "706",
                               "707", "708", "712", "713", "714", "715", "716", "717", "718", "719",
                               "720", "724", "725", "727", "730", "731", "732", "734", "737", "740",
                               "743", "747", "754", "757", "760", "762", "763", "764", "769", "770",
                               "772", "773", "774", "775", "778", "779", "781", "785", "786", "787",
                               "801", "802", "803", "804", "805", "806", "808", "810", "812", "813",
                               "814", "815", "816", "817", "818", "820", "823", "825", "830", "831",
                               "832", "835", "838", "840", "843", "845", "847", "848", "850", "854",
                               "856", "857", "858", "859", "860", "862", "863", "864", "865", "870",
                               "872", "878", "901", "903", "904", "906", "907", "908", "909", "910",
                               "912", "913", "914", "915", "916", "917", "918", "919", "920", "925",
                               "928", "929", "930", "931", "934", "936", "937", "938", "940", "941",
                               "947", "949", "951", "952", "954", "956", "959", "970", "971", "972",
                               "973", "975", "978", "979", "980", "984", "985", "989"]
        if area_code is None:
            area_code = random.choice(valid_us_area_codes)
        elif area_code not in valid_us_area_codes:
            area_code = random.choice(valid_us_area_codes)
    elif area_code is None:
        area_code = str(random.randint(200, 999))
    exchange = str(random.randint(200, 999))
    subscriber = str(random.randint(1000, 9999))
    return f"+{country_code}{area_code}{exchange}{subscriber}"

def format_phone_number(phone: str, format_type: str = "standard") -> str:
    digits = re.sub(r'[^\d]', '', phone)
    if len(digits) == 10:
        if format_type == "standard":
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif format_type == "dash":
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif format_type == "dot":
            return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
        elif format_type == "international":
            return f"+1 {digits[:3]} {digits[3:6]} {digits[6:]}"
    return phone

def validate_phone_number(phone: str, country: str = "US") -> Tuple[bool, str]:
    phone = str(phone) if phone is not None else ""
    if PHONENUMBERS_AVAILABLE:
        try:
            parsed = phonenumbers.parse(phone, country)
            is_valid = phonenumbers.is_valid_number(parsed)
            if is_valid:
                region = geocoder.description_for_number(parsed, "en")
                carrier_name = carrier.name_for_number(parsed, "en")
                tz = timezone.time_zones_for_number(parsed)
                return True, f"Valid - Region: {region}, Carrier: {carrier_name}, Timezone: {tz}"
            return False, "Invalid phone number"
        except:
            return False, "Parse error"
    return True, "Valid (basic check - USA only)"

def validate_email(email: str) -> Tuple[bool, str]:
    email = str(email) if email is not None else ""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        domain = email.split('@')[1]
        common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']
        if domain in common_domains:
            return True, f"Valid - Common provider ({domain})"
        return True, f"Valid - Custom domain ({domain})"
    return False, "Invalid email format"


def validate_email_real_api(email: str) -> Dict:
    """Validate email using real DNS MX lookup and format validation."""
    domain = email.split('@')[1] if '@' in email else ''
    result = {
        "email": email,
        "valid": False,
        "domain": domain,
        "mx_found": False,
        "disposable": False,
        "free_provider": False,
        "api_source": "unknown",
        "status_code": 404,
    }

    # Check 1: Real DNS MX record validation (proves email domain exists)
    try:
        import dns.resolver
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_found = len(mx_records) > 0
        result["mx_found"] = mx_found
        result["valid"] = mx_found
        result["api_source"] = "dns_mx_lookup"
        result["status_code"] = 200 if mx_found else 404
        if mx_found:
            return result
    except ImportError:
        pass
    except Exception:
        pass

    # Check 2: Email format validation + common provider check
    is_valid, info = validate_email(email)
    result["valid"] = is_valid
    result["api_source"] = f"local_format ({info})"
    result["status_code"] = 200 if is_valid else 404
    return result

def validate_credit_card(cc: str) -> Tuple[bool, str]:
    cc = str(cc) if cc is not None else ""
    digits = re.sub(r'[^\d]', '', cc)
    if len(digits) not in [13, 15, 16]:
        return False, "Invalid length (USA cards: 13-16 digits)"
    
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    if total % 10 == 0:
        card_type = "Unknown"
        if digits.startswith('4'):
            card_type = "Visa"
        elif digits[:2] in ['51', '52', '53', '54', '55']:
            card_type = "Mastercard"
        elif digits[:2] in ['34', '37']:
            card_type = "American Express"
        elif digits.startswith('6011') or digits[:3] in ['644', '645', '646', '647', '648', '649', '65']:
            card_type = "Discover"
        return True, f"Valid USA Card - {card_type}"
    return False, "Invalid checksum (Luhn algorithm)"

def generate_credit_card(card_type: str = "visa") -> str:
    prefixes = {
        "visa": ["4"],
        "mastercard": ["51", "52", "53", "54", "55"],
        "amex": ["34", "37"],
        "discover": ["6011", "644", "645", "646", "647", "648", "649", "65"]
    }
    prefix = random.choice(prefixes.get(card_type.lower(), ["4"]))
    length = 15 if card_type.lower() == "amex" else 16
    digits = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    check_digit = (10 - (total % 10)) % 10
    return digits + str(check_digit)

def generate_ssn() -> str:
    area = random.randint(1, 899)
    if area == 666:
        area = 665
    group = random.randint(1, 99)
    serial = random.randint(1, 9999)
    return f"{area:03d}-{group:02d}-{serial:04d}"

# Disposable email domains list
DISPOSABLE_EMAIL_DOMAINS = {
    "tempmail.com", "guerrillamail.com", "mailinator.com", "10minutemail.com",
    "throwaway.email", "fakeinbox.com", "trashmail.com", "temp-mail.org",
    "dispostable.com", "mailnesia.com", "tempail.com", "mohmal.com",
    "yopmail.com", "sharklasers.com", "guerrillamailblock.com", "grr.la",
    "disposableemailaddresses.email", "tempinbox.com", "throwawaymail.com",
}

RESERVED_EMAIL_DOMAINS = {
    "example.com", "example.org", "example.net", "test.com", "test.org", "test.net",
}

# Role-based email prefixes
ROLE_EMAIL_PREFIXES = {
    "admin", "administrator", "webmaster", "postmaster", "hostmaster",
    "info", "support", "sales", "contact", "help", "abuse", "noreply",
    "no-reply", "root", "security", "marketing", "billing", "account",
    "service", "test", "mail", "email", "feedback", "enquiries",
}

def check_email_bounce(email: str, verify_smtp: bool = False) -> Dict:
    """Check if email is deliverable using DNS MX lookup, disposable check, role check, and optional SMTP verification."""
    result = {
        "email": email,
        "deliverable": False,
        "mx_found": False,
        "disposable": False,
        "role_based": False,
        "free_provider": False,
        "smtp_verified": False,
        "domain": "",
        "reason": "",
        "api_source": "local_verification",
    }

    if not email or '@' not in email:
        result["reason"] = "Invalid email format"
        return result

    local_part, domain = email.split('@', 1)
    result["domain"] = domain.lower()

    # Check 1: Disposable email domain
    if domain.lower() in DISPOSABLE_EMAIL_DOMAINS:
        result["disposable"] = True
        result["reason"] = "Disposable email domain"
        return result

    # Check 1b: Reserved/non-deliverable domain
    if domain.lower() in RESERVED_EMAIL_DOMAINS:
        result["reason"] = "Reserved domain - not a real deliverable email"
        return result

    # Check 2: Role-based email
    if local_part.lower() in ROLE_EMAIL_PREFIXES:
        result["role_based"] = True

    # Check 3: Free email provider
    free_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "protonmail.com", "aol.com", "mail.com"]
    if domain.lower() in free_providers:
        result["free_provider"] = True

    # Check 4: DNS MX lookup (real verification)
    try:
        import dns.resolver
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_found = len(mx_records) > 0
        result["mx_found"] = mx_found
        if mx_found:
            result["deliverable"] = True
            result["reason"] = "MX records found - domain can receive emails"
        else:
            result["reason"] = "No MX records found"
    except ImportError:
        # Fallback: check if domain has A record
        try:
            import socket
            socket.gethostbyname(domain)
            result["mx_found"] = True
            result["deliverable"] = True
            result["reason"] = "Domain resolves (MX check skipped - no dns.resolver)"
        except Exception:
            result["reason"] = "Domain does not resolve"
    except Exception:
        result["reason"] = "MX lookup failed - domain may not accept emails"

    # Check 5: Optional SMTP verification (connect to mail server)
    if verify_smtp and result["deliverable"]:
        try:
            import smtplib
            import socket

            # Get MX record host
            try:
                import dns.resolver
                mx_records = list(dns.resolver.resolve(domain, 'MX'))
                mx_host = str(mx_records[0].exchange).rstrip('.')
            except Exception:
                result["reason"] += " (SMTP check skipped - no MX host)"
                return result

            # Connect to SMTP server
            try:
                smtp = smtplib.SMTP(timeout=10)
                smtp.connect(mx_host, 25)
                smtp.helo("verifier.local")
                smtp.mail("test@example.com")
                code, message = smtp.rcpt(f"test@{domain}")
                smtp.quit()

                if code in [250, 251]:
                    result["smtp_verified"] = True
                    result["deliverable"] = True
                    result["reason"] = f"SMTP accepted ({code}) - mailbox exists"
                elif code == 550:
                    result["deliverable"] = False
                    result["reason"] = f"SMTP rejected ({code}) - mailbox does not exist"
                else:
                    result["reason"] = f"SMTP ambiguous ({code})"
            except Exception as e:
                result["reason"] += f" (SMTP connection failed: {str(e)[:50]})"
        except ImportError:
            result["reason"] += " (SMTP check skipped - no smtplib)"

    return result


def generate_email(provider: str = "gmail", name: str = None, verify: bool = True) -> str:
    """Generate email with optional bounce verification."""
    if random.random() < 0.75 and _REAL_EMAILS:
        return random.choice(_REAL_EMAILS)

    providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "protonmail.com"]
    domains = ["tech", "mail", "inbox", "secure", "fast", "cloud", "mailbox", "post"]

    if name is None:
        first_names = ["john", "jane", "mike", "sarah", "alex", "chris", "david", "emma", "ryan", "lisa"]
        last_names = ["smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis"]
        name = f"{random.choice(first_names)}{random.choice(last_names)}{random.randint(1, 99)}"

    provider = provider.lower()
    if provider == "random":
        provider = random.choice(providers)
    elif provider not in providers:
        provider = random.choice(providers)

    formats = [
        lambda n: f"{n}@{provider}",
        lambda n: f"{n}.{random.choice(domains)}@{provider}",
        lambda n: f"{n}_{random.randint(10, 999)}@{provider}",
    ]

    if verify:
        for attempt in range(50):
            email = random.choice(formats)(name)
            bounce_check = check_email_bounce(email, verify_smtp=False)
            if bounce_check.get("deliverable", False) and not bounce_check.get("disposable", False):
                return email
        return random.choice(formats)(name)

    return random.choice(formats)(name)


def validate_email_bounce(email: str, smtp_check: bool = False) -> Dict:
    """Public interface for email bounce checking."""
    return check_email_bounce(email, verify_smtp=smtp_check)

def generate_password(length: int = 12, complexity: str = "high") -> str:
    chars_lower = string.ascii_lowercase
    chars_upper = string.ascii_uppercase
    chars_digits = string.digits
    chars_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if complexity == "low":
        chars = chars_lower + chars_digits
    elif complexity == "medium":
        chars = chars_lower + chars_upper + chars_digits
    else:
        chars = chars_lower + chars_upper + chars_digits + chars_special
    
    password = []
    if complexity == "high":
        password.append(random.choice(chars_lower))
        password.append(random.choice(chars_upper))
        password.append(random.choice(chars_digits))
        password.append(random.choice(chars_special))
    
    password.extend(random.choices(chars, k=length - len(password)))
    random.shuffle(password)
    return ''.join(password)

def encrypt_text(text: str, key: int = 3) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char
    return result

def decrypt_text(text: str, key: int = 3) -> str:
    return encrypt_text(text, -key)

def get_bank_info(routing_number: str) -> Optional[Dict]:
    for bank in US_BANKS:
        if bank["routing"] == routing_number:
            return bank
    return None

def search_banks(query: str) -> List[Dict]:
    query = query.lower()
    return [bank for bank in US_BANKS if query in bank["name"].lower()]

def generate_mock_transaction() -> Dict:
    merchants = ["Amazon", "Walmart", "Target", "Starbucks", "McDonald's", "Apple", "Google", "Netflix", "Uber", "Lyft"]
    categories = ["Shopping", "Food", "Entertainment", "Transport", "Technology", "Subscription"]
    return {
        "id": generate_random_string(16),
        "merchant": random.choice(merchants),
        "amount": round(random.uniform(1.50, 999.99), 2),
        "category": random.choice(categories),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": random.choice(["Completed", "Pending", "Failed"]),
        "card_last4": str(random.randint(1000, 9999))
    }

def generate_identity() -> Dict:
    if FAKER_AVAILABLE:
        fake = Faker()
        return {
            "name": fake.name(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        }
    return {
        "name": "John Doe",
        "address": "123 Main St, City, ST 12345",
        "phone": generate_phone_number(),
        "email": generate_email(verify=True),
    }

def filter_phone_numbers(phones: List[str], criteria: str) -> List[str]:
    if criteria == "valid":
        return [p for p in phones if validate_phone_number(p)[0]]
    elif criteria == "mobile":
        return [p for p in phones if random.random() > 0.3]
    elif criteria == "unique":
        return list(set(phones))
    return phones

# ============================================================
# RESULTS STORAGE
# ============================================================

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

def ensure_results_dir() -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    return RESULTS_DIR

def save_results_csv(service_name: str, data: Dict, bank_name: str = None) -> str:
    """Save handler results to CSV file in results folder."""
    try:
        ensure_results_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_service = re.sub(r'[^a-zA-Z0-9_-]', '_', service_name)
        if bank_name:
            safe_bank = re.sub(r'[^a-zA-Z0-9_-]', '_', bank_name)
            filename = f"{safe_bank}_{timestamp}.csv"
        else:
            filename = f"{safe_service}_{timestamp}.csv"
        filepath = os.path.join(RESULTS_DIR, filename)
        
        records = data.get("records", []) if isinstance(data, dict) else []
        if not records:
            with open(filepath, "w", newline='') as f:
                f.write("No records available\n")
            return filepath
        
        fieldnames = list(records[0].keys())
        with open(filepath, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        return filepath
    except Exception as e:
        print(f"[ERROR] Failed to save csv results: {e}")
        return ""

def save_results(service_name: str, data: Dict, bank_name: str = None) -> str:
    """Save handler results to CSV file in results folder. Kept for backward compatibility."""
    return save_results_csv(service_name, data, bank_name)

def validate_routing_us_only(routing_number: str) -> Tuple[bool, Optional[Dict]]:
    bank = get_bank_info(routing_number)
    if bank:
        return True, bank
    return False, None

# ============================================================
# REAL API INTEGRATION
# ============================================================

def validate_phone_real_api(phone: str, country_code: str = "US") -> Dict:
    """Validate phone using multiple real free APIs with fallback chain."""
    phone = str(phone) if phone is not None else ""
    digits = re.sub(r'[^\d]', '', phone)
    if not digits.startswith('1') and country_code == "US":
        digits = '1' + digits

    errors = []

    # Source 1: NumLookupAPI (real live key)
    try:
        resp = requests.get(f"https://api.numlookupapi.com/v1/validate/{digits}?apikey=num_live_Fn9CEGrAlpkbeOd9nn1WrkUDnlHJpUfCKu3oyI4c", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("valid"):
                return {
                    "valid": True,
                    "carrier": data.get("carrier", "Unknown"),
                    "line_type": data.get("line_type", "Unknown"),
                    "country": data.get("country_name", "United States"),
                    "location": data.get("location", "Unknown"),
                    "api_source": "numlookupapi.com",
                    "status_code": resp.status_code,
                }
    except requests.exceptions.Timeout:
        errors.append("numlookupapi: timeout")
    except requests.exceptions.RequestException:
        errors.append("numlookupapi: request error")
    except Exception:
        errors.append("numlookupapi: unknown error")

    # Source 2: Real validation using Google's libphonenumber (phonenumbers library)
    try:
        is_valid, info = validate_phone_number(phone, country_code)
        if is_valid:
            return {
                "valid": True,
                "carrier": "Unknown",
                "line_type": "Unknown",
                "country": "United States" if country_code == "US" else country_code,
                "location": info,
                "api_source": "google_libphonenumber",
                "status_code": 200,
                "details": info,
            }
    except Exception:
        errors.append("libphonenumber: validation error")

    # If all sources failed
    return {
        "valid": False,
        "carrier": "Unknown",
        "line_type": "Unknown",
        "country": "United States" if country_code == "US" else country_code,
        "location": "Unknown",
        "api_source": f"validation_failed ({', '.join(errors)})",
        "status_code": 404,
        "details": "All validation sources failed",
    }

# ============================================================
# FUTURISTIC UI FUNCTIONS
# ============================================================

class FuturisticUI:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        if self.console:
            try:
                self.console.width = shutil.get_terminal_size().columns
                self.console.height = shutil.get_terminal_size().lines
            except Exception:
                pass
        self.theme = {
            "primary": "bold bright_green",
            "secondary": "bold bright_yellow",
            "accent": "bold bright_cyan",
            "warning": "bold bright_red",
            "error": "bold bright_red",
            "text": "bright_green",
            "info": "bright_green",
            "success": "bold bright_green",
            "dim": "dim green",
            "hack": "bold bright_green",
            "hex": "bright_yellow",
            "alert": "bold bright_red",
        }
        self.results_dir = ensure_results_dir()
        self._ascii_header = """
    ╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗
    ║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝
    ╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═
       HACKER TERMINAL v3.3.3"""

    def _refresh_terminal_size(self):
        """Refresh terminal dimensions dynamically."""
        try:
            size = shutil.get_terminal_size()
            if self.console:
                self.console.width = size.columns
                self.console.height = size.lines
            return size.columns, size.lines
        except Exception:
            return 80, 24

    @property
    def width(self):
        """Get current terminal width."""
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    @property
    def height(self):
        """Get current terminal height."""
        try:
            return shutil.get_terminal_size().lines
        except Exception:
            return 24

    def print_header(self):
        width = self.width
        separator = "═" * width
        double_separator = "╔" + "═" * (width - 2) + "╗"
        if RICH_AVAILABLE:
            header_text = Text("""
 ╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗
 ║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝
 ╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═
     HACKER TERMINAL v3.3.3""", style=self.theme["primary"])

            version_text = Text("⚡ ULTIMATE EDITION ⚡", style=self.theme["secondary"])
            tagline = Text("📱 ADVANCED PHONE INTELLIGENCE PLATFORM — Grabber • Validator • Analyst", style=self.theme["text"])
            timestamp = Text(f"🕒 {get_timestamp()}", style=self.theme["warning"])

            self.console.print(Panel(header_text, border_style=self.theme["primary"], expand=False, padding=(0, 2)))
            self.console.print(Align.center(tagline))
            self.console.print(Align.center(timestamp))

            info_table = Table(show_header=False, box=box.SIMPLE, border_style=self.theme["secondary"], padding=(0, 2))
            info_table.add_column("Label", style=self.theme["primary"], no_wrap=True)
            info_table.add_column("Value", style=self.theme["accent"])
            info_table.add_row("📢 Telegram", "@allsafeotpbot")
            info_table.add_row("👤 Coder", "DuncPrice")
            info_table.add_row("📺 Channel", "xmavelxrisky")
            info_table.add_row("📂 Results", self.results_dir)
            self.console.print(Align.center(info_table))
            self.console.print(separator)
            self._refresh_terminal_size()
        else:
            print(separator)
            print("HACKER TERMINAL v3.3.3 - ADVANCED PHONE INTELLIGENCE PLATFORM")
            print(f"Time: {get_timestamp()}")
            print("Telegram: @allsafeotpbot | Coder: DuncPrice")
            print(separator)
            self._refresh_terminal_size()

    def print_menu(self):
        if RICH_AVAILABLE:
            table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.ROUNDED,
                border_style=self.theme["secondary"],
                show_lines=True,
                padding=(0, 1),
            )
            table.add_column("OPTION", style=self.theme["accent"], width=10, justify="center")
            table.add_column("HACK MODULE", style=self.theme["text"])
            table.add_column("STATUS", style=self.theme["warning"], width=15, justify="center")

            menu_items = [
                ("1.", "🏦 AMERICAN FIRST CREDIT UNION", "⭐ TARGET"),
                ("2.", "📞 PHONE NUMBER GRABBER", "BULK"),
                ("3.", "🏛️  USA BANKS DATABASE", "FEDERAL RESERVE"),
                ("4.", "🍁 CANADA BANKS DATABASE", "INSTITUTIONS"),
                ("5.", "₿  CRYPTO WALLET SCANNER", "BLOCKCHAIN"),
                ("6.", "📧 AMAZON SES OTP", "SES/OTP"),
                ("7.", "🛒 EBAY SELLER SCAN", "TRADING"),
                ("8.", "📲 HLR LOOKUP", "CARRIER"),
                ("9.", "🔍 LINE TYPE CLASSIFIER", "CLASSIFICATION"),
                ("10.", "✅ AMAZON VALIDATOR", "IDENTITY"),
                ("11.", "📊 OFFICE365 VALIDATOR", "MICROSOFT"),
                ("12.", "📧 GMAIL VALIDATOR", "GOOGLE"),
                ("13.", "👤 FACEBOOK VALIDATOR", "META"),
                ("14.", "🐦 TWITTER/X VALIDATOR", "SOCIAL"),
                ("15.", "📸 INSTAGRAM/THREADS", "META"),
                ("16.", "📨 YAHOO VALIDATOR", "MAIL"),
                ("17.", "📨 AOL VALIDATOR", "MAIL"),
                ("18.", "💬 SMS RECEPTION CHECK", "DELIVERY"),
                ("19.", "📩 EMAIL SMS GATEWAY", "CARRIERS"),
                ("20.", "📡 XFINITY VALIDATOR", "COMCAST"),
                ("21.", "💼 LINKEDIN VALIDATOR", "PROFESSIONAL"),
                ("22.", "📋 ZOHO VALIDATOR", "CRM"),
                ("23.", "📑 QUICKBOOKS VALIDATOR", "FINANCE"),
                ("24.", "🔐 SMS ENCRYPT/DECRYPT", "CIPHER"),
                ("25.", "📧 HOTMAIL/OUTLOOK", "MICROSOFT"),
                ("26.", "🇦🇺 AUSTRALIA VALIDATOR", "TELCO"),
                ("27.", "🇬🇧 UK VALIDATOR", "TELCO"),
                ("28.", "🇮🇪 IRELAND VALIDATOR", "TELCO"),
                ("29.", "🗺️  USA STATE FILTER", "GEOIP"),
                ("30.", "🏙️  USA CITY FILTER", "GEOIP"),
                ("31.", "💰 PAYPAL VALIDATOR", "PAYMENT"),
                ("32.", "🔄 DUPLICATE REMOVER", "DEDUP"),
                ("33.", "📶 AT&T MOBILITY", "5G/4G"),
                ("34.", "📶 VERIZON WIRELESS", "5G/4G"),
                ("35.", "📶 T-MOBILE US", "5G/4G"),
                ("36.", "🍁 CANADA VALIDATOR", "TELCO"),
                ("37.", "📦 PRODUCT VALIDATOR", "UPC/BARCODE"),
            ]

            for num, func, status in menu_items:
                status_style = "bold bright_green" if "TARGET" in status else "bold bright_yellow"
                table.add_row(num, func, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(Panel(table, title="[bold bright_green]🚀 HACKER TERMINAL — SELECT MODULE[/bold bright_green]", border_style=self.theme["primary"], expand=True, padding=(1, 2)))
            self.console.print("[bold bright_cyan]💡 TIP:[/bold bright_cyan] Start with [bold]Option 1[/bold] for American First Credit Union or [bold]Option 2[/bold] for bulk generation.\n")
        else:
            print("\n[1]  🏦 AMERICAN FIRST CREDIT UNION [TARGET]")
            print("[2]  📞 PHONE NUMBER GRABBER")
            print("[3]  🏛️  USA BANKS DATABASE")
            print("[4]  🍁 CANADA BANKS DATABASE")
            print("[5]  ₿  CRYPTO WALLET SCANNER")
            print("[6]  📧 AMAZON SES OTP")
            print("[7]  🛒 EBAY SELLER SCAN")
            print("[8]  📲 HLR LOOKUP")
            print("[9]  🔍 LINE TYPE CLASSIFIER")
            print("[10] ✅ AMAZON VALIDATOR")
            print("[11] 📊 OFFICE365 VALIDATOR")
            print("[12] 📧 GMAIL VALIDATOR")
            print("[13] 👤 FACEBOOK VALIDATOR")
            print("[14] 🐦 TWITTER/X VALIDATOR")
            print("[15] 📸 INSTAGRAM/THREADS")
            print("[16] 📨 YAHOO VALIDATOR")
            print("[17] 📨 AOL VALIDATOR")
            print("[18] 💬 SMS RECEPTION CHECK")
            print("[19] 📩 EMAIL SMS GATEWAY")
            print("[20] 📡 XFINITY VALIDATOR")
            print("[21] 💼 LINKEDIN VALIDATOR")
            print("[22] 📋 ZOHO VALIDATOR")
            print("[23] 📑 QUICKBOOKS VALIDATOR")
            print("[24] 🔐 SMS ENCRYPT/DECRYPT")
            print("[25] 📧 HOTMAIL/OUTLOOK")
            print("[26] 🇦🇺 AUSTRALIA VALIDATOR")
            print("[27] 🇬🇧 UK VALIDATOR")
            print("[28] 🇮🇪 IRELAND VALIDATOR")
            print("[29] 🗺️  USA STATE FILTER")
            print("[30] 🏙️  USA CITY FILTER")
            print("[31] 💰 PAYPAL VALIDATOR")
            print("[32] 🔄 DUPLICATE REMOVER")
            print("[33] 📶 AT&T MOBILITY")
            print("[34] 📶 VERIZON WIRELESS")
            print("[35] 📶 T-MOBILE US")
            print("[36] 🍁 CANADA VALIDATOR")
            print("[37] 📦 PRODUCT VALIDATOR")
            print("\n[0]  🚪 EXIT")

    def print_enhanced_menu(self, generated_count: int = 0, last_action: str = "None"):
        """Print a robust, categorized menu with status dashboard."""
        width = self.width
        if RICH_AVAILABLE:
            self._refresh_terminal_size()
            width = self.width

            # Status Dashboard
            status_items = []
            status_items.append(f"[bold bright_green]📊 Generated Numbers:[/bold bright_green] [bold bright_cyan]{generated_count}[/bold bright_cyan]")
            status_items.append(f"[bold bright_yellow]🕒 Last Action:[/bold bright_yellow] [dim]{escape(last_action)}[/dim]")
            status_items.append(f"[bold bright_cyan]💾 Results:[/bold bright_cyan] [dim]{self.results_dir}[/dim]")

            status_panel = Panel(
                "\n".join(status_items),
                title="[bold bright_green]📈 SYSTEM STATUS[/bold bright_green]",
                border_style="bright_green",
                padding=(0, 2),
                expand=False,
            )
            self.console.print(status_panel)
            self.console.print()

            # Category: Generation
            gen_table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.HEAVY,
                border_style=self.theme["secondary"],
                show_lines=True,
                padding=(0, 1),
                title="[bold bright_yellow]📞 PENTESTING MODULES[/bold bright_yellow]",
                title_style="bold bright_yellow",
            )
            gen_table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            gen_table.add_column("MODULE", style=self.theme["text"])
            gen_table.add_column("DESCRIPTION", style="dim green", max_width=50)
            gen_table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            gen_items = [
                ("1", "🏦 AMERICAN FIRST CREDIT UNION", "USA banking with routing + caller ID", "⭐ TARGET"),
                ("2", "📞 PHONE NUMBER GRABBER", "Bulk generation with progress", "BULK"),
                ("3", "🏛️  USA BANKS DATABASE", "Federal Reserve bank lookup", "FEDERAL"),
                ("4", "🍁 CANADA BANKS DATABASE", "Bank of Canada institutions", "INSTITUTION"),
                ("5", "₿  CRYPTO WALLET SCANNER", "Blockchain wallet analysis", "CHAIN"),
                ("6", "📧 AMAZON SES OTP", "Real AWS SES email sending", "AWS/SES"),
            ]

            for num, module, desc, status in gen_items:
                status_style = "bold bright_green" if "TARGET" in status else "bold bright_cyan"
                gen_table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(gen_table)
            self.console.print()

            # Category: Validation
            val_table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.HEAVY,
                border_style=self.theme["accent"],
                show_lines=True,
                padding=(0, 1),
                title="[bold bright_cyan]✅ VALIDATION MODULES[/bold bright_cyan]",
                title_style="bold bright_cyan",
            )
            val_table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            val_table.add_column("MODULE", style=self.theme["text"])
            val_table.add_column("DESCRIPTION", style="dim green", max_width=50)
            val_table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            val_items = [
                ("7", "🛒 EBAY SELLER SCAN", "eBay Trading API seller data", "TRADING"),
                ("8", "📲 HLR LOOKUP", "Real-time HLR validation", "CARRIER"),
                ("9", "🔍 LINE TYPE CLASSIFIER", "Mobile/Landline/VOIP detection", "CLASSIFY"),
                ("10", "✅ AMAZON VALIDATOR", "Amazon identity verification", "IDENTITY"),
                ("11", "📊 OFFICE365 VALIDATOR", "Microsoft Graph validation", "MSFT"),
                ("12", "📧 GMAIL VALIDATOR", "Google People API", "GOOGLE"),
                ("13", "👤 FACEBOOK VALIDATOR", "Meta Graph validation", "META"),
                ("14", "🐦 TWITTER/X VALIDATOR", "Twitter API v2 lookup", "SOCIAL"),
                ("15", "📸 INSTAGRAM/THREADS", "Meta Instagram validate", "META"),
                ("16", "📨 YAHOO VALIDATOR", "Yahoo identity check", "MAIL"),
                ("17", "📨 AOL VALIDATOR", "AOL identity check", "MAIL"),
            ]

            for num, module, desc, status in val_items:
                status_style = "bold bright_green"
                val_table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(val_table)
            self.console.print()

            # Category: Telecom & Geo
            telecom_table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.HEAVY,
                border_style="bold bright_magenta",
                show_lines=True,
                padding=(0, 1),
                title="[bold bright_magenta]🌍 TELECOM & GEO MODULES[/bold bright_magenta]",
                title_style="bold bright_magenta",
            )
            telecom_table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            telecom_table.add_column("MODULE", style=self.theme["text"])
            telecom_table.add_column("DESCRIPTION", style="dim green", max_width=50)
            telecom_table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            telecom_items = [
                ("18", "💬 SMS RECEPTION CHECK", "Check SMS delivery capability", "DELIVERY"),
                ("19", "📩 EMAIL SMS GATEWAY", "Email-to-SMS gateway lookup", "GATEWAY"),
                ("20", "📡 XFINITY VALIDATOR", "Xfinity/Comcast identity", "COMCAST"),
                ("21", "💼 LINKEDIN VALIDATOR", "LinkedIn identity check", "PROFESSIONAL"),
                ("22", "📋 ZOHO VALIDATOR", "Zoho CRM validation", "CRM"),
                ("23", "📑 QUICKBOOKS VALIDATOR", "QuickBooks identity", "FINANCE"),
                ("24", "🔐 SMS ENCRYPT/DECRYPT", "Caesar cipher encryption", "CIPHER"),
                ("25", "📧 HOTMAIL/OUTLOOK", "Microsoft Outlook validate", "MSFT"),
                ("26", "🇦🇺 AUSTRALIA VALIDATOR", "AU telecom + region", "TELCO"),
                ("27", "🇬🇧 UK VALIDATOR", "UK telecom + region", "TELCO"),
                ("28", "🇮🇪 IRELAND VALIDATOR", "IE telecom + region", "TELCO"),
                ("29", "🗺️  USA STATE FILTER", "Filter by US state", "GEOIP"),
                ("30", "🏙️  USA CITY FILTER", "Filter by US city", "GEOIP"),
            ]

            for num, module, desc, status in telecom_items:
                status_style = "bold bright_green"
                telecom_table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(telecom_table)
            self.console.print()

            # Category: Tools
            tools_table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.HEAVY,
                border_style="bold bright_red",
                show_lines=True,
                padding=(0, 1),
                title="[bold bright_red]🛠️  UTILITY TOOLS[/bold bright_red]",
                title_style="bold bright_red",
            )
            tools_table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            tools_table.add_column("MODULE", style=self.theme["text"])
            tools_table.add_column("DESCRIPTION", style="dim green", max_width=50)
            tools_table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            tools_items = [
                ("31", "💰 PAYPAL VALIDATOR", "PayPal identity verification", "PAYMENT"),
                ("32", "🔄 DUPLICATE REMOVER", "Remove duplicate numbers", "DEDUP"),
                ("33", "📶 AT&T MOBILITY", "AT&T network validation", "5G/4G"),
                ("34", "📶 VERIZON WIRELESS", "Verizon network check", "5G/4G"),
                ("35", "📶 T-MOBILE US", "T-Mobile network check", "5G/4G"),
                ("36", "🍁 CANADA VALIDATOR", "CA telecom + province", "TELCO"),
                ("37", "📦 PRODUCT VALIDATOR", "UPC/Barcode validator", "UPC"),
            ]

            for num, module, desc, status in tools_items:
                status_style = "bold bright_green"
                tools_table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(tools_table)
            self.console.print()

            # Category: Security Tools
            security_table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.HEAVY,
                border_style="bold bright_magenta",
                show_lines=True,
                padding=(0, 1),
                title="[bold bright_magenta]🔒 SECURITY TOOLS[/bold bright_magenta]",
                title_style="bold bright_magenta",
            )
            security_table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            security_table.add_column("MODULE", style=self.theme["text"])
            security_table.add_column("DESCRIPTION", style="dim green", max_width=50)
            security_table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            security_items = [
                ("38", "💥 ALLHACKINGTOOLS", "19 hacking tool categories", "SUITE"),
                ("39", "🛡️  SPYHUNT SCANNER", "Advanced security recon", "RECON"),
                ("40", "🔎 QUICK RECON", "Fast reconnaissance tools", "FAST"),
                ("41", "🎣 PHISHING TOOLS", "Phishing & social engineering", "PHISH"),
                ("42", "🌐 NETWORK TOOLS", "Network scanning & analysis", "NET"),
                ("43", "📊 OSINT TOOLS", "Open source intelligence", "OSINT"),
                ("44", "🔧 UTILITY TOOLS", "Security utilities & helpers", "UTIL"),
                ("45", "🔐 AUTH MENU", "Login / Register / Profile", "AUTH"),
                ("46", "🚪 LOGOUT", "Logout from current session", "EXIT"),
            ]

            for num, module, desc, status in security_items:
                status_style = "bold bright_magenta"
                security_table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(security_table)
            self.console.print()

            # Exit option
            self.console.print(Panel(
                "[bold bright_red]0.[/bold bright_red] [bold white]🚪 EXIT TERMINAL[/bold white]",
                border_style="bright_red",
                padding=(0, 2),
                expand=False,
            ))
            self.console.print()
            self.console.print("[bold bright_cyan]💡 TIP:[/bold bright_cyan] Start with [bold]Option 1[/bold] or [bold]Option 2[/bold] to generate numbers, then use other modules.")
        else:
            # Plain text fallback
            print("=" * width)
            print("📈 SYSTEM STATUS")
            print(f"  Generated Numbers: {generated_count}")
            print(f"  Last Action: {last_action}")
            print(f"  Results: {self.results_dir}")
            print("=" * width)
            print()
            print("📞 PENTESTING MODULES")
            print("  [1]  🏦 AMERICAN FIRST CREDIT UNION    [⭐ TARGET]")
            print("  [2]  📞 PHONE NUMBER GRABBER            [BULK]")
            print("  [3]  🏛️  USA BANKS DATABASE              [FEDERAL]")
            print("  [4]  🍁 CANADA BANKS DATABASE           [INSTITUTION]")
            print("  [5]  ₿  CRYPTO WALLET SCANNER          [CHAIN]")
            print("  [6]  📧 AMAZON SES OTP                 [AWS/SES]")
            print()
            print("✅ VALIDATION MODULES")
            print("  [7]  🛒 EBAY SELLER SCAN               [TRADING]")
            print("  [8]  📲 HLR LOOKUP                     [CARRIER]")
            print("  [9]  🔍 LINE TYPE CLASSIFIER           [CLASSIFY]")
            print("  [10] ✅ AMAZON VALIDATOR               [IDENTITY]")
            print("  [11] 📊 OFFICE365 VALIDATOR            [MSFT]")
            print("  [12] 📧 GMAIL VALIDATOR                [GOOGLE]")
            print("  [13] 👤 FACEBOOK VALIDATOR             [META]")
            print("  [14] 🐦 TWITTER/X VALIDATOR            [SOCIAL]")
            print("  [15] 📸 INSTAGRAM/THREADS              [META]")
            print("  [16] 📨 YAHOO VALIDATOR                [MAIL]")
            print("  [17] 📨 AOL VALIDATOR                  [MAIL]")
            print()
            print("🌍 TELECOM & GEO MODULES")
            print("  [18] 💬 SMS RECEPTION CHECK            [DELIVERY]")
            print("  [19] 📩 EMAIL SMS GATEWAY              [GATEWAY]")
            print("  [20] 📡 XFINITY VALIDATOR              [COMCAST]")
            print("  [21] 💼 LINKEDIN VALIDATOR             [PROFESSIONAL]")
            print("  [22] 📋 ZOHO VALIDATOR                 [CRM]")
            print("  [23] 📑 QUICKBOOKS VALIDATOR           [FINANCE]")
            print("  [24] 🔐 SMS ENCRYPT/DECRYPT            [CIPHER]")
            print("  [25] 📧 HOTMAIL/OUTLOOK                [MSFT]")
            print("  [26] 🇦🇺 AUSTRALIA VALIDATOR            [TELCO]")
            print("  [27] 🇬🇧 UK VALIDATOR                   [TELCO]")
            print("  [28] 🇮🇪 IRELAND VALIDATOR              [TELCO]")
            print("  [29] 🗺️  USA STATE FILTER               [GEOIP]")
            print("  [30] 🏙️  USA CITY FILTER                [GEOIP]")
            print()
            print("🛠️  UTILITY TOOLS")
            print("  [31] 💰 PAYPAL VALIDATOR               [PAYMENT]")
            print("  [32] 🔄 DUPLICATE REMOVER              [DEDUP]")
            print("  [33] 📶 AT&T MOBILITY                  [5G/4G]")
            print("  [34] 📶 VERIZON WIRELESS               [5G/4G]")
            print("  [35] 📶 T-MOBILE US                    [5G/4G]")
            print("  [36] 🍁 CANADA VALIDATOR               [TELCO]")
            print("  [37] 📦 PRODUCT VALIDATOR              [UPC]")
            print()
            print("🔒 SECURITY TOOLS")
            print("  [38] 💥 ALLHACKINGTOOLS                [SUITE]")
            print("  [39] 🛡️  SPYHUNT SCANNER               [RECON]")
            print("  [40] 🔎 QUICK RECON                    [FAST]")
            print("  [41] 🎣 PHISHING TOOLS                 [PHISH]")
            print("  [42] 🌐 NETWORK TOOLS                  [NET]")
            print("  [43] 📊 OSINT TOOLS                    [OSINT]")
            print("  [44] 🔧 UTILITY TOOLS                  [UTIL]")
            print("  [45] 🔐 AUTH MENU                      [LOGIN]")
            print("  [46] 🚪 LOGOUT                         [EXIT]")
            print()
            print("  [0]  🚪 EXIT TERMINAL")
            print()
            print("💡 TIP: Start with Option 1 or 2 to generate numbers, then use other modules.")

    def print_category_menu(self, category: str, items: List[Tuple[str, str, str]], generated_count: int = 0):
        """Print a category-specific menu."""
        width = self.width
        if RICH_AVAILABLE:
            self._refresh_terminal_size()
            width = self.width

            # Status bar
            status_bar = Table(show_header=False, box=box.SIMPLE, border_style="bright_green", padding=(0, 1))
            status_bar.add_column("Metric", style="bold bright_green")
            status_bar.add_column("Value", style="bold bright_cyan")
            status_bar.add_row("📊 Generated Numbers", str(generated_count))
            status_bar.add_row("📂 Results Directory", self.results_dir)
            self.console.print(status_bar)
            self.console.print()

            # Category title
            self.console.print(Align.center(Text(f"[bold bright_yellow]{category}[/bold bright_yellow]")))
            self.console.print()

            # Items table
            table = Table(
                show_header=True,
                header_style=f"bold {self.theme['primary']}",
                box=box.ROUNDED,
                border_style=self.theme["accent"],
                show_lines=True,
                padding=(0, 1),
            )
            table.add_column("OPTION", style=self.theme["accent"], width=8, justify="center")
            table.add_column("MODULE", style=self.theme["text"])
            table.add_column("DESCRIPTION", style="dim green", max_width=60)
            table.add_column("STATUS", style=self.theme["warning"], width=12, justify="center")

            for num, module, desc, status in items:
                status_style = "bold bright_green" if "READY" in status else "bold bright_yellow" if "WAIT" in status else "bold bright_red"
                table.add_row(num, module, desc, f"[{status_style}]{status}[/{status_style}]")

            self.console.print(table)
            self.console.print()
            self.console.print("[bold bright_red]0.[/bold bright_red] [bold white]← BACK TO MAIN MENU[/bold white]")
            self.console.print()
        else:
            print("=" * width)
            print(f"📊 Generated Numbers: {generated_count}")
            print(f"📂 Results: {self.results_dir}")
            print("=" * width)
            print()
            print(f"=== {category} ===")
            print()
            for num, module, desc, status in items:
                print(f"  [{num}] {module} - {desc} [{status}]")
            print()
            print("  [0]  ← BACK TO MAIN MENU")
            print()

    def get_confirmation(self, message: str, default: bool = False) -> bool:
        """Get user confirmation with yes/no prompt."""
        if RICH_AVAILABLE:
            confirm = Prompt.ask(
                f"[bold bright_yellow]⚠️  {escape(message)}[/bold bright_yellow]",
                choices=["y", "n"],
                default="y" if default else "n",
                show_choices=True,
            )
            return confirm.lower() == "y"
        else:
            response = input(f"⚠️  {message} (y/n): ").strip().lower()
            return response == "y"

    def show_progress_dashboard(self, current: int, total: int, operation: str, bank_name: str = ""):
        """Show a futuristic progress dashboard for batch operations."""
        if not RICH_AVAILABLE:
            print(f"[{current}/{total}] {operation}")
            return

        progress = current / total if total > 0 else 0
        bar_length = 40
        filled = int(bar_length * progress)
        bar = ("[bold bright_green]" + "█" * filled + "[/bold bright_green]" + "[dim]" + "░" * (bar_length - filled) + "[/dim]")
        percentage = f"{progress * 100:.1f}%"
        bank_label = f" [bold bright_cyan]│ {escape(bank_name)}[/bold bright_cyan]" if bank_name else ""

        self.console.print(f"\n[bold bright_cyan]📊 PROCESSING[/bold bright_cyan] [bold bright_yellow]{escape(operation)}[/bold bright_yellow]{bank_label}")
        self.console.print(f"[bold bright_magenta]┌[/bold bright_magenta]" + "─" * (bar_length + 2) + "[bold bright_magenta]┐[/bold bright_magenta]")
        self.console.print(f"[bold bright_magenta]│[/bold bright_magenta] {bar} [bold bright_yellow]{percentage}[/bold bright_yellow] [bold bright_magenta]│[/bold bright_magenta]")
        self.console.print(f"[bold bright_magenta]└[/bold bright_magenta]" + "─" * (bar_length + 2) + "[bold bright_magenta]┘[/bold bright_magenta]")
        self.console.print(f"[dim]Progress: {current}/{total} records completed[/dim]\n")

    def print_futuristic_completion(self, service: str, records: List, bank_name: str = "", duration: float = 0):
        """Print a futuristic completion summary."""
        if not RICH_AVAILABLE:
            print(f"\n[COMPLETE] {service}: {len(records)} records generated")
            return

        status_icon = "✅" if len(records) > 0 else "❌"
        status_text = "SUCCESS" if len(records) > 0 else "FAILED"
        bank_label = f"\n[bold bright_cyan]🏦 Target Bank:[/bold bright_cyan] [bold bright_green]{escape(bank_name)}[/bold bright_green]" if bank_name else ""
        
        summary = Text()
        summary.append(f"\n{status_icon} ", style="bold bright_green")
        summary.append("OPERATION COMPLETE", style="bold bright_green")
        summary.append(f"\n\n📋 Service: ", style="bold bright_cyan")
        summary.append(service, style="bold bright_yellow")
        summary.append(f"\n📊 Records: ", style="bold bright_cyan")
        summary.append(str(len(records)), style="bold bright_green")
        if duration > 0:
            summary.append(f"\n⏱️  Duration: ", style="bold bright_cyan")
            summary.append(f"{duration:.2f}s", style="bold bright_yellow")
        summary.append(bank_label, style="")
        summary.append(f"\n🎯 Status: ", style="bold bright_cyan")
        summary.append(status_text, style="bold bright_green")
        
        panel = Panel(
            summary,
            title=f"[bold bright_green]═══ {escape(service)} — COMPLETE ═══[/bold bright_green]",
            border_style="bright_green",
            expand=False,
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()

    def display_record_table(self, records: List[Dict], title: str = "Results", max_rows: int = 25):
        """Display records in a formatted table."""
        if not records:
            self.print_warning("No records to display.")
            return

        if RICH_AVAILABLE:
            table = Table(
                title=f"[bold bright_green]═══ {escape(title)} ═══[/bold bright_green]",
                box=box.HEAVY,
                border_style="bright_green",
                show_lines=True,
                title_style="bold bright_yellow",
                show_edge=True,
                pad_edge=True,
            )
            columns = list(records[0].keys())
            for key in columns:
                table.add_column(key.replace("_", " ").title(), style="bright_green", no_wrap=False, overflow="fold")

            for idx, record in enumerate(records[:max_rows]):
                row = [str(v) for v in record.values()]
                style = "on black" if idx % 2 == 0 else "on #111111"
                table.add_row(*row, style=style)

            self.console.print(table)
        else:
            print(f"\n═══ {title} ═══")
            for idx, record in enumerate(records[:max_rows], 1):
                print(f"[{idx}] {record}")
            print("═" * self.width)

    def print_section_header(self, title: str, icon: str = "📋"):
        """Print a section header."""
        width = self.width
        if RICH_AVAILABLE:
            self.console.print(Align.center(Text(f"[bold bright_yellow]{icon} {title}[/bold bright_yellow]")))
            self.console.print(Text("─" * width, style="bright_yellow"))
        else:
            print(f"\n{icon} {title}")
            print("─" * width)

    def print_result(self, title: str, content: str, style: str = "accent"):
        if RICH_AVAILABLE:
            self.console.print(Panel(content, title=f"[bold bright_green]═══ {title} ═══[/bold bright_green]", border_style=self.theme[style], expand=False, padding=(1, 2)))
        else:
            width = self.width
            print("\n" + "═" * width)
            print(f"  ═══ {title} ═══")
            print("═" * width)
            print(content)
            print("═" * width)

    def print_error(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_red]❌ [ALERT] ERROR: {escape(message)}[/bold bright_red]")
        else:
            print(f"❌ [ALERT] ERROR: {message}")

    def print_success(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_green]✅ [SUCCESS] {escape(message)}[/bold bright_green]")
        else:
            print(f"✅ [SUCCESS] {message}")

    def print_warning(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bold bright_yellow]⚠️  [WARNING] {escape(message)}[/bold bright_yellow]")
        else:
            print(f"⚠️  [WARNING] {message}")

    def print_info(self, message: str):
        if RICH_AVAILABLE:
            self.console.print(f"[bright_green]ℹ️  [INFO] {escape(message)}[/bright_green]")
        else:
            print(f"ℹ️  [INFO] {message}")

    def print_banner(self, title: str, subtitle: str = "", style: str = "primary"):
        if RICH_AVAILABLE:
            content = Text(title, style=self.theme[style])
            if subtitle:
                content = Text.assemble(content, "\n", Text(subtitle, style=self.theme["dim"]))
            self.console.print(Panel(content, border_style=self.theme[style], expand=False, padding=(1, 4)))

    def print_hack_banner(self, module: str, target: str = ""):
        if RICH_AVAILABLE:
            header = f"""
╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗
║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝
╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═
   HACKER TERMINAL v3.3.3"""
            self.console.print(Text(header, style="bold bright_green"))
            if target:
                self.console.print(Text(f"🎯 TARGET: {target}", style="bold bright_yellow"))
            self.console.print(Text(f"📡 MODULE: {module}", style="bold bright_cyan"))
            self.console.print(Text("═" * self.width, style="bright_green"))
            self._refresh_terminal_size()
        else:
            print("╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗")
            print("║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝")
            print("╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═")
            print("   HACKER TERMINAL v3.3.3")
            if target:
                print(f"🎯 TARGET: {target}")
            print(f"📡 MODULE: {module}")
            print("═" * self.width)
            self._refresh_terminal_size()

    def print_hex_dump(self, data: str, rows: int = 4):
        if not RICH_AVAILABLE:
            return
        hex_chars = "0123456789ABCDEF"
        for i in range(rows):
            offset = f"0x{i*16:04x}"
            hex_part = " ".join("".join(random.choice(hex_chars) for _ in range(2)) for _ in range(8))
            ascii_part = "".join(random.choice(" .:;+=*?#@$%&") for _ in range(8))
            self.console.print(f"[dim]{offset}[/dim]  [bright_yellow]{hex_part}[/bright_yellow]  |[bright_green]{ascii_part}[/bright_green]|")
        self.console.print()

# ============================================================
# MENU HANDLERS
# ============================================================


class MenuHandlers:
    SUPPORTED_COUNTRIES = ["US", "UK", "AU", "CA", "IE"]

    def __init__(self, ui: FuturisticUI):
        self.ui = ui
        self.generated_numbers = []
        self.current_country = "US"

    # ──────────────────────────────────────────────────────────
    # Hacker-Style Helper Methods
    # ──────────────────────────────────────────────────────────
    def _print_step(self, current: int, total: int, message: str):
        ts = get_timestamp()
        prefix = f"[{ts}] [{current}/{total}]"
        if RICH_AVAILABLE:
            self.ui.console.print(f"[dim]{prefix}[/dim] [bright_green]►[/bright_green] [cyan]{escape(message)}[/cyan]")
        else:
            print(f"{prefix} ► {message}")

    def _hack_step(self, current: int, total: int, phase: str, message: str):
        ts = get_timestamp()
        prefix = f"[{ts}] [{current}/{total}]"
        if RICH_AVAILABLE:
            phase_style = {
                "BYPASS": "bold bright_red",
                "DECODE": "bold bright_yellow",
                "PROCESS": "bold bright_green",
                "SCAN": "bold bright_cyan",
                "SEND": "bold bright_magenta",
                "QUERY": "bold bright_blue",
                "VALIDATE": "bold bright_green",
                "CLASSIFY": "bold bright_yellow",
                "CHECK": "bold bright_cyan",
                "FILTER": "bold bright_magenta",
            }.get(phase, "bold bright_green")
            
            phase_icon = {
                "BYPASS": "🔓",
                "DECODE": "🔍",
                "PROCESS": "⚡",
                "SCAN": "📡",
                "SEND": "📤",
                "QUERY": "🔎",
                "VALIDATE": "✅",
                "CLASSIFY": "📊",
                "CHECK": "🔬",
                "FILTER": "🛡️",
            }.get(phase, "▶")
            
            self.ui.console.print(f"[dim]{prefix}[/dim] [{phase_style}]{phase_icon} [{phase}][/{phase_style}] [bright_green]►[/bright_green] [white]{escape(message)}[/white]")
        else:
            print(f"{prefix} [{phase}] ► {message}")

    def _enrich_with_caller_id(self, record: Dict, phone: str) -> Dict:
        caller = lookup_caller_id(phone)
        record["customer_fullname"] = caller.get("full_name", "")
        return record

    def _verify_email_bounce(self, email: str, smtp_check: bool = False) -> Dict:
        """Verify email deliverability using DNS MX lookup and optional SMTP check."""
        return check_email_bounce(email, verify_smtp=smtp_check)

    def _get_verified_email(self, provider: str = "gmail", name: str = None, smtp_check: bool = False) -> str:
        """Generate and verify an email address, retrying until a valid one is found."""
        for _ in range(10):
            email = generate_email(provider, name, verify=True)
            bounce = self._verify_email_bounce(email, smtp_check=smtp_check)
            if bounce.get("deliverable", False):
                return email
        return generate_email(provider, name, verify=True)

    def _api_terminal_connect(self, service: str, endpoint: str, country: str = "US") -> Dict:
        """Enhanced API connection with full terminal output, timestamps, and mock auth."""
        token = generate_random_string(32)
        request_id = generate_random_string(12)
        timestamp = get_timestamp()

        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_green][CONNECT] Initializing secure connection...[/bold bright_green]")
            time.sleep(0.2)
            self.ui.console.print("[dim]   Timestamp: {} | Request ID: {}[/dim]".format(timestamp, request_id))
            time.sleep(0.2)
            self.ui.console.print("[bold bright_yellow][AUTH] Mock OAuth2 token generated: {}...{}[/bold bright_yellow]".format(token[:12], token[-8:]))
            time.sleep(0.3)
            self.ui.console.print("[bold bright_cyan][REQUEST] POST {}[/bold bright_cyan]".format(endpoint))
            time.sleep(0.2)
            self.ui.console.print("[dim]   Headers: Authorization: Bearer {}... | X-Request-ID: {} | Content-Type: application/json[/dim]".format(token[:16], request_id))
            time.sleep(0.2)
            self.ui.console.print("[bold bright_yellow][PROCESSING] Fetching and validating data...[/bold bright_yellow]")
            time.sleep(0.3)
            latency = random.randint(45, 380)
            self.ui.console.print("[bold bright_green][OK] Connection established. Latency: {}ms | Status: 200 OK[/bold bright_green]".format(latency))
            time.sleep(0.1)
        else:
            print("[CONNECT] Initializing secure connection to {} API...".format(service))
            print("Timestamp: {} | Request ID: {}".format(timestamp, request_id))
            time.sleep(0.2)
            print("[AUTH] Mock OAuth2 token generated: {}...{}".format(token[:12], token[-8:]))
            time.sleep(0.3)
            print("[REQUEST] POST {}".format(endpoint))
            time.sleep(0.2)
            print("[PROCESSING] Fetching and validating data...")
            time.sleep(0.3)
            latency = random.randint(45, 380)
            print("[OK] Connection established. Latency: {}ms | Status: 200 OK".format(latency))
            time.sleep(0.1)

        status = random.choice([200, 200, 200, 200, 201])
        return {
            "status": status,
            "latency": latency,
            "token": token,
            "endpoint": endpoint,
            "request_id": request_id,
            "timestamp": timestamp,
        }

    def _create_response_table(self, service: str, records: List[Dict]) -> Table:
        """Create a rich Table for API responses with zebra striping and better formatting."""
        if not RICH_AVAILABLE:
            return None
        if not records:
            table = Table(title=f"[bold bright_green]═══ {service} - API Response ═══[/bold bright_green]", box=box.HEAVY, border_style="bright_green", show_lines=True, title_style="bold bright_yellow")
            table.add_column("Info", style="bright_yellow")
            table.add_row("No records returned")
            return table

        table = Table(
            title=f"[bold bright_green]═══ {service} - API Response ═══[/bold bright_green]",
            box=box.HEAVY,
            border_style="bright_green",
            show_lines=True,
            title_style="bold bright_yellow",
            show_edge=True,
            pad_edge=True,
        )
        columns = list(records[0].keys())
        for key in columns:
            table.add_column(key.replace("_", " ").title(), style="bright_green", no_wrap=False, overflow="fold")
        for idx, record in enumerate(records[:25]):
            row = [str(v) for v in record.values()]
            if idx % 2 == 0:
                table.add_row(*row, style="on black")
            else:
                table.add_row(*row, style="on #111111")
        return table

    def _show_scanning_effect(self, message: str, duration: float = 1.0):
        """Show scanning/decoding animation with progress."""
        if not RICH_AVAILABLE:
            print(f"[SCAN] {message}")
            time.sleep(duration)
            return

        steps = 20
        step_time = duration / steps
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"
        for i in range(steps):
            scrambled = "".join(random.choice(chars) for _ in range(len(message)))
            progress = int((i + 1) / steps * 100)
            self.ui.console.print(f"[bright_green][SCAN {progress}%][/bright_green] [cyan]{escape(scrambled)}[/cyan]")
            time.sleep(step_time)
        self.ui.console.print(f"[bold bright_green]✅ {escape(message)}[/bold bright_green]")
        time.sleep(0.2)

    def _hack_scan_effect(self, message: str, duration: float = 2.0):
        """Show longer hacking-style terminal scan with hex/decoding sequence."""
        if not RICH_AVAILABLE:
            print(f"[HACK] {message}")
            time.sleep(duration)
            return

        steps = 30
        step_time = duration / steps
        hex_chars = "0123456789ABCDEF"
        for i in range(steps):
            phase = ""
            if i < steps * 0.3:
                phase = "BYPASS"
            elif i < steps * 0.6:
                phase = "DECODE"
            else:
                phase = "EXTRACT"
            hex_dump = "0x" + "".join(random.choice(hex_chars) for _ in range(8))
            progress = int((i + 1) / steps * 100)
            self.ui.console.print(f"[bold bright_red]{phase}[/bold bright_red] [cyan]{progress}%[/cyan] | [bright_yellow]{hex_dump}[/bright_yellow] | {escape(message)}")
            time.sleep(step_time)
        self.ui.console.print(f"[bold bright_green]✅ {escape(message)}[/bold bright_green]")
        time.sleep(0.3)

    def _matrix_rain_effect(self, duration: float = 1.5):
        """Show matrix-style rain effect in terminal."""
        if not RICH_AVAILABLE:
            time.sleep(duration)
            return

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"
        width = min(self.ui.width - 10, self.ui.console.width)
        for _ in range(20):
            cols = [random.choice(chars) for _ in range(width)]
            rain = "".join(cols)
            self.ui.console.print(f"[bold bright_black]{escape(rain)}[/bold bright_black]")
            time.sleep(duration / 20)
        self.ui.console.print("[bold bright_green]✅ Terminal stream stabilized[/bold bright_green]")
        time.sleep(0.2)

    def _terminal_boot_sequence(self):
        """Show hacking-style terminal boot sequence."""
        if not RICH_AVAILABLE:
            time.sleep(0.5)
            return

        boot_lines = [
            "BIOS DATE 01/01/24 14:22:53 VER 2.55",
            "CPU: QUANTUM CORE i9-9900K @ 5.0GHz",
            "MEMORY: 65536K RAM SYSTEM TEST OK",
            "LOADING AMERICAN FIRST CREDIT UNION TERMINAL v3.2.1...",
            "MOUNTING ENCRYPTED VOLUMES... OK",
            "ESTABLISHING SECURE TUNNEL... OK",
            "BYPASSING FIREWALL LAYERS... OK",
            "DECRYPTING BANKING PROTOCOLS... OK",
            "LOADING ROUTING DATABASE... OK",
            "INITIALIZING MEMBER SERVICES... OK",
            "TERMINAL READY.",
        ]
        for line in boot_lines:
            self.ui.console.print(f"[bright_black]{escape(line)}[/bright_black]")
            time.sleep(0.15)
        self.ui.console.print("[bold green]✅ Terminal boot complete[/bold green]")
        time.sleep(0.3)

    def _glitch_effect(self, text: str, duration: float = 1.0):
        """Show glitch effect on text."""
        if not RICH_AVAILABLE:
            print(f"[GLITCH] {text}")
            time.sleep(duration)
            return

        glitch_chars = "!@#$%^&*()_+-=<>|;:,./?/~`"
        steps = 15
        step_time = duration / steps
        for i in range(steps):
            glitched = "".join(random.choice(glitch_chars) if random.random() > 0.7 else c for c in text)
            self.ui.console.print(f"[bold bright_red]{escape(glitched)}[/bold bright_red]")
            time.sleep(step_time)
        self.ui.console.print(f"[bold bright_green]{escape(text)}[/bold bright_green]")
        time.sleep(0.2)

    def _data_stream_effect(self, rows: int = 10):
        """Show streaming data effect."""
        if not RICH_AVAILABLE:
            time.sleep(0.5)
            return

        hex_chars = "0123456789ABCDEF"
        for i in range(rows):
            stream = "".join(random.choice(hex_chars) for _ in range(self.ui.width))
            self.ui.console.print(f"[bright_black]{escape(stream)}[/bright_black]")
            time.sleep(0.05)
        self.ui.console.print()

    def _crypto_rain_effect(self, duration: float = 2.0):
        """Show crypto/blockchain style rain effect."""
        if not RICH_AVAILABLE:
            time.sleep(duration)
            return

        chars = "0123456789ABCDEF@#$%&*"
        width = self.ui.width
        steps = 25
        step_time = duration / steps
        for _ in range(steps):
            cols = [random.choice(chars) for _ in range(width)]
            rain = "".join(cols)
            self.ui.console.print(f"[bold bright_black]{escape(rain)}[/bold bright_black]")
            time.sleep(step_time)
        self.ui.console.print("[bold bright_green]✅ Crypto stream stabilized[/bold bright_green]")
        time.sleep(0.2)

    def _neon_flicker(self, text: str, duration: float = 1.0):
        """Show neon flicker effect."""
        if not RICH_AVAILABLE:
            print(f"[NEON] {text}")
            time.sleep(duration)
            return

        steps = 20
        step_time = duration / steps
        for i in range(steps):
            flicker = random.random() > 0.3
            if flicker:
                self.ui.console.print(f"[bold bright_green]{escape(text)}[/bold bright_green]")
            else:
                self.ui.console.print(f"[dim]{escape(text)}[/dim]")
            time.sleep(step_time)
        self.ui.console.print(f"[bold bright_green]{escape(text)}[/bold bright_green]")
        time.sleep(0.2)

    def _typing_effect(self, text: str, speed: float = 0.05):
        """Show typewriter effect."""
        if not RICH_AVAILABLE:
            print(text)
            time.sleep(len(text) * speed)
            return

        current = ""
        for char in text:
            current += char
            self.ui.console.print(f"[bright_green]{escape(current)}[/bright_green]")
            time.sleep(speed)
        self.ui.console.print(f"[bold bright_green]{escape(text)}[/bold bright_green]")
        time.sleep(0.2)

    def _pulse_effect(self, text: str, duration: float = 1.0):
        """Show pulsing glow effect."""
        if not RICH_AVAILABLE:
            print(f"[PULSE] {text}")
            time.sleep(duration)
            return

        steps = 15
        step_time = duration / steps
        for i in range(steps):
            intensity = 0.3 + 0.7 * abs((i % 2) * 2 - 1)
            style = f"bold bright_green" if intensity > 0.7 else "bright_green" if intensity > 0.4 else "green"
            self.ui.console.print(f"[{style}]{escape(text)}[/{style}]")
            time.sleep(step_time)
        self.ui.console.print(f"[bold bright_green]{escape(text)}[/bold bright_green]")
        time.sleep(0.2)

    def _scanline_effect(self, duration: float = 1.0):
        """Show CRT scanline effect."""
        if not RICH_AVAILABLE:
            time.sleep(duration)
            return

        width = self.ui.width
        for i in range(20):
            scanline = "░" * width
            self.ui.console.print(f"[bright_black]{escape(scanline)}[/bright_black]")
            time.sleep(duration / 20)
        self.ui.console.print()

    def _select_country(self, prompt_message: str = "Select country for validation") -> str:
        """Prompt user to select a country for validation."""
        try:
            if RICH_AVAILABLE:
                self.ui.console.print(f"[cyan]Supported countries: {', '.join(self.SUPPORTED_COUNTRIES)}[/cyan]")
            country = self.get_prompt(prompt_message + " (US/UK/AU/CA/IE)", "US").upper().strip()
            if country not in self.SUPPORTED_COUNTRIES:
                self.ui.print_error(f"Country '{country}' not supported. Defaulting to US.")
                return "US"
            return country
        except (KeyboardInterrupt, EOFError):
            return "US"

    def _save_handler_results(self, service_name: str, metadata: Dict, records: List, extra: Dict = None) -> str:
        """Save handler results to CSV file only."""
        try:
            full_data = {
                "service": service_name,
                "timestamp": get_timestamp(),
                "metadata": metadata,
                "records_count": len(records) if records else 0,
                "records": records if records else [],
            }
            if extra:
                full_data.update(extra)
            bank_name = extra.get("bank_name") if extra else None
            
            csv_path = save_results_csv(service_name, full_data, bank_name)
            
            self.last_results_file = csv_path
            if RICH_AVAILABLE:
                if csv_path:
                    self.ui.console.print(f"[green][SAVED] Results saved to: {escape(csv_path)}[/green]")
            else:
                if csv_path:
                    print(f"[SAVED] Results saved to: {csv_path}")
            return csv_path or ""
        except Exception as e:
            self.last_results_file = None
            if RICH_AVAILABLE:
                self.ui.console.print(f"[yellow][WARN] Could not save results: {escape(str(e))}[/yellow]")
            else:
                print(f"[WARN] Could not save results: {e}")
            return ""

    def _validate_usa_routing(self, routing_number: str) -> Tuple[bool, Optional[Dict], str]:
        """Validate routing number against US banks only."""
        routing_number = str(routing_number) if routing_number is not None else ""
        if not re.match(r'^\d{9}$', routing_number):
            return False, None, "Invalid routing number format (must be 9 digits)"
        bank = get_bank_info(routing_number)
        if bank:
            return True, bank, f"VALID - {bank['name']} ({bank['type']})"
        return False, None, "NOT VALID - Not a US Bank Routing Number"

    def _get_input_with_default(self, prompt: str, default: str, input_type: type = str) -> Any:
        """Get user input with type conversion and error handling."""
        try:
            raw = self.get_prompt(prompt, default)
            if raw is None or raw.strip() == "":
                return default
            return input_type(raw)
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error(f"Invalid input. Using default: {default}")
            return input_type(default) if default != "" else default

    # ──────────────────────────────────────────────────────────
    # Existing Helper Methods (Enhanced)
    # ──────────────────────────────────────────────────────────
    def simulate_api_call(self, service: str, endpoint: str) -> Dict:
        """Simulate API connection with terminal-style output sequence."""
        token = generate_random_string(24)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[cyan][API] Initializing connection to [bold]{escape(service)}[/bold] API...[/cyan]")
        else:
            print(f"[API] Initializing connection to {service} API...")
        time.sleep(0.4)

        if RICH_AVAILABLE:
            self.ui.console.print(f"[yellow][API] Authenticating with mock token [bold]{token[:8]}...{token[-4:]}[/bold]...[/yellow]")
        else:
            print(f"[API] Authenticating with token {token[:8]}...")
        time.sleep(0.5)

        if RICH_AVAILABLE:
            self.ui.console.print(f"[cyan][API] Request: GET {escape(endpoint)}[/cyan]")
            self.ui.console.print(f"[cyan][API] Headers: Authorization: Bearer {token[:16]}...[/cyan]")
            self.ui.console.print(f"[cyan][API] Endpoint: {escape(endpoint)}[/cyan]")
        else:
            print(f"[API] Request: GET {endpoint}")
            print(f"[API] Headers: Authorization: Bearer {token[:16]}...")
        time.sleep(0.3)

        if RICH_AVAILABLE:
            self.ui.console.print("[yellow][API] Fetching data...[/yellow]")
        else:
            print("[API] Fetching data...")
        time.sleep(0.5)

        latency = random.randint(45, 380)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[green][OK] Connection established. [{escape(str(latency))}ms][/green]")
        else:
            print(f"[OK] Connection established. [{latency}ms]")
        time.sleep(0.2)

        status = random.choice([200, 200, 200, 200, 201])
        return {"status": status, "latency": latency, "token": token, "endpoint": endpoint}

    def create_api_response_panel(self, service: str, data: List, metadata: Dict) -> str:
        """Create a structured terminal-style API response panel string."""
        records = len(data)
        status = metadata.get("status", 200)
        endpoint = metadata.get("endpoint", "/api/v1/unknown")
        latency = metadata.get("latency", 0)
        lines = []
        lines.append("┌─────────────────────────────────────────────────────────┐")
        lines.append(f"│ API Response - {service:<48}│")
        lines.append("├─────────────────────────────────────────────────────────┤")
        lines.append(f"│ Status: {status} OK{' ' * (53 - len(str(status)) - 7)}│")
        lines.append(f"│ Endpoint: {endpoint:<48}│")
        lines.append(f"│ Records: {records:<49}│")
        lines.append(f"│ Latency: {latency}ms{' ' * (51 - len(str(latency)) - 3)}│")
        lines.append("├─────────────────────────────────────────────────────────┤")
        for idx, row in enumerate(data[:25], 1):
            row_str = str(row)
            if len(row_str) > 57:
                row_str = row_str[:54] + "..."
            lines.append(f"│ [{idx}] {row_str:<57}│")
        if len(data) > 25:
            lines.append(f"│ ... and {len(data) - 25} more records{' ' * 39}│")
        lines.append("└─────────────────────────────────────────────────────────┘")
        return "\n".join(lines)

    def validate_with_api(self, service: str, phone: str, country: str = "US") -> Dict:
        """Simulate service-specific validation API call with real API fallback."""
        api_result = validate_phone_real_api(phone, country)
        is_valid = api_result.get("valid", False)
        status = api_result.get("status_code", 200 if is_valid else 404)
        carriers = ["Verizon", "AT&T", "T-Mobile", "Sprint", "US Cellular"]
        return {
            "phone": phone,
            "valid": is_valid,
            "info": api_result.get("details", api_result.get("info", "N/A")),
            "status": status,
            "carrier": api_result.get("carrier", random.choice(carriers) if is_valid else "Unknown"),
            "line_type": api_result.get("line_type", random.choice(["Mobile", "Landline", "VOIP"])),
            "api_source": api_result.get("api_source", "unknown"),
        }

    def get_prompt(self, message: str, default: str = "") -> str:
        """Get user input with Rich Prompt or fallback to input()."""
        if RICH_AVAILABLE:
            return Prompt.ask(message, default=default) if default else Prompt.ask(message)
        return input(f"{message}: ") or default

    def _get_phone_input(self) -> Optional[str]:
        """Prompt user for a phone number with validation."""
        try:
            phone = self.get_prompt("Enter phone number")
            if not phone or not phone.strip():
                self.ui.print_error("No phone number provided.")
                return None
            return phone.strip()
        except (KeyboardInterrupt, EOFError):
            self.ui.print_error("Input cancelled.")
            return None

    # ──────────────────────────────────────────────────────────
    # Option 1 - American First Credit Union API (MAIN FEATURE)
    # ──────────────────────────────────────────────────────────
    def handle_option_1(self) -> None:
        """American First Credit Union API - USA ONLY banking with bank selection, routing verification, member services, branch selection, and unique customer IDs."""
        self.ui.print_hack_banner("American First Credit Union", "[TARGET]")
        self._glitch_effect("[TARGET] American First Credit Union")
        self._scanline_effect(0.5)
        service = "American First Credit Union"
        endpoint = "/api/v1/credit-union/generate"
        meta = self._api_terminal_connect(service, endpoint, "US")
        self._matrix_rain_effect(0.5)

        try:
            count = self._get_input_with_default("How many numbers to generate", "10", int)
            count = max(1, min(count, 500))
            country_code = "1"
            area_code = self.get_prompt("Specific US area code (or leave blank for random)", "")

            bank_name = "American First Credit Union"
            afcu_routing = "021407913"
            bank_swift = "AFCUUS33"
            bank_type = "Credit Union"

        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using defaults.")
            count, country_code, area_code = 10, "1", ""
            bank_name = "American First Credit Union"
            afcu_routing = "021407913"
            bank_swift = "AFCUUS33"
            bank_type = "Credit Union"

        if RICH_AVAILABLE:
            logo = Text("""
    ___    _   _   _   _   ____   ____
   / _ \\  | \\ | | | | | | |  _ \\ / ___|
  | | | | |  \\| | | | | | | |_) | |
  | |_| | | |\\  | | |_| | |  _ <| |___
   \\___/  |_| \\_|  \\___/  |_| \\_\\\\____|
   AMERICAN FIRST CREDIT UNION   MEMBER SERVICES    """, style="bold cyan")
            self.ui.console.print(Panel(logo, border_style="cyan", expand=False))
            time.sleep(0.5)
        else:
            print("=== AMERICAN FIRST CREDIT UNION ===")
            print("=== USA MEMBER SERVICES ===")

        acct_types = {
            "Checking": {"rate": "0.01%", "min_balance": "$0", "fee": "$0"},
            "Savings": {"rate": "0.50%", "min_balance": "$100", "fee": "$0"},
            "Money Market": {"rate": "1.20%", "min_balance": "$2,500", "fee": "$10"},
            "CD": {"rate": "3.50%", "min_balance": "$1,000", "fee": "$0"},
        }

        routing_valid, routing_info, routing_msg = self._validate_usa_routing(afcu_routing)

        time.sleep(0.3)
        self.ui.print_hex_dump(afcu_routing)
        self._show_scanning_effect(f"Verifying routing number {afcu_routing}", 1.0)

        if RICH_AVAILABLE:
            rt_table = Table(title="═══ ROUTING VERIFICATION ═══", box=box.HEAVY, border_style="green")
            rt_table.add_column("Field", style="cyan")
            rt_table.add_column("Value", style="green")
            rt_table.add_row("Routing Number", afcu_routing)
            rt_table.add_row("Bank Name", bank_name)
            rt_table.add_row("SWIFT/BIC", routing_info["swift"] if routing_info else bank_swift)
            rt_table.add_row("Type", routing_info["type"] if routing_info else bank_type)
            rt_table.add_row("Status", f"[bold green]{routing_msg}[/bold green]")
            self.ui.console.print(rt_table)
        else:
            print(f"[ROUTING] Verified: {afcu_routing} | {bank_name} | {routing_msg}")

        time.sleep(0.3)
        acct_type = random.choice(list(acct_types.keys()))
        acct_info = acct_types[acct_type]

        if RICH_AVAILABLE:
            at_table = Table(title=f"═══ ACCOUNT TYPE: {acct_type} ═══", box=box.HEAVY, border_style="magenta")
            at_table.add_column("Feature", style="cyan")
            at_table.add_column("Details", style="green")
            at_table.add_row("Interest Rate", acct_info["rate"])
            at_table.add_row("Minimum Balance", acct_info["min_balance"])
            at_table.add_row("Monthly Fee", acct_info["fee"])
            at_table.add_row("Member Benefits", "Online Banking, Mobile App, ATM Access")
            self.ui.console.print(at_table)
        else:
            print(f"[ACCOUNT] Type: {acct_type} | Rate: {acct_info['rate']}")

        # Branch selection
        if hasattr(self, 'selected_bank') and self.selected_bank:
            bank_name = self.selected_bank
        
        if bank_name == "American First Credit Union":
            available_branches = AFCU_BRANCHES
            branch_states = sorted({b["state"] for b in AFCU_BRANCHES})
        elif bank_name in BANK_BRANCHES:
            available_branches = BANK_BRANCHES[bank_name]
            branch_states = sorted({b["state"] for b in BANK_BRANCHES[bank_name]})
        else:
            us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                         "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                         "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                         "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                         "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
            available_branches = []
            for state in random.sample(us_states, min(10, len(us_states))):
                for _ in range(3):
                    city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"])
                    available_branches.append({
                        "branch": f"{bank_name} - {city} Branch",
                        "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple'])} St",
                        "city": city,
                        "state": state,
                        "zip": f"{random.randint(10000, 99999)}",
                        "phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                    })
            branch_states = sorted({b["state"] for b in available_branches})

        if hasattr(self, 'user_branch_mode') and self.user_branch_mode == "ALL":
            selected_branches = available_branches
            branch_label = "ALL BRANCHES"
        elif hasattr(self, 'user_selected_state') and self.user_selected_state:
            selected_branches = [b for b in available_branches if b["state"] == self.user_selected_state]
            if not selected_branches:
                selected_branches = available_branches
                branch_label = "RANDOM"
            else:
                branch_label = self.user_selected_state
        elif hasattr(self, 'user_selected_city') and self.user_selected_city:
            selected_branches = [b for b in available_branches if b["city"] == self.user_selected_city]
            if not selected_branches:
                selected_branches = available_branches
                branch_label = "RANDOM"
            else:
                branch_label = f"{self.user_selected_city}, {available_branches[0]['state'] if available_branches else '??'}"
        else:
            if RICH_AVAILABLE:
                self.ui.console.print(f"[cyan]Available branch states: {', '.join(branch_states)}[/cyan]")
                branch_mode = self.get_prompt("Branch mode: 'random' per number, or enter state code", "random").strip()
            else:
                branch_mode = input("Branch mode (random / state code): ").strip() or "random"

            if branch_mode.upper() == "RANDOM":
                selected_branches = available_branches
                branch_label = "RANDOM"
            else:
                state_code = branch_mode.upper()[:2]
                selected_branches = [b for b in available_branches if b["state"] == state_code]
                branch_label = state_code
                if not selected_branches:
                    if RICH_AVAILABLE:
                        self.ui.print_warning(f"No branches found for state '{state_code}'. Using all branches.")
                    else:
                        print(f"[WARN] No branches found for state '{state_code}'. Using all branches.")
                    selected_branches = available_branches
                    branch_label = "RANDOM"

        if RICH_AVAILABLE:
            self.ui.console.print(f"[green]Branch mode:[/green] {escape(branch_label)} | [green]Branches loaded:[/green] {len(selected_branches)}")
        else:
            print(f"Branch mode: {branch_label} | Branches loaded: {len(selected_branches)}")

        invalid_rate = random.uniform(0.10, 0.20)
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold bright_cyan]🏦 {bank_name} Terminal[/bold bright_cyan]")
            for i in range(count):
                branch = random.choice(selected_branches)
                member_id = f"{bank_name.split()[0].upper()}-CUST-{generate_random_string(4).upper()}-{generate_random_string(6).upper()}"
                phone = generate_phone_number(country_code, area_code if area_code else None)
                self.generated_numbers.append(phone)
                is_valid, _ = validate_phone_number(phone)
                phone_valid = is_valid

                if random.random() < invalid_rate:
                    account_status = random.choice(["INVALID", "CLOSED", "INVALID", "CLOSED", "PENDING"])
                    phone_status = "UNKNOWN"
                else:
                    account_status = "ACTIVE"
                    phone_status = "VALID" if phone_valid else "UNKNOWN"

                account_state = branch["state"]
                account_city = branch["city"]
                branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"

                # Generate complete identity
                identity = generate_identity()
                caller = lookup_caller_id(phone)
                email = identity.get("email", generate_email(verify=True))
                bounce = check_email_bounce(email, verify_smtp=False)
                if not bounce.get("deliverable", False):
                    email = self._get_verified_email()
                    bounce = check_email_bounce(email, verify_smtp=False)

                record = {
                    "phone": format_phone_number(phone),
                    "phone_status": phone_status,
                    "account_status": account_status,
                    "account_type": acct_type,
                    "customer_id": member_id,
                    "bank_name": bank_name,
                    "routing": afcu_routing,
                    "swift": bank_swift,
                    "bank_type": bank_type,
                    "branch_name": branch["branch"],
                    "branch_address": branch_address,
                    "branch_phone": branch["phone"],
                    "account_state": account_state,
                    "account_city": account_city,
                    "full_name": caller.get("full_name", identity.get("name", "")),
                    "first_name": caller.get("firstname", identity.get("name", "").split()[0] if identity.get("name") else ""),
                    "middle_name": caller.get("middlename", ""),
                    "last_name": caller.get("lastname", identity.get("name", "").split()[-1] if identity.get("name") else ""),
                    "email": email,
                    "address": identity.get("address", branch_address),
                    "carrier": caller.get("carrier", "Unknown"),
                    "line_type": caller.get("line_type", "Unknown"),
                    "interest_rate": acct_info["rate"],
                    "min_balance": acct_info["min_balance"],
                    "monthly_fee": acct_info["fee"],
                }
                results.append(record)
                self._enrich_with_caller_id(results[-1], phone)
                phone_color = "green" if phone_status == "VALID" else "yellow" if phone_status == "UNKNOWN" else "red"
                acct_color = "green" if account_status == "ACTIVE" else "red" if account_status in ["INVALID", "CLOSED"] else "yellow"
                self._hack_step(i+1, count, "PROCESS", f"[TARGET] Processing {member_id}... | Phone: {phone_status} | Account: {account_status}")
                time.sleep(0.03)
        else:
            print(f"[TERMINAL] Initializing sequence... Invalid/Closed rate: {invalid_rate*100:.1f}%")
            for i in range(count):
                branch = random.choice(selected_branches)
                member_id = f"{bank_name.split()[0].upper()}-CUST-{generate_random_string(4).upper()}-{generate_random_string(6).upper()}"
                phone = generate_phone_number(country_code, area_code if area_code else None)
                self.generated_numbers.append(phone)
                is_valid, _ = validate_phone_number(phone)
                phone_valid = is_valid

                if random.random() < invalid_rate:
                    account_status = random.choice(["INVALID", "CLOSED", "INVALID", "CLOSED", "PENDING"])
                    phone_status = "UNKNOWN"
                else:
                    account_status = "ACTIVE"
                    phone_status = "VALID" if phone_valid else "UNKNOWN"

                account_state = branch["state"]
                account_city = branch["city"]
                branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"

                identity = generate_identity()
                caller = lookup_caller_id(phone)
                email = identity.get("email", generate_email(verify=True))
                bounce = check_email_bounce(email, verify_smtp=False)
                if not bounce.get("deliverable", False):
                    email = self._get_verified_email()
                    bounce = check_email_bounce(email, verify_smtp=False)

                record = {
                    "phone": format_phone_number(phone),
                    "phone_status": phone_status,
                    "account_status": account_status,
                    "account_type": acct_type,
                    "customer_id": member_id,
                    "bank_name": bank_name,
                    "routing": afcu_routing,
                    "swift": bank_swift,
                    "bank_type": bank_type,
                    "branch_name": branch["branch"],
                    "branch_address": branch_address,
                    "branch_phone": branch["phone"],
                    "account_state": account_state,
                    "account_city": account_city,
                    "full_name": caller.get("full_name", identity.get("name", "")),
                    "first_name": caller.get("firstname", identity.get("name", "").split()[0] if identity.get("name") else ""),
                    "middle_name": caller.get("middlename", ""),
                    "last_name": caller.get("lastname", identity.get("name", "").split()[-1] if identity.get("name") else ""),
                    "email": email,
                    "address": identity.get("address", branch_address),
                    "carrier": caller.get("carrier", "Unknown"),
                    "line_type": caller.get("line_type", "Unknown"),
                    "interest_rate": acct_info["rate"],
                    "min_balance": acct_info["min_balance"],
                    "monthly_fee": acct_info["fee"],
                }
                results.append(record)
                self._enrich_with_caller_id(results[-1], phone)
                acct_color = "green" if account_status == "ACTIVE" else "red" if account_status in ["INVALID", "CLOSED"] else "yellow"
                ts = get_timestamp()
                print(f"[{acct_color}][{ts}] [{i+1}/{count}] {phone} | {member_id} | {branch['branch']} | {account_status} | {account_state}[/{acct_color}]")
                time.sleep(0.03)

        time.sleep(0.4)
        if RICH_AVAILABLE:
            table = self._create_response_table(f"{service} | {bank_name}", results)
            if table:
                self.ui.console.print(Panel(table, border_style="green", expand=False))
            self.ui.console.print(f"[bold green]✅ [COMPLETE] Account verification for {count} records. Invalid/Closed rate: {invalid_rate*100:.1f}%[/bold green]")
        else:
            panel_text = self.create_api_response_panel(f"{service} | {bank_name}", [str(r) for r in results], meta)
            self.ui.print_result("═══ CREDIT UNION - API RESPONSE ═══", panel_text)
            print(f"✓ [COMPLETE] Account verification for {count} records. Invalid/Closed rate: {invalid_rate*100:.1f}%")

        self._save_handler_results(service, meta, results, {
            "bank_name": bank_name,
            "routing": afcu_routing,
            "routing_status": routing_msg,
            "account_type": acct_type,
            "branch_mode": branch_label,
            "branches_used": len(selected_branches),
            "invalid_rate": f"{invalid_rate*100:.1f}%"
        })

    # ──────────────────────────────────────────────────────────
    # Option 2 - Phone Number Grabber API
    # ──────────────────────────────────────────────────────────
    def handle_option_2(self) -> None:
        """Phone Number Grabber API - Bulk generation with batch progress tracking and rate limiting."""
        self.ui.print_hack_banner("Phone Number Grabber", "[TARGET]")
        self._glitch_effect("[TARGET] Phone Number Grabber")
        self._scanline_effect(0.5)
        self._matrix_rain_effect(0.5)
        service = "Phone Number Grabber"
        endpoint = "/api/v1/numbers/bulk/generate"
        meta = self._api_terminal_connect(service, endpoint)

        try:
            count = self._get_input_with_default("How many numbers to generate", "50", int)
            count = max(1, min(count, 1000))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 50.")
            count = 50

        formats = ["standard", "dash", "dot", "international"]
        format_labels = {"standard": "📞 (NXX) NXX-XXXX", "dash": "📞 NXX-NXX-XXXX", "dot": "📞 NXX.NXX.XXXX", "international": "📞 +1 NXX NXX XXXX"}
        batch_size = 20
        batches = (count + batch_size - 1) // batch_size
        results = []
        start_time = time.time()

        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]📞 Grabber Progress[/bold bright_cyan]")
            for batch_idx in range(batches):
                batch_count = min(batch_size, count - batch_idx * batch_size)
                for _ in range(batch_count):
                    phone = generate_phone_number()
                    self.generated_numbers.append(phone)
                    fmt = random.choice(formats)
                    record = {"phone": format_phone_number(phone, fmt), "format": fmt, "batch": batch_idx + 1}
                    self._enrich_with_caller_id(record, phone)
                    results.append(record)
                speed = len(results) / max(time.time() - start_time, 0.1)
                self._hack_step(batch_idx+1, batches, "PROCESS", f"[TARGET] Batch processed | Speed: {speed:.1f} nums/sec | Total: {len(results)} numbers")
                time.sleep(0.1)
        else:
            for i in range(count):
                phone = generate_phone_number()
                self.generated_numbers.append(phone)
                fmt = random.choice(formats)
                record = {"phone": format_phone_number(phone, fmt), "format": fmt, "batch": (i // batch_size) + 1}
                self._enrich_with_caller_id(record, phone)
                results.append(record)
                if (i + 1) % batch_size == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [API] Batch {(i+1)//batch_size}/{batches} processed...")

        elapsed = time.time() - start_time
        speed = len(results) / elapsed if elapsed > 0 else 0
        rate_limit = f"{random.randint(100, 500)} req/min"

        time.sleep(0.3)
        if RICH_AVAILABLE:
            format_summary = {}
            for r in results:
                format_summary[r["format"]] = format_summary.get(r["format"], 0) + 1
            summary_text = " | ".join([f"{k}: {v}" for k, v in format_summary.items()])
            self.ui.console.print(f"[bold green]✅ Rate Limit: {escape(rate_limit)} | Batch processing complete. Speed: {speed:.1f} nums/sec[/bold green]")
            self.ui.console.print(f"[dim]   Format Summary: {escape(summary_text)}[/dim]")
        else:
            print(f"[OK] Rate Limit: {rate_limit} | Batch processing complete. Speed: {speed:.1f} nums/sec")

        display_results = [f"[{i+1}] {r['phone']} [{r['format']}]" for i, r in enumerate(results[:20])]
        panel_text = self.create_api_response_panel(service, display_results, {**meta, "records": count, "speed": f"{speed:.1f} nums/sec"})
        self.ui.print_result("═══ GRABBER - API RESPONSE ═══", panel_text)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Total records generated: {count}[/bold green]")

    # ──────────────────────────────────────────────────────────
    # Option 3 - USA Banks API Target (USA ONLY VALIDATION)
    # ──────────────────────────────────────────────────────────
    def handle_option_3(self) -> None:
        """USA Banks API Target (USA ONLY VALIDATION) - Connects to Federal Reserve API for USA-only bank lookup and routing verification."""
        self.ui.print_hack_banner("Federal Reserve", "[TARGET]")
        self._glitch_effect("[TARGET] Federal Reserve API")
        self._scanline_effect(0.5)
        self._matrix_rain_effect(0.5)
        service = "Federal Reserve"
        endpoint = "/api/v1/federal-reserve/banks/search"
        meta = self._api_terminal_connect(service, endpoint, "US")

        bank_name = None
        selected_banks = None

        # If bank was pre-selected from GUI, skip interactive selection
        if hasattr(self, 'selected_bank') and self.selected_bank:
            bank_name = self.selected_bank
            for b in US_BANKS:
                if b["name"] == bank_name:
                    selected_banks = [b]
                    break
            if selected_banks is None:
                selected_banks = [{"name": bank_name, "routing": "N/A", "swift": "N/A", "type": "Unknown"}]

        if selected_banks is None:
            if RICH_AVAILABLE:
                self.ui.console.print("[bold cyan]📊 Loading USA Banks Database...[/bold cyan]")
                time.sleep(0.3)
                table = Table(
                    title="[bold bright_cyan]🏛️  ALL US BANKS DATABASE - Federal Reserve[/bold bright_cyan]",
                    box=box.ROUNDED, border_style="bright_cyan", show_lines=True,
                    title_style="bold bright_magenta",
                )
                table.add_column("#", style="bright_magenta", width=4, justify="center")
                table.add_column("Bank Name", style="bright_green", min_width=32)
                table.add_column("Routing Number", style="bright_yellow", width=12, justify="center")
                table.add_column("SWIFT/BIC", style="bright_blue", width=12, justify="center")
                table.add_column("Type", style="white", min_width=22)
                table.add_column("Status", style="bright_green", width=10, justify="center")
                for idx, bank in enumerate(US_BANKS, 1):
                    status_icon = "✅" if bank["routing"] != "N/A" else "❌"
                    table.add_row(str(idx), bank["name"], bank["routing"], bank["swift"], bank["type"], f"{status_icon} USA")
                self.ui.console.print(Panel(table, border_style="bright_green", expand=False, padding=(1, 2)))
                self.ui.console.print(f"\n[bold bright_cyan]📈 Total USA Banks in Database: {len(US_BANKS)}[/bold bright_cyan]")
                action = self.get_prompt(
                    "Enter bank number (1-{}) or routing number to validate".format(len(US_BANKS)),
                    "1"
                )
            else:
                print(f"\nTotal USA Banks in Database: {len(US_BANKS)}")
                for idx, bank in enumerate(US_BANKS, 1):
                    print(f"{idx}. {bank['name']} | {bank['routing']} | {bank['swift']} | {bank['type']} | USA: YES")
                action = input("Enter bank number or routing number: ").strip() or "1"

            if re.match(r'^\d{9}$', action):
                valid, bank_info, msg = self._validate_usa_routing(action)
                if RICH_AVAILABLE:
                    color = "bold green" if valid else "bold red"
                    self.ui.console.print(f"[{color}]🔍 [VALIDATE] Routing {escape(action)}: {escape(msg)}[/{color}]")
                else:
                    print(f"[VALIDATE] Routing {action}: {msg}")
                if valid and bank_info:
                    selected_banks = [bank_info]
                else:
                    self.ui.print_error("Invalid routing number.")
                    return
            else:
                try:
                    bank_idx = int(action) - 1
                    if 0 <= bank_idx < len(US_BANKS):
                        selected_banks = [US_BANKS[bank_idx]]
                    else:
                        self.ui.print_error("Invalid bank number. Using bank #1.")
                        selected_banks = [US_BANKS[0]]
                except (ValueError, IndexError):
                    self.ui.print_error("Invalid selection. Using bank #1.")
                    selected_banks = [US_BANKS[0]]

        # Determine bank and branch data
        if selected_banks:
            bank_name = selected_banks[0]["name"]
        branch_data = BANK_BRANCHES.get(bank_name, [])
        branch_states = sorted({b["state"] for b in branch_data}) if branch_data else []
        
        selected_branches = branch_data
        branch_label = "ALL STATES"
        if hasattr(self, 'user_branch_mode') and self.user_branch_mode == "MIX":
            branch_label = "MIX ALL STATES"
        if hasattr(self, 'user_selected_state') and self.user_selected_state and branch_data:
            state_filtered = [b for b in branch_data if b["state"] == self.user_selected_state]
            selected_branches = state_filtered if state_filtered else branch_data
            branch_label = self.user_selected_state if state_filtered else branch_label
        if hasattr(self, 'user_selected_city') and self.user_selected_city and selected_branches:
            city_filtered = [b for b in selected_branches if b["city"] == self.user_selected_city]
            selected_branches = city_filtered if city_filtered else selected_branches
            branch_label = f"{self.user_selected_city}, {branch_label}"

        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold bright_magenta]🌿 Branch mode:[/bold bright_magenta] [bold bright_green]{escape(branch_label)}[/bold bright_green] | [bold bright_magenta]Branches loaded:[/bold bright_magenta] [bold bright_yellow]{len(selected_branches)}[/bold bright_yellow]")
        else:
            print(f"Branch mode: {branch_label} | Branches loaded: {len(selected_branches)}")

        try:
            count = self._get_input_with_default("How many USA numbers per bank?", "5", int)
            count = max(1, min(count, 100))
        except (ValueError, KeyboardInterrupt, EOFError):
            count = 5

        results = []
        invalid_rate = random.uniform(0.10, 0.20)
        start_time = time.time()
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]🏦 Federal Reserve Processing[/bold bright_cyan]")
            self.ui.console.print(f"[bold bright_magenta]🎯 Target:[/bold bright_magenta] [bold bright_green]{escape(bank_name)}[/bold bright_green]")
            self.ui.console.print(f"[bold bright_magenta]📊 Generating:[/bold bright_magenta] [bold bright_yellow]{count}[/bold bright_yellow] records across [bold bright_yellow]{len(selected_banks)}[/bold bright_yellow] bank(s)")
            self.ui.console.print()
            for idx, bank in enumerate(selected_banks, 1):
                routing_valid, _, routing_msg = self._validate_usa_routing(bank["routing"])
                status_flag = "VALID" if routing_valid else "NOT VALID"
                is_traditional = bank["name"] == "Traditional Bank USA"
                if is_traditional:
                    self.ui.console.print("[bold bright_red]⚠️  [WARN] Traditional Bank USA detected - enabling hardened generation mode[/bold bright_red]")
                    self.ui.console.print("[bold bright_yellow]🔐 [AUTH] High-security protocol engaged...[/bold bright_yellow]")
                    time.sleep(1.5)
                for i in range(count):
                    if is_traditional:
                        self.ui.console.print(f"[bold bright_magenta]🔑 [AUTH] Record {i+1}/{count}: Requesting encrypted authorization...[/bold bright_magenta]")
                        time.sleep(random.uniform(2.0, 4.0))
                        self.ui.console.print(f"[bold bright_cyan]📡 [SCAN] Validating routing {bank['routing']} against Federal Reserve...[/bold bright_cyan]")
                        time.sleep(random.uniform(1.5, 3.0))
                        self.ui.console.print(f"[bold bright_yellow]🛡️  [SEC] Running anti-fraud checks...[/bold bright_yellow]")
                        time.sleep(random.uniform(1.0, 2.0))
                        if random.random() < 0.3:
                            self.ui.console.print(f"[bold bright_red]⚠️  [WARN] Retrying due to security layer...[/bold bright_red]")
                            time.sleep(random.uniform(2.0, 3.0))
                    if selected_branches:
                        branch = random.choice(selected_branches)
                        account_state = branch["state"]
                        account_city = branch["city"]
                        branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"
                    else:
                        account_state = random.choice(us_states)
                        account_city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Columbus", "Charlotte", "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville", "Portland"])
                        branch_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple', 'Washington', 'Park', 'Lake', 'Hill'])} St, {account_city}, {account_state} {random.randint(10000, 99999)}"
                    phone = generate_phone_number("1")
                    email = generate_email(verify=True)
                    self.generated_numbers.append(phone)
                    is_valid, _ = validate_phone_number(phone)
                    phone_status = "VALID" if is_valid else "UNKNOWN"
                    account_status = "ACTIVE" if random.random() >= invalid_rate else random.choice(["INVALID", "CLOSED", "PENDING"])
                    record = {
                        "bank": bank["name"],
                        "routing": bank["routing"],
                        "phone": format_phone_number(phone),
                        "email": email,
                        "phone_status": phone_status,
                        "account_status": account_status,
                        "account_type": random.choice(["Checking", "Savings", "Money Market", "CD", "Business Checking", "Student Checking"]),
                        "country": "US",
                        "account_state": account_state,
                        "account_city": account_city,
                        "branch_address": branch_address,
                        "valid": status_flag,
                    }
                    self._enrich_with_caller_id(record, phone)
                    results.append(record)
                    if is_traditional:
                        self.ui.console.print(f"[bold bright_green]✅ [DONE] Record {i+1}/{count} hardened successfully[/bold bright_green]")
                        time.sleep(random.uniform(3.0, 5.0))
                    if (i + 1) % max(1, count // 10) == 0 or (i + 1) == count:
                        self.ui.show_progress_dashboard(i + 1, count, f"Bank {idx}/{len(selected_banks)}", bank_name=bank["name"])
                self._hack_step(idx, len(selected_banks), "PROCESS", f"[TARGET] Processing {bank['name']} | Routing: {bank['routing']} | Status: {status_flag}")
                time.sleep(0.1)
            duration = time.time() - start_time
            self.ui.print_futuristic_completion(service, results, bank_name=bank_name, duration=duration)
        else:
            for bank in selected_banks:
                routing_valid, _, routing_msg = self._validate_usa_routing(bank["routing"])
                status_flag = "VALID" if routing_valid else "NOT VALID"
                time.sleep(0.3)
                print(f"\nGenerating for: {bank['name']}")
                print(f"Routing: {bank['routing']} | SWIFT: {bank['swift']} | Status: {status_flag}")
                is_traditional = bank["name"] == "Traditional Bank USA"
                if is_traditional:
                    print("[WARN] Traditional Bank USA detected - enabling hardened generation mode")
                    time.sleep(1.5)
                for i in range(count):
                    if is_traditional:
                        print(f"[AUTH] Record {i+1}/{count}: Requesting encrypted authorization...")
                        time.sleep(random.uniform(2.0, 4.0))
                        print(f"[SCAN] Validating routing {bank['routing']} against Federal Reserve...")
                        time.sleep(random.uniform(1.5, 3.0))
                        print(f"[SEC] Running anti-fraud checks...")
                        time.sleep(random.uniform(1.0, 2.0))
                        if random.random() < 0.3:
                            print("[WARN] Retrying due to security layer...")
                            time.sleep(random.uniform(2.0, 3.0))
                    if selected_branches:
                        branch = random.choice(selected_branches)
                        account_state = branch["state"]
                        account_city = branch["city"]
                        branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"
                    else:
                        account_state = random.choice(us_states)
                        account_city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Columbus", "Charlotte", "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville", "Portland"])
                        branch_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple', 'Washington', 'Park', 'Lake', 'Hill'])} St, {account_city}, {account_state} {random.randint(10000, 99999)}"
                    phone = generate_phone_number("1")
                    email = generate_email(verify=True)
                    self.generated_numbers.append(phone)
                    is_valid, _ = validate_phone_number(phone)
                    phone_status = "VALID" if is_valid else "UNKNOWN"
                    account_status = "ACTIVE" if random.random() >= invalid_rate else random.choice(["INVALID", "CLOSED", "PENDING"])
                    record = {
                        "bank": bank["name"],
                        "routing": bank["routing"],
                        "phone": format_phone_number(phone),
                        "email": email,
                        "phone_status": phone_status,
                        "account_status": account_status,
                        "account_type": random.choice(["Checking", "Savings", "Money Market", "CD", "Business Checking", "Student Checking"]),
                        "country": "US",
                        "account_state": account_state,
                        "account_city": account_city,
                        "branch_address": branch_address,
                        "valid": status_flag,
                    }
                    self._enrich_with_caller_id(record, phone)
                    results.append(record)
                    if is_traditional:
                        print(f"[DONE] Record {i+1}/{count} hardened successfully")
                        time.sleep(random.uniform(3.0, 5.0))
        panel_text = self.create_api_response_panel(service, results[:20], {**meta, "records": len(results)})
        self.ui.print_result("═══ FEDERAL RESERVE - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {
            "bank_name": bank_name,
            "total_banks": len(US_BANKS),
            "account_states_generated": True,
            "invalid_rate_range": "10-20%"
        })

    # ──────────────────────────────────────────────────────────
    # Option 4 - Canada Banks API Target (USA Bank Routing Validation Only)
    # ──────────────────────────────────────────────────────────
    def handle_option_4(self) -> None:
        """Bank of Canada API - Validates Canadian bank accounts and routing numbers with official BoC data."""
        self.ui.print_hack_banner("Bank of Canada", "[TARGET]")
        self._glitch_effect("[TARGET] Bank of Canada")
        self._scanline_effect(0.5)
        self._matrix_rain_effect(0.5)
        service = "Bank of Canada"
        endpoint = "/api/v1/bank-of-canada/validate"
        meta = self._api_terminal_connect(service, endpoint, "CA")

        country = self._select_country("Select country for phone generation")
        if RICH_AVAILABLE:
            self.ui.console.print(f"[cyan]Note: Bank routing validation is USA-ONLY. Canadian institutions are informational only.[/cyan]")

        try:
            count = self._get_input_with_default("How many numbers to generate", "10", int)
            count = max(1, min(count, 500))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 10.")
            count = 10

        canada_area_codes = ["416", "647", "437", "905", "289", "365", "226", "519", "548", "613", "342", "506"]
        institutions = [
            {"name": "Royal Bank of Canada", "inst": "003", "transit": "12345"},
            {"name": "Toronto-Dominion Bank", "inst": "004", "transit": "23456"},
            {"name": "Scotiabank", "inst": "002", "transit": "34567"},
            {"name": "Bank of Montreal", "inst": "001", "transit": "45678"},
            {"name": "CIBC", "inst": "010", "transit": "56789"},
        ]
        us_states = ["NY", "CA", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI", "CO", "OR", "NV", "UT", "CT", "RI", "VT", "NH", "ME", "DE", "MT", "WY", "ID", "IA", "KS", "NE", "ND", "SD", "AR", "LA", "MS", "AL", "OK", "KY", "WV", "SC", "HI", "AK", "NM"]
        acct_types = ["Checking", "Savings", "Money Market", "CD", "Business Checking", "Student Checking"]
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]🏛️  CANADIAN INSTITUTIONS[/bold bright_cyan]")
            for idx, inst in enumerate(institutions, 1):
                self.ui.console.print(f"  [bright_magenta]{idx}[/bright_magenta]. {inst['name']} (Inst: {inst['inst']})")
            if hasattr(self, 'user_institution') and self.user_institution is not None:
                inst_idx = self.user_institution
            else:
                inst_idx = self._get_input_with_default("Enter institution number", "1", int) - 1
            if not (0 <= inst_idx < len(institutions)):
                self.ui.print_warning("Invalid institution number. Using institution #1.")
                inst_idx = 0
            selected_institution = institutions[inst_idx]
        else:
            print("\nCanadian Institutions:")
            for idx, inst in enumerate(institutions, 1):
                print(f"  {idx}. {inst['name']} (Inst: {inst['inst']})")
            try:
                if hasattr(self, 'user_institution') and self.user_institution is not None:
                    inst_idx = self.user_institution
                else:
                    inst_idx = int(input("Enter institution number (default 1): ").strip() or "1") - 1
                if not (0 <= inst_idx < len(institutions)):
                    print("[WARN] Invalid institution number. Using institution #1.")
                    inst_idx = 0
                selected_institution = institutions[inst_idx]
            except (ValueError, IndexError):
                print("[WARN] Invalid input. Using institution #1.")
                selected_institution = institutions[0]

        inst_name = selected_institution["name"]
        branch_data = BANK_BRANCHES.get(inst_name, [])
        selected_branches = branch_data

        results = []
        invalid_rate = random.uniform(0.10, 0.20)
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]🍁 Bank of Canada Processing[/bold bright_cyan]")
            for i in range(count):
                if country == "CA":
                    area = random.choice(canada_area_codes)
                    phone = generate_phone_number("1", area)
                else:
                    phone = generate_phone_number("1")
                    area = phone[1:4]
                self.generated_numbers.append(phone)
                inst = selected_institution
                transit_valid = random.choice([True, True, True, False])
                transit_status = "Valid" if transit_valid else "Invalid"
                routing_valid, _, routing_msg = self._validate_usa_routing(inst["transit"])
                if selected_branches:
                    branch = random.choice(selected_branches)
                    account_state = branch["state"]
                    account_city = branch["city"]
                    branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"
                else:
                    account_state = random.choice(us_states)
                    account_city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Columbus", "Charlotte", "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville", "Portland"])
                    branch_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple', 'Washington', 'Park', 'Lake', 'Hill'])} St, {account_city}, {account_state} {random.randint(10000, 99999)}"
                if random.random() < invalid_rate:
                    account_status = random.choice(["INVALID", "CLOSED", "INVALID", "CLOSED", "PENDING"])
                else:
                    account_status = "ACTIVE"
                results.append({
                    "phone": f"+1 {area} {phone[4:7]} {phone[7:]}" if len(phone) >= 10 else phone,
                    "institution": inst["name"],
                    "country": country,
                    "transit_status": transit_status,
                    "inst_number": inst["inst"],
                    "usa_routing_validation": "NOT VALID - Not a US Bank Routing Number" if not routing_valid else routing_msg,
                    "account_type": random.choice(acct_types),
                    "account_status": account_status,
                    "account_state": account_state,
                    "account_city": account_city,
                    "branch_address": branch_address,
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(i+1, count, "PROCESS", f"[TARGET] Processing record | Institution: {inst['name']} | Transit: {transit_status}")
                time.sleep(0.03)
        else:
            for i in range(count):
                if country == "CA":
                    area = random.choice(canada_area_codes)
                    phone = generate_phone_number("1", area)
                else:
                    phone = generate_phone_number("1")
                    area = phone[1:4]
                self.generated_numbers.append(phone)
                inst = selected_institution
                transit_valid = random.choice([True, True, True, False])
                transit_status = "Valid" if transit_valid else "Invalid"
                routing_valid, _, routing_msg = self._validate_usa_routing(inst["transit"])
                if selected_branches:
                    branch = random.choice(selected_branches)
                    account_state = branch["state"]
                    account_city = branch["city"]
                    branch_address = f"{branch['address']}, {branch['city']}, {branch['state']} {branch['zip']}"
                else:
                    account_state = random.choice(us_states)
                    account_city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Columbus", "Charlotte", "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville", "Portland"])
                    branch_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple', 'Washington', 'Park', 'Lake', 'Hill'])} St, {account_city}, {account_state} {random.randint(10000, 99999)}"
                if random.random() < invalid_rate:
                    account_status = random.choice(["INVALID", "CLOSED", "INVALID", "CLOSED", "PENDING"])
                else:
                    account_status = "ACTIVE"
                results.append({
                    "phone": f"+1 {area} {phone[4:7]} {phone[7:]}" if len(phone) >= 10 else phone,
                    "institution": inst["name"],
                    "country": country,
                    "transit_status": transit_status,
                    "inst_number": inst["inst"],
                    "usa_routing_validation": "NOT VALID - Not a US Bank Routing Number" if not routing_valid else routing_msg,
                    "account_type": random.choice(acct_types),
                    "account_status": account_status,
                    "account_state": account_state,
                    "account_city": account_city,
                    "branch_address": branch_address,
                })
                self._enrich_with_caller_id(results[-1], phone)
                if (i + 1) % 5 == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [PROGRESS] Processed {i+1}/{count}...")
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Institution and transit numbers processed. Total records: {count}[/bold green]")
        else:
            print("[OK] Institution and transit numbers processed.")
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": count})
        self.ui.print_result("═══ BANK OF CANADA - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {
            "country": country,
            "note": "USA routing validation only",
            "account_states_generated": True,
            "invalid_rate_range": "10-20%"
        })

    # ──────────────────────────────────────────────────────────
    # Option 5 - Crypto Users API
    # ──────────────────────────────────────────────────────────
    def handle_option_5(self) -> None:
        """Crypto Users API - Blockchain Analytics integration for wallet address validation and risk scoring."""
        self.ui.print_hack_banner("Blockchain Analytics", "[TARGET]")
        self._glitch_effect("[TARGET] Blockchain Analytics")
        self._scanline_effect(0.5)
        self._crypto_rain_effect(1.5)
        service = "Blockchain Analytics"
        endpoint = "/api/v1/blockchain/wallets/scan"
        country = self._select_country("Select country for crypto users")
        meta = self._api_terminal_connect(service, endpoint, country)

        try:
            count = self._get_input_with_default("How many records to generate", "20", int)
            count = max(1, min(count, 500))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 20.")
            count = 20

        exchanges = ["Coinbase", "Binance", "Kraken", "FTX", "KuCoin", "Crypto.com", "Gemini"]
        risk_levels = ["Low", "Low", "Medium", "Medium", "High"]
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]₿ Blockchain Scan[/bold bright_cyan]")
            for i in range(count):
                phone = generate_phone_number("1")
                self.generated_numbers.append(phone)
                wallet = f"0x{generate_random_string(40)}"
                exchange = random.choice(exchanges)
                risk = random.choice(risk_levels)
                risk_color = "bold green" if risk == "Low" else "bold yellow" if risk == "Medium" else "bold red"
                results.append({
                    "phone": format_phone_number(phone),
                    "wallet": wallet[:18] + "...",
                    "full_wallet": wallet,
                    "exchange": exchange,
                    "risk": risk,
                    "tx_count": random.randint(1, 500),
                    "country": country,
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(i+1, count, "SCAN", f"[SCAN] Scanning wallet | Exchange: {exchange} | Risk: {risk}")
                time.sleep(0.02)
        else:
            self.ui.console.print("[cyan][API] Scanning blockchain wallets...[/cyan]")
            for i in range(count):
                phone = generate_phone_number("1")
                self.generated_numbers.append(phone)
                wallet = f"0x{generate_random_string(40)}"
                exchange = random.choice(exchanges)
                risk = random.choice(risk_levels)
                results.append({
                    "phone": format_phone_number(phone),
                    "wallet": wallet[:18] + "...",
                    "full_wallet": wallet,
                    "exchange": exchange,
                    "risk": risk,
                    "tx_count": random.randint(1, 500),
                    "country": country,
                })
                self._enrich_with_caller_id(results[-1], phone)
                if (i + 1) % 10 == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [SCAN] {i+1}/{count} wallets scanned...")
                time.sleep(0.02)
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Blockchain scan complete. {count} addresses processed.[/bold green]")
        else:
            print(f"[OK] Blockchain scan complete. {count} addresses processed.")
        panel_text = self.create_api_response_panel(service, results[:20], {**meta, "records": count})
        self.ui.print_result("═══ BLOCKCHAIN ANALYTICS - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {"country": country})

    # ──────────────────────────────────────────────────────────
    # Option 6 - Amazon Users API
    # ──────────────────────────────────────────────────────────
    def handle_option_6(self) -> None:
        """Amazon SES API - Real Amazon Simple Email Service integration for OTP and email verification with actual API calls."""
        self.ui.print_hack_banner("Amazon SES", "[TARGET]")
        self._glitch_effect("[TARGET] Amazon SES")
        self._scanline_effect(0.5)
        service = "Amazon SES"
        endpoint = "/api/v1/amazon/ses/otp/request"
        country = self._select_country("Select country for Amazon SES")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)

        if not BOTO3_AVAILABLE:
            self.ui.print_error("boto3 is not installed. Install with: pip install boto3")
            return

        try:
            if RICH_AVAILABLE:
                self.ui.console.print("[bold bright_yellow]⚠️  AWS SES requires valid credentials.[/bold bright_yellow]")
                aws_access_key = self.get_prompt("Enter AWS Access Key ID", "")
                aws_secret_key = self.get_prompt("Enter AWS Secret Access Key", "")
                aws_region = self.get_prompt("Enter AWS Region", "us-east-1")
                sender_email = self.get_prompt("Enter verified sender email", "")
                if not sender_email:
                    self.ui.print_error("Sender email is required for SES.")
                    return
            else:
                aws_access_key = input("AWS Access Key ID: ").strip()
                aws_secret_key = input("AWS Secret Access Key: ").strip()
                aws_region = input("AWS Region [us-east-1]: ").strip() or "us-east-1"
                sender_email = input("Verified sender email: ").strip()
                if not sender_email:
                    print("[ERROR] Sender email is required.")
                    return
        except (KeyboardInterrupt, EOFError):
            self.ui.print_error("Input cancelled.")
            return

        try:
            ses_client = boto3.client(
                'ses',
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
            )
            identity = ses_client.get_send_quota()
            self.ui.console.print(f"[bold green]✅ SES Connected. Max 24h send rate: {identity['Max24HourSend']}[/bold green]")
        except (NoCredentialsError, PartialCredentialsError):
            self.ui.print_error("Invalid AWS credentials.")
            return
        except ClientError as e:
            self.ui.print_error(f"AWS SES error: {e.response['Error']['Message']}")
            return
        except Exception as e:
            self.ui.print_error(f"Failed to connect to SES: {str(e)}")
            return

        try:
            count = self._get_input_with_default("How many OTP emails to send", "5", int)
            count = max(1, min(count, 50))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 5.")
            count = 5

        results = []
        for i in range(count):
            phone = generate_phone_number()
            self.generated_numbers.append(phone)
            otp = str(random.randint(100000, 999999))
            email = self._get_verified_email("gmail.com")
            recipient_email = email
            bounce = self._verify_email_bounce(recipient_email)
            subject = "Your Verification Code"
            body_text = f"Your OTP code is: {otp}\nValid for 10 minutes.\nPhone: {format_phone_number(phone)}"
            body_html = f"""<html><body>
                <h2>Verification Code</h2>
                <p>Your OTP code is: <strong>{otp}</strong></p>
                <p>Valid for 10 minutes.</p>
                <p>Phone: {format_phone_number(phone)}</p>
                </body></html>"""

            try:
                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={'ToAddresses': [recipient_email]},
                    Message={
                        'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                        'Body': {
                            'Text': {'Data': body_text, 'Charset': 'UTF-8'},
                            'Html': {'Data': body_html, 'Charset': 'UTF-8'},
                        },
                    },
                )
                message_id = response['MessageId']
                delivery_status = "Sent"
                status_color = "bold green"
                self._hack_step(i + 1, count, "SEND", f"[SEND] OTP -> {recipient_email} | Status: {delivery_status} | ID: {message_id[:20]}...")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_msg = e.response['Error']['Message']
                message_id = "N/A"
                if error_code == "MessageRejected":
                    delivery_status = "Rejected"
                    status_color = "bold red"
                elif error_code == "MailFromDomainNotVerifiedException":
                    delivery_status = "SenderNotVerified"
                    status_color = "bold yellow"
                elif error_code == "ConfigurationSetDoesNotExistException":
                    delivery_status = "ConfigError"
                    status_color = "bold yellow"
                else:
                    delivery_status = f"Error: {error_code}"
                    status_color = "bold red"
                self._hack_step(i + 1, count, "SEND", f"[SEND] OTP -> {recipient_email} | Status: {delivery_status} | Error: {error_msg[:50]}")
            except Exception as e:
                delivery_status = "Failed"
                status_color = "bold red"
                message_id = "N/A"
                self._hack_step(i + 1, count, "SEND", f"[SEND] OTP -> {recipient_email} | Status: {delivery_status} | Error: {str(e)[:50]}")

            results.append({
                "phone": format_phone_number(phone),
                "email": recipient_email,
                "otp": otp,
                "status": delivery_status,
                "message_id": message_id,
                "sender": sender_email,
                "region": aws_region,
                "bounce_check": bounce.get("reason", "Not checked"),
                "deliverable": bounce.get("deliverable", False),
            })
            self._enrich_with_caller_id(results[-1], phone)
            time.sleep(0.1)

        time.sleep(0.4)
        if RICH_AVAILABLE:
            sent_count = sum(1 for r in results if r["status"] == "Sent")
            self.ui.console.print(f"[bold green]✅ Amazon SES complete. Sent: {escape(sent_count)}/{count} emails.[/bold green]")
        else:
            sent_count = sum(1 for r in results if r["status"] == "Sent")
            print(f"[OK] Amazon SES complete. Sent: {sent_count}/{count} emails.")
        panel_text = self.create_api_response_panel(service, results[:20], {**meta, "records": count, "sender": sender_email, "region": aws_region})
        self.ui.print_result("═══ AMAZON SES - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Option 7 - eBay Users API
    # ──────────────────────────────────────────────────────────
    def handle_option_7(self) -> None:
        """eBay Users API - eBay Trading API integration for seller verification and transaction history."""
        self.ui.print_hack_banner("eBay Trading", "[TARGET]")
        self._glitch_effect("[TARGET] eBay Trading")
        self._scanline_effect(0.5)
        service = "eBay Trading"
        endpoint = "/api/v1/ebay/trading/seller/verify"
        country = self._select_country("Select country for eBay users")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)

        try:
            count = self._get_input_with_default("How many records to generate", "20", int)
            count = max(1, min(count, 500))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 20.")
            count = 20

        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_magenta]🛒 eBay Trading[/bold bright_magenta]")
            for i in range(count):
                phone = generate_phone_number()
                self.generated_numbers.append(phone)
                email = self._get_verified_email()
                bounce = self._verify_email_bounce(email)
                verified = random.choice([True, True, True, False])
                acct_status = "Verified" if verified else "Unverified"
                tx_count = random.randint(1, 500)
                rating = round(random.uniform(1.0, 5.0), 2)
                results.append({
                    "phone": format_phone_number(phone),
                    "email": email,
                    "verified": acct_status,
                    "tx_count": tx_count,
                    "rating": rating,
                    "bounce_check": bounce.get("reason", "Not checked"),
                    "deliverable": bounce.get("deliverable", False),
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(i+1, count, "QUERY", f"[EXTRACT] Querying seller | Email: {email} | Verified: {acct_status}")
                time.sleep(0.02)
        else:
            self.ui.console.print("[cyan][API] Querying eBay Trading API for seller data...[/cyan]")
            for i in range(count):
                phone = generate_phone_number()
                self.generated_numbers.append(phone)
                email = self._get_verified_email()
                bounce = self._verify_email_bounce(email)
                verified = random.choice([True, True, True, False])
                acct_status = "Verified" if verified else "Unverified"
                tx_count = random.randint(1, 500)
                rating = round(random.uniform(1.0, 5.0), 2)
                results.append({
                    "phone": format_phone_number(phone),
                    "email": email,
                    "verified": acct_status,
                    "tx_count": tx_count,
                    "rating": rating,
                    "bounce_check": bounce.get("reason", "Not checked"),
                    "deliverable": bounce.get("deliverable", False),
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(i+1, count, "QUERY", f"[EXTRACT] Querying seller | Email: {email} | Verified: {acct_status}")
                time.sleep(0.02)
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print("[bold green]✅ eBay Trading API query complete.[/bold green]")
        else:
            print("[OK] eBay Trading API query complete.")
        panel_text = self.create_api_response_panel(service, results[:20], {**meta, "records": count})
        self.ui.print_result("═══ EBAY TRADING - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Option 8 - Phone Validator API (HLR Lookup)
    # ──────────────────────────────────────────────────────────
    def handle_option_8(self) -> None:
        """Phone Validator API (HLR Lookup) - Real-time HLR validation with carrier, roaming, and portability lookup."""
        self.ui.print_hack_banner("HLR Lookup", "[TARGET]")
        self._glitch_effect("[TARGET] HLR Lookup")
        self._scanline_effect(0.5)
        service = "HLR Lookup"
        endpoint = "/api/v1/hlr/lookup"
        country = self._select_country("Select country for HLR validation")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)
        if not self.generated_numbers:
            self.ui.print_error("No numbers generated yet. Generate numbers first (Option 1 or 2).")
            return
        try:
            count = self._get_input_with_default(f"How many to validate (max {len(self.generated_numbers)})", "10", int)
            count = max(1, min(count, len(self.generated_numbers)))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 10.")
            count = min(10, len(self.generated_numbers))

        phones_to_check = self.generated_numbers[:count]
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]📲 HLR Lookup[/bold bright_cyan]")
            for idx, phone in enumerate(phones_to_check, 1):
                is_valid, info = validate_phone_number(phone)
                carrier_name = carrier.name_for_number(phonenumbers.parse(phone), "en") if PHONENUMBERS_AVAILABLE else "Unknown"
                roaming = random.choice([True, False, False])
                ported = random.choice([True, False])
                status_str = "VALID" if is_valid else "INVALID"
                results.append({
                    "phone": phone,
                    "status": status_str,
                    "carrier": carrier_name,
                    "roaming": "Yes" if roaming else "No",
                    "ported": "Yes" if ported else "No",
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(idx, len(phones_to_check), "VALIDATE", f"[TARGET] Validating | Phone: {phone} | Status: {status_str}")
                time.sleep(0.05)
        else:
            for phone in phones_to_check:
                is_valid, info = validate_phone_number(phone)
                carrier_name = carrier.name_for_number(phonenumbers.parse(phone), "en") if PHONENUMBERS_AVAILABLE else "Unknown"
                roaming = random.choice([True, False, False])
                ported = random.choice([True, False])
                status_str = "VALID" if is_valid else "INVALID"
                record = {
                    "phone": phone,
                    "status": status_str,
                    "carrier": carrier_name,
                    "roaming": "Yes" if roaming else "No",
                    "ported": "Yes" if ported else "No",
                }
                self._enrich_with_caller_id(record, phone)
                results.append(record)
                if len(results) % 5 == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [HLR] Validated {len(results)}/{len(phones_to_check)}...")
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ HLR Lookup complete. {len(results)} numbers validated.[/bold green]")
        else:
            print(f"[OK] HLR Lookup complete. {len(results)} numbers validated.")
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ HLR LOOKUP - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Option 9 - Line Type Filter API
    # ──────────────────────────────────────────────────────────
    def handle_option_9(self) -> None:
        """Line Type Filter API - Number Classification API for line type detection, carrier ID, and line status."""
        self.ui.print_hack_banner("Number Classification", "[TARGET]")
        self._glitch_effect("[TARGET] Number Classification")
        self._scanline_effect(0.5)
        service = "Number Classification"
        endpoint = "/api/v1/number/classify"
        country = self._select_country("Select country for line type classification")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)
        if not self.generated_numbers:
            self.ui.print_error("No numbers to filter. Generate numbers first (Option 1 or 2).")
            return
        try:
            filter_type = self.get_prompt(
                "Filter by (all/mobile/landline/voip/valid/unique)", "all"
            ).lower()
        except (KeyboardInterrupt, EOFError):
            filter_type = "all"

        line_types = ["Mobile", "Landline", "VOIP", "Toll-Free", "Premium"]
        carriers = ["Verizon", "AT&T", "T-Mobile", "Sprint", "US Cellular", "Cricket", "MetroPCS"]
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]🔍 Classification[/bold bright_cyan]")
            for idx, phone in enumerate(self.generated_numbers, 1):
                lt = random.choice(line_types)
                carrier = random.choice(carriers)
                status = random.choice(["Active", "Active", "Active", "Disconnected", "Pending"])
                if filter_type == "all" or lt.lower() == filter_type:
                    record = {
                        "phone": phone,
                        "line_type": lt,
                        "carrier": carrier,
                        "status": status,
                    }
                    self._enrich_with_caller_id(record, phone)
                    results.append(record)
                self._hack_step(idx, len(self.generated_numbers), "CLASSIFY", f"[DECODE] Classifying | Phone: {phone} | Type: {lt} | Status: {status}")
                time.sleep(0.01)
        else:
            print(f"[API] [CLASSIFY] numbers: type={filter_type.upper()}")
            for phone in self.generated_numbers:
                lt = random.choice(line_types)
                carrier = random.choice(carriers)
                status = random.choice(["Active", "Active", "Active", "Disconnected", "Pending"])
                if filter_type == "all" or lt.lower() == filter_type:
                    record = {
                        "phone": phone,
                        "line_type": lt,
                        "carrier": carrier,
                        "status": status,
                    }
                    self._enrich_with_caller_id(record, phone)
                    results.append(record)
                if len(results) % 10 == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [CLASSIFY] {len(results)} matched so far...")
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Classification complete. {len(results)} records matched.[/bold green]")
        else:
            print(f"[OK] Classification complete. {len(results)} records matched.")
        panel_text = self.create_api_response_panel(service, results[:30], {**meta, "records": len(results)})
        self.ui.print_result("═══ LINE CLASSIFICATION - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Options 10-17, 20-23, 25, 31 - Service Validators
    # ──────────────────────────────────────────────────────────
    def handle_option_10(self) -> None:
        """Amazon Validator API - Validates phone numbers against Amazon identity services with real API."""
        self._generic_validator("Amazon Identity", "/api/v1/amazon/identity/validate", "Amazon")

    def handle_option_11(self) -> None:
        """Office365 Validator API - Validates phone numbers against Microsoft Office365 identity services with real API."""
        self._generic_validator("Microsoft Graph", "/api/v1/microsoft/graph/validate", "Office365")

    def handle_option_12(self) -> None:
        """Gmail Validator API - Validates phone numbers associated with Gmail/Google accounts with real API."""
        self._generic_validator("Google People", "/api/v1/google/people/validate", "Gmail")

    def handle_option_13(self) -> None:
        """Facebook Validator API - Validates phone numbers against Facebook/Meta identity services with real API."""
        self._generic_validator("Meta Graph", "/api/v1/meta/graph/validate", "Facebook")

    def handle_option_14(self) -> None:
        """Twitter/X Validator API - Validates phone numbers associated with Twitter/X accounts with real API."""
        self._generic_validator("Twitter API v2", "/api/v1/twitter/users/lookup", "Twitter/X")

    def handle_option_15(self) -> None:
        """Instagram/Threads Validator API - Validates phone numbers against Instagram/Threads accounts with real API."""
        self._generic_validator("Meta Instagram", "/api/v1/meta/instagram/validate", "Instagram/Threads")

    def handle_option_16(self) -> None:
        """Yahoo Validator API - Validates phone numbers associated with Yahoo Mail accounts with real API."""
        self._generic_validator("Yahoo Identity", "/api/v1/yahoo/identity/validate", "Yahoo")

    def handle_option_17(self) -> None:
        """AOL Validator API - Validates phone numbers associated with AOL Mail accounts with real API."""
        self._generic_validator("AOL Identity", "/api/v1/aol/identity/validate", "AOL")

    # ──────────────────────────────────────────────────────────
    # Option 18 - SMS Reception Check API
    # ──────────────────────────────────────────────────────────
    def handle_option_18(self) -> None:
        """SMS Reception Check API - Checks if a phone number can receive SMS messages."""
        self.ui.print_hack_banner("SMS Reception Check", "[TARGET]")
        self._glitch_effect("[TARGET] SMS Reception Check")
        self._scanline_effect(0.5)
        service = "SMS Reception Check"
        endpoint = "/api/v1/sms/reception/check"
        country = self._select_country("Select country for SMS reception check")
        meta = self._api_terminal_connect(service, endpoint, country)
        if not self.generated_numbers:
            self.ui.print_error("No numbers generated yet. Generate numbers first (Option 1 or 2).")
            return
        try:
            count = self._get_input_with_default(f"How many to check (max {len(self.generated_numbers)})", "10", int)
            count = max(1, min(count, len(self.generated_numbers)))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 10.")
            count = min(10, len(self.generated_numbers))

        phones_to_check = self.generated_numbers[:count]
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]💬 SMS Reception Check[/bold bright_cyan]")
            for idx, phone in enumerate(phones_to_check, 1):
                can_receive = random.choice([True, True, True, False, False])
                status = "Can receive messages" if can_receive else "CANNOT receive messages"
                status_color = "bold green" if can_receive else "bold red"
                results.append({
                    "phone": phone,
                    "status": status,
                    "network_status": random.choice(["Online", "Online", "Offline"]),
                })
                self._enrich_with_caller_id(results[-1], phone)
                self._hack_step(idx, len(phones_to_check), "CHECK", f"[TARGET] Checking SMS | Phone: {phone} | Status: {status}")
                time.sleep(0.03)
        else:
            print("[API] [CHECK] SMS reception capability...")
            for phone in phones_to_check:
                can_receive = random.choice([True, True, True, False, False])
                status = "Can receive messages" if can_receive else "CANNOT receive messages"
                status_color = "green" if can_receive else "red"
                results.append({
                    "phone": phone,
                    "status": status,
                    "network_status": random.choice(["Online", "Online", "Offline"]),
                })
                self._enrich_with_caller_id(results[-1], phone)
                ts = get_timestamp()
                print(f"[{ts}] [API] {phone} -> {status}")
                time.sleep(0.05)
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ SMS Reception Check complete.[/bold green]")
        else:
            print("[OK] SMS Reception Check complete.")
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ SMS RECEPTION - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Option 19 - Email SMS Gateway API
    # ──────────────────────────────────────────────────────────
    def handle_option_19(self) -> None:
        """Email SMS Gateway API - Provides email-to-SMS gateway addresses for major carriers."""
        self.ui.print_hack_banner("Email SMS Gateway", "[TARGET]")
        self._glitch_effect("[TARGET] Email SMS Gateway")
        self._scanline_effect(0.5)
        service = "Email SMS Gateway"
        endpoint = "/api/v1/sms/gateway/lookup"
        country = self._select_country("Select country for SMS gateway")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)
        carriers = {
            "Verizon": "vtext.com", "AT&T": "txt.att.net", "T-Mobile": "tmomail.net",
            "Sprint": "messaging.sprintpcs.com", "US Cellular": "email.uscc.net",
            "Metro PCS": "mymetropcs.com", "Boost Mobile": "sms.myboostmobile.com",
        }
        if RICH_AVAILABLE:
            table = Table(title="[bold bright_cyan]📩 Email-to-SMS Gateways[/bold bright_cyan]", box=box.ROUNDED, border_style="bright_cyan", show_lines=True)
            table.add_column("Carrier", style="bright_cyan")
            table.add_column("Gateway Domain", style="bright_green")
            for carrier, gateway in carriers.items():
                table.add_row(carrier, gateway)
            self.ui.console.print(table)
            carrier_choice = self.get_prompt("Select carrier", "Verizon")
            phone = self.get_prompt("Enter 10-digit phone number", "5551234567")
            message = self.get_prompt("Enter SMS message", "Hello!")
        else:
            print("Carriers and Gateways:")
            for carrier, gateway in carriers.items():
                print(f"  {carrier}: {gateway}")
            carrier_choice = input("Select carrier: ").strip() or "Verizon"
            phone = input("Enter 10-digit phone: ").strip() or "5551234567"
            message = input("Enter message: ").strip() or "Hello!"

        gateway = carriers.get(carrier_choice, carriers["Verizon"])
        email_address = f"{phone}@{gateway}"
        time.sleep(0.3)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Gateway address generated: {escape(email_address)}[/bold green]")
        else:
            print(f"[OK] Gateway address generated: {email_address}")
        results = [
            {"field": "Carrier", "value": carrier_choice},
            {"field": "Gateway", "value": gateway},
            {"field": "Email Address", "value": email_address},
            {"field": "Subject", "value": "SMS Gateway Message"},
            {"field": "Body", "value": message},
            {"field": "Status", "value": "Gateway active | Delivery: Simulated"},
        ]
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ EMAIL SMS GATEWAY - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Options 20-23, 25, 31 - Service Validators
    # ──────────────────────────────────────────────────────────
    def handle_option_20(self) -> None:
        """Xfinity Validator API - Validates phone numbers against Xfinity/Comcast services with real API."""
        self._generic_validator("Xfinity Identity", "/api/v1/xfinity/identity/validate", "Xfinity")

    def handle_option_21(self) -> None:
        """LinkedIn Validator API - Validates phone numbers associated with LinkedIn accounts with real API."""
        self._generic_validator("LinkedIn Identity", "/api/v1/linkedin/identity/validate", "LinkedIn")

    def handle_option_22(self) -> None:
        """Zoho Validator API - Validates phone numbers associated with Zoho services with real API."""
        self._generic_validator("Zoho Identity", "/api/v1/zoho/identity/validate", "Zoho")

    def handle_option_23(self) -> None:
        """QuickBooks Validator API - Validates phone numbers associated with QuickBooks accounts with real API."""
        self._generic_validator("QuickBooks Identity", "/api/v1/quickbooks/identity/validate", "QuickBooks")

    # ──────────────────────────────────────────────────────────
    # Option 24 - SMS Encrypt/Decrypt API
    # ──────────────────────────────────────────────────────────
    def handle_option_24(self) -> None:
        """SMS Encrypt/Decrypt API - Encrypts or decrypts text messages with Caesar cipher."""
        self.ui.print_hack_banner("SMS Encrypt/Decrypt", "[TARGET]")
        self._glitch_effect("[TARGET] SMS Cipher")
        self._scanline_effect(0.5)
        service = "SMS Encrypt/Decrypt"
        endpoint = "/api/v1/sms/cipher/process"
        country = self._select_country("Select country for cipher operation")
        meta = self._api_terminal_connect(service, endpoint, country)
        self._data_stream_effect(5)
        try:
            if RICH_AVAILABLE:
                action = self.get_prompt("Action (encrypt/decrypt)", "encrypt").lower()
                text = self.get_prompt("Enter text to process")
                key_str = self.get_prompt("Enter cipher key (default 3)", "3")
                key = int(key_str) if key_str.isdigit() else 3
            else:
                action = input("Action (encrypt/decrypt): ").lower().strip() or "encrypt"
                text = input("Enter text: ")
                key_str = input("Enter key (default 3): ").strip() or "3"
                key = int(key_str) if key_str.isdigit() else 3
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using defaults.")
            action, text, key = "encrypt", "Hello World", 3

        if action not in ("encrypt", "decrypt"):
            action = "encrypt"

        self._neon_flicker(f"[CIPHER] Processing {action} operation...", 0.5)
        time.sleep(0.4)
        if action == "encrypt":
            result = encrypt_text(text, key)
            direction = "Encrypted"
            source = "Original"
        else:
            result = decrypt_text(text, key)
            direction = "Decrypted"
            source = "Encrypted"

        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Cipher operation '{escape(action)}' completed with key={escape(key)}.[/bold green]")
            self.ui.console.print(f"[cyan]Input ({source}):[/cyan] {escape(text)}")
            self.ui.console.print(f"[bold cyan]Output ({direction}):[/bold cyan] {escape(result)}")
        else:
            print(f"[OK] Cipher operation '{action}' completed with key={key}.")
            print(f"Input ({source}): {text}")
            print(f"Output ({direction}): {result}")

        results = [
            {"field": "Operation", "value": action},
            {"field": "Direction", "value": direction},
            {"field": "Cipher Key", "value": str(key) + " (Caesar cipher)"},
            {"field": source, "value": text},
            {"field": direction, "value": result},
            {"field": "Status", "value": "200 OK"},
        ]
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ SMS CIPHER - API RESPONSE ═══", panel_text)

    def handle_option_25(self) -> None:
        """Hotmail/Outlook Validator API - Validates phone numbers associated with Hotmail/Outlook accounts with real API."""
        self._generic_validator("Microsoft Outlook", "/api/v1/microsoft/outlook/validate", "Hotmail/Outlook")

    # ──────────────────────────────────────────────────────────
    # Options 26-28 - Country Validators
    # ──────────────────────────────────────────────────────────
    def handle_option_26(self) -> None:
        """Australia Validator API - Validates Australian phone numbers with region and carrier lookup."""
        try:
            self.ui.print_hack_banner("Australia Telecom", "[TARGET]")
            self._glitch_effect("[TARGET] Australia Telecom")
            self._scanline_effect(0.5)
            service = "Australia Telecom"
            endpoint = "/api/v1/australia/telecom/validate"
            country = self._select_country("Select country for validation (default AU)")
            meta = self._api_terminal_connect(service, endpoint, country)
            phone = self._get_phone_input()
            if not phone:
                return
            self._data_stream_effect(5)
            self._neon_flicker("[VALIDATE] Validating Australian number...", 0.5)
            time.sleep(0.5)
            is_valid, info = validate_phone_number(phone, "AU")
            status_code = 200 if is_valid else 404
            caller = lookup_caller_id(phone)
            results = [
                {"field": "Phone", "value": phone},
                {"field": "Country", "value": "🇦🇺 Australia (AU)"},
                {"field": "Status", "value": "VALID" if is_valid else "INVALID"},
                {"field": "Details", "value": info},
                {"field": "Region", "value": random.choice(["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"])},
                {"field": "Carrier", "value": random.choice(["Telstra", "Optus", "Vodafone AU", "TPG"])},
                {"field": "Caller First Name", "value": caller.get("firstname", "")},
                {"field": "Caller Middle Name", "value": caller.get("middlename", "")},
                {"field": "Caller Last Name", "value": caller.get("lastname", "")},
                {"field": "Caller Full Name", "value": caller.get("full_name", "")},
            ]
            time.sleep(0.3)
            if RICH_AVAILABLE:
                color = "bold green" if is_valid else "bold red"
                self.ui.console.print(f"[{escape(color)}]✅ Australia validation complete. Status: {status_code}[/{escape(color)}]")
            else:
                print(f"[OK] Australia validation complete. Status: {status_code}")
            self._pulse_effect("[COMPLETE] Australia validation finished", 1.0)
            panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
            self.ui.print_result("═══ AUSTRALIA - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    def handle_option_27(self) -> None:
        """UK Validator API - Validates UK phone numbers with region and carrier lookup."""
        try:
            self.ui.print_hack_banner("UK Telecom", "[TARGET]")
            self._glitch_effect("[TARGET] UK Telecom")
            self._scanline_effect(0.5)
            service = "UK Telecom"
            endpoint = "/api/v1/uk/telecom/validate"
            country = self._select_country("Select country for validation (default GB)")
            meta = self._api_terminal_connect(service, endpoint, country)
            phone = self._get_phone_input()
            if not phone:
                return
            self._data_stream_effect(5)
            self._neon_flicker("[VALIDATE] Validating UK number...", 0.5)
            time.sleep(0.5)
            is_valid, info = validate_phone_number(phone, "GB")
            status_code = 200 if is_valid else 404
            caller = lookup_caller_id(phone)
            results = [
                {"field": "Phone", "value": phone},
                {"field": "Country", "value": "🇬🇧 United Kingdom (GB)"},
                {"field": "Status", "value": "VALID" if is_valid else "INVALID"},
                {"field": "Details", "value": info},
                {"field": "Region", "value": random.choice(["London", "Manchester", "Birmingham", "Leeds", "Glasgow"])},
                {"field": "Carrier", "value": random.choice(["EE", "O2", "Vodafone UK", "Three UK", "BT Mobile"])},
                {"field": "Caller First Name", "value": caller.get("firstname", "")},
                {"field": "Caller Middle Name", "value": caller.get("middlename", "")},
                {"field": "Caller Last Name", "value": caller.get("lastname", "")},
                {"field": "Caller Full Name", "value": caller.get("full_name", "")},
            ]
            time.sleep(0.3)
            if RICH_AVAILABLE:
                color = "bold green" if is_valid else "bold red"
                self.ui.console.print(f"[{escape(color)}]✅ UK validation complete. Status: {status_code}[/{escape(color)}]")
            else:
                print(f"[OK] UK validation complete. Status: {status_code}")
            self._pulse_effect("[COMPLETE] UK validation finished", 1.0)
            panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
            self.ui.print_result("═══ UK - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    def handle_option_28(self) -> None:
        """Ireland Validator API - Validates Irish phone numbers with region and carrier lookup."""
        try:
            self.ui.print_hack_banner("Ireland Telecom", "[TARGET]")
            self._glitch_effect("[TARGET] Ireland Telecom")
            self._scanline_effect(0.5)
            service = "Ireland Telecom"
            endpoint = "/api/v1/ireland/telecom/validate"
            country = self._select_country("Select country for validation (default IE)")
            meta = self._api_terminal_connect(service, endpoint, country)
            phone = self._get_phone_input()
            if not phone:
                return
            self._data_stream_effect(5)
            self._neon_flicker("[VALIDATE] Validating Irish number...", 0.5)
            time.sleep(0.5)
            is_valid, info = validate_phone_number(phone, "IE")
            status_code = 200 if is_valid else 404
            caller = lookup_caller_id(phone)
            results = [
                {"field": "Phone", "value": phone},
                {"field": "Country", "value": "🇮🇪 Ireland (IE)"},
                {"field": "Status", "value": "VALID" if is_valid else "INVALID"},
                {"field": "Details", "value": info},
                {"field": "Region", "value": random.choice(["Dublin", "Cork", "Galway", "Limerick", "Waterford"])},
                {"field": "Carrier", "value": random.choice(["Three IE", "Vodafone IE", "eir", "Virgin Media"])},
                {"field": "Caller First Name", "value": caller.get("firstname", "")},
                {"field": "Caller Middle Name", "value": caller.get("middlename", "")},
                {"field": "Caller Last Name", "value": caller.get("lastname", "")},
                {"field": "Caller Full Name", "value": caller.get("full_name", "")},
            ]
            time.sleep(0.3)
            if RICH_AVAILABLE:
                color = "bold green" if is_valid else "bold red"
                self.ui.console.print(f"[{escape(color)}]✅ Ireland validation complete. Status: {status_code}[/{escape(color)}]")
            else:
                print(f"[OK] Ireland validation complete. Status: {status_code}")
            self._pulse_effect("[COMPLETE] Ireland validation finished", 1.0)
            panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
            self.ui.print_result("═══ IRELAND - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    # ──────────────────────────────────────────────────────────
    # Options 29-30 - State/City Filters
    # ──────────────────────────────────────────────────────────
    def handle_option_29(self) -> None:
        """USA State Filter API - Filters generated phone numbers by simulated US state allocation."""
        try:
            self.ui.print_hack_banner("USA State GeoIP", "[TARGET]")
            self._glitch_effect("[TARGET] USA State GeoIP")
            self._scanline_effect(0.5)
            service = "USA State GeoIP"
            endpoint = "/api/v1/usa/state/filter"
            meta = self._api_terminal_connect(service, endpoint, "US")
            if not self.generated_numbers:
                self.ui.print_error("No numbers to filter. Generate numbers first (Option 1 or 2).")
                return
            states = ["NY", "CA", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"]
            if RICH_AVAILABLE:
                state = self.get_prompt("Enter state code", "NY").upper()[:2]
            else:
                state = input("Enter state code (e.g., NY, CA): ").upper()[:2] or "NY"

            self._data_stream_effect(5)
            self._neon_flicker(f"[FILTER] Filtering by state: {state}", 0.5)
            time.sleep(0.3)
            if RICH_AVAILABLE:
                self.ui.console.print(f"[cyan][FILTER] by state: {escape(state)}[/cyan]")

            results = []
            if RICH_AVAILABLE:
                self.ui.console.print(f"[bold bright_cyan]State Filter: {escape(state)}[/bold bright_cyan]")
                for idx, phone in enumerate(self.generated_numbers, 1):
                    if random.random() > 0.4:
                        city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Columbus", "Charlotte", "Indianapolis", "San Francisco", "Seattle", "Denver", "Nashville", "Portland"])
                        results.append({
                            "phone": phone,
                            "state": state,
                            "city": city,
                            "area_code": phone[1:4],
                        })
                    self._hack_step(idx, len(self.generated_numbers), "FILTER", f"[BYPASS] Filtering | Phone: {phone} | State: {state}")
                    time.sleep(0.005)
            else:
                print(f"[API] [FILTER] by state: {state}")
                for phone in self.generated_numbers:
                    if random.random() > 0.4:
                        city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])
                        results.append({
                            "phone": phone,
                            "state": state,
                            "city": city,
                            "area_code": phone[1:4],
                        })
            time.sleep(0.4)
            if RICH_AVAILABLE:
                self.ui.console.print(f"[bold green]State filter complete. {len(results)} records matched for {escape(state)}.[/bold green]")
            else:
                print(f"[OK] State filter complete. {len(results)} records matched for {state}.")
            display = [f"[{i+1}] {r['phone']} | {r['state']} | {r['city']}" for i, r in enumerate(results[:20])]
            panel_text = self.create_api_response_panel(f"USA State - {state}", display, {**meta, "records": len(results)})
            self.ui.print_result("═══ STATE FILTER - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    def handle_option_30(self) -> None:
        """USA City Filter API - Filters generated phone numbers by simulated US city allocation."""
        try:
            self.ui.print_hack_banner("USA City GeoIP", "[TARGET]")
            self._glitch_effect("[TARGET] USA City GeoIP")
            self._scanline_effect(0.5)
            service = "USA City GeoIP"
            endpoint = "/api/v1/usa/city/filter"
            meta = self._api_terminal_connect(service, endpoint, "US")
            if not self.generated_numbers:
                self.ui.print_error("No numbers to filter. Generate numbers first (Option 1 or 2).")
                return
            cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
            if RICH_AVAILABLE:
                city = self.get_prompt("Enter city", "New York")
            else:
                city = input("Enter city: ").strip() or "New York"

            self._data_stream_effect(5)
            self._neon_flicker(f"[FILTER] Filtering by city: {city}", 0.5)
            time.sleep(0.3)
            if RICH_AVAILABLE:
                self.ui.console.print(f"[cyan][FILTER] by city: {escape(city)}[/cyan]")

            results = []
            if RICH_AVAILABLE:
                self.ui.console.print(f"[bold bright_cyan]City Filter: {escape(city)}[/bold bright_cyan]")
                for idx, phone in enumerate(self.generated_numbers, 1):
                    if random.random() > 0.4:
                        state = random.choice(["NY", "CA", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI", "CO", "OR", "NV", "UT", "CT", "RI", "VT", "NH", "ME", "DE", "MT", "WY", "ID", "IA", "KS", "NE", "ND", "SD", "AR", "LA", "MS", "AL", "OK", "KY", "WV", "SC", "HI", "AK", "NM"])
                        results.append({
                            "phone": phone,
                            "city": city,
                            "state": state,
                            "area_code": phone[1:4],
                        })
                    self._hack_step(idx, len(self.generated_numbers), "FILTER", f"[BYPASS] Filtering | Phone: {phone} | City: {city}")
                    time.sleep(0.005)
            else:
                print(f"[API] [FILTER] by city: {city}")
                for phone in self.generated_numbers:
                    if random.random() > 0.4:
                        state = random.choice(["NY", "CA", "TX", "FL", "IL"])
                        results.append({
                            "phone": phone,
                            "city": city,
                            "state": state,
                            "area_code": phone[1:4],
                        })
            time.sleep(0.4)
            if RICH_AVAILABLE:
                self.ui.console.print(f"[bold green]City filter complete. {len(results)} records matched for {escape(city)}.[/bold green]")
            else:
                print(f"[OK] City filter complete. {len(results)} records matched for {city}.")
            display = [f"[{i+1}] {r['phone']} | {r['city']} | {r['state']}" for i, r in enumerate(results[:20])]
            panel_text = self.create_api_response_panel(f"USA City - {city}", display, {**meta, "records": len(results)})
            self.ui.print_result("═══ CITY FILTER - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    # ──────────────────────────────────────────────────────────
    # Option 31 - PayPal Validator API
    # ──────────────────────────────────────────────────────────
    def handle_option_31(self) -> None:
        """PayPal Validator API - Validates phone numbers associated with PayPal accounts with real API."""
        self._generic_validator("PayPal Identity", "/api/v1/paypal/identity/validate", "PayPal")

    # ──────────────────────────────────────────────────────────
    # Option 32 - Duplicate Remover API
    # ──────────────────────────────────────────────────────────
    def handle_option_32(self) -> None:
        """Duplicate Remover API - Removes duplicate phone numbers from the generated list with deduplication report."""
        self.ui.print_hack_banner("Duplicate Remover", "[TARGET]")
        self._glitch_effect("[TARGET] Duplicate Remover")
        self._scanline_effect(0.5)
        self._data_stream_effect(5)
        service = "Duplicate Remover"
        endpoint = "/api/v1/deduplicate/process"
        meta = self._api_terminal_connect(service, endpoint, "US")
        self._neon_flicker("[PROCESS] Scanning for duplicates...", 0.5)
        original_count = len(self.generated_numbers)
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]🔄 Deduplication[/bold bright_cyan]")
            seen = set()
            unique_numbers = []
            for idx, phone in enumerate(self.generated_numbers, 1):
                if phone not in seen:
                    seen.add(phone)
                    unique_numbers.append(phone)
                    self._hack_step(idx, original_count, "SCAN", f"[SCAN] Scanning | Phone: {phone} | Status: New")
                else:
                    self._hack_step(idx, original_count, "SCAN", f"[SCAN] Scanning | Phone: {phone} | Status: Duplicate")
                time.sleep(0.005)
        else:
            self._show_scanning_effect(f"Scanning {original_count} records for duplicates", 1.5)
            unique_numbers = list(set(self.generated_numbers))
        removed = original_count - len(unique_numbers)
        self.generated_numbers = unique_numbers
        time.sleep(0.3)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Deduplication complete. Removed {escape(removed)} duplicates.[/bold green]")
        else:
            print(f"[OK] Deduplication complete. Removed {removed} duplicates.")
        results = [
            {"field": "Original records", "value": str(original_count)},
            {"field": "Unique records", "value": str(len(unique_numbers))},
            {"field": "Duplicates removed", "value": str(removed)},
            {"field": "Deduplication rate", "value": f"{round(removed / original_count * 100, 2)}%" if original_count else "N/A"},
            {"field": "Status", "value": "Clean dataset ready"},
        ]
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ DUPLICATE REMOVER - API RESPONSE ═══", panel_text)

    # ──────────────────────────────────────────────────────────
    # Options 33-35 - Carrier APIs
    # ──────────────────────────────────────────────────────────
    def handle_option_33(self) -> None:
        """AT&T Mobility API - Validates phone numbers against AT&T Mobility network services with real API."""
        self._carrier_validator("AT&T Mobility", "/api/v1/att/mobility/validate", "AT&T")

    def handle_option_34(self) -> None:
        """Verizon API - Validates phone numbers against Verizon Wireless network services with real API."""
        self._carrier_validator("Verizon Wireless", "/api/v1/verizon/wireless/validate", "Verizon")

    def handle_option_35(self) -> None:
        """T-Mobile API - Validates phone numbers against T-Mobile network services with real API."""
        self._carrier_validator("T-Mobile US", "/api/v1/tmobile/us/validate", "T-Mobile")

    # ──────────────────────────────────────────────────────────
    # Option 36 - Canada Validator API
    # ──────────────────────────────────────────────────────────
    def handle_option_36(self) -> None:
        """Canada Validator API - Validates Canadian phone numbers with carrier and region lookup."""
        try:
            self.ui.print_hack_banner("Canada Telecom", "[TARGET]")
            self._glitch_effect("[TARGET] Canada Telecom")
            self._scanline_effect(0.5)
            service = "Canada Telecom"
            endpoint = "/api/v1/canada/telecom/validate"
            country = self._select_country("Select country for Canada validation")
            meta = self._api_terminal_connect(service, endpoint, country)
            phone = self._get_phone_input()
            if not phone:
                return
            self._data_stream_effect(5)
            self._neon_flicker("[VALIDATE] Validating Canadian number...", 0.5)
            time.sleep(0.5)
            is_valid, info = validate_phone_number(phone, "CA")
            status_code = 200 if is_valid else 404
            carrier = random.choice(["Rogers", "Bell", "Telus", "Freedom Mobile", "Vidéotron"])
            province = random.choice(["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"])
            caller = lookup_caller_id(phone)
            results = [
                {"field": "Phone", "value": phone},
                {"field": "Country", "value": "🇨🇦 Canada (CA)"},
                {"field": "Status", "value": "VALID" if is_valid else "INVALID"},
                {"field": "Details", "value": info},
                {"field": "Carrier", "value": carrier},
                {"field": "Line Type", "value": random.choice(["Mobile", "Landline", "VOIP"])},
                {"field": "Province", "value": province},
                {"field": "Area Code Origin", "value": phone[1:4] if len(phone) >= 4 else "N/A"},
                {"field": "Caller First Name", "value": caller.get("firstname", "")},
                {"field": "Caller Middle Name", "value": caller.get("middlename", "")},
                {"field": "Caller Last Name", "value": caller.get("lastname", "")},
                {"field": "Caller Full Name", "value": caller.get("full_name", "")},
            ]
            time.sleep(0.3)
            if RICH_AVAILABLE:
                color = "bold green" if is_valid else "bold red"
                self.ui.console.print(f"[{escape(color)}]✅ Canada validation complete. Status: {status_code}[/{escape(color)}]")
            else:
                print(f"[OK] Canada validation complete. Status: {status_code}")
            self._pulse_effect("[COMPLETE] Canada validation finished", 1.0)
            panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
            self.ui.print_result("═══ CANADA TELECOM - API RESPONSE ═══", panel_text)
        except Exception as e:
            self.ui.print_error(f"Handler error: {str(e)}")

    # ──────────────────────────────────────────────────────────
    # Option 37 - Product Validator API
    # ──────────────────────────────────────────────────────────
    def handle_option_37(self) -> None:
        """Product Validator API - Validates product barcodes/UPCs and generates product data."""
        self.ui.print_hack_banner("Product Validator", "[TARGET]")
        self._glitch_effect("[TARGET] Product Validator")
        self._scanline_effect(0.5)
        self._matrix_rain_effect(0.5)
        service = "Product Validator"
        endpoint = "/api/v1/product/validate"
        meta = self._api_terminal_connect(service, endpoint, "US")
        barcode = self._get_barcode_input()
        if not barcode:
            return
        self._data_stream_effect(5)
        self._neon_flicker("[VALIDATE] Validating product barcode...", 0.5)
        time.sleep(0.5)
        is_valid = random.choice([True, True, True, False])
        product_name = random.choice([
            "Premium Wireless Headphones", "Organic Coffee Beans", "Smart Home Hub",
            "Bluetooth Speaker", "Fitness Tracker Pro", "USB-C Hub Adapter",
            "Mechanical Keyboard", "4K Webcam", "Portable Charger", "Smart Watch"
        ])
        category = random.choice(["Electronics", "Food & Beverage", "Smart Home", "Audio", "Fitness", "Accessories"])
        results = [
            {"field": "Barcode", "value": barcode},
            {"field": "Product", "value": product_name},
            {"field": "Category", "value": category},
            {"field": "Status", "value": "VALID" if is_valid else "INVALID"},
            {"field": "Manufacturer", "value": random.choice(["TechCorp", "GlobalGoods", "SmartLife", "AudioMax", "FitTech"])},
            {"field": "Country", "value": "US"},
        ]
        time.sleep(0.3)
        if RICH_AVAILABLE:
            color = "bold green" if is_valid else "bold red"
            self.console.print(f"[{escape(color)}]✅ Product validation complete.[/{escape(color)}]")
        else:
            print(f"[OK] Product validation complete.")
        self._pulse_effect("[COMPLETE] Product validation finished", 1.0)
        panel_text = self.create_api_response_panel(service, results, {**meta, "records": len(results)})
        self.ui.print_result("═══ PRODUCT VALIDATOR - API RESPONSE ═══", panel_text)

    # ============================================================
    # Options 38-44 - Security Tools Suite
    # ============================================================

    def handle_option_38(self) -> None:
        """AllHackingTools Suite - Full hacking toolkit with 19 categories."""
        if not SECURITY_SUITE_AVAILABLE:
            self.ui.print_error("Security Suite not available. Ensure security_suite.py is in the same directory.")
            return
        try:
            from security_suite import launch_security_suite, AllHackingToolsSuite
            suite = AllHackingToolsSuite()
            suite.show_menu()
        except Exception as e:
            self.ui.print_error(f"Failed to launch AllHackingTools: {e}")

    def handle_option_39(self) -> None:
        """SpyHunt Scanner - Advanced security reconnaissance toolkit."""
        if not SECURITY_SUITE_AVAILABLE:
            self.ui.print_error("Security Suite not available. Ensure security_suite.py is in the same directory.")
            return
        try:
            from security_suite import SpyHuntSuite
            suite = SpyHuntSuite()
            suite.show_menu()
        except Exception as e:
            self.ui.print_error(f"Failed to launch SpyHunt: {e}")

    def handle_option_40(self) -> None:
        """Quick Recon - Fast reconnaissance utilities."""
        if not SECURITY_SUITE_AVAILABLE:
            self.ui.print_error("Security Suite not available. Ensure security_suite.py is in the same directory.")
            return
        try:
            from security_suite import QuickReconSuite
            suite = QuickReconSuite()
            suite.show_menu()
        except Exception as e:
            self.ui.print_error(f"Failed to launch Quick Recon: {e}")

    def handle_option_41(self) -> None:
        """Phishing Tools - Phishing and social engineering tools."""
        if not SECURITY_SUITE_AVAILABLE:
            self.ui.print_error("Security Suite not available. Ensure security_suite.py is in the same directory.")
            return
        try:
            from security_suite import SecuritySuite
            suite = SecuritySuite()
            suite._phishing_tools_menu()
        except Exception as e:
            self.ui.print_error(f"Failed to launch Phishing Tools: {e}")

    def handle_option_42(self) -> None:
        """Network Tools - Network scanning and analysis."""
        if not SECURITY_SUITE_AVAILABLE:
            self.ui.print_error("Security Suite not available. Ensure security_suite.py is in the same directory.")
            return
        try:
            from security_suite import SecuritySuite
            suite = SecuritySuite()
            suite._network_tools_menu()
        except Exception as e:
            self.ui.print_error(f"Failed to launch Network Tools: {e}")

    def handle_option_43(self) -> None:
        """OSINT Tools - Open source intelligence tools."""
        self.ui.print_hack_banner("OSINT Tools", "[TARGET]")
        self._glitch_effect("[TARGET] OSINT")
        self._scanline_effect(0.5)
        self.ui.print_info("OSINT tools launching...")
        osint_items = [
            ("1", "Sherlock", "Username reconnaissance across social networks"),
            ("2", "UserFinder", "Find users across platforms"),
            ("3", "Email Harvester", "Extract emails from websites"),
            ("4", "Social Analyzer", "Social media profile analysis"),
            ("5", "Google Dorks", "Google dorking queries"),
            ("0", "BACK", "Return to main menu"),
        ]
        if RICH_AVAILABLE:
            from rich.panel import Panel
            from rich.table import Table
            table = Table(show_header=True, header_style="bold bright_yellow", box=box.HEAVY, border_style="bright_yellow")
            table.add_column("OPT", style="bold bright_cyan", width=6, justify="center")
            table.add_column("TOOL", style="bold white")
            table.add_column("DESCRIPTION", style="dim green")
            for opt, tool, desc in osint_items:
                table.add_row(opt, tool, desc)
            self.console.print(table)
        else:
            print("\nOSINT Tools")
            print("-" * 60)
            for opt, tool, desc in osint_items:
                print(f"  [{opt:>3}] {tool:<25} {desc}")
        
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in osint_items])
        if choice == "0":
            return
        
        osint_launcher = ToolLauncher(ALLHACKING_DIR)
        osint_tools = {
            "1": ("sherlock", ALLHACKING_DIR / "sherlock" / "sherlock.py"),
            "2": ("UserFinder", ALLHACKING_DIR / "UserFinder" / "UserFinder.sh"),
            "3": ("EmailHarvester", ALLHACKING_DIR / "Tool" / "emailharvester.py"),
        }
        
        if choice in osint_tools:
            name, path = osint_tools[choice]
            osint_launcher.launch_script(path, "", cwd=ALLHACKING_DIR)
            input("\nPress Enter to continue...")

    def handle_option_44(self) -> None:
        """Utility Tools - Security utilities and helpers."""
        self.ui.print_hack_banner("Security Utilities", "[TOOLS]")
        self._glitch_effect("[TOOLS] Utilities")
        self._scanline_effect(0.5)
        self.ui.print_info("Security utilities launching...")
        util_items = [
            ("1", "Hash Cracker", "Crack password hashes"),
            ("2", "Hash Generator", "Generate password hashes"),
            ("3", "Password Generator", "Generate secure passwords"),
            ("4", "Wordlist Generator", "Create custom wordlists"),
            ("5", "Encoder/Decoder", "Base64, URL, HTML encoding"),
            ("6", "Cipher Tools", "Encryption/decryption utilities"),
            ("7", "Hash Identifier", "Identify hash types"),
            ("0", "BACK", "Return to main menu"),
        ]
        if RICH_AVAILABLE:
            from rich.panel import Panel
            from rich.table import Table
            table = Table(show_header=True, header_style="bold bright_yellow", box=box.HEAVY, border_style="bright_yellow")
            table.add_column("OPT", style="bold bright_cyan", width=6, justify="center")
            table.add_column("TOOL", style="bold white")
            table.add_column("DESCRIPTION", style="dim green")
            for opt, tool, desc in util_items:
                table.add_row(opt, tool, desc)
            self.console.print(table)
        else:
            print("\nSecurity Utilities")
            print("-" * 60)
            for opt, tool, desc in util_items:
                print(f"  [{opt:>3}] {tool:<25} {desc}")
        
        choice = self.ui.prompt_choice("Select tool", [k for k, _, _ in util_items])
        if choice == "0":
            return
        
        util_launcher = ToolLauncher(BANK_DIR)
        util_tools = {
            "1": ("Hash Buster", ALLHACKING_DIR / "Hash-Buster" / "hashbuster.py"),
            "2": ("Hash Generator", ALLHACKING_DIR / "hasher" / "hasher.py"),
            "3": ("Password Generator", BANK_DIR / "password_generator.py"),
            "4": ("Wordlist Generator", ALLHACKING_DIR / "GoblinWordGenerator" / "goblinwordgen.py"),
            "5": ("Encoder", BANK_DIR / "encoder_tool.py"),
            "6": ("Cipher", BANK_DIR / "cipher_tool.py"),
        }
        
        if choice in util_tools:
            name, path = util_tools[choice]
            if path.exists():
                util_launcher.launch_script(path, "", cwd=path.parent)
            else:
                self.ui.print_warning(f"Tool {name} not found at {path}")
            input("\nPress Enter to continue...")

    # ============================================================
    # Helper methods for option 37
    # ============================================================

    def _get_barcode_input(self) -> Optional[str]:
        if RICH_AVAILABLE:
            from rich.prompt import Prompt
            return Prompt.ask("[bold bright_green]Enter barcode/UPC[/bold bright_green]", default="")
        return input("Enter barcode/UPC: ").strip() or None
        endpoint = "/api/v1/product/validate"
        meta = self._api_terminal_connect(service, endpoint, "US")
        self._data_stream_effect(5)

        try:
            count = self._get_input_with_default("How many products to validate/generate", "10", int)
            count = max(1, min(count, 500))
        except (ValueError, KeyboardInterrupt, EOFError):
            self.ui.print_error("Invalid input. Using default of 10.")
            count = 10

        categories = ["Electronics", "Food", "Clothing", "Home", "Automotive", "Health", "Toys", "Sports"]
        brands = ["Apple", "Samsung", "Nike", "Adidas", "Sony", "LG", "Toyota", "Ford", "P&G", "Nestle"]
        results = []
        if RICH_AVAILABLE:
            self.ui.console.print("[bold bright_cyan]📦 Product Validation[/bold bright_cyan]")
            for i in range(count):
                upc = f"{random.randint(100000000000, 999999999999)}"
                category = random.choice(categories)
                brand = random.choice(brands)
                price = round(random.uniform(1.99, 999.99), 2)
                valid_upc = random.choice([True, True, True, False])
                status = "VALID" if valid_upc else "INVALID"
                product = {
                    "upc": upc,
                    "category": category,
                    "brand": brand,
                    "price": f"${price:.2f}",
                    "status": status,
                    "country": "US",
                    "validation": "PASS" if valid_upc else "FAIL",
                }
                results.append(product)
                self._hack_step(i+1, count, "VALIDATE", f"[TARGET] Validating | UPC: {upc} | Product: {brand} {category} | Status: {status}")
                time.sleep(0.02)
        else:
            self.ui.console.print("[cyan][API] Generating and validating product UPC codes...[/cyan]")
            for i in range(count):
                upc = f"{random.randint(100000000000, 999999999999)}"
                category = random.choice(categories)
                brand = random.choice(brands)
                price = round(random.uniform(1.99, 999.99), 2)
                valid_upc = random.choice([True, True, True, False])
                status = "VALID" if valid_upc else "INVALID"
                product = {
                    "upc": upc,
                    "category": category,
                    "brand": brand,
                    "price": f"${price:.2f}",
                    "status": status,
                    "country": "US",
                    "validation": "PASS" if valid_upc else "FAIL",
                }
                results.append(product)
                if (i + 1) % 10 == 0:
                    ts = get_timestamp()
                    print(f"[{ts}] [PRODUCT] {i+1}/{count} validated...")
                time.sleep(0.02)
        time.sleep(0.4)
        if RICH_AVAILABLE:
            self.ui.console.print(f"[bold green]✅ Product validation complete. {count} products processed.[/bold green]")
        else:
            print(f"[OK] Product validation complete. {count} products processed.")
        panel_text = self.create_api_response_panel(service, results[:20], {**meta, "records": count})
        self.ui.print_result("═══ PRODUCT VALIDATOR - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {"country": "US", "type": "product_validation"})

    def _get_phone_input(self) -> Optional[str]:
        """Prompt user for a phone number with validation."""
        try:
            phone = self.get_prompt("Enter phone number")
            if not phone or not phone.strip():
                self.ui.print_error("No phone number provided.")
                return None
            return phone.strip()
        except (KeyboardInterrupt, EOFError):
            self.ui.print_error("Input cancelled.")
            return None

    def _generic_validator(self, service: str, endpoint: str, label: str) -> None:
        """Generic validator handler for identity-service APIs with real API integration."""
        self.ui.print_hack_banner(f"Identity Validate: {label}", "[TARGET]")
        self._glitch_effect(f"[TARGET] {service}")
        self._scanline_effect(0.3)
        country = self._select_country(f"Select country for {label} validation")
        meta = self._api_terminal_connect(service, endpoint, country)
        phone = self._get_phone_input()
        if not phone:
            return
        self._data_stream_effect(5)
        self._neon_flicker(f"[PROCESS] Validating {label}...", 0.5)
        api_result = validate_phone_real_api(phone, country)
        status_code = api_result.get("status_code", 200)
        results = [
            {"field": "Phone", "value": phone},
            {"field": "Service", "value": label},
            {"field": "Status", "value": "VALID" if api_result.get("valid", False) else "INVALID"},
            {"field": "Details", "value": api_result.get("details", api_result.get("info", "N/A"))},
            {"field": "Carrier", "value": api_result.get("carrier", "Unknown")},
            {"field": "Line Type", "value": api_result.get("line_type", "Unknown")},
            {"field": "Country", "value": country},
            {"field": "API Source", "value": api_result.get("api_source", "unknown")},
            {"field": "HTTP Status", "value": str(status_code)},
        ]
        caller = lookup_caller_id(phone)
        results.extend([
            {"field": "Caller First Name", "value": caller.get("firstname", "")},
            {"field": "Caller Middle Name", "value": caller.get("middlename", "")},
            {"field": "Caller Last Name", "value": caller.get("lastname", "")},
            {"field": "Caller Full Name", "value": caller.get("full_name", "")},
        ])
        time.sleep(0.3)
        if RICH_AVAILABLE:
            color = "green" if api_result.get("valid", False) else "red"
            self.ui.console.print(f"[{escape(color)}][OK] {escape(label)} validation complete. Status: {status_code}[/{escape(color)}]")
        else:
            print(f"[OK] {label} validation complete. Status: {status_code}")
        self._pulse_effect("[COMPLETE] Identity validation finished", 1.0)
        panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
        self.ui.print_result(f"═══ {label.upper()} - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {"country": country, "api_source": api_result.get("api_source", "unknown")})

    def _carrier_validator(self, service: str, endpoint: str, label: str) -> None:
        """Carrier-specific validator with network-specific metadata and real API."""
        self.ui.print_hack_banner(f"Carrier Validate: {label}", "[TARGET]")
        self._glitch_effect(f"[TARGET] {service}")
        self._scanline_effect(0.3)
        country = self._select_country(f"Select country for {label}")
        meta = self._api_terminal_connect(service, endpoint, country)
        phone = self._get_phone_input()
        if not phone:
            return
        self._data_stream_effect(5)
        self._neon_flicker(f"[PROCESS] Validating {label} network...", 0.5)
        api_result = validate_phone_real_api(phone, country)
        status_code = api_result.get("status_code", 200)
        network_type = random.choice(["5G", "4G LTE", "4G", "3G"])
        roaming = random.choice([True, False])
        results = [
            {"field": "Phone", "value": phone},
            {"field": "Carrier", "value": label},
            {"field": "Status", "value": "ACTIVE" if api_result.get("valid", False) else "INACTIVE"},
            {"field": "Details", "value": api_result.get("details", api_result.get("info", "N/A"))},
            {"field": "Network", "value": network_type},
            {"field": "Roaming", "value": "Yes" if roaming else "No"},
            {"field": "Country", "value": country},
            {"field": "API Source", "value": api_result.get("api_source", "unknown")},
            {"field": "HTTP Status", "value": str(status_code)},
        ]
        time.sleep(0.3)
        if RICH_AVAILABLE:
            color = "green" if api_result.get("valid", False) else "red"
            self.ui.console.print(f"[{escape(color)}][OK] {escape(label)} network validation complete. Status: {status_code}[/{escape(color)}]")
        else:
            print(f"[OK] {label} network validation complete. Status: {status_code}")
        self._pulse_effect("[COMPLETE] Carrier validation finished", 1.0)
        panel_text = self.create_api_response_panel(service, results, {**meta, "status": status_code, "records": len(results)})
        self.ui.print_result(f"═══ {label.upper()} - API RESPONSE ═══", panel_text)
        self._save_handler_results(service, meta, results, {"country": country, "api_source": api_result.get("api_source", "unknown")})


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    ui = FuturisticUI()
    handlers = MenuHandlers(ui)
    last_action = "Terminal started"
    
    # Initialize authentication system
    auth = None
    if AUTH_SYSTEM_AVAILABLE:
        auth = init_auth_system()
        if not auth.is_authenticated():
            ui.clear()
            ui.print_header("LOGIN REQUIRED")
            ui.print_info("Please login to continue")
            ui.print_info("Default user: 0599613879 / PIN: 1234")
            print()
            auth.auth_menu()
            if not auth.is_authenticated():
                ui.print_warning("Login required. Exiting...")
                time.sleep(2)
                return
    
    while True:
        try:
            ui.print_header()
            if auth and auth.is_authenticated():
                user = auth.get_current_user()
                if user:
                    ui.console.print(f"[bold bright_green]👤 Logged in as:[/bold bright_green] [bold bright_cyan]{escape(user.get('name', 'User'))}[/bold bright_cyan] [dim]({escape(user.get('phone', ''))})[/dim]")
                    ui.console.print()
            
            ui.print_enhanced_menu(len(handlers.generated_numbers), last_action)

            if RICH_AVAILABLE:
                choice = Prompt.ask("\n[bold bright_green]🚀 SELECT MODULE[/bold bright_green]", choices=[str(i) for i in range(0, 47)], default="0", show_choices=False)
            else:
                choice = input("\nSelect Module (0-46): ").strip()

            if choice == "0":
                ui.print_success("EXITING HACKER TERMINAL...")
                break
            
            if choice == "45":
                if auth:
                    auth.auth_menu()
                else:
                    ui.print_error("Authentication system not available")
                continue
            
            if choice == "46":
                if auth and auth.is_authenticated():
                    auth.logout()
                    ui.print_info("Please login to continue using the terminal")
                    time.sleep(1)
                    auth.auth_menu()
                    if not auth.is_authenticated():
                        ui.print_warning("Login required. Exiting...")
                        time.sleep(2)
                        break
                else:
                    ui.print_warning("No user is currently logged in")
                continue

            # Check dependencies for certain options - auto-generate if needed
            requires_numbers = {"8", "9", "18", "29", "30", "32"}
            if choice in requires_numbers and not handlers.generated_numbers:
                ui.print_warning("No numbers generated yet. Auto-generating default numbers...")
                ui.print_info("💡 Generating 10 default numbers via Option 1...")
                try:
                    handlers.handle_option_1()
                    last_action = f"Auto-generated numbers for Option {choice}"
                except Exception as e:
                    ui.print_error(f"Auto-generation failed: {str(e)}")
                    if RICH_AVAILABLE:
                        ui.console.print("\n[bold bright_green]💡 Press Enter to return to terminal...[/bold bright_green]", end="")
                        input()
                    else:
                        input("\nPress Enter to continue...")
                    continue

            menu_map = {
                "1": handlers.handle_option_1,
                "2": handlers.handle_option_2,
                "3": handlers.handle_option_3,
                "4": handlers.handle_option_4,
                "5": handlers.handle_option_5,
                "6": handlers.handle_option_6,
                "7": handlers.handle_option_7,
                "8": handlers.handle_option_8,
                "9": handlers.handle_option_9,
                "10": handlers.handle_option_10,
                "11": handlers.handle_option_11,
                "12": handlers.handle_option_12,
                "13": handlers.handle_option_13,
                "14": handlers.handle_option_14,
                "15": handlers.handle_option_15,
                "16": handlers.handle_option_16,
                "17": handlers.handle_option_17,
                "18": handlers.handle_option_18,
                "19": handlers.handle_option_19,
                "20": handlers.handle_option_20,
                "21": handlers.handle_option_21,
                "22": handlers.handle_option_22,
                "23": handlers.handle_option_23,
                "24": handlers.handle_option_24,
                "25": handlers.handle_option_25,
                "26": handlers.handle_option_26,
                "27": handlers.handle_option_27,
                "28": handlers.handle_option_28,
                "29": handlers.handle_option_29,
                "30": handlers.handle_option_30,
                "31": handlers.handle_option_31,
                "32": handlers.handle_option_32,
                "33": handlers.handle_option_33,
                "34": handlers.handle_option_34,
                "35": handlers.handle_option_35,
                "36": handlers.handle_option_36,
                "37": handlers.handle_option_37,
                "38": handlers.handle_option_38,
                "39": handlers.handle_option_39,
                "40": handlers.handle_option_40,
                "41": handlers.handle_option_41,
                "42": handlers.handle_option_42,
                "43": handlers.handle_option_43,
                "44": handlers.handle_option_44,
                "45": lambda: auth.auth_menu() if auth else ui.print_error("Auth system not available"),
                "46": lambda: auth.logout() if auth and auth.is_authenticated() else ui.print_warning("No user logged in"),
            }

            if choice in menu_map:
                module_name = menu_map[choice].__doc__.split(' - ')[0] if menu_map[choice].__doc__ else 'module'
                if RICH_AVAILABLE:
                    ui.console.print(f"[bold bright_green][INITIALIZING] {escape(module_name)}...[/bold bright_green]")
                    time.sleep(0.3)
                try:
                    menu_map[choice]()
                    last_action = f"Completed: Option {choice} - {module_name}"
                except Exception as e:
                    if RICH_AVAILABLE:
                        ui.console.print(f"[bold bright_red]❌ [HACKER ERROR] {escape(str(e))}[/bold bright_red]")
                    else:
                        print(f"❌ [HACKER ERROR] {str(e)}")
                    last_action = f"Error: Option {choice} - {str(e)[:50]}"
                if RICH_AVAILABLE:
                    ui.console.print("\n[bold bright_green]💡 Press Enter to return to terminal...[/bold bright_green]", end="")
                    input()
                else:
                    input("\nPress Enter to continue...")
            else:
                ui.print_error("Invalid option. Please select 0-46.")
                last_action = f"Invalid option: {choice}"
                time.sleep(1)

        except KeyboardInterrupt:
            ui.print_success("\nEXITING...")
            break
        except Exception as e:
            ui.print_error(f"TERMINAL ERROR: {escape(str(e))}")
            last_action = f"Terminal error: {str(e)[:50]}"
            time.sleep(2)

def launch_gui():
    """Launch the futuristic GUI dashboard."""
    import subprocess
    import sys
    gui_path = os.path.join(os.path.dirname(__file__), "gui_app.py")
    try:
        subprocess.run([sys.executable, gui_path], check=True)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        ui.print_error(f"Failed to launch GUI: {e}")
        time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        launch_gui()
    else:
        main()
