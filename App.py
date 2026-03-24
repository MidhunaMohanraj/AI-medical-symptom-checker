"""
app.py — AI Medical Symptom Checker
Enter symptoms → Get possible conditions, urgency level, specialist recommendations
Uses rule-based triage + Gemini AI (free) for detailed analysis
DISCLAIMER: For educational purposes only. Not a substitute for professional medical advice.
"""

import streamlit as st
import google.generativeai as genai
import json
import re
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Symptom Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .main { background: #07080f; }

  .hero {
    background: linear-gradient(135deg, #07080f 0%, #0a0f1e 50%, #070f0a 100%);
    border: 1px solid #1a2030;
    border-radius: 16px;
    padding: 32px 40px;
    text-align: center;
    margin-bottom: 20px;
  }
  .hero h1 { font-size: 38px; font-weight: 700; color: #fff; margin: 0 0 6px; }
  .hero p  { color: #64748b; font-size: 14px; margin: 0; }

  .disclaimer-banner {
    background: #150a00;
    border: 1px solid #7c2d12;
    border-left: 4px solid #f97316;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 13px;
    color: #fdba74;
    margin-bottom: 20px;
    line-height: 1.6;
  }

  .urgency-emergency {
    background: #1a0505;
    border: 2px solid #dc2626;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 12px 0;
  }
  .urgency-high {
    background: #1a0d00;
    border: 2px solid #f97316;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 12px 0;
  }
  .urgency-medium {
    background: #1a1500;
    border: 2px solid #eab308;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 12px 0;
  }
  .urgency-low {
    background: #051a0a;
    border: 2px solid #22c55e;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin: 12px 0;
  }
  .urgency-label { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 6px; }
  .urgency-title { font-size: 28px; font-weight: 700; }
  .urgency-desc  { font-size: 13px; margin-top: 6px; color: #94a3b8; }

  .condition-card {
    background: #0b0d18;
    border: 1px solid #1e2040;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 8px 0;
  }
  .condition-name  { font-size: 16px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
  .condition-match { font-size: 12px; font-weight: 600; padding: 2px 10px; border-radius: 12px; display: inline-block; margin-bottom: 8px; }
  .condition-desc  { font-size: 13px; color: #94a3b8; line-height: 1.7; }

  .specialist-chip {
    display: inline-block;
    background: #0f1020;
    border: 1px solid #2a2a50;
    color: #818cf8;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
  }

  .advice-box {
    background: #080c08;
    border-left: 4px solid #22c55e;
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    font-size: 14px;
    line-height: 1.85;
    color: #a0c0a8;
    margin: 8px 0;
  }
  .warning-box {
    background: #0f0800;
    border-left: 4px solid #f97316;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 13px;
    line-height: 1.7;
    color: #fdba74;
    margin: 8px 0;
  }

  .stat-card {
    background: #0b0d18;
    border: 1px solid #1e2040;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
  }
  .stat-val   { font-size: 22px; font-weight: 700; color: #60a5fa; }
  .stat-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 3px; }

  .symptom-tag {
    display: inline-block;
    background: #0f1020;
    border: 1px solid #2a3050;
    color: #93c5fd;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 3px;
  }

  div.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 13px 28px;
    font-size: 15px;
    width: 100%;
  }
  div.stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Emergency symptoms (rule-based, immediate alert) ──────────────────────────
EMERGENCY_SYMPTOMS = [
    "chest pain", "chest tightness", "heart attack", "stroke", "can't breathe",
    "difficulty breathing", "shortness of breath", "severe", "unconscious",
    "not breathing", "unresponsive", "seizure", "severe bleeding", "coughing blood",
    "blood in stool", "suicidal", "overdose", "poisoning", "severe allergic",
    "anaphylaxis", "sudden vision loss", "sudden numbness", "facial drooping",
    "arm weakness", "slurred speech", "severe headache", "worst headache",
    "high fever", "stiff neck", "rash with fever",
]

def check_emergency(symptoms_text: str) -> bool:
    text = symptoms_text.lower()
    return any(kw in text for kw in EMERGENCY_SYMPTOMS)

# ── Common symptom suggestions ─────────────────────────────────────────────────
SYMPTOM_EXAMPLES = [
    "Headache, fever, fatigue, sore throat",
    "Stomach pain, nausea, bloating, diarrhea",
    "Chest discomfort, shortness of breath, palpitations",
    "Skin rash, itching, redness, swelling",
    "Joint pain, stiffness, swelling in knees",
    "Cough, runny nose, congestion, sneezing",
    "Dizziness, blurred vision, balance problems",
    "Frequent urination, burning sensation, back pain",
]

# ── Body systems for context ───────────────────────────────────────────────────
BODY_SYSTEMS = [
    "Not sure", "Head / Neurological", "Chest / Heart / Lungs",
    "Stomach / Digestive", "Skin / Dermatology", "Musculoskeletal / Joints",
    "Urinary / Kidney", "Eyes / Vision", "Ears / Hearing",
    "Mental Health", "Hormonal / Endocrine", "General / Whole Body",
]

# ── Gemini analysis ────────────────────────────────────────────────────────────
def analyse_symptoms(
    symptoms: str,
    duration: str,
    severity: int,
    age: str,
    sex: str,
    body_system: str,
    existing_conditions: str,
    api_key: str,
) -> dict:

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"temperature": 0.2, "max_output_tokens": 2000},
    )

    prompt = f"""You are an AI medical education assistant. A user wants to understand their symptoms for educational purposes.

IMPORTANT: Always remind the user this is NOT medical advice and they must consult a real doctor.

PATIENT INFO:
- Symptoms: {symptoms}
- Duration: {duration}
- Severity (1-10): {severity}
- Age range: {age}
- Biological sex: {sex}
- Body system affected: {body_system}
- Existing conditions: {existing_conditions if existing_conditions else "None mentioned"}

Return ONLY this JSON (no markdown, no text outside JSON):
{{
  "urgency_level": "Emergency | High | Medium | Low",
  "urgency_color": "red | orange | yellow | green",
  "urgency_message": "One sentence describing what to do right now",
  "possible_conditions": [
    {{
      "name": "Condition name",
      "likelihood": "High | Medium | Low",
      "description": "2-sentence plain English description of this condition",
      "typical_symptoms": ["symptom1", "symptom2", "symptom3"],
      "when_to_worry": "One sentence on red flags for this condition"
    }}
  ],
  "recommended_specialists": ["Doctor type 1", "Doctor type 2"],
  "immediate_actions": ["Action 1", "Action 2", "Action 3"],
  "home_care_tips": ["Tip 1", "Tip 2", "Tip 3"],
  "questions_for_doctor": ["Question 1", "Question 2", "Question 3"],
  "red_flags": ["Warning sign 1", "Warning sign 2"],
  "lifestyle_tips": ["Tip 1", "Tip 2"],
  "summary": "2-3 sentence educational summary of what these symptoms may indicate and what the user should do next",
  "disclaimer": "Always consult a qualified healthcare professional for proper diagnosis and treatment."
}}

Rules:
- List 3-5 possible conditions ordered by likelihood
- Be educational and informative but always stress professional consultation
- If symptoms suggest emergency, set urgency_level to Emergency
- Keep all descriptions in plain English, avoid heavy medical jargon"""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"^```json\s*|^```\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)

# ── Urgency styling ────────────────────────────────────────────────────────────
URGENCY_CONFIG = {
    "Emergency": {
        "class": "urgency-emergency",
        "color": "#ef4444",
        "icon":  "🚨",
        "action": "CALL 911 / GO TO ER NOW",
    },
    "High": {
        "class": "urgency-high",
        "color": "#f97316",
        "icon":  "⚠️",
        "action": "See a doctor today or visit urgent care",
    },
    "Medium": {
        "class": "urgency-medium",
        "color": "#eab308",
        "icon":  "📋",
        "action": "Schedule a doctor appointment within a few days",
    },
    "Low": {
        "class": "urgency-low",
        "color": "#22c55e",
        "icon":  "✅",
        "action": "Monitor symptoms, home care may be appropriate",
    },
}

LIKELIHOOD_COLORS = {
    "High":   ("#dcfce7", "#166534", "#22c55e"),
    "Medium": ("#fef9c3", "#854d0e", "#eab308"),
    "Low":    ("#f1f5f9", "#334155", "#94a3b8"),
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 Symptom Checker")
    st.markdown("---")

    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "Free Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get FREE at https://aistudio.google.com"
    )
    if not api_key:
        st.info("🆓 Get a **free** key at [aistudio.google.com](https://aistudio.google.com)")

    st.markdown("---")
    st.markdown("### 🚨 Emergency Numbers")
    st.markdown("""
| Country | Emergency |
|---|---|
| 🇺🇸 USA | **911** |
| 🇬🇧 UK | **999** |
| 🇮🇳 India | **112** |
| 🇦🇺 Australia | **000** |
| 🇨🇦 Canada | **911** |
| 🇪🇺 Europe | **112** |
    """)

    st.markdown("---")
    st.markdown("### ⚡ Example Symptom Sets")
    for ex in SYMPTOM_EXAMPLES[:4]:
        if st.button(f"📋 {ex[:35]}...", key=f"ex_{ex[:10]}"):
            st.session_state["symptoms_input"] = ex

    st.markdown("---")
    st.error("⚠️ **NOT MEDICAL ADVICE** — Always consult a licensed doctor for any health concerns.")

# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🏥 AI Medical Symptom Checker</h1>
  <p>Describe your symptoms → Get possible conditions, urgency level & specialist recommendations</p>
</div>
""", unsafe_allow_html=True)

# ── Disclaimer banner ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
  🚨 <b>IMPORTANT DISCLAIMER:</b> This tool is for <b>educational purposes only</b> and does NOT provide medical advice,
  diagnosis, or treatment. Always consult a qualified healthcare professional for any health concerns.
  If you are experiencing a medical emergency, call <b>911</b> (US) or your local emergency number immediately.
</div>
""", unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown("### 📝 Describe Your Symptoms")

symptoms_input = st.text_area(
    "Symptoms",
    value=st.session_state.get("symptoms_input", ""),
    height=120,
    placeholder="e.g. I have a severe headache, fever of 101°F, stiff neck, and sensitivity to light for the past 2 days...\n\nBe as specific as possible — include location, severity, and how long you've had each symptom.",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns(3)
with col1:
    duration = st.selectbox("How long have you had these symptoms?", [
        "Less than 24 hours", "1–3 days", "4–7 days",
        "1–2 weeks", "2–4 weeks", "1–3 months", "More than 3 months",
    ])
with col2:
    severity = st.slider("Severity (1 = mild, 10 = severe)", 1, 10, 5)
with col3:
    body_system = st.selectbox("Body system affected", BODY_SYSTEMS)

col4, col5 = st.columns(2)
with col4:
    age = st.selectbox("Age range", [
        "Under 12", "12–17", "18–30", "31–45", "46–60", "61–75", "Over 75", "Prefer not to say",
    ])
with col5:
    sex = st.selectbox("Biological sex", ["Male", "Female", "Prefer not to say"])

existing_conditions = st.text_input(
    "Existing conditions or medications (optional)",
    placeholder="e.g. diabetes, hypertension, on metformin...",
)

analyse_clicked = st.button("🔍 Analyse Symptoms")

# ── Results ────────────────────────────────────────────────────────────────────
if analyse_clicked:
    symptoms = symptoms_input.strip()

    if len(symptoms) < 10:
        st.warning("⚠️ Please describe your symptoms in more detail.")
        st.stop()

    # Emergency check
    if check_emergency(symptoms):
        st.markdown("""
<div class="urgency-emergency">
  <div class="urgency-label" style="color:#fca5a5;">🚨 POTENTIAL EMERGENCY DETECTED</div>
  <div class="urgency-title" style="color:#ef4444;">SEEK IMMEDIATE MEDICAL ATTENTION</div>
  <div class="urgency-desc">Your symptoms may indicate a serious or life-threatening condition.<br/>
  Call <b>911</b> (US) / <b>112</b> (EU/India) / <b>999</b> (UK) or go to the nearest Emergency Room NOW.</div>
</div>
""", unsafe_allow_html=True)

    if not api_key:
        st.error("⚠️ Please add your free Gemini API key in the sidebar to get the full analysis.")
        st.stop()

    with st.spinner("🧠 Analysing symptoms..."):
        try:
            result = analyse_symptoms(
                symptoms, duration, severity, age, sex,
                body_system, existing_conditions, api_key,
            )
        except json.JSONDecodeError:
            st.error("Could not parse response. Please try again.")
            st.stop()
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.stop()

    urgency = result.get("urgency_level", "Medium")
    cfg     = URGENCY_CONFIG.get(urgency, URGENCY_CONFIG["Medium"])

    # ── Urgency banner ─────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="{cfg['class']}">
  <div class="urgency-label" style="color:{cfg['color']};">{cfg['icon']} URGENCY LEVEL</div>
  <div class="urgency-title" style="color:{cfg['color']};">{urgency.upper()}</div>
  <div class="urgency-desc">{result.get('urgency_message', cfg['action'])}</div>
</div>
""", unsafe_allow_html=True)

    # ── Stats row ──────────────────────────────────────────────────────────────
    conditions = result.get("possible_conditions", [])
    specialists = result.get("recommended_specialists", [])
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{len(conditions)}</div><div class="stat-label">Possible Conditions</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{severity}/10</div><div class="stat-label">Reported Severity</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{len(specialists)}</div><div class="stat-label">Specialists</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{duration.split()[0]}</div><div class="stat-label">Duration</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary ────────────────────────────────────────────────────────────────
    st.markdown(f'<div class="advice-box">📋 <b>Summary:</b> {result.get("summary", "")}</div>', unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔬 Possible Conditions", "👨‍⚕️ Recommendations", "🏠 Home Care", "⚠️ Red Flags", "❓ Questions for Doctor"
    ])

    with tab1:
        st.markdown("### 🔬 Possible Conditions")
        st.caption("*Ordered by likelihood based on your symptoms — educational only, not a diagnosis*")

        for cond in conditions:
            name       = cond.get("name", "Unknown")
            likelihood = cond.get("likelihood", "Low")
            desc       = cond.get("description", "")
            typ_syms   = cond.get("typical_symptoms", [])
            worry      = cond.get("when_to_worry", "")

            _, text_c, border_c = LIKELIHOOD_COLORS.get(likelihood, LIKELIHOOD_COLORS["Low"])
            chip_style = f"background:{border_c}22;color:{border_c};border:1px solid {border_c}44;"

            syms_html = "".join([f'<span class="symptom-tag">{s}</span>' for s in typ_syms])

            st.markdown(f"""
<div class="condition-card">
  <div class="condition-name">{name}</div>
  <span class="condition-match" style="{chip_style}">{likelihood} Likelihood</span>
  <div class="condition-desc">{desc}</div>
  <div style="margin-top:10px;">{syms_html}</div>
  <div style="margin-top:10px;font-size:12px;color:#f97316;">⚠️ {worry}</div>
</div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 👨‍⚕️ Recommended Specialists")
        chips = "".join([f'<span class="specialist-chip">👨‍⚕️ {s}</span>' for s in specialists])
        st.markdown(chips, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚡ Immediate Actions")
        for action in result.get("immediate_actions", []):
            st.markdown(f'<div class="advice-box" style="padding:12px 16px;margin:6px 0;">▶ {action}</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🏠 Home Care Tips")
        st.caption("*Only appropriate if urgency is Low or Medium and no emergency symptoms present*")
        for tip in result.get("home_care_tips", []):
            st.markdown(f'<div class="advice-box" style="padding:12px 16px;margin:6px 0;">🌿 {tip}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💊 Lifestyle Tips")
        for tip in result.get("lifestyle_tips", []):
            st.markdown(f'<div class="advice-box" style="padding:12px 16px;margin:6px 0;">✨ {tip}</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 🚨 Red Flags — Seek Immediate Care If:")
        for flag in result.get("red_flags", []):
            st.markdown(f'<div class="warning-box">🚩 {flag}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
<div class="warning-box">
  <b>Always go to the ER or call emergency services if you experience:</b><br/>
  • Difficulty breathing or chest pain<br/>
  • Sudden severe headache or vision loss<br/>
  • Facial drooping, arm weakness, or slurred speech<br/>
  • Uncontrolled bleeding or loss of consciousness<br/>
  • Severe allergic reaction (throat swelling, hives, dizziness)
</div>
""", unsafe_allow_html=True)

    with tab5:
        st.markdown("### ❓ Questions to Ask Your Doctor")
        st.caption("*Bring this list to your appointment for a more productive consultation*")
        for i, q in enumerate(result.get("questions_for_doctor", []), 1):
            st.markdown(f'<div class="condition-card" style="padding:12px 16px;">❓ {q}</div>', unsafe_allow_html=True)

        # Download report
        st.markdown("<br>", unsafe_allow_html=True)
        report_lines = [
            "AI SYMPTOM CHECKER REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 50,
            f"\nSYMPTOMS: {symptoms}",
            f"DURATION: {duration}",
            f"SEVERITY: {severity}/10",
            f"URGENCY: {urgency}",
            f"\nSUMMARY:\n{result.get('summary','')}",
            "\nPOSSIBLE CONDITIONS:",
        ]
        for c in conditions:
            report_lines.append(f"  - {c['name']} ({c['likelihood']} likelihood): {c['description']}")
        report_lines += [
            f"\nSPECIALISTS: {', '.join(specialists)}",
            "\nIMMEDIATE ACTIONS:",
        ]
        for a in result.get("immediate_actions", []):
            report_lines.append(f"  - {a}")
        report_lines += [
            "\nRED FLAGS:",
        ]
        for f in result.get("red_flags", []):
            report_lines.append(f"  - {f}")
        report_lines.append("\n" + "="*50)
        report_lines.append("DISCLAIMER: This report is for educational purposes only.")
        report_lines.append("It is NOT medical advice. Always consult a licensed healthcare professional.")

        st.download_button(
            "⬇️ Download Full Report (.txt)",
            data="\n".join(report_lines),
            file_name=f"symptom_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # Footer disclaimer
    st.markdown("""
<div style="background:#0f0800;border:1px solid #7c2d12;border-radius:8px;padding:14px 18px;margin-top:20px;font-size:12px;color:#fdba74;">
  ⚠️ <b>DISCLAIMER:</b> This AI symptom checker is for <b>educational purposes only</b>.
  It does not provide medical advice, diagnosis, or treatment recommendations.
  The information provided should never replace professional medical consultation.
  Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.
</div>
""", unsafe_allow_html=True)

else:
    st.markdown("""
<div style="text-align:center;padding:50px 20px;">
  <div style="font-size:64px;margin-bottom:16px;">🏥</div>
  <h3 style="color:#475569;">Describe your symptoms above to get started</h3>
  <p style="color:#334155;font-size:14px;max-width:540px;margin:0 auto 24px;">
    Enter your symptoms in detail — the more specific you are, the better the educational analysis.
    This tool helps you understand possible conditions and know when to seek medical care.
  </p>
</div>
""", unsafe_allow_html=True)

    # Show example symptom sets
    st.markdown("**💡 Click an example to try:**")
    cols = st.columns(2)
    for i, ex in enumerate(SYMPTOM_EXAMPLES):
        with cols[i % 2]:
            if st.button(f"📋 {ex}", key=f"main_ex_{i}"):
                st.session_state["symptoms_input"] = ex
                st.rerun()
