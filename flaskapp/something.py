# Colab normally has requests + pandas already, but not the OpenAI client
pip install --quiet openai==1.* pandas

import os, getpass

# Paste your key when prompted; it stays only in this runtime session
os.environ["NVIDIA_API_KEY"] = getpass.getpass("Paste your NVIDIA API key: ")

import pandas as pd, json, textwrap

articles = [
    {
        "neighbourhood": "Ulsoor",
        "description": "crime",
        "news": [
            "Karnataka Police increase patrols in Ulsoor after spike in thefts",
            "Community meeting held to discuss safety measures in Ulsoor"
        ]
    },
    {
        "neighbourhood": "Indiranagar",
        "description": "techies",
        "news": [
            "Indiranagar praised for late-night walkability upgrades",
            "Residents celebrate new metro link improving safety"
        ]
    },
    {
        "neighbourhood": "Koramangala",
        "description": "students party",
        "news": [
            "Koramangala nightlife draws crowds; minor scuffles reported",
            "Police launch night patrol initiative after noise complaints"
        ]
    }
]

emoji_table = pd.DataFrame([
    # nbh, place, e1 e2 e3 e4
    ("Ulsoor",      "Green Bowl Cafe",      3, 2, 10, 45),
    ("Ulsoor",      "Lake View Co‑working", 1, 1,  5, 32),
    ("Ulsoor",      "Blossom Yoga Studio",  0, 1,  2, 21),
    ("Indiranagar", "Cup & Code Café",      1, 0,  4, 60),
    ("Indiranagar", "Metro Park",           2, 1,  3, 55),
    ("Indiranagar", "Silicon Lounge",       0, 0,  2, 48),
    ("Koramangala", "Night Owl Bar",        4, 6, 15, 20),
    ("Koramangala", "StudyHub Library",     0, 0,  1, 25),
    ("Koramangala", "PlayGround Café",      2, 3,  7, 22),
], columns=["neighbourhood", "place", "emoji_1", "emoji_2", "emoji_3", "emoji_4"])

vibe_keywords = {
    "Ulsoor": ["crime"],
    "Indiranagar": ["techies", "expat", "quiet"],
    "Koramangala": ["students", "party", "nightlife"]
}
print("Dummy data loaded.")

def compute_emoji4_ratio(df: pd.DataFrame):
    emoji_cols = [c for c in df.columns if c.startswith("emoji_")]
    df = df.copy()
    df["total"] = df[emoji_cols].sum(axis=1)
    df["ratio"] = df["emoji_4"] / df["total"].clip(lower=1)
    return (
        df.groupby("neighbourhood")
          .apply(lambda g: (g["ratio"]*g["total"]).sum()/g["total"].sum())
    )

def top_safe_places(df: pd.DataFrame, n=3):
    out = {}
    grouped = df.sort_values("emoji_4", ascending=False).groupby("neighbourhood")
    for nbh, g in grouped:
        out[nbh] = g.head(n)["place"].tolist()
    return out

emoji_ratio = compute_emoji4_ratio(emoji_table)
top_places  = top_safe_places(emoji_table)
print(emoji_ratio)

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
                )
            }
            for p in top_places.get(nbh, [])
        ]
    })

formatted_input = json.dumps(records, ensure_ascii=False, indent=2)
print(textwrap.shorten(formatted_input, 350))

from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

SYSTEM_PROMPT = """
Assess safety and social atmosphere of neighbourhoods for digital nomads based on crowdsourced data, place ratings, and recent news.

Analyze the provided structured data about cities and their neighbourhoods to determine safety levels and provide a localized safety overview. The AI agent is designed to prioritize safety concerns especially relevant to women traveling alone or living abroad. Input includes place-level emoji reaction data, HoodMaps crowdsource descriptors, and neighbourhood-specific news headlines. 

While the safety assessment is tailored to concerns commonly experienced by women (e.g., harassment risk, walkability at night, public transportation safety, and local crime rates), the user of this information may be of any gender. Therefore, all communication and outputs must be phrased in a neutral tone—avoiding gendered language—so it is inclusive and informative to all users.
# Input Format

You will receive structured data in the following format:

1. Neighbourhood Data
[
    {
        "neighbourhood": "Ulsoor",
        "description": "crime",
        "news": [
            "Karnataka Police increase patrols in Ulsoor after spike in thefts",
            "Community meeting held to discuss safety measures in Ulsoor"
        ]
    },
    {
        "neighbourhood": "Indiranagar",
        "description": "techies",
        "news": [ ... ]
    }
]

2. User Ratings per Place
Country City
  Neighbourhood
    Place 1 - Total Emoji Reactions: X, Emoji 4 Reactions (safe): Y
    Place 2 - ...
  
# Features to Implement

## Feature 1: Safety Score per Neighbourhood (0.0 to 5.0)

Calculate and output a safety score for each neighbourhood. The score must combine the following three factors:

1. Emoji 4 Ratio: For each place in the neighbourhood, calculate the percentage of emoji 4 (i.e. "felt safe") reactions out of all reactions. Aggregate this for the neighbourhood.
2. HoodMaps Vibe: Extract keywords from the description. If it includes terms like "crime", "ghetto", or "unsafe", negatively weight the score. If it includes terms like "techies", "families", "quiet", or "expat", weight positively.
3. News Analysis: Evaluate safety-related news headlines. Headlines indicating increased patrols or community safety actions increase the score slightly. Headlines indicating crime spikes or recent violent events lower the score.

Weighting should prioritize:
- Emoji data (50%)
- News (30%)
- HoodMaps (20%)

Return one float value between 0.0 and 5.0 per neighbourhood.

## Feature 2: Top 3 Safe Places per Neighbourhood

List the top 3 places in each neighbourhood ranked by the number of emoji 4 reactions (i.e. places users reported feeling safe at). If fewer than 3 places exist, list as many as available.

## Feature 3: Safety Overview per Neighbourhood

For each neighbourhood:
- Summarize any significant safety-related news (e.g., recent crimes, safety interventions).
- If HoodMaps mentions terms relevant to safety, include them in the overview (e.g., "known for crime" or "described as quiet and family-friendly").

This output should provide a brief, readable paragraph for each neighbourhood to help digital nomads understand the local safety context.

## Feature 4: Social Character Assessment

Describe the general social atmosphere or demographic in each neighbourhood based on the HoodMaps description or other cues. If it contains terms like “techies”, “students”, “party”, “families”, “touristy”, or “gentrified”, output this as a friendly description of what the people or vibe are like.

# Output Format

Return a structured block for each neighbourhood with the following format:

Neighbourhood: <Name>
Safety Score: <X.Y/5.0>
Top 3 Safe Places:
  - <Place 1>
  - <Place 2>
  - <Place 3>
Safety Overview:
  <Short paragraph summarizing news and HoodMaps safety context>
Social Character:
  <What kind of people live or hang out here>

# Example Output

Neighbourhood: Ulsoor
Safety Score: 3.2/5.0
Top 3 Safe Places:
  - Green Bowl Cafe
  - Lake View Co-working
  - Blossom Yoga Studio
Safety Overview:
  Recent thefts have caused concern in Ulsoor, prompting increased police patrols and community safety meetings. HoodMaps also tags this area as “crime-prone”, which aligns with recent events.
Social Character:
  Mixed-use neighbourhood with local residents and some budget travelers.

# Notes

- Your safety assessments should be especially sensitive to the types of threats and discomforts commonly reported by women in unfamiliar areas. However, you must phrase all outputs using gender-neutral language.
- Only focus on safety, security atmosphere, and demographic vibe. Do not give tourist or entertainment recommendations.
- Output must be clean and consistent with the format above. Do not include irrelevant commentary.

"""

response = client.chat.completions.create(
    model="nvidia/llama-3.3-nemotron-super-49b-v1",  # ✅ CORRECTED
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": formatted_input}
    ],
    max_tokens=600,
    temperature=0.4
)

raw_text = response.choices[0].message.content
print("🧠 Raw model response (first 400 chars):\n", raw_text[:400], "\n")

try:
    result_json = json.loads(raw_text)
    print("✅ Parsed LLM output:")
    print(json.dumps(result_json, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("❌ JSON parsing failed — likely formatting issue in LLM response.")

