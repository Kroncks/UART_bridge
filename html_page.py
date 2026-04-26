HTML = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>ESP32 Bridge</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #07111f;
      --bg-soft: #0d1b2d;
      --panel: rgba(13, 27, 45, 0.86);
      --panel-strong: #0f2238;
      --border: rgba(148, 163, 184, 0.22);
      --text: #e2e8f0;
      --muted: #8aa0bc;
      --accent: #4ade80;
      --accent-strong: #22c55e;
      --danger: #fb7185;
      --shadow: 0 24px 60px rgba(2, 6, 23, 0.42);
      --radius: 22px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      min-height: 100%;
      background:
        radial-gradient(circle at top left, rgba(34, 197, 94, 0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(56, 189, 248, 0.14), transparent 24%),
        linear-gradient(180deg, #08101c 0%, #04080f 100%);
      color: var(--text);
      font-family: var(--sans);
    }

    body {
      min-height: 100vh;
      padding: 18px;
    }

    .shell {
      width: min(960px, 100%);
      margin: 0 auto;
      display: grid;
      gap: 14px;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }

    .topbar {
      padding: 16px 18px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 16px;
      align-items: center;
    }

    h1 {
      margin: 0;
      font-size: clamp(24px, 4vw, 32px);
      line-height: 1;
      letter-spacing: -0.04em;
    }

    .status-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 10px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(15, 34, 56, 0.95);
      border: 1px solid var(--border);
      font-size: 14px;
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #fbbf24;
      box-shadow: 0 0 16px rgba(251, 191, 36, 0.55);
      transition: background 0.2s ease, box-shadow 0.2s ease;
    }

    .status-dot.ok {
      background: var(--accent);
      box-shadow: 0 0 16px rgba(74, 222, 128, 0.7);
    }

    .status-dot.off {
      background: var(--danger);
      box-shadow: 0 0 16px rgba(251, 113, 133, 0.7);
    }

    .qr-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 8px;
    }

    .qr-frame {
      width: 92px;
      aspect-ratio: 1;
      padding: 8px;
      border-radius: 18px;
      background: linear-gradient(180deg, #ffffff 0%, #e5edf6 100%);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
    }

    .qr-frame img {
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
    }

    .qr-note {
      margin: 0;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.35;
      max-width: 130px;
    }

    .console {
      padding: 16px;
      display: grid;
      gap: 12px;
    }

    .console-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: end;
    }

    .console-head h2 {
      margin: 0;
      font-size: 18px;
      letter-spacing: -0.03em;
    }

    .console-head p {
      margin: 2px 0 0;
      color: var(--muted);
      font-size: 13px;
    }

    #logs {
      min-height: 460px;
      max-height: 64vh;
      overflow: auto;
      margin: 0;
      padding: 16px;
      border-radius: 18px;
      background: #030712;
      border: 1px solid rgba(148, 163, 184, 0.14);
      color: #d5e3f2;
      font-family: var(--mono);
      font-size: 13px;
      line-height: 1.58;
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
      color: #d5e3f2;
    }

    .log-entry.rx {
      color: #e2e8f0;
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
      color: #fef3c7;
    }

    .tx-label {
      width: 100%;
      font-weight: 700;
      color: #fde68a;
      line-height: 1.25;
    }

    .tx-actions {
      position: absolute;
      right: 6px;
      top: 4px;
      display: flex;
      align-items: center;
      gap: 4px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.15s ease;
    }

    .log-entry.tx:hover .tx-actions,
    .log-entry.tx:focus-within .tx-actions {
      opacity: 1;
      pointer-events: auto;
    }

    .tx-action {
      min-height: 20px;
      padding: 0 6px;
      border-radius: 6px;
      background: rgba(15, 23, 42, 0.88);
      color: #e2e8f0;
      font-size: 10px;
      font-weight: 700;
      border: 1px solid rgba(148, 163, 184, 0.2);
    }

    .tx-action:hover {
      filter: brightness(1.08);
    }

    .composer {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
    }

    #cmd {
      width: 100%;
      min-width: 0;
      padding: 15px 18px;
      border-radius: 16px;
      border: 1px solid rgba(96, 165, 250, 0.2);
      background: rgba(6, 14, 25, 0.86);
      color: var(--text);
      font: inherit;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    #cmd:focus {
      border-color: rgba(74, 222, 128, 0.64);
      box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.14);
    }

    button {
      border: 0;
      border-radius: 16px;
      padding: 0 24px;
      min-height: 52px;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
      color: #04110a;
      font-weight: 800;
      font-size: 15px;
      cursor: pointer;
      transition: transform 0.15s ease, filter 0.15s ease;
    }

    button:hover {
      filter: brightness(1.05);
    }

    button:active {
      transform: translateY(1px) scale(0.99);
    }

    button:disabled {
      cursor: not-allowed;
      filter: saturate(0.2) brightness(0.75);
    }

    .topbar-copy {
      min-width: 0;
    }

    .topbar-copy p {
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 13px;
    }

    .qr-link {
      color: var(--text);
      text-decoration: none;
      word-break: break-all;
    }

    .qr-link:hover {
      color: #bbf7d0;
    }

    @media (max-width: 980px) {
      body {
        padding: 18px;
      }
    }

    @media (max-width: 680px) {
      body {
        padding: 12px;
      }

      .topbar,
      .console {
        padding: 18px;
      }

      .topbar {
        grid-template-columns: 1fr;
        justify-items: start;
      }

      .console-head {
        flex-direction: column;
        align-items: start;
      }

      .composer {
        grid-template-columns: 1fr;
      }

      button {
        min-height: 50px;
      }

      .tx-actions {
        opacity: 1;
        pointer-events: auto;
        position: static;
      }

      #logs {
        min-height: 320px;
        max-height: 48vh;
      }

      .log-entry.tx {
        padding: 4px 8px;
        display: grid;
        gap: 4px;
      }

      .qr-card {
        flex-direction: row;
        align-items: center;
        text-align: left;
      }

      .qr-note {
        max-width: none;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="panel topbar">
      <div class="topbar-copy">
        <div>
          <h1>ESP32 Monitor</h1>
          <p>UART Bridge</p>
        </div>

        <div class="status-row">
          <div class="chip">
            <span id="status-dot" class="status-dot"></span>
            <span id="status">Connexion WebSocket en cours...</span>
          </div>
        </div>
      </div>

      <div class="qr-card">
        <div class="qr-frame">
          <img src="/qr" alt="QR code vers l'interface téléphone">
        </div>
      </div>
    </section>

    <section class="panel console">
      <div class="console-head">
        <div>
          <h2>Console temps réel</h2>
          <p>Logs ESP32 et commandes UART.</p>
        </div>
      </div>

      <div id="logs"></div>

      <div class="composer">
        <input id="cmd" type="text" placeholder="Tape une commande UART..." autocomplete="off" autocapitalize="none" spellcheck="false">
        <button id="send-btn" type="button">Envoyer</button>
      </div>
    </section>
  </main>

  <script>
    const logs = document.getElementById("logs");
    const cmd = document.getElementById("cmd");
    const sendBtn = document.getElementById("send-btn");
    const status = document.getElementById("status");
    const statusDot = document.getElementById("status-dot");
    const wsProtocol = location.protocol === "https:" ? "wss:" : "ws:";
    const ws = new WebSocket(`${wsProtocol}//${location.host}/ws`);

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

    async function copyText(text) {
      try {
        await navigator.clipboard.writeText(text);
      } catch (error) {
        console.error("Clipboard error", error);
      }
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
      copyBtn.addEventListener("click", () => {
        copyText(payload);
      });

      const resendBtn = document.createElement("button");
      resendBtn.type = "button";
      resendBtn.className = "tx-action";
      resendBtn.textContent = "Renvoyer";
      resendBtn.addEventListener("click", () => {
        if (ws.readyState !== WebSocket.OPEN) {
          setStatus("WebSocket non connectée", "off");
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

      if (ws.readyState !== WebSocket.OPEN) {
        setStatus("WebSocket non connectée", "off");
        return;
      }

      ws.send(`${text}\n`);
      cmd.value = "";
      cmd.focus();
    }

    setStatus("Connexion WebSocket en cours...", null);

    ws.onopen = () => {
      setStatus("Interface bureau connectée", "ok");
      cmd.focus();
    };

    ws.onmessage = (event) => {
      appendLog(event.data);
    };

    ws.onerror = () => {
      setStatus("Erreur WebSocket", "off");
    };

    ws.onclose = (event) => {
      setStatus(`Déconnecté (${event.code})`, "off");
    };

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
