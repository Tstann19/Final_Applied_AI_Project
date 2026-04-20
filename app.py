import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
from pokemon_utils import fetch_random_pokemon, check_pokemon_guess
from pokemon_agent import generate_hints

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

tab1, tab2 = st.tabs(["🔢 Number Guesser", "🎮 Pokemon Guesser"])

# ── Tab 1: Number Guesser (original game) ──────────────────────────────────
with tab1:
    col_diff, col_info = st.columns([2, 1])
    with col_diff:
        difficulty = st.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1, key="num_difficulty")

    attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
    attempt_limit = attempt_limit_map[difficulty]
    low, high = get_range_for_difficulty(difficulty)

    with col_info:
        st.write("")
        st.caption(f"Range: {low}–{high}  |  Attempts: {attempt_limit}")

    if "secret" not in st.session_state:
        st.session_state.secret = random.randint(low, high)
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "status" not in st.session_state:
        st.session_state.status = "playing"
    if "history" not in st.session_state:
        st.session_state.history = []

    st.subheader("Make a guess")
    st.caption(f"Guess a number between {low} and {high}.")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Attempts Used", st.session_state.attempts)
    col_b.metric("Attempts Left", max(0, attempt_limit - st.session_state.attempts))
    col_c.metric("Score", st.session_state.score)

    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

    raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess 🚀")
    with col2:
        new_game = st.button("New Game 🔁")
    with col3:
        show_hint = st.checkbox("Show hint", value=True)

    if new_game:
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.status = "playing"
        st.session_state.history = []
        st.session_state.score = 0
        st.success("New game started.")
        st.rerun()

    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    elif st.session_state.status == "lost":
        st.error("Game over. Start a new game to try again.")
    else:
        if submit:
            ok, guess_int, err = parse_guess(raw_guess, low, high)

            if not ok:
                st.error(err)
            else:
                st.session_state.attempts += 1
                st.session_state.history.append(guess_int)

                if st.session_state.attempts % 2 == 0:
                    secret = st.session_state.secret
                else:
                    secret = st.session_state.secret

                outcome, message = check_guess(guess_int, secret)

                if show_hint:
                    st.warning(message)

                st.session_state.score = update_score(
                    current_score=st.session_state.score,
                    outcome=outcome,
                    attempt_number=st.session_state.attempts,
                )

                if outcome == "Win":
                    st.balloons()
                    st.session_state.status = "won"
                    st.success(
                        f"You won! The secret was {st.session_state.secret}. "
                    )
                else:
                    if st.session_state.attempts >= attempt_limit:
                        st.session_state.status = "lost"
                        st.error(
                            f"Out of attempts! "
                            f"The secret was {st.session_state.secret}. "
                            f"Score: {st.session_state.score}"
                        )

    st.divider()
    st.caption("Built by an AI that claims this code is production-ready.")

# ── Tab 2: Pokemon Guesser ──────────────────────────────────────────────────
with tab2:
    POKE_ATTEMPT_LIMITS = {"Easy": 10, "Medium": 7, "Hard": 5}

    st.subheader("Who's That Pokemon? 🎮")
    st.caption(
        "A secret Pokemon has been chosen. Use the AI-generated riddle hints to identify it! "
    )

    for _key, _default in [
        ("poke_status", "idle"),
        ("poke_pokemon", None),
        ("poke_hints", []),
        ("poke_attempts", 0),
        ("poke_history", []),
        ("poke_score", 0),
        ("poke_difficulty", "Easy"),
    ]:
        if _key not in st.session_state:
            st.session_state[_key] = _default

    col_diff, col_btn = st.columns([2, 1])
    with col_diff:
        poke_difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            help=(
                "Easy = 12 guesses, obvious hints  |  "
                "Medium = 8 guesses, moderate riddles  |  "
                "Hard = 5 guesses, cryptic riddles"
            ),
            key="poke_diff_select",
        )
    with col_btn:
        st.write("")
        start_game = st.button("New Game 🎲", key="poke_start")

    if start_game:
        attempt_limit_pk = POKE_ATTEMPT_LIMITS[poke_difficulty]
        with st.spinner("Summoning a secret Pokemon and crafting riddles..."):
            pokemon = fetch_random_pokemon()
            if pokemon is None:
                st.error(
                    "Could not reach PokeAPI. Check your internet connection and try again."
                )
            else:
                try:
                    hints = generate_hints(pokemon, poke_difficulty, attempt_limit_pk)
                    st.session_state.poke_pokemon = pokemon
                    st.session_state.poke_hints = hints
                    st.session_state.poke_attempts = 0
                    st.session_state.poke_history = []
                    st.session_state.poke_score = 0
                    st.session_state.poke_status = "playing"
                    st.session_state.poke_difficulty = poke_difficulty
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    if st.session_state.poke_status == "idle":
        st.info(
            "Press **New Game** to begin! A random Pokemon will be fetched from PokeAPI "
            "and Gemini AI will generate custom riddle hints scaled to your chosen difficulty."
        )
    else:
        pokemon = st.session_state.poke_pokemon
        hints = st.session_state.poke_hints
        diff_used = st.session_state.poke_difficulty
        attempt_limit_pk = POKE_ATTEMPT_LIMITS[diff_used]
        attempts_used = st.session_state.poke_attempts

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Attempts Used", attempts_used)
        col_b.metric("Attempts Left", max(0, attempt_limit_pk - attempts_used))
        col_c.metric("Score", st.session_state.poke_score)

        with st.expander("Developer Debug Info"):
            st.write("Secret:", pokemon["display_name"])
            st.write("ID:", pokemon["id"])
            st.write("Types:", pokemon["types"])
            st.write("Attempts:", attempts_used)
            st.write("Score:", st.session_state.poke_score)
            st.write("Difficulty:", diff_used)
            st.write("History:", st.session_state.poke_history)

        st.subheader("Riddle Hints")
        num_revealed = min(attempts_used + 1, len(hints))
        for i in range(num_revealed):
            st.info(f"**Hint {i + 1}:** {hints[i]}")

        if st.session_state.poke_status == "won":
            st.balloons()
            st.success(
                f"Correct! The secret Pokemon was **{pokemon['display_name']}** "
                #f"(#{pokemon['id']})!  Final score: **{st.session_state.poke_score}**"
            )
        elif st.session_state.poke_status == "lost":
            st.error(
                f"No guesses left! The secret Pokemon was "
                f"**{pokemon['display_name']}** (#{pokemon['id']})."
            )
        else:
            poke_guess = st.text_input(
                "Who's that Pokemon?",
                placeholder="e.g. Pikachu",
                key="poke_guess_input",
            )
            if st.button("Submit Guess 🎯", key="poke_submit_guess"):
                if not poke_guess.strip():
                    st.warning("Type a Pokemon name before submitting!")
                else:
                    st.session_state.poke_attempts += 1
                    st.session_state.poke_history.append(poke_guess.strip())

                    if check_pokemon_guess(poke_guess, pokemon["name"]):
                        pts = max(10, 100 - 10 * st.session_state.poke_attempts)
                        st.session_state.poke_score += pts
                        st.session_state.poke_status = "won"
                    else:
                        st.session_state.poke_score = max(
                            st.session_state.poke_score - 5, 0
                        )
                        if st.session_state.poke_attempts >= attempt_limit_pk:
                            st.session_state.poke_status = "lost"
                    st.rerun()

        if st.session_state.poke_history:
            with st.expander(f"Guess history ({len(st.session_state.poke_history)})"):
                for i, g in enumerate(st.session_state.poke_history, 1):
                    icon = "✅" if check_pokemon_guess(g, pokemon["name"]) else "❌"
                    st.write(f"{i}. {icon} {g}")

    st.divider()
    st.caption("Pokemon data from PokeAPI · Hints powered by Gemini AI")
