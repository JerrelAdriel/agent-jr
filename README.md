# Agent-JR 🤖

AI assistant pribadi multi-platform — tersedia di **website**, **WhatsApp bot**, dan **desktop app**. Powered by Claude (Anthropic) dengan fallback otomatis ke Groq (Llama 3.1).

![Agent-JR Preview](frontend/assets/screenshot.png)

## ✨ Features

- 💬 Multi-turn conversation dengan memory per-user
- ⚡ Streaming response (real-time typing effect)
- 🔁 Auto fallback: Claude → Groq kalau Claude tidak tersedia
- 📱 WhatsApp bot: respon saat di-tag/reply, command `/all` & `/reset`
- 🖥️ Desktop app via Electron
- 🌐 Web UI (dark mode)

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      Backend (FastAPI / Python)     │
│        Claude API + Groq API        │
└──────┬──────────┬──────────┬────────┘
       │          │          │
   ┌───▼──┐  ┌───▼────┐  ┌──▼─────┐
   │ Web  │  │WhatsApp│  │Desktop │
   │  UI  │  │  Bot   │  │ App    │
   └──────┘  └────────┘  └────────┘
```

## 🚀 Quick Start

### 1. Setup API Keys
```bash
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY dan/atau GROQ_API_KEY
```

### 2. Backend (Python)
```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
# → http://localhost:8000
```

### 3. WhatsApp Bot (Node.js)
```bash
cd whatsapp
npm install
node bot.js
# scan QR code dengan WhatsApp HP
```

### 4. Desktop App (Electron)
```bash
cd desktop
npm install
npm start
```

## 🔑 API Keys

- **Anthropic Claude** — daftar di [console.anthropic.com](https://console.anthropic.com), butuh kredit
- **Groq** — daftar di [console.groq.com](https://console.groq.com), gratis 14.400 req/hari

Salah satu cukup. Kalau dua-duanya tersedia, Claude akan dicoba dulu lalu fallback ke Groq.

## 📂 Project Structure

```
my-ai/
├── main.py              Backend FastAPI + fallback logic
├── requirements.txt     Python deps
├── .env.example         Template env vars
├── frontend/            Web UI (HTML/CSS/JS)
├── whatsapp/            WhatsApp bot (Node.js + whatsapp-web.js)
└── desktop/             Desktop wrapper (Electron)
```

## 👤 Author

**Jerrel Adriel** · [GitHub](https://github.com/JerrelAdriel) · [LinkedIn](https://www.linkedin.com/in/jerrelhutahaean)

---

📚 **Full documentation** untuk semua project saya tersedia di [Portfolio Documentation](https://github.com/JerrelAdriel/JerrelAdriel.github.io/blob/main/DOCUMENTATION.md).

Built with ❤️ in Jakarta · © 2026
