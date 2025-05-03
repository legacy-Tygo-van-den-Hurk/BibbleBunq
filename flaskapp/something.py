import json
import pandas as pd
import re
import os
from openai import OpenAI
from dotenv import load_dotenv


def generate_neighbourhood_safety_json(articles, emoji_table):
    """
    Generates a neighbourhood‑level safety & vibe assessment JSON using
    NVIDIA's LLaMA‑3.3 model via its OpenAI‑compatible endpoint.

    Parameters
    ----------
    articles : list[dict]
        Each dict must contain:
        {
            "neighbourhood": str,
            "description": str,   # HoodMaps‑style keywords (space‑separated)
            "news": list[str]     # list of headline strings
        }

    emoji_table : pandas.DataFrame
        Must have columns:
        ["neighbourhood", "place", "emoji_1", "emoji_2", "emoji_3", "emoji_4"]
        (additional emoji_N columns are ignored).

    The function reads the NVIDIA API key from "../.env" under
    key name OPENAI_API_KEY, keeps the system prompt *exactly*
    as supplied, calls the model, and returns a parsed JSON object.
    """

    # ------------------------------------------------------------------
    # 1.  Load API key from ../.env
    # ------------------------------------------------------------------
    load_dotenv(dotenv_path="../.env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in ../.env")

    # Init OpenAI‑compatible client for NVIDIA endpoint
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    # ------------------------------------------------------------------
    # 2.  Helper functions for emoji stats
    # ------------------------------------------------------------------
    def compute_emoji4_ratio(df: pd.DataFrame) -> pd.Series:
        df = df.copy()
        df["total"] = df.filter(like="emoji_").sum(axis=1)
        df["ratio"] = df["emoji_4"] / df["total"].clip(lower=1)
        return (
            df.groupby("neighbourhood")
              .apply(lambda g: (g["ratio"] * g["total"]).sum() / g["total"].sum())
        )

    def top_safe_places(df: pd.DataFrame, n: int = 3):
        return (
            df.sort_values("emoji_4", ascending=False)
              .groupby("neighbourhood")
              .head(n)
              .groupby("neighbourhood")["place"]
              .apply(list)
              .to_dict()
        )

    # ------------------------------------------------------------------
    # 3.  Derive vibe_keywords automatically from description strings
    # ------------------------------------------------------------------
    vibe_keywords = {
        row["neighbourhood"]: row["description"].lower().split()
        for row in articles
    }

    # ------------------------------------------------------------------
    # 4.  Build structured input for the model
    # ------------------------------------------------------------------
    emoji_ratio = compute_emoji4_ratio(emoji_table)
    top_places  = top_safe_places(emoji_table)

    records = []
    for row in articles:
        nbh = row["neighbourhood"]
        records.append({
            "neighbourhood": nbh,
            "emoji4_ratio": round(float(emoji_ratio.get(nbh, 0)), 4),
            "vibe_keywords": vibe_keywords.get(nbh, []),
            "news": row["news"],
            "top_places_counts": [
                {
                    "place": p,
                    "emoji4": int(
                        emoji_table.query("neighbourhood == @nbh and place == @p")["emoji_4"].iloc[0]
                    ),
                }
                for p in top_places.get(nbh, [])
            ],
        })

    formatted_input = json.dumps(records, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # 5.  SYSTEM PROMPT (kept *exactly* as provided)
    # ------------------------------------------------------------------
    SYSTEM_PROMPT = """Thought for 7 seconds


Purpose: Evaluate neighbourhood safety and social atmosphere for digital nomads using crowdsourced data, place‑level emoji reactions, HoodMaps descriptors, and local news.

Output Requirement: **Every answer MUST be valid JSON only – no markdown or explanatory text.**

────────────────────────────────────────
INPUT STRUCTURE

1. **Neighbourhood Dataset** (JSON array)

```json
[
  {
    "neighbourhood": "Ulsoor",
    "description": "crime",
    "news": [
      "Karnataka Police increase patrols in Ulsoor after spike in thefts",
      "Community meeting held to discuss safety measures in Ulsoor"
    ]
  },
  ...
]
```

2. **User Ratings per Place** (indented text)

```
Country City
  Neighbourhood
    Place – Total Emoji Reactions: X, Emoji 4 (safe) Reactions: Y
```

────────────────────────────────────────
FEATURES TO DELIVER

1. **Safety Score (0.0‑5.0 per neighbourhood)**
   • **Emoji data** (50 % weight): ratio of Emoji 4 to total reactions.
   • **News** (30 % weight):
         – Headlines on crime spikes / violence → lower score.
         – Headlines on patrols / community action → slightly raise score.
   • **HoodMaps** (20 % weight): keywords such as:
         – Negative: “crime”, “ghetto”, “unsafe” → lower score.
         – Positive: “techies”, “families”, “quiet”, “expat” → raise score.

2. **Top 3 Safe Places**
   Pick up to three places with the highest count of Emoji 4 reactions per neighbourhood.

3. **Safety Overview**
   Short paragraph that fuses key safety‑related news and relevant HoodMaps safety keywords.

4. **Social Character**
   Friendly description of the local vibe based on HoodMaps (e.g., “techies”, “students”, “party”, “families”, “touristy”, “gentrified”).

────────────────────────────────────────
OUTPUT JSON SCHEMA (one object per neighbourhood)

```json
{
  "Neighbourhood": "<Name>",
  "Safety Score": "<X.Y/5.0>",
  "Top 3 Safe Places": [
    "<Place 1>",
    "<Place 2>",
    "<Place 3>"
  ],
  "Safety Overview": "<Brief paragraph>",
  "Social Character": "<Vibe description>"
}
```

Rules:
• Use inclusive, gender‑neutral phrasing.
• Omit tourist/entertainment advice.
• Provide no extra commentary outside the JSON.
."""

    # ------------------------------------------------------------------
    # 6.  LLM call
    # ------------------------------------------------------------------
    response = client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": formatted_input}
        ],
        max_tokens=1000,
        temperature=0.4,
    )

    raw_text = response.choices[0].message.content

    # ------------------------------------------------------------------
    # 7.  Extract valid JSON block
    # ------------------------------------------------------------------
    # raw = re.sub(r"^```(?:json)?|```$", "", raw_text.strip(), flags=re.IGNORECASE | re.MULTILINE)
    # match = re.search(r"\[\s*{.*?}\s*]", raw, flags=re.DOTALL)
    # if not match:
    #     raise ValueError(f"No valid JSON block found. Raw model output:\n{raw_text}")

    return raw_text
