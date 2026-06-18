from metabolic_assessment import render_metabolic_assessment
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
    import chromadb
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.google_genai import GoogleGenAI
    from llama_index.vector_stores.chroma import ChromaVectorStore

    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
    Settings.llm = GoogleGenAI(model="gemma-4-26b-a4b-it", api_key=api_key)

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = chroma_client.get_or_create_collection("wellness_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    if chroma_collection.count() > 0:
        index = VectorStoreIndex.from_vector_store(vector_store)
    else:
        docs = SimpleDirectoryReader(".", required_exts=[".pdf", ".html"]).load_data()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

    return index.as_query_engine(
    similarity_top_k=10,
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
page = st.sidebar.radio("Choose:", ["MetaWell Check", "Ask a Question"])

# show profile status in sidebar
if st.session_state.get("profile"):
    st.sidebar.success(f"Profile loaded: {st.session_state['profile'].get('name', 'user')}")
else:
    st.sidebar.info("No profile yet. Complete a MetaWell Check first for personalised answers.")

# ===============================================================
# PAGE — METAWELL CHECK
# ===============================================================
if page == "MetaWell Check":
    render_metabolic_assessment()

# ===============================================================
# PAGE — ASK A QUESTION  (profile-aware)
# ===============================================================
elif page == "Ask a Question":
    st.title("Ask About Your Metabolic Health")
    p = st.session_state.get("profile")
    if p:
        st.caption(f"Answers personalised for {p.get('name', 'you')}, grounded in your guidelines.")
        with st.expander("Profile being used"):
            st.text(build_profile_summary(p))
    else:
        st.caption("General answers grounded in your guidelines.")

    st.markdown("**Try asking something specific, like:**")
    st.markdown(
        "- What is the difference between being overweight and being "
        "metabolically unhealthy?\n"
        "- How is insulin resistance different from diabetes?\n"
        "- What lifestyle changes reverse insulin resistance fastest?\n"
        "- My cholesterol is high but I feel fine - should I be worried?\n"
        "- What is a good eating pattern for managing high triglycerides?\n"
        "- Can losing weight improve insulin resistance?\n"
        "- What Indian foods are good for managing insulin resistance?\n"
        "- How much exercise do I actually need to improve my metabolic health?\n"
        "- What should women focus on for heart health after 50?"
    )

    engine = load_engine()
    question = st.text_input("Type your question here:")
    if question:
        guidance_note = (
            "You are a wellness coach. Answer the user's question using ONLY the provided "
            "wellness guidelines. If multiple documents are relevant, prefer India-specific "
            "guidance (such as the Dietary Guidelines for India) when the question relates to "
            "Indian diets, food patterns, or population-specific recommendations, and use "
            "general/international guidance to supplement where India-specific guidance is "
            "not available. If the guidelines do not cover the question, say so rather than "
            "inventing advice."
        )
        if p:
            summary = build_profile_summary(p)
            full_query = (
                f"{guidance_note} Personalise your answer to this person's profile.\n\n"
                f"PERSON'S PROFILE:\n{summary}\n\n"
                f"QUESTION: {question}"
            )
        else:
            full_query = f"{guidance_note}\n\nQUESTION: {question}"

        with st.spinner("Searching your documents..."):
            answer = engine.query(full_query)
        st.subheader("Answer")
        st.write(str(answer))
        if p:
            st.warning(DISCLAIMER)
