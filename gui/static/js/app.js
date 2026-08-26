/* ============================================================
   HACKER TERMINAL v3.3.3 - GUI JavaScript
   ============================================================ */

// === State ===
let currentQueueId = null;
let commandHistory = [];
let historyIndex = -1;
let isProcessRunning = false;
let waitingForPrompt = false;
let currentPrompt = '';
let modules = {};
let allTools = {};
let currentViewedFile = null;
let selectedBank = null;
let selectedState = null;
let selectedCity = null;
let bankModalToolId = null;
let selectedBranches = [];
let branchSelectionMode = 'random'; // 'all' or 'random'

// === Initialize ===
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initMatrixRain();
    initPipes();
    initTerminalVisualizer();
    initClock();
    initNavigation();
    loadModules();
    loadResults();
    loadTools();
    initTerminal();
    startSystemMonitor();
    initCommandPalette();
});

// === Particles Background ===
function initParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        particle.style.animationDelay = (Math.random() * 10) + 's';
        particle.style.opacity = Math.random() * 0.3;
        container.appendChild(particle);
    }
}

// === Matrix Rain ===
function initMatrixRain() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ';
    const fontSize = 14;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = Array(columns).fill(1);

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 50);
}

// === Hacker Pipes ===
function initPipes() {
    const canvas = document.getElementById('pipes-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const pipes = [];
    const maxPipes = 18;

    function createPipe() {
        return {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            length: Math.random() * 80 + 20,
            angle: Math.random() * Math.PI * 2,
            speed: Math.random() * 0.02 + 0.005,
            color: `rgba(0, 240, 255, ${Math.random() * 0.6 + 0.2})`,
            thickness: Math.random() * 2 + 1,
        };
    }

    for (let i = 0; i < maxPipes; i++) {
        pipes.push(createPipe());
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (const pipe of pipes) {
            ctx.beginPath();
            ctx.moveTo(pipe.x, pipe.y);
            ctx.lineTo(
                pipe.x + Math.cos(pipe.angle) * pipe.length,
                pipe.y + Math.sin(pipe.angle) * pipe.length
            );
            ctx.strokeStyle = pipe.color;
            ctx.lineWidth = pipe.thickness;
            ctx.lineCap = 'round';
            ctx.stroke();

            pipe.angle += pipe.speed;
            if (Math.random() < 0.005) {
                pipe.x = Math.random() * canvas.width;
                pipe.y = Math.random() * canvas.height;
                pipe.length = Math.random() * 80 + 20;
            }
        }
    }

    setInterval(draw, 30);
}

// === Terminal Visualizer ===
function initTerminalVisualizer() {
    const canvas = document.getElementById('terminal-visualizer');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
        const parent = canvas.parentElement;
        if (!parent) return;
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const bars = 48;
    const heights = new Array(bars).fill(0);
    const targets = new Array(bars).fill(0);

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const barWidth = canvas.width / bars;

        for (let i = 0; i < bars; i++) {
            if (Math.abs(heights[i] - targets[i]) < 0.5) {
                targets[i] = Math.random() * canvas.height * 0.7;
            }
            heights[i] += (targets[i] - heights[i]) * 0.12;

            const x = i * barWidth;
            const h = heights[i];
            const gradient = ctx.createLinearGradient(0, canvas.height, 0, canvas.height - h);
            gradient.addColorStop(0, 'rgba(0, 240, 255, 0.9)');
            gradient.addColorStop(1, 'rgba(255, 0, 255, 0.6)');
            ctx.fillStyle = gradient;
            ctx.fillRect(x + 1, canvas.height - h, barWidth - 2, h);
        }
    }

    setInterval(draw, 60);
}

// === Command Palette ===
function initCommandPalette() {
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'P') {
            e.preventDefault();
            const cmd = prompt('Enter command or tool ID:');
            if (cmd === null) return;
            const trimmed = cmd.trim();
            if (!trimmed) return;
            const toolId = parseInt(trimmed, 10);
            if (!Number.isNaN(toolId) && toolId > 0) {
                runTool(toolId);
            } else {
                addTerminalLine(`[CMD] ${trimmed}`, 'system');
            }
        }
    });
}

// === Clock ===
function initClock() {
    function updateClock() {
        const now = new Date();
        const time = now.toLocaleTimeString('en-US', { hour12: false });
        const clockEl = document.getElementById('clock');
        if (clockEl) clockEl.textContent = time;
    }
    updateClock();
    setInterval(updateClock, 1000);
}

// === Navigation ===
function initNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    const targetTab = document.getElementById(`tab-${tabId}`);
    if (targetTab) {
        targetTab.classList.add('active');
    }
    if (tabId === 'terminal') {
        const generalVideo = document.getElementById('terminal-bg-video');
        if (generalVideo) {
            generalVideo.classList.add('active');
            generalVideo.play().catch(err => console.warn('Terminal background video play failed:', err));
        }
    }
}

// === Load Modules ===
async function loadModules() {
    try {
        const response = await fetch('/api/modules');

        if (!response.ok) {
            console.error('Modules endpoint error:', response.status);
            return;
        }

        modules = await response.json();

        // Generation modules
        const genContainer = document.getElementById('gen-modules');
        if (genContainer) {
            genContainer.innerHTML = modules.generation.map(m => createModuleCard(m)).join('');
        }

        // Security modules
        const secContainer = document.getElementById('sec-modules');
        if (secContainer) {
            secContainer.innerHTML = modules.security.map(m => createModuleCard(m)).join('');
        }
    } catch (error) {
        console.error('Failed to load modules:', error);
    }
}

function createModuleCard(module) {
    return `
        <div class="module-card" onclick="runTool(${module.id})">
            <div class="module-header">
                <span class="module-icon">${module.icon}</span>
                <div>
                    <div class="module-name">${module.name}</div>
                    <div class="module-id">ID: ${module.id}</div>
                </div>
            </div>
            <div class="module-desc">${module.desc}</div>
            <div class="module-actions">
                <button class="btn btn-primary" onclick="event.stopPropagation(); runTool(${module.id})">Run</button>
                <button class="btn btn-secondary" onclick="event.stopPropagation(); showToolInfo(${module.id})">Info</button>
            </div>
        </div>
    `;
}

// === Load Tools ===
function loadTools() {
    const ahtTools = [
        { name: 'IP Hacking', action: 'IpHack.py' },
        { name: 'Router Hacking', action: 'RouterMenu.py' },
        { name: 'Mail Hacking', action: 'MailMenu.py' },
        { name: 'Web Hacking', action: 'WebMenu.py' },
        { name: 'Cam Hacking', action: 'CamHackMenu.py' },
        { name: 'Android Hacking', action: 'AndroidMenu.py' },
        { name: 'SQL Injection', action: 'SQLinjectionMenu.py' },
        { name: 'Social Engineering', action: 'SocialMenu.py' },
        { name: 'Spam Tools', action: 'SpamMenu.py' },
        { name: 'Analytics', action: 'AnalistickMenu.py' },
        { name: 'Dark Search', action: 'DarkSearchMenu.py' },
        { name: 'Phishing', action: 'PhishingMenu.py' },
        { name: 'Password Tools', action: 'PassworldMenu.py' },
        { name: 'Wordlist Generator', action: 'WordlistGeneratorMenu.py' },
        { name: 'XSS Attacks', action: 'XSSAttackMenu.py' },
        { name: 'Discord Tools', action: 'discordMenu.py' },
        { name: 'Telegram Tools', action: 'telegramMenu.py' },
        { name: 'Other Tools', action: 'Other.py' },
        { name: 'Termux Tools', action: 'TermuxS.py' },
    ];

    const spyhuntTools = [
        { name: 'Target Intelligence', action: 'analyze_target' },
        { name: 'Subdomain Enumeration', action: 'subdomain_enum' },
        { name: 'Port Scanning', action: 'port_scan' },
        { name: 'Web Vulnerability Scan', action: 'web_vuln_scan' },
        { name: 'JWT Analyzer', action: 'jwt_analyzer' },
        { name: 'S3 Security Scanner', action: 's3_scanner' },
        { name: 'SSL/TLS Analyzer', action: 'ssl_analyzer' },
        { name: 'Heap Dump Analyzer', action: 'heap_dump' },
        { name: 'Advanced Scanners', action: 'advanced_scanners' },
        { name: 'Wayback Machine', action: 'wayback' },
        { name: 'Shodan Search', action: 'shodan_search' },
        { name: 'Certificate Transparency', action: 'cert_search' },
        { name: 'Asset Finder', action: 'assetfinder' },
        { name: 'Path Hunter', action: 'pathhunt' },
        { name: 'WAF Detector', action: 'waf_detector' },
        { name: 'Smuggler', action: 'smuggler' },
        { name: 'F5 BigIP Scanner', action: 'f5_scanner' },
    ];

    const ahtContainer = document.getElementById('aht-tools');
    const spyhuntContainer = document.getElementById('spyhunt-tools');

    if (ahtContainer) {
        ahtContainer.innerHTML = ahtTools.map(t => `
            <div class="tool-item" onclick="runAHTTool('${t.action}')">
                <span class="tool-item-name">${t.name}</span>
                <span class="tool-item-action">▶ RUN</span>
            </div>
        `).join('');
    }

    if (spyhuntContainer) {
        spyhuntTools.forEach(t => {
            const item = document.createElement('div');
            item.className = 'tool-item';
            item.onclick = () => runSpyHuntTool(t.action, t.name);
            item.innerHTML = `
                <span class="tool-item-name">${t.name}</span>
                <span class="tool-item-action">▶ RUN</span>
            `;
            spyhuntContainer.appendChild(item);
        });
    }
}

// === Run Tools ===
async function runTool(toolId) {
    if (toolId === 3) {
        openBankModal(toolId);
        return;
    }
    
    const queueId = `tool_${toolId}_${Date.now()}`;
    try {
        const response = await fetch('/api/tool/' + toolId, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ params: { count: 10 }, queue_id: queueId })
        });

        if (!response.ok) {
            const text = await response.text();
            console.error('Tool response body:', text.substring(0, 200));
            throw new Error(`HTTP ${response.status}: ${text.substring(0, 100)}`);
        }

        const data = await response.json();
        if (data.queue_id) {
            currentQueueId = data.queue_id;
            isProcessRunning = true;
            switchTab('terminal');
            streamOutput(data.queue_id);
            addTerminalLine(`[INFO] Starting tool ${toolId}...`, 'info');
        }
    } catch (error) {
        addTerminalLine(`[ERROR] Failed to start tool: ${error.message}`, 'error');
    }
}

async function runAHTTool(action) {
    const commands = {
        'IpHack.py': 'python3 Files/IpHack.py',
        'RouterMenu.py': 'python3 Files/RouterMenu.py',
        'MailMenu.py': 'python3 Files/MailMenu.py',
        'WebMenu.py': 'python3 Files/WebMenu.py',
        'CamHackMenu.py': 'python3 Files/CamHackMenu.py',
        'AndroidMenu.py': 'python3 Files/AndroidMenu.py',
        'SQLinjectionMenu.py': 'python3 Files/SQLinjectionMenu.py',
        'SocialMenu.py': 'python3 Files/SocialMenu.py',
        'SpamMenu.py': 'python3 Files/SpamMenu.py',
        'AnalistickMenu.py': 'python3 Files/AnalistickMenu.py',
        'DarkSearchMenu.py': 'python3 Files/DarkSearchMenu.py',
        'PhishingMenu.py': 'python3 Files/PhishingMenu.py',
        'PassworldMenu.py': 'python3 Files/PassworldMenu.py',
        'WordlistGeneratorMenu.py': 'python3 Files/WordlistGeneratorMenu.py',
        'XSSAttackMenu.py': 'python3 Files/XSSAttackMenu.py',
        'discordMenu.py': 'python3 Files/discordMenu.py',
        'telegramMenu.py': 'python3 Files/telegramMenu.py',
        'Other.py': 'python3 Files/Other.py',
        'TermuxS.py': 'python3 Files/TermuxS.py',
    };
    const command = commands[action] || `python3 Files/${action}`;
    await executeCommand(command, { cwd: '/home/xmavel/Documents/bank/AllHackingTools' });
}

async function runSpyHuntTool(action, name) {
    const commands = {
        'analyze_target': 'python3 spyhunt.py --target-intel example.com',
        'subdomain_enum': 'python3 spyhunt.py --subdomains example.com',
        'port_scan': 'python3 spyhunt.py --ports example.com',
        'web_vuln_scan': 'python3 spyhunt.py --web-scan example.com',
        'jwt_analyzer': 'python3 spyhunt.py --jwt',
        's3_scanner': 'python3 spyhunt.py --s3-scan example.com',
        'ssl_analyzer': 'python3 spyhunt.py --ssl example.com',
        'heap_dump': 'python3 spyhunt.py --heap-dump',
        'advanced_scanners': 'python3 spyhunt.py --advanced-scan example.com',
        'wayback': 'python3 spyhunt.py --wayback example.com',
        'shodan_search': 'python3 spyhunt.py --shodan',
        'cert_search': 'python3 spyhunt.py --cert example.com',
        'assetfinder': 'python3 spyhunt.py --assetfinder example.com',
        'pathhunt': 'python3 tools/pathhunt.py -t https://example.com',
        'waf_detector': 'python3 spyhunt.py --waf example.com',
        'smuggler': 'python3 tools/smuggler/smuggler.py -u example.com',
        'f5_scanner': 'python3 tools/f5bigip_scanner.py',
    };

    const command = commands[action] || 'python3 spyhunt.py --help';
    await executeCommand(command, { cwd: '/home/xmavel/Documents/bank/spyhunt-main' });
}

async function executeCommand(command, options = {}) {
    const queueId = `cmd_${Date.now()}`;
    const cwd = options.cwd || '/home/xmavel/Documents/bank';
    const stdinData = options.stdinData || null;

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command, cwd, queue_id: queueId, stdin_data: stdinData })
        });

        const data = await response.json();
        if (data.queue_id) {
            currentQueueId = data.queue_id;
            switchTab('terminal');
            streamOutput(data.queue_id);
            addTerminalLine(`$ ${command}`, 'system');
        }
    } catch (error) {
        addTerminalLine(`[ERROR] ${error.message}`, 'error');
    }
}

// === Stream Output ===
 async function streamOutput(queueId) {
     let traditionalActive = false;
     try {
         updateTerminalPrompt();
         const response = await fetch(`/api/stream/${queueId}`);
         const reader = response.body.getReader();
         const decoder = new TextDecoder();
         let buffer = '';

         while (true) {
             const { done, value } = await reader.read();
             if (done) break;

             buffer += decoder.decode(value, { stream: true });
             const frames = buffer.split('\n\n');
             buffer = frames.pop() || '';

             for (const frame of frames) {
                 const lines = frame.split('\n');
                 let dataLine = '';
                 let isComment = false;

                 for (const raw of lines) {
                     const trimmed = raw.trim();
                     if (!trimmed) continue;
                     if (trimmed.startsWith(':')) {
                         isComment = true;
                         continue;
                     }
                     if (trimmed.startsWith('data:')) {
                         dataLine += trimmed.slice(5).trimStart();
                     }
                 }

                 if (isComment || !dataLine) continue;

                 if (!traditionalActive && dataLine.includes('Traditional Bank USA')) {
                     traditionalActive = true;
                     const generalVideo = document.getElementById('terminal-bg-video');
                     const specialVideo = document.getElementById('terminal-bg-video-special');
                     if (generalVideo) generalVideo.classList.remove('active');
                     if (specialVideo) {
                         specialVideo.classList.add('active');
                         specialVideo.play().catch(err => console.warn('Special background video play failed:', err));
                     }
                 }

                 if (dataLine.startsWith('[PROMPT]')) {
                     waitingForPrompt = true;
                     currentPrompt = dataLine.replace('[PROMPT]', '').trim();
                     const input = document.getElementById('cmd-input');
                     if (input) {
                         input.placeholder = currentPrompt || 'Enter value...';
                         input.focus();
                     }
                     continue;
                 }

                 addTerminalLine(dataLine, 'output');
             }
         }
     } catch (error) {
         addTerminalLine(`[STREAM ERROR] ${error.message}`, 'error');
     } finally {
         waitingForPrompt = false;
         isProcessRunning = false;
         updateTerminalPrompt();
         const input = document.getElementById('cmd-input');
         if (input) {
             input.placeholder = 'Enter command...';
         }
         const generalVideo = document.getElementById('terminal-bg-video');
         const specialVideo = document.getElementById('terminal-bg-video-special');
         if (specialVideo) specialVideo.classList.remove('active');
         if (generalVideo) {
             generalVideo.classList.add('active');
             generalVideo.play().catch(err => console.warn('General background video play failed:', err));
         }
     }
 }

 // === Terminal ===
 function initTerminal() {
     const input = document.getElementById('cmd-input');
     if (input) {
         input.addEventListener('keydown', (e) => {
             if (e.key === 'Enter') {
                 e.preventDefault();
                 runCommand();
             } else if (e.key === 'ArrowUp') {
                 e.preventDefault();
                 navigateHistory(-1);
             } else if (e.key === 'ArrowDown') {
                 e.preventDefault();
                 navigateHistory(1);
             }
         });
     }

     playHackerBoot();
 }

  function playHackerBoot() {
      const terminal = document.getElementById('terminal-output');
      if (!terminal) return;

      const video = document.getElementById('terminal-bg-video');
      const videoSpecial = document.getElementById('terminal-bg-video-special');
      if (video) video.play().catch(err => console.warn('Initial terminal background video play failed:', err));

      const lines = [
          '[SYS] Initializing hacker terminal v3.3.3...',
          '[NET] Establishing secure connection...',
          '[SEC] Loading encryption modules...',
          '[SYS] Mounting virtual filesystem...',
          '[NET] Connection established [OK]',
          '[SEC] All security protocols active',
          '[SYS] System ready.',
          '────────────────────────────────────────',
      ];

      let i = 0;
      terminal.innerHTML = '';

      function next() {
          if (i >= lines.length) {
              addTerminalLine('Welcome to Hacker Terminal GUI v3.3.3', 'info');
              addTerminalLine('Type a command or use tools from other tabs', 'info');
              addTerminalLine('────────────────────────────────────────', 'system');
              return;
          }
          addTerminalLine(lines[i], i === 4 ? 'success' : i === 5 ? 'success' : 'system');
          i++;
          setTimeout(next, 120);
      }

      next();
  }

function navigateHistory(direction) {
    const input = document.getElementById('cmd-input');
    if (!input) return;

    if (commandHistory.length === 0) return;

    historyIndex += direction;
    if (historyIndex < 0) {
        historyIndex = 0;
    } else if (historyIndex >= commandHistory.length) {
        historyIndex = commandHistory.length;
        input.value = '';
        return;
    }

    input.value = commandHistory[commandHistory.length - 1 - historyIndex];
}

function runCommand() {
    const input = document.getElementById('cmd-input');
    const command = input.value.trim();
    if (!command) return;

    // If waiting for interactive prompt, send input to the tool
    if (waitingForPrompt && currentQueueId) {
        waitingForPrompt = false;
        sendStdin(command);
        addTerminalLine(command, 'output');
        input.value = '';
        input.placeholder = 'Enter command...';
        return;
    }

    // If a process is running and not waiting for prompt, send input to it
    if (isProcessRunning && currentQueueId) {
        sendStdin(command);
        addTerminalLine(command, 'output');
        input.value = '';
        return;
    }

    addTerminalLine(`$ ${command}`, 'system');
    input.value = '';
    historyIndex = -1;

    if (command === 'clear') {
        clearTerminal();
        return;
    }

    if (command === 'stop') {
        stopCurrentProcess();
        return;
    }

    const generalVideo = document.getElementById('terminal-bg-video');
    if (generalVideo) {
        generalVideo.classList.add('active');
        generalVideo.play().catch(err => console.warn('Terminal background video play failed:', err));
    }

    executeCommand(command);
}

function updateTerminalPrompt() {
    const prompt = document.querySelector('.prompt');
    const input = document.getElementById('cmd-input');
    if (!prompt || !input) return;

    if (isProcessRunning) {
        prompt.textContent = '>';
        prompt.style.color = 'var(--accent-amber)';
        input.classList.add('active');
    } else {
        prompt.textContent = '$';
        prompt.style.color = 'var(--accent-green)';
        input.classList.remove('active');
    }
}

 function addTerminalLine(text, type = 'output') {
     const terminal = document.getElementById('terminal-output');
     if (!terminal) return;

     const line = document.createElement('div');
     line.className = `terminal-line ${type}`;

     const ts = new Date().toLocaleTimeString('en-US', { hour12: false });
     const prefix = document.createElement('span');
     prefix.className = 'terminal-ts';
     prefix.textContent = `[${ts}] `;

     const content = document.createElement('span');
     content.className = 'terminal-content';
     content.textContent = text;

     line.appendChild(prefix);
     line.appendChild(content);
     terminal.appendChild(line);
     terminal.scrollTop = terminal.scrollHeight;
 }

function clearTerminal() {
    const terminal = document.getElementById('terminal-output');
    if (terminal) {
        terminal.innerHTML = '<div class="terminal-line info">Terminal cleared</div>';
    }
}

async function stopCurrentProcess() {
    if (currentQueueId) {
        try {
            await fetch('/api/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ queue_id: currentQueueId })
            });
            addTerminalLine('[INFO] Process stopped', 'warning');
            currentQueueId = null;
            isProcessRunning = false;
            updateTerminalPrompt();
        } catch (error) {
            addTerminalLine(`[ERROR] ${error.message}`, 'error');
        }
    }
}

async function sendStdin(data) {
    if (!currentQueueId) return;

    try {
        await fetch('/api/input', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ queue_id: currentQueueId, data })
        });
    } catch (error) {
        addTerminalLine(`[ERROR] ${error.message}`, 'error');
    }
}

// === Updated executeCommand for terminal ===
async function executeCommand(command, options = {}) {
    const queueId = `cmd_${Date.now()}`;
    const cwd = options.cwd || '/home/xmavel/Documents/bank';
    const stdinData = options.stdinData || null;

    // Add to history
    commandHistory.push(command);
    if (commandHistory.length > 100) {
        commandHistory.shift();
    }
    historyIndex = -1;

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command, cwd, queue_id: queueId, stdin_data: stdinData })
        });

        if (!response.ok) {
            const text = await response.text();
            console.error('Run response body:', text.substring(0, 200));
            throw new Error(`HTTP ${response.status}: ${text.substring(0, 100)}`);
        }

        const data = await response.json();
        if (data.queue_id) {
            currentQueueId = data.queue_id;
            isProcessRunning = true;
            // Only switch to terminal if we're not already there
            const terminalTab = document.getElementById('tab-terminal');
            if (terminalTab && !terminalTab.classList.contains('active')) {
                switchTab('terminal');
            }
            streamOutput(data.queue_id);
        }
    } catch (error) {
        addTerminalLine(`[ERROR] ${error.message}`, 'error');
    }
}

// === Results ===
async function loadResults() {
    try {
        const response = await fetch('/api/results');

        if (!response.ok) {
            console.error('Results endpoint error:', response.status);
            return;
        }

        const results = await response.json();

        const container = document.getElementById('results-list');
        if (container) {
            if (results.length === 0) {
                container.innerHTML = '<div class="loading">No results yet. Run a tool to generate results.</div>';
                return;
            }

            container.innerHTML = results.map(r => `
                <div class="result-item">
                    <div class="result-info">
                        <span class="result-name">${r.name}</span>
                        <span class="result-meta">${formatSize(r.size)} - ${formatDate(r.modified)} - ${r.type.toUpperCase()}</span>
                    </div>
                    <button class="btn btn-sm btn-view" onclick="viewResult('${r.name}')">View</button>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load results:', error);
    }
}

async function viewResult(filename) {
    currentViewedFile = filename;
    try {
        const response = await fetch('/api/results/view/' + encodeURIComponent(filename));

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text.substring(0, 100)}`);
        }

        const data = await response.json();
        
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');
        
        if (data.error) {
            modalTitle.textContent = 'Error';
            modalBody.innerHTML = '<div class="terminal-output"><div class="terminal-line error">' + data.error + '</div></div>';
            document.getElementById('modal').classList.add('active');
            return;
        }
        
        modalTitle.textContent = data.filename;
        
        if (data.type === 'csv' && data.headers) {
            let tableHtml = '<div class="csv-viewer"><table class="csv-table"><thead><tr>';
            data.headers.forEach(h => {
                tableHtml += '<th>' + escapeHtml(h) + '</th>';
            });
            tableHtml += '</tr></thead><tbody>';
            data.rows.forEach(row => {
                tableHtml += '<tr>';
                row.forEach(cell => {
                    tableHtml += '<td>' + escapeHtml(cell) + '</td>';
                });
                tableHtml += '</tr>';
            });
            tableHtml += '</tbody></table></div>';
            modalBody.innerHTML = tableHtml;
        } else {
            modalBody.innerHTML = '<div class="terminal-output"><pre class="txt-content">' + escapeHtml(data.content || '') + '</pre></div>';
        }
        
        document.getElementById('modal').classList.add('active');
    } catch (error) {
        console.error('Failed to view result:', error);
        alert('Failed to view result: ' + error.message);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// === Bank Selection ===
async function openBankModal(toolId) {
    bankModalToolId = toolId;
    selectedBank = null;
    selectedBranches = [];
    branchSelectionMode = 'random';
    
    document.getElementById('bank-modal-title').textContent = 'Select Bank';
    document.getElementById('bank-list-step').style.display = 'block';
    document.getElementById('branch-selection-step').style.display = 'none';
    document.getElementById('bank-generate-btn').disabled = true;
    
    try {
        const response = await fetch('/api/banks');

        if (!response.ok) {
            const text = await response.text();
            console.error('Banks endpoint error:', response.status, text.substring(0, 100));
            alert('Failed to load banks: HTTP ' + response.status);
            return;
        }

        const banks = await response.json();
        
        const bankList = document.getElementById('bank-list');
        bankList.innerHTML = '';
        
        banks.forEach(bank => {
            const bankCard = document.createElement('div');
            bankCard.className = 'bank-card';
            bankCard.innerHTML = `
                <div class="bank-card-name">${escapeHtml(bank.name)}</div>
                <div class="bank-card-meta">${bank.branches} branches | ${bank.states.length} states</div>
            `;
            bankCard.onclick = () => selectBank(bank.name);
            bankList.appendChild(bankCard);
        });
    } catch (error) {
        console.error('Failed to load banks:', error);
        alert('Failed to load banks: ' + error.message);
    }
    
    document.getElementById('bank-modal').classList.add('active');
}

function closeBankModal() {
    document.getElementById('bank-modal').classList.remove('active');
    bankModalToolId = null;
    selectedBank = null;
    selectedBranches = [];
    branchSelectionMode = 'random';
}

 async function selectBank(bankName) {
     selectedBank = bankName;
     selectedBranches = [];
     branchSelectionMode = 'random';
     
     document.getElementById('bank-modal-title').textContent = `Branches - ${bankName}`;
     document.getElementById('bank-list-step').style.display = 'none';
     document.getElementById('branch-selection-step').style.display = 'block';
     document.getElementById('selected-bank-name').textContent = bankName;
     document.getElementById('bank-generate-btn').disabled = true;
     
     try {
         const response = await fetch(`/api/banks/${encodeURIComponent(bankName)}`);

         if (!response.ok) {
             const text = await response.text();
             console.error('Bank detail endpoint error:', response.status, text.substring(0, 100));
             alert('Failed to load bank data: HTTP ' + response.status);
             return;
         }

         const data = await response.json();
         
         const branchList = document.getElementById('branch-list');
         branchList.innerHTML = '';
         
         const branches = data.branches || [];
         branches.forEach(branch => {
             const item = document.createElement('div');
             item.className = 'branch-item';
             item.innerHTML = `
                 <div class="branch-name">${escapeHtml(branch.branch)}</div>
                 <div class="branch-address">${escapeHtml(branch.address)}, ${escapeHtml(branch.city)}, ${escapeHtml(branch.state)} ${escapeHtml(branch.zip)}</div>
                 <div class="branch-phone">${escapeHtml(branch.phone)}</div>
             `;
             branchList.appendChild(item);
         });
         
         if (branches.length === 0) {
             branchList.innerHTML = '<div class="branch-item">No branches available</div>';
         }

         const stateSelect = document.getElementById('state-select');
         if (stateSelect) {
             stateSelect.innerHTML = '<option value="">All States</option>';
             const states = data.states || [];
             states.forEach(state => {
                 const option = document.createElement('option');
                 option.value = state;
                 option.textContent = state;
                 stateSelect.appendChild(option);
             });
         }
     } catch (error) {
         console.error('Failed to load branches:', error);
         alert('Failed to load branches: ' + error.message);
     }
 }

 function selectAllBranches() {
     branchSelectionMode = 'all';
     document.getElementById('bank-generate-btn').disabled = false;
     addTerminalLine(`[INFO] Selected ALL branches for ${selectedBank}`, 'info');
 }

 function selectRandomBranch() {
     branchSelectionMode = 'random';
     document.getElementById('bank-generate-btn').disabled = false;
     addTerminalLine(`[INFO] Selected RANDOM branch for ${selectedBank}`, 'info');
 }

 function selectMixBranches() {
     branchSelectionMode = 'mix';
     document.getElementById('bank-generate-btn').disabled = false;
     addTerminalLine(`[INFO] Selected MIX branches for ${selectedBank}`, 'info');
 }

 async function runSelectedBankTool() {
     if (!bankModalToolId || !selectedBank) return;
     
     const toolId = bankModalToolId;
     const bankName = selectedBank;
     const mode = branchSelectionMode;
     const countInput = document.getElementById('lead-count');
     const count = countInput ? parseInt(countInput.value) || 10 : 10;
     const stateSelect = document.getElementById('state-select');
     const state = stateSelect ? stateSelect.value : '';
     
     closeBankModal();
     
     const queueId = `tool_${toolId}_${Date.now()}`;
     try {
         const response = await fetch('/api/tool/' + toolId, {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({
                 params: { count: count },
                 queue_id: queueId,
                 bank_name: bankName,
                 state: state || undefined,
                 branch_mode: mode,
                 auto_mode: true
             })
         });
         
         console.log('Tool response status:', response.status);
         console.log('Tool response headers:', [...response.headers.entries()]);
         
         if (!response.ok) {
             const text = await response.text();
             console.error('Tool response body:', text.substring(0, 200));
             throw new Error(`HTTP ${response.status}: ${text.substring(0, 100)}`);
         }
         
         const data = await response.json();
         if (data.queue_id) {
             currentQueueId = data.queue_id;
             isProcessRunning = true;
             switchTab('terminal');
             streamOutput(data.queue_id);
             addTerminalLine(`[INFO] Starting tool ${toolId} with ${count} leads for ${bankName} (${mode} branches)...`, 'info');
             addTerminalLine(`[INFO] Auto-continuing through prompts...`, 'info');
         }
     } catch (error) {
         addTerminalLine(`[ERROR] Failed to start tool: ${error.message}`, 'error');
         console.error('Tool start error:', error);
     }
 }

// === System Monitor ===
async function startSystemMonitor() {
    async function updateStats() {
        try {
            const response = await fetch('/api/system/status');
            const data = await response.json();

            const cpuEl = document.getElementById('cpu-usage');
            const memEl = document.getElementById('mem-usage');

            if (cpuEl && data.cpu !== undefined) {
                cpuEl.textContent = data.cpu.toFixed(1) + '%';
            }
            if (memEl && data.memory) {
                memEl.textContent = data.memory.percent.toFixed(1) + '%';
            }

            const ffCpu = document.getElementById('ff-cpu');
            const ffMem = document.getElementById('ff-mem');
            const ffDisk = document.getElementById('ff-disk');
            if (ffCpu && data.cpu !== undefined) ffCpu.textContent = data.cpu.toFixed(1) + '%';
            if (ffMem && data.memory) ffMem.textContent = data.memory.percent.toFixed(1) + '%';
            if (ffDisk && data.disk) ffDisk.textContent = data.disk.percent.toFixed(1) + '%';
        } catch (error) {
            // Silently fail
        }
    }

    updateStats();
    setInterval(updateStats, 5000);
}

// === Modal ===
function showToolInfo(toolId) {
    const module = [...(modules.generation || []), ...(modules.security || [])].find(m => m.id === toolId);
    if (!module) return;

    document.getElementById('modal-title').textContent = module.name;
    document.getElementById('modal-body').innerHTML = `
        <div class="terminal-output">
            <div class="terminal-line info">${module.icon} ${module.name}</div>
            <div class="terminal-line output">${module.desc}</div>
            <div class="terminal-line system">ID: ${module.id}</div>
            <div class="terminal-line system">Category: ${toolId <= 6 ? 'Generation' : 'Security'}</div>
        </div>
    `;
    document.getElementById('modal').classList.add('active');
}

function closeModal() {
    document.getElementById('modal').classList.remove('active');
}

function downloadResults() {
    if (!currentViewedFile) {
        alert('No file selected for download');
        return;
    }
    window.location.href = '/api/results/download/' + encodeURIComponent(currentViewedFile);
}

// === Utilities ===
function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function formatDate(iso) {
    const date = new Date(iso);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// === Theme ===
document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        // Theme switching logic can be added here
    });
});
