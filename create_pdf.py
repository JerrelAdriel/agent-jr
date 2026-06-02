from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = r"D:\Claude\my-ai\Agent-JR-Documentation.pdf"

PURPLE = colors.HexColor("#7c3aed")
PURPLE_LIGHT = colors.HexColor("#ede9fe")
DARK = colors.HexColor("#1a1a2e")
GRAY = colors.HexColor("#6b7280")
WHITE = colors.white

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle("title", fontSize=28, textColor=PURPLE,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6)
subtitle_style = ParagraphStyle("subtitle", fontSize=13, textColor=GRAY,
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4)
section_style = ParagraphStyle("section", fontSize=14, textColor=WHITE,
    fontName="Helvetica-Bold", spaceAfter=8, spaceBefore=16,
    backColor=PURPLE, leftIndent=-1*cm, rightIndent=-1*cm,
    borderPad=8, leading=20)
body_style = ParagraphStyle("body", fontSize=10.5, textColor=DARK,
    fontName="Helvetica", spaceAfter=5, leading=16)
bullet_style = ParagraphStyle("bullet", fontSize=10.5, textColor=DARK,
    fontName="Helvetica", spaceAfter=4, leading=15,
    leftIndent=16, bulletIndent=0)
code_style = ParagraphStyle("code", fontSize=9, textColor=DARK,
    fontName="Courier", spaceAfter=4, leading=14,
    backColor=colors.HexColor("#f3f0ff"), leftIndent=12,
    borderPad=6)
small_style = ParagraphStyle("small", fontSize=9, textColor=GRAY,
    fontName="Helvetica", alignment=TA_CENTER)

def section(title):
    return [
        Spacer(1, 0.3*cm),
        Table([[Paragraph(f"  {title}", ParagraphStyle("sh", fontSize=13,
            textColor=WHITE, fontName="Helvetica-Bold", leading=18))]],
            colWidths=[17*cm],
            style=TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), PURPLE),
                ("ROWBACKGROUNDS", (0,0), (-1,-1), [PURPLE]),
                ("TOPPADDING", (0,0), (-1,-1), 8),
                ("BOTTOMPADDING", (0,0), (-1,-1), 8),
                ("LEFTPADDING", (0,0), (-1,-1), 12),
            ])
        ),
        Spacer(1, 0.3*cm),
    ]

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", bullet_style)

def body(text):
    return Paragraph(text, body_style)

def code(text):
    return Paragraph(text.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style)

story = []

# ── COVER ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(Table([[Paragraph("JR", ParagraphStyle("av", fontSize=48,
    textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=56))]],
    colWidths=[4*cm], rowHeights=[4*cm],
    style=TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PURPLE),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [12,12,12,12]),
    ]),
    hAlign="CENTER"
))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph("Agent-JR", title_style))
story.append(Paragraph("Dokumentasi Pembuatan AI Pribadi", subtitle_style))
story.append(Paragraph("Panduan Lengkap Membangun AI Asisten Multi-Platform", subtitle_style))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="100%", thickness=2, color=PURPLE))
story.append(Spacer(1, 0.4*cm))

# Info table
info_data = [
    ["Dibuat oleh", "Jerrel Adriel"],
    ["Tanggal", "28 Mei 2026"],
    ["Versi", "1.0.0"],
    ["Status", "Aktif"],
]
info_table = Table(info_data, colWidths=[4*cm, 13*cm])
info_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("TEXTCOLOR", (0,0), (0,-1), PURPLE),
    ("TEXTCOLOR", (1,0), (1,-1), DARK),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#e5e7eb")),
]))
story.append(info_table)

# ── BAGIAN 1 ───────────────────────────────────────────────────────────────
story += section("1. Gambaran Umum")
overview = [
    ["Nama AI", "Agent-JR"],
    ["Tipe", "AI Asisten Pribadi (Opsi 3 - Custom Persona)"],
    ["Platform", "Website, WhatsApp Bot, Desktop App"],
    ["Bahasa", "Indonesia (casual & bersahabat)"],
    ["Kepribadian", "Santai, pintar, helpful seperti teman dekat"],
]
ov_table = Table(overview, colWidths=[4*cm, 13*cm])
ov_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("TEXTCOLOR", (0,0), (0,-1), PURPLE),
    ("TEXTCOLOR", (1,0), (1,-1), DARK),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [PURPLE_LIGHT, WHITE]),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
]))
story.append(ov_table)

# ── BAGIAN 2 ───────────────────────────────────────────────────────────────
story += section("2. Teknologi yang Digunakan")
tech = [
    ["Backend", "Python + FastAPI", "Server API utama"],
    ["AI Engine (Utama)", "Claude Haiku (Anthropic)", "Memerlukan kredit"],
    ["AI Engine (Fallback)", "Llama 3.1 via Groq", "Gratis, 14.400 req/hari"],
    ["Frontend", "HTML + CSS + JavaScript", "Chat UI dark mode"],
    ["WhatsApp Bot", "Node.js + whatsapp-web.js", "Koneksi WhatsApp"],
    ["Desktop App", "Electron", "Wrap web app ke desktop"],
]
tech_table = Table([["Komponen", "Teknologi", "Keterangan"]] + tech,
    colWidths=[4.5*cm, 5.5*cm, 7*cm])
tech_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE),
    ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("TEXTCOLOR", (0,1), (-1,-1), DARK),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [PURPLE_LIGHT, WHITE]),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
]))
story.append(tech_table)

# ── BAGIAN 3 ───────────────────────────────────────────────────────────────
story += section("3. Arsitektur Sistem")
story.append(body("Sistem Agent-JR menggunakan arsitektur terpusat dengan satu backend FastAPI "
    "yang melayani tiga platform sekaligus:"))
story.append(Spacer(1, 0.2*cm))

arch = [
    ["", "BACKEND (Python FastAPI)\nClaude API + Groq API", ""],
    ["Website\n(localhost:8000)", "", "WhatsApp Bot\n(whatsapp-web.js)"],
    ["", "Desktop App\n(Electron)", ""],
]
arch_table = Table([
    [Paragraph("<b>BACKEND (Python FastAPI)</b><br/>Claude API + Groq Fallback",
        ParagraphStyle("ac", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER, leading=14))],
    [Paragraph("Website &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; WhatsApp Bot &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; Desktop App",
        ParagraphStyle("ap", fontSize=10, textColor=DARK, fontName="Helvetica",
        alignment=TA_CENTER))],
], colWidths=[17*cm])
arch_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE),
    ("BACKGROUND", (0,1), (-1,1), PURPLE_LIGHT),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ("TOPPADDING", (0,0), (-1,-1), 12),
    ("BOX", (0,0), (-1,-1), 1, PURPLE),
]))
story.append(arch_table)
story.append(Spacer(1, 0.3*cm))
story.append(bullet("Satu backend melayani semua platform"))
story.append(bullet("Frontend website di-serve langsung oleh FastAPI sebagai static files"))
story.append(bullet("WhatsApp bot berkomunikasi dengan backend via HTTP POST"))
story.append(bullet("Desktop app (Electron) membuka tampilan web dari localhost"))

# ── BAGIAN 4 ───────────────────────────────────────────────────────────────
story += section("4. Fitur Agent-JR")
features = [
    ("Multi-turn Conversation", "Bot mengingat seluruh riwayat percakapan dalam satu sesi"),
    ("Streaming Response", "Jawaban muncul real-time seperti efek mengetik"),
    ("Fallback Otomatis", "Claude gagal? Otomatis beralih ke Groq (Llama 3.1)"),
    ("WhatsApp: Tag & Reply", "Bot hanya merespon saat di-tag atau di-reply di grup"),
    ("WhatsApp: /all", "Tag semua anggota grup sekaligus"),
    ("WhatsApp: /reset", "Reset riwayat percakapan"),
    ("Dark Mode UI", "Tampilan modern gelap yang responsif di semua layar"),
]
for name, desc in features:
    story.append(Table([[
        Paragraph(f"<b>{name}</b>", ParagraphStyle("fn", fontSize=10,
            textColor=PURPLE, fontName="Helvetica-Bold")),
        Paragraph(desc, ParagraphStyle("fd", fontSize=10,
            textColor=DARK, fontName="Helvetica")),
    ]], colWidths=[5*cm, 12*cm],
    style=TableStyle([
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
    ])))

# ── BAGIAN 5 ───────────────────────────────────────────────────────────────
story += section("5. Struktur Proyek")
story.append(code(
    "my-ai/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;main.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    "# Backend FastAPI + AI logic<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;requirements.txt&nbsp;&nbsp;&nbsp;# Python dependencies<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;.env&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    "# API Keys (rahasia!)<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;frontend/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index.html&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Halaman chat<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;style.css&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Tampilan dark mode<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;script.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Logika chat + streaming<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;whatsapp/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bot.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# WhatsApp bot<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;package.json&nbsp;&nbsp;&nbsp;# Node dependencies<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;desktop/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;main.js&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Electron entry point<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;package.json&nbsp;&nbsp;&nbsp;# Electron config"
))

# ── BAGIAN 6 ───────────────────────────────────────────────────────────────
story += section("6. API Keys")
keys = [
    ["ANTHROPIC_API_KEY", "Claude AI", "Berbayar (kredit)", "console.anthropic.com"],
    ["GROQ_API_KEY", "Llama 3.1 via Groq", "Gratis (14.400/hari)", "console.groq.com"],
]
key_table = Table([["Environment Variable", "Untuk", "Biaya", "Daftar di"]] + keys,
    colWidths=[5*cm, 4*cm, 3.5*cm, 4.5*cm])
key_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE),
    ("TEXTCOLOR", (0,0), (-1,0), WHITE),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("TEXTCOLOR", (0,1), (0,-1), PURPLE),
    ("TEXTCOLOR", (1,1), (-1,-1), DARK),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [PURPLE_LIGHT, WHITE]),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
]))
story.append(key_table)
story.append(Spacer(1, 0.2*cm))
story.append(body("<b>Penting:</b> Jangan pernah share file .env atau API key ke siapapun!"))

# ── BAGIAN 7 ───────────────────────────────────────────────────────────────
story += section("7. Cara Menjalankan")
steps = [
    ("1", "Jalankan Backend", "cd D:\\Claude\\my-ai\npython -m uvicorn main:app --reload"),
    ("2", "Buka Website", "Buka browser → http://localhost:8000"),
    ("3", "Jalankan WhatsApp Bot", "cd D:\\Claude\\my-ai\\whatsapp\nnode bot.js"),
    ("4", "Jalankan Desktop App", "cd D:\\Claude\\my-ai\\desktop\nnpm install && npm start"),
]
for num, title, cmd in steps:
    story.append(Table([[
        Paragraph(num, ParagraphStyle("sn", fontSize=14, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b><br/>"
            f"<font name='Courier' size='9'>{cmd.replace(chr(10), '<br/>')}</font>",
            ParagraphStyle("sc", fontSize=10, textColor=DARK,
            fontName="Helvetica", leading=16)),
    ]], colWidths=[1.2*cm, 15.8*cm],
    style=TableStyle([
        ("BACKGROUND", (0,0), (0,-1), PURPLE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (1,0), (1,-1), 12),
        ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#e5e7eb")),
    ])))
    story.append(Spacer(1, 0.15*cm))

# ── BAGIAN 8 ───────────────────────────────────────────────────────────────
story += section("8. Rencana Pengembangan")
roadmap = [
    ("Jangka Pendek", [
        "Deploy ke server publik (Railway / Render / VPS)",
        "Tambahkan ke portofolio JerrelAdriel.github.io",
    ]),
    ("Jangka Menengah", [
        "Fine-tune model open-source (LLaMA / Mistral) dengan data pribadi",
        "Tambah fitur memori jangka panjang menggunakan RAG",
        "Integrasi dengan tools (web search, kalender, dll)",
    ]),
    ("Jangka Panjang", [
        "Bangun model AI sendiri dari nol",
        "Deploy sebagai produk SaaS",
    ]),
]
for phase, items in roadmap:
    story.append(Paragraph(f"<b>{phase}</b>",
        ParagraphStyle("rp", fontSize=11, textColor=PURPLE,
        fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)))
    for item in items:
        story.append(bullet(item))

# ── FOOTER ─────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="100%", thickness=1, color=PURPLE))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Agent-JR Documentation v1.0 &nbsp;|&nbsp; Jerrel Adriel &nbsp;|&nbsp; 28 Mei 2026",
    small_style))

doc.build(story)
print(f"PDF berhasil dibuat: {OUTPUT}")
