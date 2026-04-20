import streamlit as st

_CSS = """
<style>
[data-testid="metric-container"] {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 16px;
}
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}
.hint-card {
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
    border-left: 4px solid;
    line-height: 1.6;
}
.result-banner {
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 16px 0;
}
.guess-row {
    padding: 6px 2px;
    border-bottom: 1px solid #21262d;
    font-size: 0.9rem;
}
</style>
"""

IDLE_CARD = """
<div style="border:1px solid #30363d;border-radius:12px;padding:28px;
            text-align:center;background:#1c2128;margin:16px 0;">
    <div style="font-size:2.5rem;">🎮</div>
    <div style="font-size:1.15rem;font-weight:700;color:#e6edf3;margin:10px 0 6px;">
        Ready to Play?
    </div>
    <div style="color:#8b949e;font-size:0.9rem;line-height:1.6;">
        Pick a difficulty and press <strong style="color:#58a6ff;">New Game</strong> to begin.<br>
        A random Pokémon will be selected and Gemini AI will craft custom riddle hints.
    </div>
</div>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hint_html(index: int, total: int, text: str) -> str:
    """Return a styled hint card. Color shifts purple → yellow → green as hints get more obvious."""
    progress = index / max(total - 1, 1)
    if progress < 0.4:
        color, bg = "#bc8cff", "rgba(188,140,255,0.08)"
    elif progress < 0.75:
        color, bg = "#e3b341", "rgba(227,179,65,0.08)"
    else:
        color, bg = "#3fb950", "rgba(63,185,80,0.08)"
    return (
        f'<div class="hint-card" style="border-left-color:{color};background:{bg};">'
        f'<span style="color:{color};font-weight:700;font-size:0.78rem;'
        f'text-transform:uppercase;letter-spacing:0.06em;">Hint {index + 1}</span>'
        f'<div style="color:#e6edf3;margin-top:5px;">{text}</div></div>'
    )


def number_hint_html(message: str) -> str:
    """Styled feedback card for the number guesser (too high / too low)."""
    return (
        f'<div class="hint-card" style="border-left-color:#e3b341;background:rgba(227,179,65,0.08);">'
        f'<span style="color:#e3b341;font-weight:700;font-size:0.78rem;'
        f'text-transform:uppercase;letter-spacing:0.06em;">Hint</span>'
        f'<div style="color:#e6edf3;margin-top:5px;">{message}</div></div>'
    )


def banner(text: str, win: bool) -> str:
    """Win (green) or loss (red) result banner."""
    if win:
        border, bg, color, icon = "#2ea043", "rgba(46,160,67,0.12)", "#3fb950", "🏆"
    else:
        border, bg, color, icon = "#f85149", "rgba(248,81,73,0.12)", "#f85149", "💀"
    return (
        f'<div class="result-banner" style="border:1px solid {border};background:{bg};">'
        f'<div style="font-size:1.3rem;font-weight:800;color:{color};">{icon} {text}</div></div>'
    )


def guess_row_html(index: int, guess: str, correct: bool) -> str:
    icon = "✅" if correct else "❌"
    return f'<div class="guess-row">{index}. {icon} {guess}</div>'
