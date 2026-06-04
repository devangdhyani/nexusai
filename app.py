import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from src.agent.graph import build_agent, run_agent

# .env now lives at the project root alongside app.py
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexusAI — Autonomous Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800;0,14..32,900&display=swap');

/* ── RESET ─────────────────────────────────────────────────────────────── */
*, *::before, *::after {
    box-sizing: border-box;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"],
[data-testid="stStatusWidget"],
.stDeployButton,
[data-testid="collapsedControl"] { display: none !important; }

/* ── APP BASE ───────────────────────────────────────────────────────────── */
.stApp {
    background: #050816 !important;
    min-height: 100vh;
    overflow-x: hidden;
}
.block-container,
.stMainBlockContainer,
[data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── SCROLLBAR ──────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #8B5CF6 0%, #06B6D4 100%);
    border-radius: 99px;
}

/* ══════════════════════════════════════════════════════════════════════════
   BACKGROUND AURORA SYSTEM
══════════════════════════════════════════════════════════════════════════ */
.nexus-bg {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.aurora { position: absolute; border-radius: 50%; filter: blur(80px); }
.a1 {
    width: 900px; height: 900px;
    background: radial-gradient(circle, rgba(139,92,246,0.22) 0%, transparent 70%);
    top: -280px; left: -200px;
    animation: a-drift1 12s ease-in-out infinite alternate;
}
.a2 {
    width: 750px; height: 750px;
    background: radial-gradient(circle, rgba(6,182,212,0.16) 0%, transparent 70%);
    bottom: -200px; right: -180px;
    animation: a-drift2 15s ease-in-out infinite alternate;
}
.a3 {
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(236,72,153,0.1) 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    animation: a-drift3 9s ease-in-out infinite alternate;
    filter: blur(100px);
}
.a4 {
    width: 350px; height: 200px;
    background: radial-gradient(ellipse, rgba(139,92,246,0.09) 0%, transparent 70%);
    bottom: 25%; left: 20%;
    animation: a-drift4 11s ease-in-out infinite alternate;
}
.noise {
    position: absolute;
    inset: 0;
    opacity: 0.028;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n' x='0' y='0'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 300px 300px;
}
/* Floating decorative blobs */
.blob {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    animation: blob-float 6s ease-in-out infinite;
}
.blob-1 {
    width: 8px; height: 8px;
    background: rgba(139,92,246,0.5);
    box-shadow: 0 0 12px rgba(139,92,246,0.8);
    top: 20%; left: 15%;
    animation-delay: 0s;
}
.blob-2 {
    width: 5px; height: 5px;
    background: rgba(6,182,212,0.5);
    box-shadow: 0 0 10px rgba(6,182,212,0.8);
    top: 35%; right: 20%;
    animation-delay: -2s;
}
.blob-3 {
    width: 6px; height: 6px;
    background: rgba(236,72,153,0.5);
    box-shadow: 0 0 10px rgba(236,72,153,0.8);
    bottom: 30%; left: 25%;
    animation-delay: -4s;
}
.blob-4 {
    width: 4px; height: 4px;
    background: rgba(16,185,129,0.5);
    box-shadow: 0 0 8px rgba(16,185,129,0.8);
    top: 70%; right: 15%;
    animation-delay: -1s;
}

/* ══════════════════════════════════════════════════════════════════════════
   NAVBAR
══════════════════════════════════════════════════════════════════════════ */
.nexus-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 40px;
    max-width: 1100px;
    margin: 0 auto;
    position: relative;
    z-index: 100;
}
.nav-wordmark {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nav-right { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.nbadge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 11px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    border: 1px solid;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
.nb-online {
    background: rgba(16,185,129,0.07);
    border-color: rgba(16,185,129,0.2);
    color: #34d399;
}
.nb-online::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 6px #10B981;
    display: inline-block;
    animation: dot-pulse 2s ease-in-out infinite;
}
.nb-tech {
    background: rgba(139,92,246,0.06);
    border-color: rgba(139,92,246,0.18);
    color: #a78bfa;
}
.nb-ver {
    background: rgba(6,182,212,0.06);
    border-color: rgba(6,182,212,0.18);
    color: #38bdf8;
}

/* ══════════════════════════════════════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════════════════════════════════════ */
.nexus-hero {
    text-align: center !important;
    padding: 10px 20px 8px;
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* ── ORB ─────────────────────────────────────────────────────────────── */
.orb-wrap {
    width: 160px; height: 160px;
    position: relative;
    margin: 0 auto 36px;
    animation: fadeInUp 0.8s ease 0.1s both;
    overflow: visible;
}
.orb-glow {
    position: absolute;
    inset: -40px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 65%);
    animation: orb-pulse 3s ease-in-out infinite;
    filter: blur(25px);
}
.orb-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 1px solid transparent;
    transform-origin: center center;
}
.ring-1 {
    inset: -22px;
    border-color: rgba(139,92,246,0.28);
    animation: spin-cw 9s linear infinite;
    box-shadow: 0 0 8px rgba(139,92,246,0.1);
}
.ring-2 {
    inset: -10px;
    border-style: dashed;
    border-color: rgba(6,182,212,0.32);
    animation: spin-ccw 6s linear infinite;
}
.ring-3 {
    inset: -38px;
    border-color: rgba(236,72,153,0.14);
    animation: spin-cw 14s linear infinite reverse;
}
.orb-sphere {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(from 180deg, #8B5CF6, #06B6D4, #EC4899, #8B5CF6);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.1),
        0 0 40px rgba(139,92,246,0.55),
        0 0 80px rgba(139,92,246,0.28),
        0 0 120px rgba(6,182,212,0.18);
    animation: orb-pulse 3s ease-in-out infinite, spin-cw 20s linear infinite;
    display: flex;
    align-items: center;
    justify-content: center;
}
.orb-gloss {
    width: 60%;
    height: 60%;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 28%, rgba(255,255,255,0.35), rgba(255,255,255,0.04) 55%, transparent);
}
/* Orbiting particles */
.orb-p {
    position: absolute;
    width: 5px; height: 5px;
    border-radius: 50%;
    top: 50%; left: 50%;
}
.p1 {
    background: #06B6D4;
    box-shadow: 0 0 8px #06B6D4, 0 0 16px rgba(6,182,212,0.5);
    animation: orbit 4.5s linear infinite;
}
.p2 {
    background: #EC4899;
    box-shadow: 0 0 8px #EC4899, 0 0 16px rgba(236,72,153,0.5);
    animation: orbit 4.5s linear infinite;
    animation-delay: -1.5s;
}
.p3 {
    background: #8B5CF6;
    box-shadow: 0 0 8px #8B5CF6, 0 0 16px rgba(139,92,246,0.5);
    animation: orbit 4.5s linear infinite;
    animation-delay: -3s;
}

/* ── HERO TEXT ──────────────────────────────────────────────────────── */
.hero-eyebrow {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a78bfa;
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 999px;
    padding: 4px 14px;
    margin-bottom: 22px;
    animation: fadeInUp 0.7s ease both;
}
.hero-h1 {
    font-size: clamp(2.2rem, 5.5vw, 3.8rem);
    font-weight: 900;
    letter-spacing: -0.04em;
    line-height: 1.05;
    margin: 0 0 20px;
    background: linear-gradient(135deg,
        #ffffff 0%,
        #e2e8f0 20%,
        #a78bfa 50%,
        #38bdf8 75%,
        #f472b6 100%
    );
    background-size: 250% 250%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-pan 8s ease-in-out infinite alternate, fadeInUp 0.8s ease 0.1s both;
}
.hero-sub {
    font-size: clamp(0.9rem, 2vw, 1.05rem);
    color: #94A3B8;
    font-weight: 400;
    line-height: 1.65;
    max-width: 500px;
    margin: 0 auto 44px;
    text-align: center !important;
    display: block;
    animation: fadeInUp 0.8s ease 0.2s both;
}

/* ── SUGGESTION CARDS ─────────────────────────────────────────────── */
.scard-row {
    max-width: 820px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
    z-index: 10;
}

/* Suggestion card buttons — Streamlit st.columns renders outside any wrapping div
   so we target the horizontal block directly. This is the only horizontal block
   with buttons in the entire app, so there is no selector conflict. */
[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
    position: relative;
    z-index: 10;
}
[data-testid="stHorizontalBlock"] .stButton button {
    background: rgba(255,255,255,0.032) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 18px !important;
    color: #cbd5e1 !important;
    padding: 18px 14px !important;
    height: auto !important;
    min-height: 90px !important;
    font-size: 0.8rem !important;
    line-height: 1.55 !important;
    text-align: left !important;
    white-space: pre-line !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: none !important;
    width: 100% !important;
}
[data-testid="stHorizontalBlock"] .stButton button:hover {
    transform: translateY(-5px) scale(1.01) !important;
    background: rgba(139,92,246,0.08) !important;
    border-color: rgba(139,92,246,0.32) !important;
    box-shadow: 0 16px 40px rgba(139,92,246,0.2),
                0 0 0 1px rgba(139,92,246,0.08) !important;
    color: #f1f5f9 !important;
}
[data-testid="stHorizontalBlock"] .stButton button:active {
    transform: translateY(-2px) scale(0.99) !important;
}

/* ── CHAT MODE COMPACT HEADER ────────────────────────────────────── */
.nexus-compact {
    text-align: center;
    padding: 22px 0 12px;
    position: relative;
    z-index: 10;
}
.compact-logo {
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.compact-line {
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.5), transparent);
    margin: 0 auto;
    border-radius: 99px;
}

/* ══════════════════════════════════════════════════════════════════════════
   CHAT MESSAGES
   Streamlit 1.36 DOM: stChatMessage > chatAvatarIcon-* + stChatMessageContent
   Native layout: display:flex, align-items:flex-start, gap:0.5rem
   Avatar (An): width:2rem, height:2rem, flex-shrink:0
   Content (zn): flex-grow:1, min-width:0, margin:auto
══════════════════════════════════════════════════════════════════════════ */

/* Outer row
   KEY FIX: native Streamlit adds backgroundColor to this container for user messages
   (gray90 at 50% alpha in dark mode) which made it look like the avatar was INSIDE
   the bubble. Setting it transparent makes avatar+bubble visually separate. */
[data-testid="stChatMessage"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: flex-start !important;
    gap: 14px !important;
    max-width: 800px !important;
    width: 100% !important;
    margin: 6px auto !important;
    padding: 6px 20px !important;
    box-sizing: border-box !important;
    position: static !important;
    z-index: auto !important;
    background: transparent !important;       /* ← removes native gray box around avatar */
    background-color: transparent !important;
    border-radius: 0 !important;
}

/* ── Avatar icons ────────────────────────────────────────────────────
   Native: borderRadius=t.radii.default (rounded rect), width/height=2rem
   Fix: force circle, hide the icon-name text that shows when Material
   Symbols font doesn't load, ensure it never grows or shrinks        */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-custom"] {
    flex: 0 0 36px !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    min-height: 36px !important;
    max-height: 36px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: static !important;
    overflow: hidden !important;       /* clips icon glyph + prevents text overflow */
    font-size: 0 !important;           /* hides icon-name fallback text ("face","smart_toy") */
    box-shadow: 0 2px 12px rgba(0,0,0,0.35) !important;
    flex-shrink: 0 !important;
    flex-grow: 0 !important;
}
/* Restore icon size for the SVG/span child — only the text fallback gets font-size:0 */
[data-testid="chatAvatarIcon-user"] > *,
[data-testid="chatAvatarIcon-assistant"] > *,
[data-testid="chatAvatarIcon-custom"] > * {
    font-size: 1.1rem !important;
    color: #ffffff !important;
    line-height: 1 !important;
}
/* User avatar: violet gradient */
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #8B5CF6, #6D28D9) !important;
}
/* Assistant avatar: cyan gradient */
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #06B6D4, #0E7490) !important;
}

/* ── Message content bubble ──────────────────────────────────────────── */
[data-testid="stChatMessageContent"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;         /* prevents flex item overflowing its container */
    margin: 0 !important;
    background: rgba(255,255,255,0.028) !important;
    border: 1px solid rgba(255,255,255,0.065) !important;
    border-radius: 18px !important;
    padding: 14px 18px !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
    box-sizing: border-box !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    overflow: hidden !important;
}
[data-testid="stChatMessageContent"] p {
    color: #dde5f0 !important;
    line-height: 1.78 !important;
    font-size: 0.92rem !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessageContent"] p:last-child { margin-bottom: 0 !important; }
[data-testid="stChatMessageContent"] strong { color: #f8fafc !important; font-weight: 600 !important; }
[data-testid="stChatMessageContent"] em { color: #a78bfa !important; font-style: italic; }
[data-testid="stChatMessageContent"] a { color: #38bdf8 !important; text-decoration: underline; text-decoration-color: rgba(56,189,248,0.4); }
[data-testid="stChatMessageContent"] code {
    background: rgba(139,92,246,0.1) !important;
    color: #a78bfa !important;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 0.83em !important;
    border: 1px solid rgba(139,92,246,0.18);
}
[data-testid="stChatMessageContent"] pre {
    background: rgba(0,0,0,0.45) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    overflow-x: auto;
}
[data-testid="stChatMessageContent"] ul,
[data-testid="stChatMessageContent"] ol {
    color: #cbd5e1 !important;
    padding-left: 1.3rem !important;
}
[data-testid="stChatMessageContent"] li { margin-bottom: 5px !important; }
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 {
    color: #f1f5f9 !important;
    letter-spacing: -0.02em;
    margin-top: 1.2rem !important;
}
[data-testid="stChatMessageContent"] blockquote {
    border-left: 3px solid rgba(139,92,246,0.5) !important;
    padding-left: 14px !important;
    color: #94a3b8 !important;
    font-style: italic;
    margin: 10px 0 !important;
}

/* User message — subtle violet tint (matches user avatar gradient) */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: rgba(139,92,246,0.055) !important;
    border-color: rgba(139,92,246,0.16) !important;
}
/* Assistant message — subtle cyan tint (matches assistant avatar gradient) */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
    background: rgba(6,182,212,0.04) !important;
    border-color: rgba(6,182,212,0.12) !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   CHAT INPUT
══════════════════════════════════════════════════════════════════════════ */

/* Override Streamlit's CSS variables so internal components inherit dark bg */
:root {
    --background-color: #050816;
    --secondary-background-color: #0d1b3e;
}

/* ── Sticky bottom bar — nuke every level of Streamlit's white bg ─────── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] > div > div,
[data-testid="stBottom"] > section,
[data-testid="stBottom"] > section > div,
[data-testid="stBottom"] section[tabindex],
.stBottom, .stBottom > div {
    background: #050816 !important;
    background-color: #050816 !important;
    background-image: none !important;
    border-top: 1px solid rgba(255,255,255,0.04) !important;
}
[data-testid="stBottom"] {
    padding: 14px 0 26px !important;
    z-index: 50;
}

/* ── Chat input outer shell — solid dark navy ────────────────────────── */
[data-testid="stChatInput"] {
    background: #0d1b3e !important;
    background-color: #0d1b3e !important;
    border: 1px solid rgba(139,92,246,0.35) !important;
    border-radius: 26px !important;
    max-width: 820px !important;
    margin: 0 auto !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
    transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
    overflow: hidden !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(139,92,246,0.65) !important;
    box-shadow:
        0 0 0 4px rgba(139,92,246,0.1),
        0 0 40px rgba(139,92,246,0.15),
        0 8px 32px rgba(0,0,0,0.5) !important;
}

/* ── All inner divs — transparent so outer navy shows through ─────────── */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] > div > div > div,
[data-testid="stChatInput"] [data-baseweb],
[data-testid="stChatInput"] [class*="InputContainer"],
[data-testid="stChatInput"] [class*="inputContainer"],
[data-testid="stChatInput"] [class*="Input"],
[data-testid="stChatInput"] [class*="emotion-cache"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* ── Textarea — always white text, never navy ────────────────────────── */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] textarea:hover,
[data-testid="stChatInput"] textarea:active,
[data-testid="stChatInput"] textarea:visited {
    color: #f0f6ff !important;
    -webkit-text-fill-color: #f0f6ff !important;
    font-size: 0.93rem !important;
    background: transparent !important;
    background-color: transparent !important;
    line-height: 1.55 !important;
    caret-color: #a78bfa !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(148,163,184,0.42) !important;
    -webkit-text-fill-color: rgba(148,163,184,0.42) !important;
}
[data-testid="stChatInput"] textarea::selection {
    background: rgba(139,92,246,0.35) !important;
    color: #ffffff !important;
}

/* ── Send button ─────────────────────────────────────────────────────── */
[data-testid="stChatInputSubmitButton"] button {
    background: linear-gradient(135deg, #8B5CF6, #6D28D9) !important;
    border: none !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(139,92,246,0.4) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    background: linear-gradient(135deg, #a78bfa, #8B5CF6) !important;
    box-shadow: 0 6px 20px rgba(139,92,246,0.55) !important;
    transform: scale(1.05) !important;
}

/* ── SPINNER ─────────────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #8B5CF6 !important;
    width: 20px !important;
    height: 20px !important;
}
[data-testid="stSpinner"] p {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   KEYFRAME ANIMATIONS
══════════════════════════════════════════════════════════════════════════ */
@keyframes a-drift1 {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(90px, 70px) scale(1.15); }
}
@keyframes a-drift2 {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(-70px, -50px) scale(1.2); }
}
@keyframes a-drift3 {
    0%   { transform: translate(-50%,-50%) scale(0.9); opacity: 0.7; }
    100% { transform: translate(-50%,-50%) scale(1.3); opacity: 1.0; }
}
@keyframes a-drift4 {
    0%   { transform: translate(0,0); opacity: 0.5; }
    100% { transform: translate(50px,-40px); opacity: 1.0; }
}
@keyframes blob-float {
    0%,100% { transform: translateY(0) scale(1); opacity: 0.7; }
    50%      { transform: translateY(-18px) scale(1.2); opacity: 1; }
}
@keyframes orb-pulse {
    0%,100% { transform: scale(1);    opacity: 1; }
    50%      { transform: scale(1.07); opacity: 0.9; }
}
@keyframes spin-cw {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes spin-ccw {
    from { transform: rotate(0deg); }
    to   { transform: rotate(-360deg); }
}
@keyframes orbit {
    from { transform: translate(-50%,-50%) rotate(0deg) translateX(95px) rotate(0deg); }
    to   { transform: translate(-50%,-50%) rotate(360deg) translateX(95px) rotate(-360deg); }
}
@keyframes gradient-pan {
    0%   { background-position: 0%   50%; }
    100% { background-position: 100% 50%; }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes dot-pulse {
    0%,100% { opacity: 1;   transform: scale(1);   box-shadow: 0 0 6px #10B981; }
    50%      { opacity: 0.5; transform: scale(0.75); box-shadow: 0 0 3px #10B981; }
}
@keyframes shimmer-text {
    0%   { background-position: -200% center; }
    100% { background-position: 200%  center; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FIXED BACKGROUND
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nexus-bg">
  <div class="aurora a1"></div>
  <div class="aurora a2"></div>
  <div class="aurora a3"></div>
  <div class="aurora a4"></div>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
  <div class="blob blob-4"></div>
  <div class="noise"></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CACHED AGENT
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def get_agent():
    return build_agent()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "triggered_prompt" not in st.session_state:
    st.session_state.triggered_prompt = None


# ══════════════════════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nexus-nav">
  <span class="nav-wordmark">⚡ NexusAI</span>
  <div class="nav-right">
    <span class="nbadge nb-online">AI Online</span>
    <span class="nbadge nb-tech">LangGraph · Groq · Tavily</span>
    <span class="nbadge nb-ver">v2.0</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LANDING STATE — hero + orb + cards
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.messages:

    st.markdown("""
    <div class="nexus-hero">

      <!-- Orb -->
      <div class="orb-wrap">
        <div class="orb-glow"></div>
        <div class="orb-ring ring-1"></div>
        <div class="orb-ring ring-2"></div>
        <div class="orb-ring ring-3"></div>
        <div class="orb-sphere">
          <div class="orb-gloss"></div>
        </div>
        <div class="orb-p p1"></div>
        <div class="orb-p p2"></div>
        <div class="orb-p p3"></div>
      </div>

      <!-- Text -->
      <div class="hero-eyebrow">Autonomous AI Research Agent</div>
      <h1 class="hero-h1">The Future of<br>Intelligent Search</h1>
      <p class="hero-sub">
        Search, reason, analyze, and discover insights across the web in real
        time — powered by a ReAct loop that thinks before it answers.
      </p>

    </div>
    """, unsafe_allow_html=True)

    # Suggestion cards
    CARDS = [
        ("🔍", "Latest AI Research",   "Recent breakthroughs\nin AI & ML"),
        ("📊", "Market Trends",         "Tech & startup\nanalysis"),
        ("🌐", "Real-time Web Search",  "Any topic,\nright now"),
        ("🧠", "Explain Concepts",      "Complex ideas\nmade simple"),
    ]
    PROMPTS = [
        "What are the most exciting AI research breakthroughs from the last few months?",
        "Analyze the current AI startup market trends and notable recent developments.",
        "Search the web and tell me what's happening in AI and tech today.",
        "Explain how LangGraph's ReAct loop works in simple, clear terms.",
    ]

    cols = st.columns(4)
    for col, (icon, title, desc), prompt in zip(cols, CARDS, PROMPTS):
        with col:
            label = f"{icon} {title}\n{desc}"
            if st.button(label, key=f"sc_{title}", use_container_width=True):
                st.session_state.triggered_prompt = prompt
                st.rerun()

    # Spacer so content doesn't hide behind the fixed input bar
    st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHAT STATE — compact header
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="nexus-compact">
      <div class="compact-logo">⚡ NexusAI</div>
      <div class="compact-line"></div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MESSAGES
# ══════════════════════════════════════════════════════════════════════════════
_AVATAR = {"user": "🧑‍💻", "assistant": "⚡"}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=_AVATAR.get(msg["role"], "🤖")):
        st.markdown(msg["content"])


# ══════════════════════════════════════════════════════════════════════════════
# INPUT — handles both direct typing AND card-triggered prompts
# ══════════════════════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask NexusAI anything...")

# Resolve prompt source
prompt = st.session_state.triggered_prompt or user_input
if st.session_state.triggered_prompt:
    st.session_state.triggered_prompt = None

if prompt:
    # 1. Persist user message to state first
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Render user bubble
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 3. Run agent — spinner only wraps the computation, NOT the render
    reply = None
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Reasoning..."):
            try:
                agent  = get_agent()
                reply  = run_agent(agent, prompt, st.session_state.messages[:-1])
            except Exception as exc:
                reply = (
                    f"⚠️ **Agent error:** `{exc}`\n\n"
                    "Please verify `GROQ_API_KEY` and `TAVILY_API_KEY` are set in your `.env` file."
                )

        # Render reply OUTSIDE the spinner (but still inside the assistant bubble)
        # so the text is visible before st.rerun() fires
        if reply:
            st.markdown(reply)

    # 4. Always save reply to session state so it survives the rerun
    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # 5. Rerun to trigger landing → chat mode transition (hides the hero)
    st.rerun()
