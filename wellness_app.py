import os
import math
import streamlit as st

# ----------------------------------------------------------------------
# Wellness Coach — Combined App (Stage B)
#   Two linked modes:
#     "Get My Wellness Plan" -> questionnaire + calculations + auto plan
#     "Ask a Question"       -> profile-aware grounded Q&A
#   The profile filled on the plan page is remembered and used to
#   personalise both the auto-plan and any questions asked.
# ----------------------------------------------------------------------

st.set_page_config(page_title="Wellness Coach", layout="wide")

DISCLAIMER = (
    "This is general wellness guidance based on the provided guidelines, "
    "not personalised medical advice. Please consult your doctor for any "
    "medical decisions, diagnosis, or treatment."
)


# ---------------------------------------------------------------
# Shared engine loader (cached, loaded once)
# ---------------------------------------------------------------
@st.cache_resource
def load_engine():
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.google_genai import GoogleGenAI

    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
    Settings.llm = GoogleGenAI(model="gemma-4-26b-a4b-it", api_key=api_key)
    docs = SimpleDirectoryReader(".", required_exts=[".pdf", ".html"]).load_data()
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine(
    similarity_top_k=5,
    response_mode="tree_summarize",
)


# ---------------------------------------------------------------
# Calculation helpers (pure functions)
# ---------------------------------------------------------------
def calc_bmi(weight_kg, height_cm):
    if weight_kg and height_cm:
        h = height_cm / 100.0
        return round(weight_kg / (h * h), 1)
    return None


def bmi_band(bmi):
    if bmi is None:
        return "—"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calc_whr(waist_cm, hip_cm):
    if waist_cm and hip_cm:
        return round(waist_cm / hip_cm, 2)
    return None


def calc_whtr(waist_cm, height_cm):
    if waist_cm and height_cm:
        return round(waist_cm / height_cm, 2)
    return None


def calc_tyg(triglycerides, glucose):
    if triglycerides and glucose and triglycerides > 0 and glucose > 0:
        return round(math.log((triglycerides * glucose) / 2.0), 2)
    return None


def waist_flag(waist_cm, sex):
    if not waist_cm:
        return None
    cutoff = 90 if sex == "Male" else 80
    return "Elevated" if waist_cm >= cutoff else "Normal"


def whr_flag(whr, sex):
    if whr is None:
        return None
    cutoff = 0.90 if sex == "Male" else 0.85
    return "Elevated" if whr >= cutoff else "Normal"


def whtr_flag(whtr):
    if whtr is None:
        return None
    return "Elevated" if whtr >= 0.5 else "Normal"


def tyg_flag(tyg):
    if tyg is None:
        return None
    return "Elevated" if tyg >= 8.5 else "Normal"


FFQ_POINTS = {"Never": 0, "Monthly": 1, "Weekly": 2, "Several times a week": 3, "Daily": 4}

FFQ_ITEMS = [
    "Biscuits / cookies", "Namkeen / chips / savoury snacks", "Instant noodles",
    "Packaged bread / buns", "Colas / soft drinks", "Packaged fruit juices",
    "Chocolates / candies", "Ice cream", "Cakes / pastries",
    "Sweetened breakfast cereals", "Processed / cured meats", "Ketchup / sauces",
    "Deep-fried street food (samosa, pakora, vada)", "Mithai / Indian sweets",
    "Bakery items (puffs, rusks)", "Sugar in tea / coffee", "Energy drinks",
    "Processed cheese", "Flavoured / sweetened yoghurt", "Packaged instant soups",
]


def ffq_band(total, max_total):
    if max_total == 0:
        return "—", 0
    pct = total / max_total
    if pct < 0.33:
        return "Low", pct
    if pct < 0.66:
        return "Moderate", pct
    return "High", pct


# ---------------------------------------------------------------
# Build a readable profile summary string (used in prompts + display)
# ---------------------------------------------------------------
def build_profile_summary(p):
    if not p:
        return ""
    bmi = calc_bmi(p.get("weight_kg"), p.get("height_cm"))
    waist = p.get("waist_cm") if p.get("waist_cm", 0) > 0 else None
    hip = p.get("hip_cm") if p.get("hip_cm", 0) > 0 else None
    whr = calc_whr(waist, hip)
    whtr = calc_whtr(waist, p.get("height_cm"))
    tg = p.get("triglycerides") if p.get("triglycerides", 0) > 0 else None
    glu = p.get("fasting_glucose") if p.get("fasting_glucose", 0) > 0 else None
    tyg = calc_tyg(tg, glu)

    lines = []
    lines.append(f"Age: {int(p.get('age', 0))}, Sex: {p.get('sex', '')}")
    if bmi:
        lines.append(f"BMI: {bmi} ({bmi_band(bmi)})")
    if waist:
        lines.append(f"Waist: {waist} cm ({waist_flag(waist, p.get('sex'))})")
    if whr:
        lines.append(f"Waist-Hip Ratio: {whr} ({whr_flag(whr, p.get('sex'))})")
    if whtr:
        lines.append(f"Waist-Height Ratio: {whtr} ({whtr_flag(whtr)})")
    if tyg:
        lines.append(f"TyG Index: {tyg} ({tyg_flag(tyg)} for insulin resistance)")
    if p.get("diet_type"):
        lines.append(f"Diet type: {p.get('diet_type')}")
    if p.get("foods_liked"):
        lines.append(f"Likes: {', '.join(p.get('foods_liked'))}")
    if p.get("daily_pattern"):
        lines.append(f"Typical eating: {p.get('daily_pattern')}")
    if p.get("restrictions"):
        lines.append(f"Restrictions: {', '.join(p.get('restrictions'))}")
    if p.get("activity_type"):
        lines.append(
            f"Activity: {', '.join(p.get('activity_type'))}, "
            f"{p.get('activity_days', 0)} days/week, "
            f"{p.get('activity_minutes', 0)} min/session"
        )
    lines.append(f"Work: {p.get('work_type', '')}")
    if p.get("intermittent_fasting") == "Yes":
        lines.append(f"Intermittent fasting: Yes ({p.get('if_hours', '?')} h window)")
    lines.append(
        f"Sleep: {p.get('sleep_hours', 0)} h ({p.get('sleep_quality', '')}), "
        f"Water: {p.get('water_glasses', 0)} glasses/day, "
        f"Stress: {p.get('stress', '')}"
    )
    smoke = p.get("smoking", "")
    if smoke == "Current":
        smoke += f" ({p.get('smoking_qty', '?')}/day)"
    alc = p.get("alcohol", "")
    if alc == "Regular":
        alc += f" ({p.get('alcohol_qty', '?')}/week)"
    lines.append(f"Smoking: {smoke}, Alcohol: {alc}")
    if p.get("conditions"):
        cond = ', '.join(p.get('conditions'))
        if p.get("htn_meds"):
            cond += f" (HTN meds: {p.get('htn_meds')})"
        lines.append(f"Conditions: {cond}")
    if p.get("goals"):
        lines.append(f"Goals: {', '.join(p.get('goals'))}")
    if p.get("ffq_band"):
        lines.append(f"Ultra-processed/HFSS food intake: {p.get('ffq_band')}")
    return "\n".join(lines)


# ---------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------
st.sidebar.title("Wellness Coach")
page = st.sidebar.radio("Choose:", ["Get My Wellness Plan", "Ask a Question"])

# show profile status in sidebar
if st.session_state.get("profile"):
    st.sidebar.success(f"Profile loaded: {st.session_state['profile'].get('name', 'user')}")
else:
    st.sidebar.info("No profile yet. Fill 'Get My Wellness Plan' first for personalised answers.")


# ===============================================================
# PAGE — GET MY WELLNESS PLAN
# ===============================================================
if page == "Get My Wellness Plan":
    st.title("Get My Wellness Plan")
    st.caption("Tell us about yourself — your details stay in this session only (prototype).")

    profile = {}

    st.header("1. About You")
    c1, c2, c3 = st.columns(3)
    profile["name"] = c1.text_input("Name (abbreviation / optional)")
    profile["email"] = c2.text_input("Email (optional)")
    profile["age"] = c3.number_input("Age *", min_value=0, max_value=120, value=40, step=1)
    profile["sex"] = st.radio("Sex", ["Male", "Female", "Other"], horizontal=True)

    st.header("2. Physical Parameters")
    c1, c2 = st.columns(2)
    profile["height_cm"] = c1.number_input("Height (cm) *", min_value=0.0, max_value=250.0, value=165.0, step=0.5)
    profile["weight_kg"] = c2.number_input("Weight (kg) *", min_value=0.0, max_value=300.0, value=70.0, step=0.5)
    c1, c2 = st.columns(2)
    profile["waist_cm"] = c1.number_input("Waist (cm) — optional", min_value=0.0, max_value=200.0, value=0.0, step=0.5)
    profile["hip_cm"] = c2.number_input("Hip (cm) — optional", min_value=0.0, max_value=200.0, value=0.0, step=0.5)

    st.header("3. Diet")
    st.write("**Foods you like to eat** — pick your top 5 in descending order of liking (1 = most liked). Leave blank if fewer.")
    food_options = ["", "Fruits", "Vegetables", "Whole grains", "Dairy", "Red meat", "Poultry",
                    "Fish", "Eggs", "Fried or fast food", "Sweets and desserts",
                    "Sugary drinks", "Nuts and seeds", "Pulses and legumes"]
    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    food_ranked = [
        fc1.selectbox("1st", food_options, key="food1"),
        fc2.selectbox("2nd", food_options, key="food2"),
        fc3.selectbox("3rd", food_options, key="food3"),
        fc4.selectbox("4th", food_options, key="food4"),
        fc5.selectbox("5th", food_options, key="food5"),
    ]
    profile["foods_liked"] = [f for f in food_ranked if f]
    profile["diet_type"] = st.radio(
        "Dietary type", ["Vegetarian", "Non-vegetarian", "Eggetarian", "Vegan"], horizontal=True
    )
    profile["daily_pattern"] = st.text_area(
        "Describe what you usually eat in breakfast, lunch and dinner (specify approximate quantity)"
    )
    profile["restrictions"] = st.multiselect(
        "Restrictions or allergies",
        ["None", "Diabetic diet", "Gluten-free", "Lactose intolerant", "Nut allergy", "Other"],
    )

    st.header("4. Physical Activity")
    profile["activity_type"] = st.multiselect(
        "Type of activity",
        ["None", "Walking", "Running", "Gym or weights", "Yoga", "Swimming",
         "Cycling", "Golf", "Football", "Hockey", "Basketball", "Squash",
         "Badminton", "Tennis", "Other"],
    )
    c1, c2 = st.columns(2)
    profile["activity_days"] = c1.number_input("Days per week", min_value=0, max_value=7, value=3, step=1)
    profile["activity_minutes"] = c2.number_input("Minutes per session", min_value=0, max_value=300, value=30, step=5)
    profile["intermittent_fasting"] = st.radio(
        "Do you practise intermittent fasting?", ["No", "Yes"], horizontal=True
    )
    if profile["intermittent_fasting"] == "Yes":
        profile["if_hours"] = st.number_input("If yes, for how many hours (fasting window)?", min_value=0, max_value=24, value=16, step=1)

    st.header("5. Work & Lifestyle")
    profile["work_type"] = st.radio(
        "Work type",
        ["Desk / sedentary", "Standing", "Physically active", "Shift work", "Mixed"],
    )
    c1, c2 = st.columns(2)
    profile["sleep_hours"] = c1.number_input("Sleep (hours per night)", min_value=0.0, max_value=16.0, value=7.0, step=0.5)
    profile["sleep_quality"] = c2.radio("Sleep quality", ["Good", "Fair", "Poor"], horizontal=True)
    c1, c2 = st.columns(2)
    profile["water_glasses"] = c1.number_input("Water (glasses per day)", min_value=0, max_value=30, value=6, step=1)
    profile["stress"] = c2.radio("Stress level", ["Low", "Moderate", "High"], horizontal=True)

    st.header("6. Habits")
    profile["smoking"] = st.radio("Smoking", ["Never", "Former", "Current"], horizontal=True)
    if profile["smoking"] == "Current":
        profile["smoking_qty"] = st.number_input("Cigarettes per day", min_value=0, max_value=100, value=5, step=1)
    profile["alcohol"] = st.radio("Alcohol", ["Never", "Occasional", "Regular"], horizontal=True)
    if profile["alcohol"] == "Regular":
        profile["alcohol_qty"] = st.text_input("Roughly how much per week?")

    st.header("7. Existing Conditions")
    profile["conditions"] = st.multiselect(
        "Select any that apply",
        ["None", "Hypertension", "Type 2 Diabetes", "Pre-diabetes", "High cholesterol",
         "Thyroid disorder", "Heart disease", "PCOS", "Joint or back problems",
         "Anxiety or depression", "Other"],
    )
    if "Type 2 Diabetes" in profile["conditions"] or "Pre-diabetes" in profile["conditions"]:
        c1, c2 = st.columns(2)
        profile["diabetes_meds"] = c1.radio("On diabetes medication?", ["Yes", "No"], horizontal=True)
        profile["last_sugar"] = c2.text_input("Last sugar reading (if known)")
    if "Hypertension" in profile["conditions"]:
        profile["htn_meds"] = st.text_input("For Hypertension — which medicines? (please name them)")

    st.header("8. Your Goals")
    profile["goals"] = st.multiselect(
        "What would you like to achieve?",
        ["Weight loss", "Weight gain", "More energy", "Better sleep",
         "Manage a condition", "Build fitness", "Reduce stress", "General wellbeing"],
    )
    if "Weight loss" in profile["goals"]:
        profile["weight_target"] = st.text_input("Target weight or how much you'd like to lose")

    st.header("9. Advanced Metabolic Markers (optional)")
    st.caption("Needs recent fasting lab values. Leave at 0 to skip.")
    c1, c2 = st.columns(2)
    profile["fasting_glucose"] = c1.number_input("Fasting glucose (mg/dL)", min_value=0.0, max_value=600.0, value=0.0, step=1.0)
    profile["triglycerides"] = c2.number_input("Fasting triglycerides (mg/dL)", min_value=0.0, max_value=2000.0, value=0.0, step=1.0)

    st.header("10. Food Frequency (optional)")
    st.caption("How often do you usually consume each? Helps assess processed-food intake.")
    ffq_responses = {}
    show_ffq = st.checkbox("Fill in the food frequency questionnaire")
    if show_ffq:
        for item in FFQ_ITEMS:
            ffq_responses[item] = st.select_slider(item, options=list(FFQ_POINTS.keys()), value="Never")
    profile["ffq"] = ffq_responses

    st.divider()

    if st.button("Calculate My Profile & Save", type="primary"):
        if True:
            if not profile.get("name"):
                profile["name"] = "User"
            # FFQ band stored into profile
            if show_ffq and ffq_responses:
                total = sum(FFQ_POINTS[v] for v in ffq_responses.values())
                band, pct = ffq_band(total, len(FFQ_ITEMS) * 4)
                profile["ffq_band"] = band
                profile["ffq_total"] = total

            st.session_state["profile"] = profile

            bmi = calc_bmi(profile["weight_kg"], profile["height_cm"])
            waist = profile["waist_cm"] if profile["waist_cm"] > 0 else None
            hip = profile["hip_cm"] if profile["hip_cm"] > 0 else None
            whr = calc_whr(waist, hip)
            whtr = calc_whtr(waist, profile["height_cm"])
            tg = profile["triglycerides"] if profile["triglycerides"] > 0 else None
            glu = profile["fasting_glucose"] if profile["fasting_glucose"] > 0 else None
            tyg = calc_tyg(tg, glu)

            st.subheader("Your Calculated Profile")
            m1, m2, m3 = st.columns(3)
            m1.metric("BMI", bmi if bmi else "—", bmi_band(bmi))
            m2.metric("Waist-Hip Ratio", whr if whr else "—", whr_flag(whr, profile["sex"]) or "—")
            m3.metric("Waist-Height Ratio", whtr if whtr else "—", whtr_flag(whtr) or "—")
            m4, m5, m6 = st.columns(3)
            m4.metric("Waist (cm)", waist if waist else "—", waist_flag(waist, profile["sex"]) or "—")
            m5.metric("TyG Index", tyg if tyg else "—", tyg_flag(tyg) or "—")
            m6.metric("Age", int(profile["age"]))

            if show_ffq and ffq_responses:
                st.subheader("Ultra-Processed / HFSS Food Intake")
                st.metric("Pattern", profile["ffq_band"], f"{profile['ffq_total']}/{len(FFQ_ITEMS) * 4} points")

            st.success("Profile saved. Now click the button below for your plan, or go to 'Ask a Question' for personalised answers.")

    # ---- Generate full plan (uses saved profile) ----
    if st.session_state.get("profile"):
        st.divider()
        st.subheader("Your Personalised Wellness Plan")
        if st.button("Generate My Wellness Plan", type="primary"):
            p = st.session_state["profile"]
            summary = build_profile_summary(p)
            engine = load_engine()
            prompt = (
                "You are a wellness coach. Based ONLY on the wellness and healthy-ageing "
                "guidelines provided in the knowledge base, create a personalised wellness plan "
                "for the following person. Cover diet, physical activity, and lifestyle, and "
                "note any specific risk flags shown. Be practical and specific. If the guidelines "
                "do not cover something, say so rather than inventing advice.\n\n"
                f"PERSON'S PROFILE:\n{summary}\n\n"
                "Give the plan in clear sections."
            )
            with st.spinner("Building your personalised plan from the guidelines..."):
                answer = engine.query(prompt)
            st.write(str(answer))
            st.caption("Sources:")
            for i, node in enumerate(answer.source_nodes):
                st.caption(f"Source {i + 1} (relevance {node.score:.2f})")
            st.warning(DISCLAIMER)


# ===============================================================
# PAGE — ASK A QUESTION  (profile-aware)
# ===============================================================
else:
    st.title("Ask a Question")
    p = st.session_state.get("profile")
    if p:
        st.caption(f"Answers personalised for {p.get('name', 'you')}, grounded in your guidelines.")
        with st.expander("Profile being used"):
            st.text(build_profile_summary(p))
    else:
        st.caption("General answers grounded in your guidelines. Fill 'Get My Wellness Plan' for personalised answers.")

    engine = load_engine()
    question = st.text_input("Ask a question (e.g. 'suggest a workout for me', 'what diet suits me?'):")
    if question:
        if p:
            summary = build_profile_summary(p)
            full_query = (
                "You are a wellness coach. Answer the user's question using ONLY the provided "
                "wellness guidelines, personalised to this person's profile. If the guidelines "
                "do not cover it, say so rather than inventing advice.\n\n"
                f"PERSON'S PROFILE:\n{summary}\n\n"
                f"QUESTION: {question}"
            )
        else:
            full_query = question

        with st.spinner("Searching your documents..."):
            answer = engine.query(full_query)
        st.subheader("Answer")
        st.write(str(answer))
        st.subheader("Sources used")
        for i, node in enumerate(answer.source_nodes):
            st.markdown(f"**Source {i + 1}** (relevance: {node.score:.2f})")
            st.write(node.node.get_content()[:300] + "...")
        if p:
            st.warning(DISCLAIMER)
