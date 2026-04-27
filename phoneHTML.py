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
      --app-height: 100dvh;
      --panel: rgba(10, 19, 35, 0.94);
      --panel-soft: rgba(10, 19, 35, 0.96);
      --border: rgba(148, 163, 184, 0.16);
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
        radial-gradient(circle at top, rgba(56, 189, 248, 0.14), transparent 28%),
        linear-gradient(180deg, #07101e 0%, #030712 100%);
      color: var(--text);
      font-family: var(--sans);
      overscroll-behavior: none;
    }

    body {
      height: var(--app-height);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      padding-top: env(safe-area-inset-top);
    }

    header {
      flex: 0 0 auto;
      padding: 12px 14px 10px;
      background: rgba(5, 9, 20, 0.94);
      border-bottom: 1px solid var(--border);
      backdrop-filter: blur(16px);
    }

    .header-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }

    h1 {
      margin: 0;
      font-size: 19px;
      letter-spacing: -0.04em;
    }

    .pill {
      padding: 4px 8px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      color: #bae6fd;
      font-size: 11px;
      font-weight: 700;
      white-space: nowrap;
    }

    .status-row {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--muted);
      font-size: 13px;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #fbbf24;
      box-shadow: 0 0 14px rgba(251, 191, 36, 0.45);
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
      flex: 1 1 auto;
      min-height: 0;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      padding: 12px 14px;
      font-family: var(--mono);
      font-size: 13px;
      line-height: 1.45;
      background: linear-gradient(180deg, rgba(10, 19, 35, 0.3) 0%, rgba(3, 7, 18, 0.75) 100%);
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .log-entry {
      white-space: pre-wrap;
      word-break: break-word;
      border-radius: 12px;
    }

    .log-entry.plain,
    .log-entry.rx {
      color: var(--text);
    }

    .log-entry.tcp-connected {
      color: #86efac;
      font-weight: 700;
    }

    .log-entry.tx {
      position: relative;
      padding: 3px 84px 3px 8px;
      background: rgba(100, 116, 139, 0.18);
      border: 1px solid rgba(148, 163, 184, 0.14);
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
      border: 1px solid rgba(148, 163, 184, 0.18);
      background: rgba(15, 23, 42, 0.9);
      color: var(--text);
      font-size: 10px;
      font-weight: 700;
    }

    .toolbar {
      flex: 0 0 auto;
      padding: 10px 10px calc(10px + env(safe-area-inset-bottom));
      background: rgba(5, 9, 20, 0.97);
      border-top: 1px solid var(--border);
      backdrop-filter: blur(18px);
    }

    .input-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      align-items: end;
    }

    #cmd {
      width: 100%;
      min-width: 0;
      min-height: 46px;
      max-height: 104px;
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid rgba(56, 189, 248, 0.2);
      background: var(--panel-soft);
      color: var(--text);
      font: inherit;
      font-size: 16px;
      line-height: 1.35;
      outline: none;
      resize: none;
      overflow-y: auto;
    }

    #cmd:focus {
      border-color: rgba(56, 189, 248, 0.72);
      box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.12);
    }

    button {
      min-height: 46px;
      padding: 0 16px;
      border: 0;
      border-radius: 14px;
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
    <div class="header-top">
      <h1>ESP32 Monitor</h1>
      <span class="pill">Téléphone</span>
    </div>
    <div class="status-row">
      <span id="status-dot" class="status-dot"></span>
      <span id="status">Connexion WebSocket en cours...</span>
    </div>
  </header>

  <div id="logs"></div>

  <section class="toolbar">
    <div class="input-row">
      <textarea id="cmd" rows="1" placeholder="Commande UART..." autocomplete="off" autocapitalize="none" spellcheck="false"></textarea>
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
    const autoReloadKey = "uart-bridge-phone-autoreload";

    let ws = null;
    let reconnectTimer = null;
    let stickToBottom = true;

    function updateViewportHeight() {
      const height = window.visualViewport ? window.visualViewport.height : window.innerHeight;
      document.documentElement.style.setProperty("--app-height", `${height}px`);
      scrollLogsToBottom();
    }

    function setStatus(text, state) {
      status.textContent = text;
      statusDot.classList.remove("ok", "off");
      if (state) {
        statusDot.classList.add(state);
      }
      sendBtn.disabled = state === "off";
    }

    function shouldStickToBottom() {
      const distance = logs.scrollHeight - logs.scrollTop - logs.clientHeight;
      return distance < 36;
    }

    function scrollLogsToBottom(force = false) {
      if (!force && !stickToBottom) {
        return;
      }

      window.requestAnimationFrame(() => {
        logs.scrollTop = logs.scrollHeight;
      });
    }

    function resizeComposer() {
      cmd.style.height = "auto";
      cmd.style.height = `${Math.min(cmd.scrollHeight, 104)}px`;
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

      setStatus("Reconnexion...", "off");
      reconnectTimer = window.setTimeout(() => {
        reconnectTimer = null;
        connectWebSocket(true);
      }, 1200);
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
          connectWebSocket(true);
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
      const follow = stickToBottom || shouldStickToBottom();
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
      if (follow) {
        stickToBottom = true;
        scrollLogsToBottom(true);
      }
    }

    function sendCmd() {
      const text = cmd.value.trim();
      if (!text) {
        return;
      }

      if (!ws || ws.readyState !== WebSocket.OPEN) {
        setStatus("WebSocket non connectée", "off");
        connectWebSocket(true);
        return;
      }

      ws.send(`${text}\n`);
      cmd.value = "";
      resizeComposer();
      stickToBottom = true;
      scrollLogsToBottom(true);
    }

    function ensureConnection() {
      if (!ws || ws.readyState === WebSocket.CLOSED || ws.readyState === WebSocket.CLOSING) {
        connectWebSocket(true);
      }
    }

    window.setTimeout(() => {
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

    logs.addEventListener("scroll", () => {
      stickToBottom = shouldStickToBottom();
    });

    cmd.addEventListener("input", () => {
      resizeComposer();
      scrollLogsToBottom();
    });

    cmd.addEventListener("focus", () => {
      window.setTimeout(() => scrollLogsToBottom(), 120);
    });

    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", updateViewportHeight);
      window.visualViewport.addEventListener("scroll", updateViewportHeight);
    }

    window.addEventListener("resize", updateViewportHeight);

    sendBtn.addEventListener("click", sendCmd);
    cmd.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendCmd();
      }
    });

    updateViewportHeight();
    resizeComposer();
    scrollLogsToBottom(true);
  </script>
</body>
</html>
"""
