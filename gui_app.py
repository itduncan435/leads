from flask import Flask, render_template, request, jsonify, Response
import subprocess
import json
import os
import sys
import threading
import queue
import time
import re
from pathlib import Path
from datetime import datetime

import main as main_module

# Project paths
BASE_DIR = Path(__file__).resolve().parent
BANK_DIR = BASE_DIR
ALLHACKING_DIR = BANK_DIR / "AllHackingTools"
SPYHUNT_DIR = BANK_DIR / "spyhunt-main"
RESULTS_DIR = BANK_DIR / "results"

app = Flask(__name__,
    template_folder=str(BASE_DIR / "gui" / "templates"),
    static_folder=str(BASE_DIR / "gui" / "static"))
app.config['SECRET_KEY'] = 'hacker-terminal-gui-v3.3.3'
app.config['OUTPUT_QUEUES'] = {}
app.config['RUNNING_PROCESSES'] = {}
app.config['INPUT_QUEUES'] = {}
app.config['INPUT_EVENTS'] = {}

# Prevent stale JS/CSS from being cached between deployments
@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/static/'):
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.cache_control.must_revalidate = True
        response.cache_control.max_age = 0
    return response

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/api/tool/<int:tool_id>', methods=['OPTIONS'])
def api_tool_options(tool_id):
    return '', 204

# Ensure directories exist
RESULTS_DIR.mkdir(exist_ok=True)


def get_project_root():
    return BANK_DIR


# === Interactive Input System ===
import builtins
import threading as _threading

_original_input = builtins.input


class TerminalInput:
    """Replacement for builtins.input that reads from the GUI terminal."""
    def __init__(self, queue_id):
        self.queue_id = queue_id

    def __call__(self, prompt='', default=''):
        output_q = app.config['OUTPUT_QUEUES'].get(self.queue_id)
        input_q = app.config['INPUT_QUEUES'].get(self.queue_id)
        event = app.config['INPUT_EVENTS'].get(self.queue_id)
        if not input_q or not event:
            return default or ''

        # Send prompt to frontend via output queue
        if output_q:
            output_q.put(f"[PROMPT]{prompt}|default={default}")

        # Wait for user input
        event.clear()
        result = [default or '']
        while not event.wait(timeout=300):
            if output_q:
                output_q.put("[PROMPT]Waiting for input...")

        if self.queue_id in app.config['INPUT_QUEUES']:
            try:
                result[0] = input_q.get_nowait()
            except Exception:
                pass

        return result[0]


def send_terminal_input(queue_id, text):
    """Send user input to a waiting prompt."""
    q = app.config['INPUT_QUEUES'].get(queue_id)
    event = app.config['INPUT_EVENTS'].get(queue_id)
    if q and event:
        q.put(text)
        event.set()


# === Main.py Integration ===
_main_module = None
_auth_module = None
_security_module = None
_bank_module = None

def get_main_module():
    global _main_module
    if _main_module is None:
        try:
            _main_module = main_module
        except Exception as e:
            print(f"Warning: Could not load main.py: {e}")
    return _main_module


def get_auth_module():
    global _auth_module
    if _auth_module is None:
        try:
            from auth_system import init_auth_system, get_auth_system
            _auth_module = {'init': init_auth_system, 'get': get_auth_system}
        except Exception:
            pass
    return _auth_module


def get_security_module():
    global _security_module
    if _security_module is None:
        try:
            from security_suite import SecuritySuite, ToolLauncher
            _security_module = {'suite': SecuritySuite, 'launcher': ToolLauncher}
        except Exception:
            pass
    return _security_module


def get_bank_module():
    global _bank_module
    if _bank_module is None:
        try:
            from bank_accounts import get_bank_account_manager
            _bank_module = {'manager': get_bank_account_manager}
        except Exception:
            pass
    return _bank_module


# === AllHackingTools Integration ===
AHT_MENU_STDIN = {
    'MainMenu.py': '24\n',
    'RouterMenu.py': '6\n',
    'MailMenu.py': '6\n',
    'WebMenu.py': '6\n',
    'CamHackMenu.py': '6\n',
    'AndroidMenu.py': '6\n',
    'SQLinjectionMenu.py': '6\n',
    'SocialMenu.py': '6\n',
    'SpamMenu.py': '6\n',
    'AnalistickMenu.py': '6\n',
    'DarkSearchMenu.py': '6\n',
    'PhishingMenu.py': '6\n',
    'PassworldMenu.py': '6\n',
    'WordlistGeneratorMenu.py': '6\n',
    'XSSAttackMenu.py': '6\n',
    'discordMenu.py': '6\n',
    'telegramMenu.py': '6\n',
    'Other.py': '6\n',
    'TermuxS.py': '14\n',
    'TermuxS1.py': '6\n',
    'TermuxS2.py': '6\n',
    'TermuxS3.py': '6\n',
    'HelpTermuxMenu.py': '6\n',
    'TracingMenu.py': '6\n',
    'IpMenu.py': '6\n',
    'IpHack.py': '6\n',
}

AHT_DIRECT_TOOLS = {
    'IpHack.py': 'python3 IpHack.py',
    'DarkDump.py': 'python3 DarkDump.py',
    'Other.py': 'python3 Other.py',
    'TermuxS.py': 'python3 TermuxS.py',
    'TermuxS1.py': 'python3 TermuxS1.py',
    'TermuxS2.py': 'python3 TermuxS2.py',
    'TermuxS3.py': 'python3 TermuxS3.py',
    'HelpTermuxMenu.py': 'python3 HelpTermuxMenu.py',
    'TracingMenu.py': 'python3 TracingMenu.py',
    'IpMenu.py': 'python3 IpMenu.py',
}


def get_aht_script_input(script_name):
    """Get default stdin input for AllHackingTools menu scripts."""
    basename = os.path.basename(script_name)
    return AHT_MENU_STDIN.get(basename, '6\n')


def run_aht_tool(action):
    """Run AllHackingTools tool with appropriate stdin handling."""
    script_name = os.path.basename(action) if '/' in action else action
    stdin_data = get_aht_script_input(script_name)
    command = f'python3 {script_name}' if not script_name.endswith('.py') else f'python3 {script_name}'
    return command, stdin_data
class QueueFile:
    """File-like object that writes to a queue."""
    def __init__(self, q):
        self.q = q
        self._buffer = ""

    def write(self, data):
        self._buffer += data
        if '\n' in self._buffer:
            lines = self._buffer.split('\n')
            for line in lines[:-1]:
                if line:
                    self.q.put(line + '\n')
            self._buffer = lines[-1]

    def flush(self):
        if self._buffer:
            self.q.put(self._buffer)
            self._buffer = ""


class QueueUI(main_module.FuturisticUI):
    """FuturisticUI subclass that captures console output and avoids stdin."""
    def __init__(self, q):
        self.q = q
        self._queue_file = QueueFile(q)
        try:
            from rich.console import Console
            self.console = Console(file=self._queue_file, width=120)
        except Exception:
            self.console = None
        self.theme = main_module.FuturisticUI().theme
        self.results_dir = main_module.FuturisticUI().results_dir
        self._ascii_header = main_module.FuturisticUI()._ascii_header

    def _flush(self):
        self._queue_file.flush()

    def get_prompt(self, message: str, default: str = "") -> str:
        if self.queue_id and self.queue_id in app.config['INPUT_QUEUES']:
            terminal_input = TerminalInput(self.queue_id)
            return terminal_input(message, default)
        return default

    def _get_phone_input(self):
        return main_module.generate_phone_number("1")

    def console_print(self, *args, **kwargs):
        if self.console:
            self.console.print(*args, **kwargs)
            self._flush()

    def print_success(self, message):
        self.q.put(f"[OK] {message}\n")

    def print_error(self, message):
        self.q.put(f"[ERROR] {message}\n")

    def print_info(self, message):
        self.q.put(f"[INFO] {message}\n")

    def print_warning(self, message):
        self.q.put(f"[WARN] {message}\n")

    def print_header(self, title="AUTHENTICATION"):
        self.q.put(f"\n{'='*60}\n  {title}\n{'='*60}\n")

    def clear(self):
        self.q.put("\033c")


class GuiHandlers(main_module.MenuHandlers):
    """MenuHandlers subclass that uses interactive terminal input."""
    def __init__(self, q, main_mod, queue_id=None, branch_mode='random', auto_mode=False):
        self.q = q
        self.main_mod = main_mod
        self.queue_id = queue_id
        self.ui = QueueUI(q)
        super().__init__(self.ui)
        self.user_count = 10
        self.user_area_code = ""
        self.user_branch_mode = "ALL" if branch_mode == 'all' else "MIX" if branch_mode == 'mix' else "RANDOM"
        self.user_selected_state = None
        self.user_selected_city = None
        self.user_country = "US"
        self.user_institution = None
        self.selected_bank = None
        self.auto_mode = auto_mode

    def get_prompt(self, message: str, default: str = "") -> str:
        if self.auto_mode:
            return default or ''
        if self.queue_id and self.queue_id in app.config['INPUT_QUEUES']:
            terminal_input = TerminalInput(self.queue_id)
            return terminal_input(message, default)
        return default

    def _get_input_with_default(self, prompt: str, default: str, input_type: type = str):
        if self.auto_mode and input_type == int:
            return self.user_count
        return super()._get_input_with_default(prompt, default, input_type)

    def _get_phone_input(self):
        return self.main_mod.generate_phone_number("1")


def run_main_tool_direct(tool_id, count=10, queue_id=None, bank_name=None, state=None, city=None, branch_mode='random', auto_mode=False):
    """Run main.py tool directly in-process and stream output."""
    q = queue.Queue()
    if queue_id:
        app.config['OUTPUT_QUEUES'][queue_id] = q
        app.config['INPUT_QUEUES'][queue_id] = queue.Queue()
        app.config['INPUT_EVENTS'][queue_id] = _threading.Event()

    def worker():
        original_input = builtins.input
        try:
            if queue_id:
                builtins.input = TerminalInput(queue_id)

            main_mod = get_main_module()
            if not main_mod:
                q.put("[ERROR] main.py module not available\n")
                q.put(None)
                return

            handlers = GuiHandlers(q, main_mod, queue_id=queue_id, branch_mode=branch_mode, auto_mode=auto_mode)
            handlers.user_count = count
            
            if bank_name:
                handlers.selected_bank = bank_name
            if state:
                handlers.user_selected_state = state
            if city:
                handlers.user_selected_city = city

            handler_map = {
                1: handlers.handle_option_1,
                2: handlers.handle_option_2,
                3: handlers.handle_option_3,
                4: handlers.handle_option_4,
                5: handlers.handle_option_5,
                6: handlers.handle_option_6,
                7: handlers.handle_option_7,
                8: handlers.handle_option_8,
                9: handlers.handle_option_9,
                10: handlers.handle_option_10,
                11: handlers.handle_option_11,
                12: handlers.handle_option_12,
                13: handlers.handle_option_13,
                14: handlers.handle_option_14,
                15: handlers.handle_option_15,
                16: handlers.handle_option_16,
                17: handlers.handle_option_17,
                18: handlers.handle_option_18,
                19: handlers.handle_option_19,
                20: handlers.handle_option_20,
                21: handlers.handle_option_21,
                22: handlers.handle_option_22,
                23: handlers.handle_option_23,
                24: handlers.handle_option_24,
                25: handlers.handle_option_25,
                26: handlers.handle_option_26,
                27: handlers.handle_option_27,
                28: handlers.handle_option_28,
                29: handlers.handle_option_29,
                30: handlers.handle_option_30,
                31: handlers.handle_option_31,
                32: handlers.handle_option_32,
                33: handlers.handle_option_33,
                34: handlers.handle_option_34,
                35: handlers.handle_option_35,
                36: handlers.handle_option_36,
                37: handlers.handle_option_37,
            }

            if tool_id == 45:
                auth_mod = get_auth_module()
                if auth_mod:
                    auth = auth_mod['init']()
                    try:
                        auth.quick_login()
                    except Exception as e:
                        q.put(f"[AUTH] Quick login failed: {e}\n")
                else:
                    q.put("[ERROR] Auth system not available\n")
            elif tool_id in handler_map:
                try:
                    handler_map[tool_id]()
                except Exception as e:
                    q.put(f"[ERROR] Tool execution failed: {e}\n")
            else:
                q.put(f"[ERROR] Tool {tool_id} not yet mapped for direct execution\n")

            q.put(f"\n[PROCESS EXITED WITH CODE 0]\n")
        except Exception as e:
            q.put(f"[ERROR] {str(e)}\n")
        finally:
            builtins.input = original_input
            if queue_id:
                q.put(None)

    thread = _threading.Thread(target=worker, daemon=True)
    thread.start()
    return q


# === Command Execution ===
def run_command_async(command, cwd=None, queue_id=None, stdin_data=None):
    """Run command asynchronously and stream output to queue."""
    q = queue.Queue()
    if queue_id:
        app.config['OUTPUT_QUEUES'][queue_id] = q

    def worker():
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=str(cwd or BANK_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            if queue_id:
                app.config['RUNNING_PROCESSES'][queue_id] = process

            if stdin_data:
                try:
                    process.stdin.write(stdin_data)
                    process.stdin.flush()
                except Exception:
                    pass
                finally:
                    try:
                        process.stdin.close()
                    except Exception:
                        pass

            for line in process.stdout:
                q.put(line)
            process.wait()
            q.put(f"\n[PROCESS EXITED WITH CODE {process.returncode}]")
        except Exception as e:
            q.put(f"[ERROR] {str(e)}\n")
        finally:
            q.put(None)  # Signal end

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    return q


def stop_process(queue_id):
    """Stop a running process."""
    if queue_id in app.config['RUNNING_PROCESSES']:
        process = app.config['RUNNING_PROCESSES'][queue_id]
        try:
            process.terminate()
            process.wait(timeout=5)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
        del app.config['RUNNING_PROCESSES'][queue_id]
        return True
    return False


# === Routes ===
@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/run', methods=['POST'])
def api_run():
    data = request.json or {}
    command = data.get('command', '')
    cwd = data.get('cwd', str(BANK_DIR))
    queue_id = data.get('queue_id', f'q_{int(time.time() * 1000)}')
    stdin_data = data.get('stdin_data', None)

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    # Security: basic command validation
    dangerous = ['rm -rf /', 'mkfs', 'dd if=', ':(){:|:&};:']
    if any(d in command for d in dangerous):
        return jsonify({'error': 'Dangerous command blocked'}), 403

    q = run_command_async(command, cwd=cwd, queue_id=queue_id, stdin_data=stdin_data)
    return jsonify({'queue_id': queue_id, 'status': 'started'})


@app.route('/api/stream/<queue_id>')
def api_stream(queue_id):
    def generate():
        q = app.config['OUTPUT_QUEUES'].get(queue_id)
        if not q:
            yield f"data: [ERROR] Queue not found\n\n"
            return

        last_activity = time.time()
        while True:
            try:
                line = q.get(timeout=1)
                if line is None:
                    break
                last_activity = time.time()
                yield f"data: {line}\n\n"
            except queue.Empty:
                now = time.time()
                if now - last_activity > 120:
                    yield f"data: [TIMEOUT] No output for 120s\n\n"
                    break

    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/stop', methods=['POST'])
def api_stop():
    data = request.json or {}
    queue_id = data.get('queue_id', '')
    if stop_process(queue_id):
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Process not found'}), 404


@app.route('/api/input', methods=['POST'])
def api_input():
    """Send stdin data to a running process or interactive prompt."""
    data = request.json or {}
    queue_id = data.get('queue_id', '')
    input_data = data.get('data', '')

    if not queue_id:
        return jsonify({'error': 'No queue_id provided'}), 400

    # Try interactive prompt first
    if queue_id in app.config['INPUT_QUEUES']:
        send_terminal_input(queue_id, input_data)
        return jsonify({'status': 'sent to prompt'})

    # Fall back to subprocess stdin
    process = app.config['RUNNING_PROCESSES'].get(queue_id)
    if not process:
        return jsonify({'error': 'Process not found'}), 404

    if process.stdin and process.stdin.writable():
        try:
            process.stdin.write(input_data + '\n')
            process.stdin.flush()
            return jsonify({'status': 'sent'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Process stdin not available'}), 400


@app.route('/api/results/download/<path:filename>')
def api_results_download(filename):
    """Download a result file."""
    try:
        filepath = RESULTS_DIR / filename
        if not filepath.exists() or not filepath.is_file():
            return jsonify({'error': 'File not found'}), 404
        
        from flask import send_file
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/modules')
def api_modules():
    """Return all available modules and tools."""
    modules = {
        'generation': [
            {'id': 1, 'name': 'American First Credit Union', 'desc': 'USA banking with routing + caller ID', 'icon': '🏦'},
            {'id': 2, 'name': 'Phone Number Grabber', 'desc': 'Bulk generation with progress', 'icon': '📞'},
            {'id': 3, 'name': 'USA Banks Database', 'desc': 'Federal Reserve bank lookup', 'icon': '🏛️'},
            {'id': 4, 'name': 'Canada Banks Database', 'desc': 'Bank of Canada institutions', 'icon': '🍁'},
            {'id': 5, 'name': 'Crypto Wallet Scanner', 'desc': 'Blockchain wallet analysis', 'icon': '₿'},
            {'id': 6, 'name': 'Amazon SES OTP', 'desc': 'Real AWS SES email sending', 'icon': '📧'},
        ],
        'validation': [
            {'id': 7, 'name': 'eBay Seller Scan', 'desc': 'eBay Trading API seller data', 'icon': '🛒'},
            {'id': 8, 'name': 'HLR Lookup', 'desc': 'Real-time HLR validation', 'icon': '📲'},
            {'id': 9, 'name': 'Line Type Classifier', 'desc': 'Mobile/Landline/VOIP detection', 'icon': '🔍'},
            {'id': 10, 'name': 'Amazon Validator', 'desc': 'Amazon identity verification', 'icon': '✅'},
            {'id': 11, 'name': 'Office365 Validator', 'desc': 'Microsoft Graph validation', 'icon': '📊'},
            {'id': 12, 'name': 'Gmail Validator', 'desc': 'Google People API', 'icon': '📧'},
            {'id': 13, 'name': 'Facebook Validator', 'desc': 'Meta Graph validation', 'icon': '👤'},
            {'id': 14, 'name': 'Twitter/X Validator', 'desc': 'Twitter API v2 lookup', 'icon': '🐦'},
            {'id': 15, 'name': 'Instagram/Threads', 'desc': 'Meta Instagram validate', 'icon': '📸'},
            {'id': 16, 'name': 'Yahoo Validator', 'desc': 'Yahoo identity check', 'icon': '📨'},
            {'id': 17, 'name': 'AOL Validator', 'desc': 'AOL identity check', 'icon': '📨'},
        ],
        'telecom': [
            {'id': 18, 'name': 'SMS Reception Check', 'desc': 'Check SMS delivery capability', 'icon': '💬'},
            {'id': 19, 'name': 'Email SMS Gateway', 'desc': 'Email-to-SMS gateway lookup', 'icon': '📩'},
            {'id': 20, 'name': 'Xfinity Validator', 'desc': 'Xfinity/Comcast identity', 'icon': '📡'},
            {'id': 21, 'name': 'LinkedIn Validator', 'desc': 'LinkedIn identity check', 'icon': '💼'},
            {'id': 22, 'name': 'Zoho Validator', 'desc': 'Zoho CRM validation', 'icon': '📋'},
            {'id': 23, 'name': 'QuickBooks Validator', 'desc': 'QuickBooks identity', 'icon': '📑'},
            {'id': 24, 'name': 'SMS Encrypt/Decrypt', 'desc': 'Caesar cipher encryption', 'icon': '🔐'},
            {'id': 25, 'name': 'Hotmail/Outlook', 'desc': 'Microsoft Outlook validate', 'icon': '📧'},
            {'id': 26, 'name': 'Australia Validator', 'desc': 'AU telecom + region', 'icon': '🇦🇺'},
            {'id': 27, 'name': 'UK Validator', 'desc': 'UK telecom + region', 'icon': '🇬🇧'},
            {'id': 28, 'name': 'Ireland Validator', 'desc': 'IE telecom + region', 'icon': '🇮🇪'},
            {'id': 29, 'name': 'USA State Filter', 'desc': 'Filter by US state', 'icon': '🗺️'},
            {'id': 30, 'name': 'USA City Filter', 'desc': 'Filter by US city', 'icon': '🏙️'},
        ],
        'security': [
            {'id': 31, 'name': 'PayPal Validator', 'desc': 'PayPal identity verification', 'icon': '💰'},
            {'id': 32, 'name': 'Duplicate Remover', 'desc': 'Remove duplicate numbers', 'icon': '🔄'},
            {'id': 33, 'name': 'AT&T Mobility', 'desc': 'AT&T network validation', 'icon': '📶'},
            {'id': 34, 'name': 'Verizon Wireless', 'desc': 'Verizon network check', 'icon': '📶'},
            {'id': 35, 'name': 'T-Mobile US', 'desc': 'T-Mobile network check', 'icon': '📶'},
            {'id': 36, 'name': 'Canada Validator', 'desc': 'CA telecom + province', 'icon': '🍁'},
            {'id': 37, 'name': 'Product Validator', 'desc': 'UPC/Barcode validator', 'icon': '📦'},
            {'id': 38, 'name': 'AllHackingTools', 'desc': '19 hacking tool categories', 'icon': '💥'},
            {'id': 39, 'name': 'SpyHunt Scanner', 'desc': 'Advanced security recon', 'icon': '🛡️'},
            {'id': 40, 'name': 'Quick Recon', 'desc': 'Fast reconnaissance tools', 'icon': '🔎'},
            {'id': 41, 'name': 'Phishing Tools', 'desc': 'Phishing & social engineering', 'icon': '🎣'},
            {'id': 42, 'name': 'Network Tools', 'desc': 'Network scanning & analysis', 'icon': '🌐'},
            {'id': 43, 'name': 'OSINT Tools', 'desc': 'Open source intelligence', 'icon': '📊'},
            {'id': 44, 'name': 'Utility Tools', 'desc': 'Security utilities & helpers', 'icon': '🔧'},
            {'id': 45, 'name': 'Auth Menu', 'desc': 'Login / Register / Profile', 'icon': '🔐'},
        ]
    }
    return jsonify(modules)


@app.route('/api/tool/<int:tool_id>', methods=['POST'])
def api_run_tool(tool_id):
    """Run a specific tool by ID."""
    try:
        raw_data = request.get_data(as_text=True)
        content_type = request.content_type or ''
        print(f"[DEBUG] /api/tool/{tool_id} method={request.method} ct={content_type} body={raw_data[:200]}", flush=True)
        
        data = {}
        try:
            data = request.get_json(silent=True) or {}
        except Exception as json_err:
            print(f"[DEBUG] JSON parse error: {json_err}", flush=True)
            return jsonify({'error': f'Invalid JSON: {str(json_err)}', 'body': raw_data[:200]}), 400
        
        params = data.get('params', {})
        count = int(params.get('count', 10))

        queue_id = f'tool_{tool_id}_{int(time.time() * 1000)}'
        print(f"[DEBUG] Starting tool {tool_id} count={count} qid={queue_id}", flush=True)

        # Run main.py tools directly in-process to avoid stdin EOF errors
        direct_tools = list(range(1, 38)) + [45]
        if tool_id in direct_tools:
            bank_name = data.get('bank_name')
            state = data.get('state')
            city = data.get('city')
            branch_mode = data.get('branch_mode', 'random')
            auto_mode = data.get('auto_mode', False)
            q = run_main_tool_direct(tool_id, count=count, queue_id=queue_id, bank_name=bank_name, state=state, city=city, branch_mode=branch_mode, auto_mode=auto_mode)
            print(f"[DEBUG] Direct tool started: {tool_id} mode=direct", flush=True)
            return jsonify({'queue_id': queue_id, 'status': 'started', 'tool': tool_id, 'mode': 'direct'})

        # External tools via subprocess
        tool_commands = {
            38: 'python3 MainMenu.py',
            39: 'python3 spyhunt.py --help',
            40: 'python3 Files/QuickRecon.py',
        }

        cwd_map = {
            38: str(ALLHACKING_DIR),
            39: str(SPYHUNT_DIR),
            40: str(BANK_DIR),
        }

        command = tool_commands.get(tool_id, f'python3 Files/Other.py')
        cwd = cwd_map.get(tool_id, BANK_DIR)
        
        # For AllHackingTools menu scripts, provide stdin to avoid EOFError
        stdin_data = None
        if tool_id == 38 or (BANK_DIR / "AllHackingTools" / "Files" / command.split('/')[-1]).exists():
            script_name = command.split('/')[-1]
            if script_name.startswith('python3 '):
                script_name = script_name[len('python3 '):]
            stdin_data = get_aht_script_input(script_name)
        
        q = run_command_async(command, cwd=cwd, queue_id=queue_id, stdin_data=stdin_data)
        print(f"[DEBUG] Subprocess tool started: {tool_id} mode=subprocess", flush=True)
        return jsonify({'queue_id': queue_id, 'status': 'started', 'tool': tool_id, 'mode': 'subprocess'})
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[DEBUG] Tool error: {e}\n{tb}", flush=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/system/status')
def api_system_status():
    """Return system status info."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return jsonify({
            'cpu': cpu,
            'memory': {
                'total': memory.total,
                'used': memory.used,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'percent': disk.percent
            },
            'timestamp': datetime.now().isoformat()
        })
    except ImportError:
        return jsonify({
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'modules_loaded': True
        })


@app.route('/api/results')
def api_results():
    """List result CSV files only."""
    results = []
    if RESULTS_DIR.exists():
        for f in sorted(RESULTS_DIR.glob('*.csv'), key=os.path.getmtime, reverse=True)[:20]:
            results.append({
                'name': f.name,
                'size': f.stat().st_size,
                'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                'type': 'csv'
            })
    return jsonify(results)


@app.route('/api/results/view/<path:filename>')
def api_results_view(filename):
    """View a result file."""
    try:
        filepath = RESULTS_DIR / filename
        if not filepath.exists() or not filepath.is_file():
            return jsonify({'error': 'File not found'}), 404
        
        if filepath.suffix.lower() == '.csv':
            import csv
            rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                for row in reader:
                    rows.append(row)
            return jsonify({
                'type': 'csv',
                'filename': filename,
                'headers': headers,
                'rows': rows
            })
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'type': 'txt',
                'filename': filename,
                'content': content
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bank/accounts')
def api_bank_accounts():
    """Get bank accounts."""
    try:
        from bank_accounts import get_bank_account_manager
        manager = get_bank_account_manager()
        accounts = manager.list_accounts()
        return jsonify({'accounts': accounts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/status')
def api_auth_status():
    """Get authentication status."""
    try:
        from auth_system import get_current_user, is_authenticated
        user = get_current_user()
        return jsonify({
            'authenticated': is_authenticated(),
            'user': user
        })
    except Exception:
        return jsonify({'authenticated': False, 'user': None})


@app.route('/api/banks')
def api_banks():
    """List all banks with branch data."""
    try:
        from bank_branches import BANK_BRANCHES
        banks = []
        for name, branches in BANK_BRANCHES.items():
            states = sorted({b['state'] for b in branches})
            banks.append({
                'name': name,
                'branches': len(branches),
                'states': states
            })
        banks.sort(key=lambda x: x['name'])
        return jsonify(banks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/banks/<bank_name>/states')
def api_bank_states(bank_name):
    """List states for a specific bank."""
    try:
        from bank_branches import get_bank_states
        states = get_bank_states(bank_name)
        return jsonify({'bank': bank_name, 'states': sorted(states)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/banks/<bank_name>/cities')
def api_bank_cities(bank_name):
    """List cities for a specific bank in a specific state."""
    try:
        from bank_branches import get_branches_by_state
        state = request.args.get('state', '').upper()
        branches = get_branches_by_state(bank_name, state)
        cities = sorted({b['city'] for b in branches})
        return jsonify({'bank': bank_name, 'state': state, 'cities': cities})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/banks/<bank_name>/branches')
def api_bank_branches(bank_name):
    """List branches for a specific bank, optionally filtered by state and city."""
    try:
        from bank_branches import search_branches
        state = request.args.get('state', '').upper()
        city = request.args.get('city', '')
        branches = search_branches(bank_name, city=city if city else None, state=state if state else None)
        return jsonify({'bank': bank_name, 'branches': branches})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/banks/<path:bank_name>')
def api_bank_detail(bank_name):
    """Get full bank detail: states, cities, and branches."""
    try:
        from bank_branches import get_bank_states, get_branches_by_state, search_branches
        branches = search_branches(bank_name)
        states = sorted({b['state'] for b in branches})
        cities = sorted({b['city'] for b in branches})
        return jsonify({
            'bank': bank_name,
            'branches': branches,
            'states': states,
            'cities': cities
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("""
╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗
║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝
╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═
   HACKER TERMINAL v3.3.3 - GUI
    🖥️  GUI MODE ACTIVATED
    📡 Dashboard: http://localhost:5000
    """)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
