import random
import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2"
TOTAL_POKEMON = 1025  # Generations 1-9


def fetch_random_pokemon() -> dict | None:
    pokemon_id = random.randint(1, TOTAL_POKEMON)
    return _fetch_by_id(pokemon_id)


def _fetch_by_id(pokemon_id: int) -> dict | None:
    try:
        poke_resp = requests.get(f"{POKEAPI_BASE}/pokemon/{pokemon_id}", timeout=10)
        poke_resp.raise_for_status()

        species_resp = requests.get(
            f"{POKEAPI_BASE}/pokemon-species/{pokemon_id}", timeout=10
        )
        species_resp.raise_for_status()

        return _build_profile(poke_resp.json(), species_resp.json())
    except requests.RequestException:
        return None


def _build_profile(poke: dict, species: dict) -> dict:
    types = [t["type"]["name"] for t in poke["types"]]

    abilities = [
        a["ability"]["name"].replace("-", " ")
        for a in poke["abilities"]
        if not a["is_hidden"]
    ]
    hidden_ability = next(
        (
            a["ability"]["name"].replace("-", " ")
            for a in poke["abilities"]
            if a["is_hidden"]
        ),
        None,
    )

    stats = {s["stat"]["name"]: s["base_stat"] for s in poke["stats"]}

    en_flavors = [
        f["flavor_text"].replace("\n", " ").replace("\f", " ")
        for f in species["flavor_text_entries"]
        if f["language"]["name"] == "en"
    ]
    pokedex_entry = en_flavors[0] if en_flavors else "No description available."

    generation = species["generation"]["name"].replace("generation-", "").upper()
    color = (species.get("color") or {}).get("name", "unknown")
    shape = (species.get("shape") or {}).get("name", "unknown")
    habitat = (species.get("habitat") or {}).get("name", "unknown")

    display_name = poke["name"].replace("-", " ").title()

    return {
        "name": poke["name"],          # raw API name — lowercase, hyphenated
        "display_name": display_name,
        "id": poke["id"],
        "types": types,
        "abilities": abilities,
        "hidden_ability": hidden_ability,
        "height_m": poke["height"] / 10,
        "weight_kg": poke["weight"] / 10,
        "base_experience": poke["base_experience"],
        "stats": stats,
        "pokedex_entry": pokedex_entry,
        "generation": generation,
        "color": color,
        "shape": shape,
        "habitat": habitat,
        "is_legendary": species["is_legendary"],
        "is_mythical": species["is_mythical"],
    }


def check_pokemon_guess(guess: str, secret_name: str) -> bool:
    def normalize(s: str) -> str:
        return s.strip().lower().replace("-", " ").replace(".", "").replace("'", "")

    return normalize(guess) == normalize(secret_name)
