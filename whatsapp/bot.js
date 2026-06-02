const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const BACKEND_URL = "http://localhost:8000";
const conversations = {};

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: { headless: true, args: ["--no-sandbox"] },
});

client.on("qr", (qr) => {
  console.log("\n=== Scan QR Code ini dengan WhatsApp kamu ===\n");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("✅ JER WhatsApp Bot aktif!");
});

client.on("message", async (msg) => {
  const from = msg.from;
  const body = msg.body.trim();
  if (!body) return;

  // Perintah /all — hanya di grup
  if (body.toLowerCase().startsWith("/all")) {
    if (!msg.from.endsWith("@g.us")) {
      msg.reply("Perintah /all hanya bisa dipakai di grup!");
      return;
    }
    const pesanTambahan = body.slice(7).trim();
    await tagAll(msg, pesanTambahan);
    return;
  }

  // Di grup: hanya respon kalau bot di-tag atau reply ke pesan bot
  if (msg.from.endsWith("@g.us")) {
    const botNumber = client.info.wid.user;
    const mentions = await msg.getMentions();
    const diTag = mentions.some(c => c.id.user === botNumber || c.number === botNumber);

    let diReply = false;
    if (!diTag && msg.hasQuotedMsg) {
      const quoted = await msg.getQuotedMessage();
      diReply = quoted.fromMe;
    }

    if (!diTag && !diReply) return;
  }

  // Perintah /reset
  if (body.toLowerCase() === "/reset") {
    conversations[from] = [];
    msg.reply("Chat direset! Hei, aku JER 👋 Ada yang bisa aku bantu?");
    return;
  }


  // Chat AI
  if (!conversations[from]) conversations[from] = [];
  conversations[from].push({ role: "user", content: body });
  if (conversations[from].length > 20) {
    conversations[from] = conversations[from].slice(-20);
  }

  try {
    const res = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: conversations[from] }),
    });

    const resText = await res.text();
    if (!res.ok) throw new Error(`Server error ${res.status}: ${resText}`);

    const data = JSON.parse(resText);
    const reply = data.reply;

    conversations[from].push({ role: "assistant", content: reply });
    msg.reply(reply);

  } catch (err) {
    console.error("Error:", err);
    msg.reply("Maaf, lagi ada masalah teknis. Coba lagi ya! 😅");
  }
});

async function tagAll(msg, pesanTambahan) {
  try {
    const chat = await msg.getChat();
    const participants = chat.participants;

    const mentions = await Promise.all(
      participants.map(p => client.getContactById(p.id._serialized))
    );

    const mentionText = mentions.map(c => `@${c.id.user}`).join(" ");
    const fullPesan = pesanTambahan
      ? `${pesanTambahan}\n\n${mentionText}`
      : mentionText;

    await chat.sendMessage(fullPesan, { mentions });
    console.log(`✅ Tag all berhasil (${mentions.length} anggota)`);
  } catch (err) {
    console.error("Tag all error:", err);
    msg.reply("Gagal tag semua anggota. Pastikan bot adalah admin grup!");
  }
}

client.initialize();
