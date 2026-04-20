import os
import pytest
from unittest.mock import MagicMock, patch
from pokemon_agent import generate_hints, _validate_and_fix_hints
from pokemon_utils import check_pokemon_guess
from logic_utils import check_guess

## GUESS NUMBER GAME AUTOMATED TESTS
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📈 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📉 Go HIGHER!")

def test_guess_edge_case_high():
    # If secret is 50 and guess is 51, hint should be "Too High"
    result = check_guess(51, 50)
    assert result == ("Too High", "📈 Go LOWER!")

def test_guess_edge_case_low():
    # If secret is 50 and guess is 49, hint should be "Too Low"
    result = check_guess(49, 50)
    assert result == ("Too Low", "📉 Go HIGHER!")

## GUESS POKE GAME AUTOMATED TESTS

_PIKACHU = {
    "name": "pikachu",
    "display_name": "Pikachu",
    "id": 25,
    "types": ["electric"],
    "abilities": ["static"],
    "hidden_ability": "lightning rod",
    "height_m": 0.4,
    "weight_kg": 6.0,
    "base_experience": 112,
    "stats": {
        "hp": 35, "attack": 55, "defense": 40,
        "special-attack": 50, "special-defense": 50, "speed": 90,
    },
    "pokedex_entry": "When several of these Pokemon gather, their electricity can cause lightning storms.",
    "generation": "I",
    "color": "yellow",
    "shape": "quadruped",
    "habitat": "forest",
    "is_legendary": False,
    "is_mythical": False,
}

def _mock_client(text: str):
    mock_resp = MagicMock()
    mock_resp.text = text
    client = MagicMock()
    client.models.generate_content.return_value = mock_resp
    return client

# --- generate_hints ---

def test_generate_hints_correct_count():
    # Both the generation and validation calls return 3 lines
    with patch("pokemon_agent.genai.Client") as MockClient, \
         patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        MockClient.return_value = _mock_client("Hint one\nHint two\nHint three")
        hints = generate_hints(_PIKACHU, "Easy", 3)
    assert len(hints) == 3

def test_generate_hints_returns_non_empty_strings():
    with patch("pokemon_agent.genai.Client") as MockClient, \
         patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        MockClient.return_value = _mock_client("Crackles with power\nSmall and fast\nA yellow mouse")
        hints = generate_hints(_PIKACHU, "Easy", 3)
    assert all(isinstance(h, str) and h.strip() for h in hints)

def test_generate_hints_excludes_pokemon_name():
    with patch("pokemon_agent.genai.Client") as MockClient, \
         patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}):
        MockClient.return_value = _mock_client("It generates electricity\nSmall yellow creature\nFound in the forest")
        hints = generate_hints(_PIKACHU, "Easy", 3)
    for hint in hints:
        assert "pikachu" not in hint.lower()

def test_generate_hints_raises_without_api_key():
    with patch.dict(os.environ, {}, clear=True), \
         patch("pokemon_agent._streamlit_secret", return_value=None):
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            generate_hints(_PIKACHU, "Easy", 3)


# --- _validate_and_fix_hints (guardrail) ---

def test_guardrail_returns_corrected_hints():
    originals = ["Cryptic hint", "Moderate hint", "Obvious hint"]
    corrected = ["Fixed cryptic hint", "Fixed moderate hint", "Fixed obvious hint"]
    result = _validate_and_fix_hints(_mock_client("\n".join(corrected)), _PIKACHU, "Medium", originals)
    assert result == corrected

def test_guardrail_fallback_on_count_mismatch():
    # If the model returns fewer lines than expected, originals are preserved
    originals = ["Hint A", "Hint B", "Hint C"]
    result = _validate_and_fix_hints(_mock_client("Only one line"), _PIKACHU, "Hard", originals)
    assert result == originals

def test_guardrail_preserves_accurate_hints():
    accurate = ["It crackles with electric power", "Small and quick", "A yellow mouse Pokemon"]
    result = _validate_and_fix_hints(_mock_client("\n".join(accurate)), _PIKACHU, "Easy", accurate)
    assert len(result) == len(accurate)


# --- check_pokemon_guess (name matching) ---

def test_guess_exact_match():
    assert check_pokemon_guess("pikachu", "pikachu")

def test_guess_case_insensitive():
    assert check_pokemon_guess("Pikachu", "pikachu")

def test_guess_hyphen_vs_space():
    assert check_pokemon_guess("Mr Mime", "mr-mime")

def test_guess_wrong_pokemon():
    assert not check_pokemon_guess("bulbasaur", "pikachu")