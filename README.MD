# 🏥 AI Medical Symptom Checker

<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,12&height=200&section=header&text=AI%20Medical%20Symptom%20Checker&fontSize=40&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Symptoms%20%E2%86%92%20Possible%20Conditions%20%E2%86%92%20Urgency%20Level%20%E2%86%92%20Specialist%20Recommendations&descAlignY=55&descSize=13)

<p>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini%201.5%20Flash-Free%20API-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Educational%20Use-Only-f97316?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge"/>
</p>

<p>
  <b>Describe your symptoms → Get possible conditions ranked by likelihood, urgency triage level, recommended specialists, home care tips, red flags, and a list of questions to ask your doctor.</b>
</p>

> ⚠️ **DISCLAIMER: This tool is for educational purposes only. It does NOT provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [How It Works](#-how-it-works) • [FAQ](#-faq)

</div>

---

## 🌟 Why This Project?

When people experience symptoms, they typically either:
- 😨 Panic and Google worst-case scenarios
- 🤷 Ignore symptoms that actually need attention
- 💸 Make unnecessary ER visits for minor issues
- 🤔 Don't know which type of doctor to see

This tool provides **structured, educational guidance** — helping people understand their symptoms, assess urgency, and prepare better questions for their doctor.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚨 **Emergency Detection** | Rule-based screening instantly flags potential emergency symptoms |
| 🎯 **Urgency Triage** | 4-level system: Emergency / High / Medium / Low |
| 🔬 **Possible Conditions** | 3–5 ranked conditions with likelihood (High/Medium/Low) |
| 👨‍⚕️ **Specialist Recommendations** | Which type of doctor to see based on symptoms |
| ⚡ **Immediate Actions** | What to do right now based on urgency level |
| 🏠 **Home Care Tips** | Safe self-care for low-urgency symptoms |
| 🚩 **Red Flag Warnings** | Specific signs that mean you must seek care immediately |
| ❓ **Doctor Questions** | Prepared questions to maximise your medical appointment |
| 📥 **Download Report** | Save the full analysis as a .txt file to bring to your doctor |
| 🌍 **Emergency Numbers** | Global emergency numbers displayed in sidebar |
| 📋 **8 Example Symptoms** | One-click demo symptom sets |

---

## 🖥️ Demo

```
╔══════════════════════════════════════════════════════════════════╗
║  🏥 AI Medical Symptom Checker                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  Symptoms: "Severe headache, stiff neck, fever 103°F,           ║
║             sensitivity to light for 18 hours"                  ║
║  Duration: Less than 24 hours │ Severity: 9/10                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🚨 URGENCY: EMERGENCY                                          ║
║  "Seek immediate emergency care — these symptoms may            ║
║   indicate a serious neurological condition."                   ║
║                                                                  ║
║  🔬 Possible Conditions:                                         ║
║  1. Bacterial Meningitis       [HIGH likelihood]                ║
║  2. Viral Meningitis           [MEDIUM likelihood]              ║
║  3. Severe Migraine with Aura  [LOW likelihood]                 ║
║                                                                  ║
║  👨‍⚕️ See: Emergency Medicine, Neurologist, Infectious Disease   ║
║                                                                  ║
║  🚩 Red Flags: Petechial rash, altered consciousness,           ║
║     rapid symptom progression                                    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+ → [Download](https://www.python.org/downloads/)
- Free Gemini API key → [Get here](https://aistudio.google.com) *(no credit card)*

### Step 1 — Clone
```bash
git clone https://github.com/YOUR_USERNAME/ai-medical-symptom-checker.git
cd ai-medical-symptom-checker
```

### Step 2 — Virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install
```bash
pip install -r requirements.txt
```

### Step 4 — Run
```bash
streamlit run app.py
```

Opens at **http://localhost:8501** 🎉

---

## 🧠 How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│  User Input                                                      │
│  Symptoms + Duration + Severity + Age + Sex + Body System       │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  Emergency Rule-Based Screen (instant, no API needed)           │
│  Checks 25+ emergency keywords: chest pain, stroke, seizure...  │
│  → Shows immediate emergency banner if triggered                │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  Gemini 1.5 Flash — Structured JSON Analysis                    │
│  Low temperature (0.2) for consistent, factual output           │
│                                                                  │
│  Returns 12 structured fields:                                  │
│  urgency_level · possible_conditions · specialists              │
│  immediate_actions · home_care_tips · red_flags                 │
│  questions_for_doctor · lifestyle_tips · summary                │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│  Streamlit UI — 5 tabs                                          │
│  + Downloadable .txt report                                     │
└──────────────────────────────────────────────────────────────────┘
```

### Urgency Triage System

| Level | Color | When | Action |
|---|---|---|---|
| 🚨 **Emergency** | Red | Life-threatening symptoms | Call 911 / Go to ER immediately |
| ⚠️ **High** | Orange | Serious symptoms | See doctor today / urgent care |
| 📋 **Medium** | Yellow | Moderate symptoms | Schedule appointment within days |
| ✅ **Low** | Green | Mild symptoms | Monitor, home care may help |

---

## 📁 Project Structure

```
ai-medical-symptom-checker/
│
├── app.py              # 🧠 Full app — triage, AI analysis, 5-tab UI
├── requirements.txt    # 📦 Only 2 dependencies
├── .gitignore          # 🚫 Excluded files
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 You are here
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| [Streamlit](https://streamlit.io) | 1.35 | Web UI |
| [Google Gemini](https://aistudio.google.com) | 1.5 Flash | Symptom analysis & condition identification |

Only **2 pip installs** — the leanest possible stack.

---

## 🌍 Emergency Numbers

| Country | Number |
|---|---|
| 🇺🇸 USA / Canada | **911** |
| 🇬🇧 UK | **999** |
| 🇮🇳 India | **112** |
| 🇦🇺 Australia | **000** |
| 🇪🇺 Europe | **112** |
| 🌍 International | **112** (works in most countries) |

---

## 🤔 FAQ

**Q: Is this a replacement for seeing a doctor?**
> Absolutely not. This is an educational tool to help understand symptoms and prepare for medical appointments. Always consult a licensed healthcare professional.

**Q: How accurate is the condition identification?**
> Gemini provides plausible educational information based on symptoms. It cannot physically examine you, review your medical history, or run tests. Real diagnosis requires a doctor.

**Q: Is my health data stored anywhere?**
> No. All processing is done in real-time. Nothing is saved to any database. Your symptoms are only sent to Google Gemini to generate the response.

**Q: What if I have an emergency?**
> Call 911 (US) or your local emergency number immediately. The app also shows emergency numbers in the sidebar. Do NOT rely on this tool in emergencies.

**Q: Can I use this for children's symptoms?**
> The tool accepts age ranges including "Under 12" but children should always be seen by a pediatrician. Do not delay seeking care for a sick child.

---

## 🗺️ Roadmap

- [ ] 📸 Image input — upload a photo of a rash or wound
- [ ] 📊 Symptom history tracker — log symptoms over time
- [ ] 💊 Medication interaction checker
- [ ] 🌍 Multi-language support
- [ ] 📍 Find nearest doctor/urgent care based on location
- [ ] 🔔 Symptom progression alerts

---

## ⚠️ Full Disclaimer

This application is provided for **informational and educational purposes only**. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Never disregard professional medical advice or delay in seeking it because of something you have read or seen in this application. If you think you may have a medical emergency, call your doctor, go to the nearest emergency room, or call emergency services immediately.

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m 'feat: your feature'`
4. Push & open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Found this useful? Star the repo — it helps a lot!**

Made with ❤️ and Python

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,12&height=100&section=footer)

</div>
