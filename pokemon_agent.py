import os
from google import genai

_DIFFICULTY_INSTRUCTIONS = {
    "Easy": (
        "Make these hints VERY OBVIOUS. Directly reference the Pokemon's most recognizable "
        "features: its iconic appearance, well-known signature moves, or famous pop-culture "
        "moments. Even a casual fan should solve it within the first few hints."
    ),
    "Medium": (
        "Make these hints moderately challenging. Use descriptive metaphors and indirect "
        "references to the Pokemon's traits, types, or lore. Require some Pokemon knowledge "
        "but avoid being obscure."
    ),
    "Hard": (
        "Make these hints VERY CRYPTIC and poetic. Use abstract metaphors, mythological "
        "allusions, and only the most obscure characteristics. Never mention types directly. "
        "Only a dedicated Pokemon master should crack these riddles."
    ),
}


def generate_hints(pokemon: dict, difficulty: str, num_hints: int) -> list[str]:
    """
    Use Gemini gemma-3-1b-it to generate `num_hints` riddle hints for the given Pokemon.
    Hints progress from most cryptic (index 0) to most obvious (index -1).
    """
    api_key = os.environ.get("GOOGLE_API_KEY") or _streamlit_secret()
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Set it as an environment variable "
            "or add it to your Streamlit secrets (.streamlit/secrets.toml)."
        )

    client = genai.Client(api_key=api_key)
    instruction = _DIFFICULTY_INSTRUCTIONS.get(difficulty, _DIFFICULTY_INSTRUCTIONS["Medium"])

    prompt = f"""You are a riddle-master hosting a Pokemon guessing game.

SECRET POKEMON DATA:
{_format_context(pokemon)}

DIFFICULTY: {difficulty}
{instruction}

Generate exactly {num_hints} hints. Hint 1 must be the MOST cryptic/vague; hint {num_hints} must be the MOST obvious.
Rules:
- NEVER mention the Pokemon's name.
- Each hint is 1-2 sentences only.
- No numbering, no bullet points, no blank lines.
- Return ONLY the hints, one per line."""

    response = client.models.generate_content(model="gemma-3-1b-it", contents=prompt)
    raw = response.text.strip()
    hints = [line.strip() for line in raw.splitlines() if line.strip()]
    return hints[:num_hints]


def _format_context(p: dict) -> str:
    stats_str = ", ".join(f"{k}: {v}" for k, v in p.get("stats", {}).items())
    abilities = ", ".join(p.get("abilities", []))
    hidden = p.get("hidden_ability") or "None"
    if p.get("is_legendary"):
        status = "Legendary"
    elif p.get("is_mythical"):
        status = "Mythical"
    else:
        status = "Regular"

    return (
        f"Type(s): {', '.join(p['types'])}\n"
        f"Abilities: {abilities}\n"
        f"Hidden Ability: {hidden}\n"
        f"Height: {p['height_m']:.1f}m  Weight: {p['weight_kg']:.1f}kg\n"
        f"Generation: {p['generation']}\n"
        f"Color: {p['color']}  Shape: {p['shape']}  Habitat: {p['habitat']}\n"
        f"Status: {status}\n"
        f"Base Stats: {stats_str}\n"
        f"Pokedex Entry: {p['pokedex_entry']}"
    )


def _streamlit_secret() -> str | None:
    try:
        import streamlit as st
        return st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        return None
