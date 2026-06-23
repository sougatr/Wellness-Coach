"""
MetWell — Layer 3: Personalised Wellness Recommendations
=========================================================
Maps metabolic risk outputs (from Layer 1 session state) to evidence-based:
  - Nutraceutical / supplement recommendations
  - Yoga asana protocols
  - Mudra therapy

Called from wellness_app.py as a third page: "My Wellness Plan"
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Evidence-based supplement database
# Each entry: name, dose, mechanism, evidence_level, domains, cautions
# ---------------------------------------------------------------------------

SUPPLEMENTS = {
    "berberine": {
        "name": "Berberine",
        "indian_name": "Daruharidra (Berberis aristata)",
        "dose": "500 mg three times daily with meals",
        "mechanism": "Activates AMPK pathway (similar to metformin) — improves insulin sensitivity, reduces triglycerides and fasting glucose",
        "evidence": "★★★★☆",
        "evidence_label": "Strong — multiple RCTs & meta-analyses",
        "domains": ["tyg", "egdr", "fib4"],
        "cautions": "May interact with metformin or other glucose-lowering medications — discuss with your doctor if diabetic",
        "color": "#028090",
    },
    "omega3": {
        "name": "Omega-3 (EPA/DHA)",
        "indian_name": "Fish oil / Flaxseed oil (ALA, less potent)",
        "dose": "2–4 g/day EPA-rich formulation; 1 g/day for general CV protection",
        "mechanism": "Reduces triglycerides, lowers VLDL, anti-inflammatory, improves endothelial function",
        "evidence": "★★★★★",
        "evidence_label": "Highest — included in international CV guidelines",
        "domains": ["ascvd"],
        "cautions": "High doses (>3 g/day) may affect bleeding — discuss if on aspirin or anticoagulants",
        "color": "#00A896",
    },
    "vitamin_d": {
        "name": "Vitamin D3",
        "indian_name": "Vitamin D3 (Cholecalciferol)",
        "dose": "1000–2000 IU/day (supplement to serum level; target >30 ng/mL)",
        "mechanism": "Improves insulin receptor sensitivity, reduces fasting glucose and HOMA-IR — deficiency near-universal in Indian urban adults",
        "evidence": "★★★★☆",
        "evidence_label": "Strong — meta-analysis of 39 RCTs in T2DM",
        "domains": ["tyg", "egdr", "ascvd"],
        "cautions": "Check 25-OH-D levels before supplementing; avoid >4000 IU/day without supervision",
        "color": "#02C39A",
    },
    "magnesium": {
        "name": "Magnesium",
        "indian_name": "Magnesium (glycinate or malate preferred)",
        "dose": "200–400 mg/day",
        "mechanism": "Cofactor in insulin signalling; deficiency common in South Asian diets and independently worsens insulin resistance",
        "evidence": "★★★☆☆",
        "evidence_label": "Moderate — multiple meta-analyses, especially in deficient populations",
        "domains": ["tyg", "egdr"],
        "cautions": "GI discomfort at high doses — magnesium glycinate is better tolerated than oxide",
        "color": "#028090",
    },
    "silymarin": {
        "name": "Silymarin (Milk Thistle)",
        "indian_name": "Dugdhapheni / Milk Thistle",
        "dose": "140–280 mg twice daily (standardised to 70–80% silymarin)",
        "mechanism": "Hepatoprotective — reduces ALT/AST, improves liver steatosis, anti-inflammatory and antioxidant in liver tissue",
        "evidence": "★★★★☆",
        "evidence_label": "Strong — multiple RCTs in NAFLD/NASH",
        "domains": ["fib4"],
        "cautions": "Generally well tolerated; rare GI upset",
        "color": "#02C39A",
    },
    "vitamin_e": {
        "name": "Vitamin E (α-tocopherol)",
        "indian_name": "Vitamin E",
        "dose": "800 IU/day",
        "mechanism": "Antioxidant — reduces hepatic oxidative stress, improves NASH histology",
        "evidence": "★★★★☆",
        "evidence_label": "Recommended by AASLD guidelines for non-diabetic NASH",
        "domains": ["fib4"],
        "cautions": "⚠️ Avoid in diabetics with high CV risk (AASLD caution). Avoid >800 IU/day long-term",
        "color": "#00A896",
    },
    "coq10": {
        "name": "Coenzyme Q10 (CoQ10)",
        "indian_name": "Ubiquinol / CoQ10",
        "dose": "100–200 mg/day (ubiquinol form preferred)",
        "mechanism": "Mitochondrial energy production, antioxidant — statins deplete CoQ10; improves adipokine profile and reduces inflammatory markers in MetS",
        "evidence": "★★★☆☆",
        "evidence_label": "Moderate — meta-analysis in metabolic syndrome",
        "domains": ["ascvd"],
        "cautions": "Particularly important if on statin therapy",
        "color": "#028090",
    },
    "berberis": {
        "name": "Ashwagandha",
        "indian_name": "Withania somnifera (KSM-66 extract)",
        "dose": "300–600 mg/day (standardised KSM-66 root extract)",
        "mechanism": "AMPK/p38MAPK activation; cortisol reduction; anti-adipogenic; anti-stress — particularly relevant when high stress co-exists with insulin resistance",
        "evidence": "★★★☆☆",
        "evidence_label": "Emerging — pre-clinical strong; human RCTs growing",
        "domains": ["tyg", "egdr", "stress"],
        "cautions": "Avoid in autoimmune conditions; not for use in pregnancy",
        "color": "#02C39A",
    },
    "fenugreek": {
        "name": "Fenugreek",
        "indian_name": "Methi (Trigonella foenum-graecum)",
        "dose": "5–10 g seeds daily or 1 g standardised extract",
        "mechanism": "Slows glucose absorption; improves fasting and postprandial glucose; soluble fibre (galactomannan) reduces glycaemic index of meals",
        "evidence": "★★★☆☆",
        "evidence_label": "Moderate — double-blind RCT evidence for FBG and PPG",
        "domains": ["tyg", "egdr"],
        "cautions": "May enhance glucose-lowering effect of diabetes medications",
        "color": "#028090",
    },
    "betaine": {
        "name": "Betaine (Trimethylglycine)",
        "indian_name": "Betaine",
        "dose": "500–1500 mg/day",
        "mechanism": "Enhances hepatic lipid metabolism, reduces homocysteine, decreases hepatic oxidative stress in MASLD",
        "evidence": "★★★☆☆",
        "evidence_label": "Moderate — RCT evidence in NAFLD",
        "domains": ["fib4"],
        "cautions": "Generally well tolerated; may cause fishy odour at high doses",
        "color": "#00A896",
    },
    "plant_sterols": {
        "name": "Plant Sterols / Stanols",
        "indian_name": "Plant Sterols (fortified foods or supplements)",
        "dose": "2–3 g/day with meals",
        "mechanism": "Competitively inhibit cholesterol absorption in the gut — LDL reduction 8–10%",
        "evidence": "★★★★★",
        "evidence_label": "Highest — included in ESC/EAS dyslipidaemia guidelines",
        "domains": ["ascvd"],
        "cautions": "Take with fatty meals for best absorption",
        "color": "#028090",
    },
}

# ---------------------------------------------------------------------------
# Yoga / Mudra database
# ---------------------------------------------------------------------------

YOGA_PROTOCOLS = {
    "insulin_resistance": {
        "label": "Insulin Resistance & Metabolic",
        "asanas": [
            {
                "name": "Surya Namaskar",
                "sanskrit": "सूर्य नमस्कार",
                "description": "12-step sun salutation — full-body dynamic sequence that activates multiple muscle groups, improves glucose uptake",
                "duration": "6–12 rounds daily (10–20 min)",
                "evidence": "Improves fasting glucose, BMI, and insulin sensitivity — RCT evidence in T2DM",
            },
            {
                "name": "Mandukasana",
                "sanskrit": "मण्डूकासन",
                "description": "Frog pose — compresses the abdominal region and directly stimulates the pancreas",
                "duration": "Hold 30 sec × 3 sets",
                "evidence": "Traditional — pancreatic stimulation; abdominal compression improves portal circulation",
            },
            {
                "name": "Dhanurasana",
                "sanskrit": "धनुरासन",
                "description": "Bow pose — stretches the entire anterior trunk, stimulates liver, pancreas and adrenal glands",
                "duration": "Hold 20–30 sec × 3 sets",
                "evidence": "Abdominal visceral pressure — reduces visceral adiposity with practice",
            },
            {
                "name": "Paschimottanasana",
                "sanskrit": "पश्चिमोत्तानासन",
                "description": "Seated forward bend — massages abdominal organs, improves flexibility and parasympathetic tone",
                "duration": "Hold 30–60 sec × 3 sets",
                "evidence": "Parasympathetic activation reduces cortisol and sympathetic metabolic dysregulation",
            },
        ],
        "mudras": [
            {
                "name": "Surya Mudra",
                "sanskrit": "सूर्य मुद्रा",
                "description": "Ring finger bent to base of thumb, thumb pressing on it. Activates fire element — boosts metabolism and fat burning",
                "duration": "15 min twice daily",
                "icon": "🔥",
            },
            {
                "name": "Apana Mudra",
                "sanskrit": "अपान मुद्रा",
                "description": "Middle and ring fingers touch tip of thumb. Regulates downward energy — supports pancreatic function and glucose regulation",
                "duration": "15 min twice daily",
                "icon": "🌿",
            },
        ],
    },
    "cardiovascular": {
        "label": "Cardiovascular & ASCVD",
        "asanas": [
            {
                "name": "Anulom Vilom Pranayama",
                "sanskrit": "अनुलोम विलोम",
                "description": "Alternate nostril breathing — balances sympathetic/parasympathetic tone, significantly reduces systolic BP",
                "duration": "10–15 min daily (morning fasting preferred)",
                "evidence": "RCT evidence: reduces SBP by 8–10 mmHg with 3-month practice",
            },
            {
                "name": "Shavasana",
                "sanskrit": "शवासन",
                "description": "Corpse pose — deep relaxation reduces cortisol, lowers heart rate and blood pressure",
                "duration": "10–15 min daily",
                "evidence": "Proven autonomic modulation — reduces resting HR and BP",
            },
            {
                "name": "Trikonasana",
                "sanskrit": "त्रिकोणासन",
                "description": "Triangle pose — opens chest, improves circulation, stretches lateral trunk and intercostal muscles",
                "duration": "Hold 30 sec each side × 3",
                "evidence": "Improves HDL and overall lipid profile with regular practice",
            },
            {
                "name": "Bhramari Pranayama",
                "sanskrit": "भ्रामरी प्राणायाम",
                "description": "Humming bee breath — powerful vagal stimulator; reduces anxiety, stress hormones and BP",
                "duration": "5–10 min daily",
                "evidence": "Strong parasympathetic activation; reduces cortisol and inflammatory markers",
            },
        ],
        "mudras": [
            {
                "name": "Apana Vayu Mudra",
                "sanskrit": "अपान वायु मुद्रा",
                "description": "Index finger to base of thumb, middle and ring fingers touch thumb tip, little finger extended. The 'heart mudra' — used traditionally for cardiac support and acute cardiac events",
                "duration": "15 min twice daily, especially morning",
                "icon": "❤️",
            },
            {
                "name": "Prana Mudra",
                "sanskrit": "प्राण मुद्रा",
                "description": "Ring and little fingers touch thumb tip. Activates life force — improves circulation and reduces fatigue",
                "duration": "15 min daily",
                "icon": "⚡",
            },
        ],
    },
    "liver": {
        "label": "Liver Health & FIB-4",
        "asanas": [
            {
                "name": "Ardha Matsyendrasana",
                "sanskrit": "अर्ध मत्स्येन्द्रासन",
                "description": "Half spinal twist — compresses and releases the liver and spleen, stimulates bile production and detoxification",
                "duration": "Hold 30 sec each side × 3",
                "evidence": "Traditional hepatic massage — improves portal circulation",
            },
            {
                "name": "Bhujangasana",
                "sanskrit": "भुजंगासन",
                "description": "Cobra pose — stretches the abdomen and stimulates liver and kidneys through anterior trunk extension",
                "duration": "Hold 20–30 sec × 3",
                "evidence": "Abdominal organ stretch improves hepatic blood flow",
            },
            {
                "name": "Naukasana",
                "sanskrit": "नौकासन",
                "description": "Boat pose — strengthens core and abdominal muscles; reduces visceral adiposity which directly improves MASLD",
                "duration": "Hold 20–30 sec × 3",
                "evidence": "Core strengthening reduces visceral fat — primary MASLD driver",
            },
        ],
        "mudras": [
            {
                "name": "Apana Mudra",
                "sanskrit": "अपान मुद्रा",
                "description": "Middle and ring fingers touch tip of thumb. Supports liver detox pathways and regulates downward elimination",
                "duration": "15 min twice daily",
                "icon": "🌿",
            },
            {
                "name": "Varun Mudra",
                "sanskrit": "वरुण मुद्रा",
                "description": "Little finger touches thumb tip. Activates water element — supports liver hydration and bile flow",
                "duration": "15 min daily",
                "icon": "💧",
            },
        ],
    },
    "stress_sleep": {
        "label": "Stress, Sleep & Wellness",
        "asanas": [
            {
                "name": "Yoga Nidra",
                "sanskrit": "योग निद्रा",
                "description": "Yogic sleep — systematic body scan and relaxation; 20 min equals 2 hours of sleep in metabolic recovery",
                "duration": "20–30 min before sleep or afternoon",
                "evidence": "Reduces cortisol, improves sleep architecture and insulin sensitivity",
            },
            {
                "name": "Balasana",
                "sanskrit": "बालासन",
                "description": "Child's pose — activates the parasympathetic system immediately; reduces anxiety and cortisol within minutes",
                "duration": "Hold 1–3 min, repeat as needed",
                "evidence": "Immediate parasympathetic activation — reduces acute stress response",
            },
            {
                "name": "Viparita Karani",
                "sanskrit": "विपरीत करणी",
                "description": "Legs-up-the-wall pose — reverses venous pooling, calms the nervous system and prepares the body for sleep",
                "duration": "10–15 min before bed",
                "evidence": "Vagal tone improvement; effective pre-sleep relaxation",
            },
        ],
        "mudras": [
            {
                "name": "Gyan Mudra",
                "sanskrit": "ज्ञान मुद्रा",
                "description": "Index finger touches thumb tip, other fingers extended. The knowledge mudra — reduces anxiety, improves concentration and sleep quality",
                "duration": "15–20 min daily (meditation or pranayama)",
                "icon": "🧘",
            },
            {
                "name": "Shuni Mudra",
                "sanskrit": "शूनि मुद्रा",
                "description": "Middle finger touches thumb tip. Mudra of patience and discipline — calms the mind and builds inner resilience",
                "duration": "15 min daily",
                "icon": "🌙",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Recommendation engine — maps risk tiers to protocols
# ---------------------------------------------------------------------------

def get_supplement_recommendations(risk: dict) -> list:
    recs = []

    # Universal — near-universal deficiency in Indian adults
    recs.append({**SUPPLEMENTS["vitamin_d"], "reason": "Near-universal deficiency in Indian urban adults — improves insulin sensitivity and immune function"})
    recs.append({**SUPPLEMENTS["magnesium"], "reason": "Commonly deficient in South Asian diets — essential cofactor for insulin receptor function"})

    # TyG / eGDR (insulin resistance)
    tyg_flag = risk.get("tyg_tier") in ["AMBER", "RED"]
    egdr_flag = risk.get("egdr_tier") in ["AMBER", "RED"]
    if tyg_flag or egdr_flag:
        recs.append({**SUPPLEMENTS["berberine"], "reason": "Your insulin resistance markers are elevated — berberine has the strongest nutraceutical evidence for improving TyG and HOMA-IR"})
        recs.append({**SUPPLEMENTS["fenugreek"], "reason": "Indian herb with RCT evidence for improving fasting and post-meal glucose — directly addresses TyG index components"})
        if risk.get("stress_t") in ["AMBER", "RED"]:
            recs.append({**SUPPLEMENTS["berberis"], "reason": "High stress combined with insulin resistance — ashwagandha addresses both the cortisol-driven metabolic disruption and stress directly"})

    # ASCVD
    if risk.get("ascvd_tier") in ["AMBER", "RED"]:
        recs.append({**SUPPLEMENTS["omega3"], "reason": "Your ASCVD risk is elevated — omega-3 EPA/DHA directly reduces triglycerides and cardiovascular event risk"})
        recs.append({**SUPPLEMENTS["plant_sterols"], "reason": "Plant sterols are the only nutraceutical in ESC/EAS dyslipidaemia guidelines — reduces LDL by 8–10% without medication"})
        recs.append({**SUPPLEMENTS["coq10"], "reason": "Supports cardiovascular mitochondrial function; essential if already on statin therapy"})

    # FIB-4 / Liver
    if risk.get("fib4_tier") in ["AMBER", "RED"]:
        recs.append({**SUPPLEMENTS["silymarin"], "reason": "Your FIB-4 liver fibrosis score is elevated — silymarin is the best-evidenced hepatoprotective nutraceutical"})
        recs.append({**SUPPLEMENTS["betaine"], "reason": "Betaine improves hepatic lipid handling and reduces oxidative stress in fatty liver disease"})
        if not risk.get("has_diabetes"):
            recs.append({**SUPPLEMENTS["vitamin_e"], "reason": "Vitamin E is recommended by AASLD guidelines for non-diabetic NASH — directly improves liver histology"})

    # Deduplicate by name
    seen = set()
    unique = []
    for r in recs:
        if r["name"] not in seen:
            seen.add(r["name"])
            unique.append(r)

    return unique


def get_yoga_recommendations(risk: dict) -> list:
    protocols = []

    tyg_flag = risk.get("tyg_tier") in ["AMBER", "RED"]
    egdr_flag = risk.get("egdr_tier") in ["AMBER", "RED"]
    ascvd_flag = risk.get("ascvd_tier") in ["AMBER", "RED"]
    fib4_flag = risk.get("fib4_tier") in ["AMBER", "RED"]
    stress_flag = risk.get("stress_t") in ["AMBER", "RED"]
    sleep_flag = risk.get("sleep_t") in ["AMBER", "RED"]

    if tyg_flag or egdr_flag or risk.get("adiposity_tier") in ["AMBER", "RED"]:
        protocols.append(YOGA_PROTOCOLS["insulin_resistance"])

    if ascvd_flag or risk.get("ascvd_tier") == "GREEN":  # always beneficial for CV
        protocols.append(YOGA_PROTOCOLS["cardiovascular"])

    if fib4_flag:
        protocols.append(YOGA_PROTOCOLS["liver"])

    if stress_flag or sleep_flag or risk.get("wellness_t") in ["AMBER", "RED"]:
        protocols.append(YOGA_PROTOCOLS["stress_sleep"])

    # If nothing flagged, give general wellness protocol
    if not protocols:
        protocols = [YOGA_PROTOCOLS["cardiovascular"], YOGA_PROTOCOLS["stress_sleep"]]

    return protocols


# ---------------------------------------------------------------------------
# Streamlit UI — Layer 3
# ---------------------------------------------------------------------------

TIER_COLORS = {
    "GREEN": ("#d1f0e0", "#028090", "🟢"),
    "AMBER": ("#fff3cd", "#856404", "🟡"),
    "RED": ("#fde8e8", "#c0392b", "🔴"),
}


def render_layer3():
    st.header("🌿 My Wellness Plan")
    st.caption("Evidence-based supplement and yoga/mudra recommendations personalised to your MetWell results.")

    risk = st.session_state.get("risk_results")

    if not risk:
        st.info(
            "Complete your **MetaWell Check** first to get personalised recommendations. "
            "Your risk profile will automatically populate this page."
        )
        if st.button("Go to MetaWell Check"):
            st.session_state["_page"] = "MetaWell Check"
            st.rerun()
        return

    # --- Summary ribbon ---
    final = risk.get("final_tier", "GREEN")
    bg, fg, icon = TIER_COLORS[final]
    st.markdown(
        f"""
        <div style='background:{bg}; border-left: 4px solid {fg}; padding: 12px 18px;
             border-radius: 6px; margin-bottom: 16px;'>
            <span style='font-size:1.1rem; font-weight:600; color:{fg};'>
                {icon} Overall tier: {final}
            </span>
            <span style='color:#444; margin-left:16px; font-size:0.95rem;'>
                Recommendations below are tailored to your specific risk profile.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Risk summary chips ---
    chips = []
    if risk.get("tyg_tier"):
        t = risk["tyg_tier"]
        chips.append((f"TyG: {risk['tyg']:.2f}", t))
    if risk.get("egdr_tier"):
        t = risk["egdr_tier"]
        chips.append((f"eGDR: {risk['egdr']:.1f}", t))
    if risk.get("ascvd_tier"):
        t = risk["ascvd_tier"]
        chips.append((f"ASCVD: {risk['ascvd']:.1f}%", t))
    if risk.get("fib4_tier"):
        t = risk["fib4_tier"]
        chips.append((f"FIB-4: {risk['fib4']:.2f}", t))

    if chips:
        chip_html = "<div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;'>"
        for label, tier in chips:
            bg2, fg2, ico = TIER_COLORS[tier]
            chip_html += (
                f"<span style='background:{bg2}; color:{fg2}; border:1px solid {fg2}; "
                f"padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600;'>"
                f"{ico} {label}</span>"
            )
        chip_html += "</div>"
        st.markdown(chip_html, unsafe_allow_html=True)

    st.divider()

    # ===================================================================
    # TAB 1 — Supplements  |  TAB 2 — Yoga & Mudras
    # ===================================================================
    tab1, tab2 = st.tabs(["💊 Nutraceuticals & Supplements", "🧘 Yoga & Mudra Therapy"])

    with tab1:
        _render_supplements(risk)

    with tab2:
        _render_yoga(risk)

    st.divider()
    st.caption(
        "⚕️ **Medical disclaimer:** These recommendations are for general wellness "
        "awareness and are not a substitute for personalised medical advice. "
        "Always discuss supplements with your doctor before starting, especially "
        "if you are on medication for diabetes, hypertension, or cardiovascular disease."
    )


def _render_supplements(risk: dict):
    supplements = get_supplement_recommendations(risk)

    st.markdown("### Your personalised supplement stack")
    st.caption(
        f"Based on your risk profile, {len(supplements)} supplements are recommended. "
        "Priority is shown by evidence rating (★ = stronger evidence)."
    )

    # Sort by evidence rating length (more stars = higher priority)
    supplements.sort(key=lambda x: x.get("evidence", ""), reverse=True)

    for s in supplements:
        color = s.get("color", "#028090")
        with st.container():
            st.markdown(
                f"""
                <div style='border-left: 4px solid {color}; padding: 10px 16px;
                     background:#f8fffe; border-radius:0 8px 8px 0; margin-bottom: 12px;'>
                    <div style='font-size:1.05rem; font-weight:700; color:#1a2e35;'>
                        {s['name']}
                        <span style='font-weight:400; font-size:0.85rem; color:#555; margin-left:8px;'>
                            {s.get('indian_name', '')}
                        </span>
                    </div>
                    <div style='color:{color}; font-size:0.88rem; margin:3px 0 6px;'>
                        {s['evidence']} &nbsp; {s['evidence_label']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Why for you:** {s['reason']}")
                st.markdown(f"**Dose:** {s['dose']}")
            with col2:
                st.markdown(f"**How it works:** {s['mechanism']}")
                if s.get("cautions"):
                    st.warning(f"⚠️ {s['cautions']}", icon=None)
            st.divider()


def _render_yoga(risk: dict):
    protocols = get_yoga_recommendations(risk)

    st.markdown("### Your personalised yoga & mudra protocol")
    st.caption(
        "Protocols are matched to your risk domains. Start with 2–3 practices "
        "and build gradually. Ideally practice in the morning on an empty stomach."
    )

    for protocol in protocols:
        color_map = {
            "Insulin Resistance & Metabolic": "#028090",
            "Cardiovascular & ASCVD": "#c0392b",
            "Liver Health & FIB-4": "#02C39A",
            "Stress, Sleep & Wellness": "#6c63a3",
        }
        pcolor = color_map.get(protocol["label"], "#028090")

        st.markdown(
            f"""
            <div style='background:linear-gradient(135deg, {pcolor}18, {pcolor}08);
                 border: 1px solid {pcolor}40; border-radius:10px;
                 padding: 12px 18px; margin: 10px 0 6px;'>
                <span style='font-size:1.1rem; font-weight:700; color:{pcolor};'>
                    {protocol['label']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Asanas
        st.markdown("**Yoga Asanas:**")
        for a in protocol["asanas"]:
            with st.expander(f"🧘 {a['name']} — {a['sanskrit']}"):
                st.markdown(f"**What:** {a['description']}")
                st.markdown(f"**Duration:** {a['duration']}")
                if a.get("evidence"):
                    st.caption(f"📚 Evidence: {a['evidence']}")

        # Mudras
        st.markdown("**Mudra Therapy:**")
        mudra_cols = st.columns(len(protocol["mudras"]))
        for i, m in enumerate(protocol["mudras"]):
            with mudra_cols[i]:
                st.markdown(
                    f"""
                    <div style='background:#f0fafa; border:1px solid {pcolor}50;
                         border-radius:10px; padding:14px; text-align:center;'>
                        <div style='font-size:2rem;'>{m['icon']}</div>
                        <div style='font-weight:700; color:{pcolor}; margin:6px 0 2px;'>{m['name']}</div>
                        <div style='font-size:0.8rem; color:#777; margin-bottom:6px;'>{m['sanskrit']}</div>
                        <div style='font-size:0.87rem; color:#333;'>{m['description']}</div>
                        <div style='margin-top:8px; font-size:0.82rem; color:{pcolor}; font-weight:600;'>
                            ⏱ {m['duration']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
