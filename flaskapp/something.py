"""
Neighbourhood Safety & Social Atmosphere Assessment
--------------------------------------------------
A tidy, script‑style refactor of the original Colab notebook.  
Run it with `python safety_analysis.py` (after placing a `.env` file with
`NVIDIA_API_KEY=<your‑key>` in the same directory or exporting the env var).
"""
from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

###############################################################################
# Configuration
###############################################################################

MODEL_NAME: str = "nvidia/llama-3.3-nemotron-super-49b-v1"
API_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
API_KEY_ENV: str = "NVIDIA_API_KEY"

# System prompt used for the chat completion
SYSTEM_PROMPT: str = """
Assess safety and social atmosphere of neighbourhoods for digital nomads based 
on crowdsourced data, place ratings, and recent news.

[Shortened for brevity … keep the full prompt text from the original here.]
""".strip()

###############################################################################
# Data definitions (in lieu of external files / API calls)
###############################################################################

ARTICLES: List[Dict[str, Any]] = [
    {
        "neighbourhood": "Ulsoor",
        "description": "crime",
        "news": [
            "Karnataka Police increase patrols in Ulsoor after spike in thefts",
            "Community meeting held to discuss safety measures in Ulsoor",
        ],
    },
    {
        "neighbourhood": "Indiranagar",
        "description": "techies",
        "news": [
            "Indiranagar praised for late-night walkability upgrades",
            "Residents celebrate new metro link improving safety",
        ],
    },
    {
        "neighbourhood": "Koramangala",
        "description": "students party",
        "news": [
            "Koramangala nightlife draws crowds; minor scuffles reported",
            "Police launch night patrol initiative after noise complaints",
        ],
    },
]

EMOJI_TABLE: pd.DataFrame = pd.DataFrame(
    [
        # nbh, place,  e1  e2  e3  e4
        ("Ulsoor", "Green Bowl Cafe", 3, 2, 10, 45),
        ("Ulsoor", "Lake View Co‑working", 1, 1, 5, 32),
        ("Ulsoor", "Blossom Yoga Studio", 0, 1, 2, 21),
        ("Indiranagar", "Cup & Code Café", 1, 0, 4, 60),
        ("Indiranagar", "Metro Park", 2, 1, 3, 55),
        ("Indiranagar", "Silicon Lounge", 0, 0, 2, 48),
        ("Koramangala", "Night Owl Bar", 4, 6, 15, 20),
        ("Koramangala", "StudyHub Library", 0, 0, 1, 25),
        ("Koramangala", "PlayGround Café", 2, 3, 7, 22),
    ],
    columns=["neighbourhood", "place", "emoji_1", "emoji_2", "emoji_3", "emoji_4"],
)

VIBE_KEYWORDS: Dict[str, List[str]] = {
    "Ulsoor": ["crime"],
    "Indiranagar": ["techies", "expat", "quiet"],
    "Koramangala": ["students", "party", "nightlife"],
}

###############################################################################
# Utility functions
###############################################################################

def load_api_key(env_var: str = API_KEY_ENV) -> str:
    """Load the NVIDIA API key from `.env` or environment."""
    load_dotenv(find_dotenv())  # silently peek at nearest .env
    api_key = os.getenv(env_var)
    if not api_key:
        raise RuntimeError(
            f"Missing environment variable '{env_var}'. "
            "Create a .env file with your key or export it first."
        )
    return api_key


def compute_emoji4_ratio(df: pd.DataFrame) -> pd.Series:
    """Return per‑neighbourhood ratio of emoji_4 to all reactions."""
    emoji_cols = [c for c in df.columns if c.startswith("emoji_")]
    df = df.copy()
    df["total"] = df[emoji_cols].sum(axis=1)
    df["ratio"] = df["emoji_4"] / df["total"].clip(lower=1)

    weighted_ratios = (
        df.groupby("neighbourhood")
        .apply(lambda g: (g["ratio"] * g["total"]).sum() / g["total"].sum())
    )
    return weighted_ratios


def top_safe_places(df: pd.DataFrame, *, n: int = 3) -> Dict[str, List[str]]:
    """Return the top‑`n` places per neighbourhood by emoji_4 count."""
    out: Dict[str, List[str]] = {}
    grouped = df.sort_values("emoji_4", ascending=False).groupby("neighbourhood")
    for nbh, group in grouped:
        out[nbh] = group.head(n)["place"].tolist()
    return out


def build_records(
    articles: List[Dict[str, Any]],
    emoji_stats: pd.Series,
    top_places: Dict[str, List[str]],
) -> List[Dict[str, Any]]:
    """Assemble the JSON payload expected by the LLM."""
    records: List[Dict[str, Any]] = []
    for row in articles:
        nbh = row["neighbourhood"]
        records.append(
            {
                "neighbourhood": nbh,
                "emoji4_ratio": round(float(emoji_stats.get(nbh, 0)), 4),
                "vibe_keywords": VIBE_KEYWORDS.get(nbh, []),
                "news": row["news"],
                "top_places_counts": [
                    {
                        "place": place,
                        "emoji4": int(
                            EMOJI_TABLE.query(
                                "neighbourhood == @nbh and place == @place"
                            )["emoji_4"].iloc[0]
                        ),
                    }
                    for place in top_places.get(nbh, [])
                ],
            }
        )
    return records


def call_llm(client: OpenAI, payload: str) -> str:
    """Request a chat completion and return its raw text."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": payload},
        ],
        max_tokens=600,
        temperature=0.4,
    )
    return response.choices[0].message.content

###############################################################################
# Main program
###############################################################################

def main() -> None:
    """Entry‑point for CLI usage."""
    # 1. Prep environment -----------------------------------------------------
    api_key = load_api_key()
    client = OpenAI(base_url=API_BASE_URL, api_key=api_key)

    # 2. Compute emoji‑based stats -------------------------------------------
    emoji_ratio = compute_emoji4_ratio(EMOJI_TABLE)
    safe_places = top_safe_places(EMOJI_TABLE)

    # 3. Build structured input ----------------------------------------------
    records = build_records(ARTICLES, emoji_ratio, safe_places)
    formatted_input = json.dumps(records, ensure_ascii=False, indent=2)
    print("📤 Sending structured payload to LLM (truncated):")
    print(textwrap.shorten(formatted_input, 350))

    # 4. Call the LLM ---------------------------------------------------------
    raw_text = call_llm(client, formatted_input)
    print("\n🧠 Raw model response (first 400 chars):")
    print(raw_text[:400], "…\n")

    # 5. Try to parse JSON (defensive) ---------------------------------------
    try:
        result_json = json.loads(raw_text)
        print("✅ Parsed response:")
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("❌ JSON parsing failed — output probably not valid JSON.")


###############################################################################
# Reusable library entry‑point
###############################################################################

if __name__ == "__main__":
    main()
