HTML_phone = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
  <title>ESP32 Phone Console</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #050914;
      --panel: #0a1323;
      --panel-soft: rgba(10, 19, 35, 0.88);
      --border: rgba(148, 163, 184, 0.18);
      --text: #e2e8f0;
      --muted: #95a9c5;
      --accent: #38bdf8;
      --accent-strong: #0ea5e9;
      --ok: #4ade80;
      --error: #fb7185;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      margin: 0;
      min-height: 100%;
      background:
        radial-gradient(circle at top, rgba(56, 189, 248, 0.16), transparent 32%),
        linear-gradient(180deg, #07101e 0%, #030712 100%);
      color: var(--text);
      font-family: var(--sans);
      overscroll-behavior: none;
    }

    body {
      min-height: 100dvh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      padding-top: env(safe-area-inset-top);
      padding-bottom: env(safe-area-inset-bottom);
    }

    header {
      padding: 16px 16px 14px;
      background: rgba(5, 9, 20, 0.92);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(16px);
    }

    .topline {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }

    h1 {
      margin: 0;
      font-size: 21px;
      letter-spacing: -0.04em;
    }

    .badge {
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      color: #bae6fd;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }

    .status-row {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--muted);
      font-size: 14px;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #fbbf24;
      box-shadow: 0 0 14px rgba(251, 191, 36, 0.5);
    }

    .status-dot.ok {
      background: var(--ok);
      box-shadow: 0 0 14px rgba(74, 222, 128, 0.65);
    }

    .status-dot.off {
      background: var(--error);
      box-shadow: 0 0 14px rgba(251, 113, 133, 0.65);
    }

    #logs {
      overflow-y: auto;
      padding: 14px 16px 24px;
      font-family: var(--mono);
      font-size: 13px;
      line-height: 1.55;
      background: linear-gradient(180deg, rgba(10, 19, 35, 0.35) 0%, rgba(3, 7, 18, 0.7) 100%);
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .log-entry {
      white-space: pre-wrap;
      word-break: break-word;
      border-radius: 14px;
    }

    .log-entry.plain {
      color: var(--text);
    }

    .log-entry.rx {
      color: var(--text);
    }

    .log-entry.tcp-connected {
      color: #86efac;
      font-weight: 700;
    }

    .log-entry.tx {
      position: relative;
      display: flex;
      align-items: flex-start;
      padding: 3px 84px 3px 8px;
      background: rgba(100, 116, 139, 0.22);
      border: 1px solid rgba(148, 163, 184, 0.18);
      color: #fde68a;
    }

    .tx-label {
      width: 100%;
      font-weight: 700;
      line-height: 1.25;
    }

    .tx-actions {
      position: absolute;
      right: 6px;
      top: 4px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .tx-action {
      min-height: 20px;
      padding: 0 6px;
      border-radius: 6px;
      background: rgba(15, 23, 42, 0.88);
      color: var(--text);
      font-size: 10px;
      font-weight: 700;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }

    .toolbar {
      display: grid;
      gap: 10px;
      padding: 12px 12px calc(12px + env(safe-area-inset-bottom));
      background: rgba(5, 9, 20, 0.96);
      border-top: 1px solid var(--border);
      backdrop-filter: blur(18px);
    }

    .hint {
      margin: 0;
      color: var(--muted);
      font-size: 12px;
      text-align: center;
    }

    .input-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
    }

    #cmd {
      min-width: 0;
      width: 100%;
      min-height: 52px;
      padding: 14px 16px;
      border-radius: 16px;
      border: 1px solid rgba(56, 189, 248, 0.2);
      background: var(--panel-soft);
      color: var(--text);
      font-size: 16px;
      outline: none;
    }

    #cmd:focus {
      border-color: rgba(56, 189, 248, 0.7);
      box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.12);
    }

    button {
      min-height: 52px;
      padding: 0 18px;
      border: 0;
      border-radius: 16px;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
      color: #04131d;
      font-size: 15px;
      font-weight: 800;
    }

    button:disabled {
      opacity: 0.5;
    }
  </style>
</head>
<body>
  <header>
    <div class="topline">
      <h1>ESP32 Monitor</h1>
      <span class="badge">Téléphone</span>
    </div>
    <div class="status-row">
      <span id="status-dot" class="status-dot"></span>
      <span id="status">Connexion WebSocket en cours...</span>
    </div>
  </header>

  <div id="logs"></div>

  <section class="toolbar">
    <div class="input-row">
      <input id="cmd" type="text" placeholder="Commande UART..." autocomplete="off" autocapitalize="none" spellcheck="false">
      <button id="send-btn" type="button">Envoyer</button>
    </div>
  </section>

  <script>
    const logs = document.getElementById("logs");
    const cmd = document.getElementById("cmd");
    const sendBtn = document.getElementById("send-btn");
    const status = document.getElementById("status");
    const statusDot = document.getElementById("status-dot");
    const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:";
    let ws = null;
    const autoReloadKey = "uart-bridge-phone-autoreload";
    let reconnectTimer = null;
    let wsBootTimer = null;

    function setStatus(text, state) {
      status.textContent = text;
      statusDot.classList.remove("ok", "off");
      if (state) {
        statusDot.classList.add(state);
      }
      sendBtn.disabled = state === "off";
    }

    function scrollLogsToBottom() {
      logs.scrollTop = logs.scrollHeight;
    }

    function fallbackCopyText(text) {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      textarea.style.pointerEvents = "none";
      textarea.style.top = "0";
      textarea.style.left = "0";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      textarea.setSelectionRange(0, textarea.value.length);

      let success = false;
      try {
        success = document.execCommand("copy");
      } catch (error) {
        console.error("Fallback clipboard error", error);
      }

      document.body.removeChild(textarea);
      return success;
    }

    async function copyText(text) {
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
          setStatus("Message copie", "ok");
          return true;
        }
      } catch (error) {
        console.error("Clipboard error", error);
      }

      const success = fallbackCopyText(text);
      setStatus(success ? "Message copie" : "Copie impossible", success ? "ok" : "off");
      return success;
    }

    function scheduleReconnect() {
      if (reconnectTimer) {
        return;
      }

      const delay = 1200;
      setStatus("Reconnexion...", "off");

      reconnectTimer = window.setTimeout(() => {
        reconnectTimer = null;
        connectWebSocket(true);
      }, delay);
    }

    function connectWebSocket(force = false) {
      if (!force && ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
        return;
      }

      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
      }

      if (ws) {
        try {
          ws.onopen = null;
          ws.onmessage = null;
          ws.onerror = null;
          ws.onclose = null;
          if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
            ws.close();
          }
        } catch (error) {
          console.error("WebSocket cleanup error", error);
        }
      }

      setStatus("Connexion WebSocket en cours...", null);
      const socket = new WebSocket(`${wsProtocol}//${location.host}/ws`);
      ws = socket;

      socket.onopen = () => {
        if (ws !== socket) {
          return;
        }
        sessionStorage.removeItem(autoReloadKey);
        setStatus("Interface téléphone connectée", "ok");
        cmd.focus();
      };

      socket.onmessage = (event) => {
        if (ws !== socket) {
          return;
        }
        appendLog(event.data);
      };

      socket.onerror = () => {
        if (ws !== socket) {
          return;
        }
        setStatus("Erreur WebSocket", "off");
      };

      socket.onclose = (event) => {
        if (ws !== socket) {
          return;
        }
        setStatus(`Déconnecté (${event.code})`, "off");
        scheduleReconnect();
      };
    }

    function createTxEntry(payload) {
      const entry = document.createElement("div");
      entry.className = "log-entry tx";

      const label = document.createElement("div");
      label.className = "tx-label";
      label.textContent = `[TX] ${payload}`;

      const actions = document.createElement("div");
      actions.className = "tx-actions";

      const copyBtn = document.createElement("button");
      copyBtn.type = "button";
      copyBtn.className = "tx-action";
      copyBtn.textContent = "Copier";
      copyBtn.addEventListener("click", async () => {
        await copyText(payload);
      });

      const resendBtn = document.createElement("button");
      resendBtn.type = "button";
      resendBtn.className = "tx-action";
      resendBtn.textContent = "Renvoyer";
      resendBtn.addEventListener("click", () => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
          setStatus("WebSocket non connectée", "off");
          connectWebSocket();
          return;
        }
        ws.send(`${payload}\n`);
      });

      actions.append(copyBtn, resendBtn);
      entry.append(label, actions);
      return entry;
    }

    function createPlainEntry(text, className = "plain") {
      const entry = document.createElement("div");
      entry.className = `log-entry ${className}`;
      entry.textContent = text;
      return entry;
    }

    function appendLog(line) {
      const txPrefix = "[PC → ESP] ";
      const rxPrefix = "[ESP → PC] ";
      const tcpConnectedPrefix = "[TCP] ESP connecté :";
      let entry;

      if (line.startsWith(txPrefix)) {
        entry = createTxEntry(line.slice(txPrefix.length));
      } else if (line.startsWith(rxPrefix)) {
        entry = createPlainEntry(line.slice(rxPrefix.length), "rx");
      } else if (line.startsWith(tcpConnectedPrefix)) {
        entry = createPlainEntry(line, "tcp-connected");
      } else {
        entry = createPlainEntry(line, "plain");
      }

      logs.appendChild(entry);
      scrollLogsToBottom();
    }

    function sendCmd() {
      const text = cmd.value.trim();
      if (!text) {
        return;
      }

      if (!ws || ws.readyState !== WebSocket.OPEN) {
        setStatus("WebSocket non connectée", "off");
        connectWebSocket();
        return;
      }

      ws.send(`${text}\n`);
      cmd.value = "";
      cmd.focus();
    }

    function ensureConnection() {
      if (!ws || ws.readyState === WebSocket.CLOSED || ws.readyState === WebSocket.CLOSING) {
        connectWebSocket(true);
      }
    }

    wsBootTimer = window.setTimeout(() => {
      connectWebSocket(true);
    }, 300);

    window.setTimeout(() => {
      const alreadyReloaded = sessionStorage.getItem(autoReloadKey) === "1";
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        if (!alreadyReloaded) {
          sessionStorage.setItem(autoReloadKey, "1");
          location.reload();
          return;
        }
        connectWebSocket(true);
      }
    }, 3200);

    window.addEventListener("pageshow", () => {
      window.setTimeout(ensureConnection, 120);
    });

    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) {
        window.setTimeout(ensureConnection, 120);
      }
    });

    window.addEventListener("online", () => {
      connectWebSocket(true);
    });

    sendBtn.addEventListener("click", sendCmd);
    cmd.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        sendCmd();
      }
    });
  </script>
</body>
</html>
"""
