# Bibble Safety Intelligence UI – README

## 🤖 About Bibble the AI Agent
**Bibble** is an AI agent designed to serve as a smart city companion for Bunq users. It provides context-aware, real-time intelligence about neighborhood safety and social atmosphere using a blend of external APIs, scraped city data, emoji reaction analytics, and LLM-powered summaries. Built as a modular AI system, Bibble is capable of adapting its behavior based on city-specific information and external data availability.

This project demonstrates how Bibble could integrate with Bunq’s infrastructure to enrich user travel experiences with safety guidance, local vibes, and personalized place insights.

---

## 🧠 Project Overview
**Bibble** is an AI agent built to assist Bunq users during travel. It acts as a personalized safety and city intelligence advisor, helping users explore neighborhoods with confidence. Bibble uses external API calls, crowdsourced emoji reactions, vibe descriptors from HoodMaps, and local news headlines to assess:

- A **Safety Score** per neighborhood
- A **Safety Overview** based on news and vibe keywords
- A friendly summary of the **Social Character**
- The **Top 3 Safe Places** per area

The app is designed with a stylish React Native frontend (Expo) and an AI-driven Python backend using NVIDIA's OpenAI-compatible LLaMA-3.3 model.

---

## 🔧 Key Dependencies

### Python Backend
- `flask` – lightweight web framework
- `requests` – for HTTP requests (e.g., Google News RSS)
- `feedparser` – parsing RSS feeds
- `pandas` – for emoji-based statistical analysis
- `faker` – generating realistic fake names for places and cities
- `python-dotenv` – to securely load environment variables
- `openai` – to communicate with NVIDIA's OpenAI-compatible endpoint
- `bs4` – (BeautifulSoup) to clean up news article summaries

Install backend requirements:
```bash
pip install flask requests feedparser pandas faker python-dotenv openai beautifulsoup4
```

### React Native Frontend (Expo)
- `expo`
- `react-native`
- `axios` – for making HTTP requests
- `expo-router` – for screen navigation
- `@expo/vector-icons` – for tab bar icons

Install frontend dependencies (in your project root):
```bash
npm install axios expo-router @expo/vector-icons
```

---

## 💡 Where and Why Fake Data Was Used

### 1. **Emoji Reaction Table (Backend)**
We simulate emoji feedback data using `faker` and `random`, since we do **not** have access to **Bunq's real user reaction storage**. However, in a production scenario:
- This table could be populated directly via Bunq's API using stored user interactions on places, locations, or cards.

### 2. **Final UI JSON Object (Frontend)**
Due to temporary connection issues between the backend and frontend, we **hardcoded synthetic JSON data** in the frontend's `/safety` screen. This ensures the UI could be designed, tested, and demonstrated independently.
- In production, this JSON would be passed via router params after a live call to the Flask backend.

---

## 🚀 How It Works

### Step 1: City Trigger from Frontend
On the Travel tab, the user taps "Learn about the safety conditions around your area."
- The frontend fetches the current city from [`ipinfo.io`](https://ipinfo.io)
- Sends this city to `/process_city` in the Flask backend

### Step 2: Backend Processing
1. `process_city_data(city)` scrapes HoodMaps and Google News to get descriptions and headlines
2. `generate_synthetic_tourist_data()` generates emoji stats per place
3. `generate_neighbourhood_safety_json()` uses LLaMA-3.3 (via OpenAI SDK) to:
   - Calculate a safety score
   - Select top 3 safe places
   - Write a safety overview
   - Write a social character description
4. The final result is a JSON object

### Step 3: UI Presentation
The frontend receives (or mocks) this JSON and renders it using a paginated `ScrollView`, with:
- Star ratings
- Vibe descriptions
- Top places
- Color-coded styling for readability

---

## 📁 File Structure
```bash
frontend/
  └── app/
      ├── (tabs)/travel.tsx    # Sends request, triggers AI
      ├── safety.tsx           # Renders final AI JSON data
      └── tabs.js              # Navigation layout
backend/
  ├── main.py                 # Flask app and routes
  ├── process_city_data.py    # Web scraping + news
  ├── my_llm_function.py      # Calls NVIDIA LLaMA-3.3
  └── generate_data.py        # Fake emoji ratings
.env                          # Stores NVIDIA API key
```

---

## ✅ Next Steps
- Replace hardcoded frontend JSON with live API data
- Move from `faker` data to real Bunq reactions (via OAuth or sandbox)
- Add visual maps and heatmaps per neighborhood
- Enable real-time feedback or reporting from users

---

## 📌 Credits
- Frontend design by your team using Expo
- Backend AI integration using NVIDIA's NIM endpoint
- Data scraped from HoodMaps and Google News

---

## ⚠️ Disclaimer
This project is a **proof-of-concept**. The safety ratings are generated by a language model using synthetic and scraped data and **must not be used as real-world safety guidance** without human moderation.