"""
MetaWell — Metabolic Health & Wellness Check Module
================================================================
Compact, India-focused metabolic risk and wellness questionnaire and
calculator.

Computes:
  - BMI
  - Waist-Hip Ratio (WHR) with WHO South Asian cutoffs
  - TyG Index (insulin resistance proxy)
  - 10-year ASCVD risk (2013 ACC/AHA Pooled Cohort Equations, "White" coefficients
    used as published, with South Asian caveat noted in output)
  - Liver health: AST/ALT ratio and FIB-4 fibrosis risk estimate
  - Wellness snapshot: sleep, physical activity, stress, mood/energy
  - RED / AMBER / GREEN overall tier

Integrate by importing `render_metabolic_assessment()` and calling it from
wellness_app.py inside a Streamlit page/tab.
"""

import math
import streamlit as st



# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

ETHNICITY_REGIONS = {
    "Himalayan / Northeastern hill states": (
        "Populations from hill regions generally show somewhat lower "
        "visceral adiposity and diabetes prevalence compared to plains "
        "populations, though this protective effect is being eroded by "
        "rapid dietary transition."
    ),
    "Bengal / Eastern India": (
        "Eastern India, particularly West Bengal, has shown some of the "
        "highest age-adjusted diabetes prevalence rates in national surveys. "
        "Extra attention to glycaemic and lipid markers is warranted."
    ),
    "South India": (
        "Southern states consistently report among the highest diabetes "
        "prevalence in India, with high rates of insulin resistance even "
        "at lower BMI. TyG index and waist measures are especially relevant."
    ),
    "North / Central plains": (
        "North Indian plains populations show high rates of central "
        "obesity and dyslipidaemia linked to dietary patterns."
    ),
    "West India": (
        "Western Indian urban populations show rising metabolic syndrome "
        "rates linked to sedentary lifestyle and dietary shifts."
    ),
    "Other / Mixed": (
        "General South Asian metabolic risk patterns apply — central "
        "adiposity and insulin resistance tend to occur at lower BMI "
        "thresholds than in Western populations."
    ),
}

# 2013 ACC/AHA Pooled Cohort Equations coefficients (10-year ASCVD risk)
# Published "White" coefficient set, used as the standard reference in the
# absence of validated South Asian-specific equations.
PCE_COEFFICIENTS = {
    "white_male": {
        "ln_age": 12.344, "ln_tc": 11.853, "ln_age_ln_tc": -2.664,
        "ln_hdl": -7.990, "ln_age_ln_hdl": 1.769,
        "ln_sbp_treated": 1.797, "ln_sbp_untreated": 1.764,
        "smoker": 7.837, "ln_age_smoker": -1.795,
        "diabetes": 0.658,
        "mean": 61.18, "baseline_survival": 0.9144,
    },
    "white_female": {
        "ln_age": -29.799, "ln_age_sq": 4.884, "ln_tc": 13.540,
        "ln_age_ln_tc": -3.114, "ln_hdl": -13.578, "ln_age_ln_hdl": 3.149,
        "ln_sbp_treated": 2.019, "ln_sbp_untreated": 1.957,
        "smoker": 7.574, "ln_age_smoker": -1.665,
        "diabetes": 0.661,
        "mean": -29.18, "baseline_survival": 0.9665,
    },
}


# ---------------------------------------------------------------------------
# Calculation functions
# ---------------------------------------------------------------------------

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)


def calculate_whr(waist_cm: float, hip_cm: float) -> dict:
    whr = waist_cm / hip_cm
    return {"value": whr}


def whr_risk_flag(whr: float, sex: str) -> str:
    """WHO South Asian-relevant WHR cutoffs."""
    cutoff = 0.90 if sex == "male" else 0.85
    return "elevated" if whr > cutoff else "normal"


def waist_risk_flag(waist_cm: float, sex: str) -> str:
    """Lower South Asian waist circumference cutoffs (commonly used in India)."""
    cutoff = 90 if sex == "male" else 80
    return "elevated" if waist_cm >= cutoff else "normal"


def calculate_tyg_index(fasting_glucose_mgdl: float, triglycerides_mgdl: float) -> float:
    """
    TyG Index = ln(fasting triglycerides [mg/dL] x fasting glucose [mg/dL] / 2)
    Higher values indicate greater insulin resistance.
    """
    return math.log((triglycerides_mgdl * fasting_glucose_mgdl) / 2.0)


def tyg_risk_tier(tyg: float) -> str:
    """
    Generic tiering based on commonly cited population-level TyG cutoffs
    for insulin resistance (values vary somewhat by study; these are
    general reference bands, not diagnostic thresholds).
    """
    if tyg < 8.5:
        return "GREEN"
    elif tyg < 9.0:
        return "AMBER"
    else:
        return "RED"


def calculate_ascvd_risk(
    age: int,
    sex: str,
    total_chol: float,
    hdl: float,
    sbp: float,
    on_bp_meds: bool,
    is_smoker: bool,
    has_diabetes: bool,
) -> float:
    """
    10-year ASCVD risk (%) using 2013 ACC/AHA Pooled Cohort Equations,
    published "White" coefficient set (used as the standard reference
    absent validated South Asian-specific equations).

    Valid for ages 40-79. Returns percentage (0-100).
    """
    age = max(40, min(age, 79))  # PCE validated range
    key = "white_male" if sex == "male" else "white_female"
    c = PCE_COEFFICIENTS[key]

    ln_age = math.log(age)
    ln_tc = math.log(total_chol)
    ln_hdl = math.log(hdl)
    ln_sbp = math.log(sbp)

    sum_terms = 0.0
    sum_terms += c["ln_age"] * ln_age
    sum_terms += c["ln_tc"] * ln_tc
    sum_terms += c["ln_age_ln_tc"] * ln_age * ln_tc
    sum_terms += c["ln_hdl"] * ln_hdl
    sum_terms += c["ln_age_ln_hdl"] * ln_age * ln_hdl

    if on_bp_meds:
        sum_terms += c["ln_sbp_treated"] * ln_sbp
    else:
        sum_terms += c["ln_sbp_untreated"] * ln_sbp

    if is_smoker:
        sum_terms += c["smoker"]
        sum_terms += c["ln_age_smoker"] * ln_age

    if has_diabetes:
        sum_terms += c["diabetes"]

    # Female equation has an additional ln(age)^2 term
    if sex == "female":
        sum_terms += c["ln_age_sq"] * (ln_age ** 2)

    risk = 1 - (c["baseline_survival"] ** math.exp(sum_terms - c["mean"]))
    return max(0.0, min(risk * 100, 100.0))


def ascvd_risk_tier(risk_pct: float) -> str:
    """Standard ACC/AHA risk categories."""
    if risk_pct < 5.0:
        return "GREEN"   # Low risk
    elif risk_pct < 7.5:
        return "AMBER"   # Borderline
    elif risk_pct < 20.0:
        return "AMBER"   # Intermediate
    else:
        return "RED"     # High


def diet_risk_tier(upf_frequency: str, salt_habit: str) -> str:
    upf_score = {
        "Rarely (few times a month)": 0,
        "A few times a week": 1,
        "Daily": 2,
        "Multiple times daily": 3,
    }[upf_frequency]

    salt_score = {"Rarely": 0, "Sometimes": 1, "Often": 2}[salt_habit]

    total = upf_score + salt_score
    if total <= 1:
        return "GREEN"
    elif total <= 3:
        return "AMBER"
    else:
        return "RED"


def ethnicity_diet_risk_note(region: str, diet_tier: str) -> str:
    """
    Combined narrative blending regional metabolic risk background with
    the person's own diet pattern, for a more pointed message than either
    factor alone.
    """
    region_text = ETHNICITY_REGIONS[region]

    if diet_tier == "RED":
        combined = (
            f"{region_text} Combined with your current diet pattern — frequent "
            "processed/HFSS foods, sugar, and salt — this represents a "
            "compounding risk. Populations with an already elevated background "
            "risk see the largest benefit from reducing these specific dietary "
            "exposures."
        )
    elif diet_tier == "AMBER":
        combined = (
            f"{region_text} Your diet pattern shows some room for improvement — "
            "given your background risk profile, even moderate reductions in "
            "processed foods, sugar, and salt are likely to be worthwhile."
        )
    else:
        combined = (
            f"{region_text} Your current diet pattern is favourable, which helps "
            "offset background regional risk factors — worth maintaining."
        )

    return combined


def calculate_ast_alt_ratio(ast: float, alt: float) -> float:
    return ast / alt


def ast_alt_interpretation(ratio: float) -> str:
    """
    Plain-language interpretation of AST/ALT ratio.
    Not diagnostic — general population framing only.
    """
    if ratio < 1.0:
        return (
            "Your ALT is higher than AST (ratio < 1), a pattern commonly seen "
            "with fatty liver (steatosis). This is very common and often "
            "improves with weight loss, reduced sugar/processed food intake, "
            "and physical activity."
        )
    elif ratio < 1.5:
        return (
            "Your AST and ALT are fairly balanced (ratio close to 1). This is "
            "generally a less specific pattern, but worth discussing with your "
            "doctor if either value is above the normal range for your lab."
        )
    else:
        return (
            "Your AST is notably higher than ALT (ratio > 1.5). This pattern "
            "can occur with several conditions, including alcohol-related liver "
            "changes or other causes — it's a good idea to discuss this "
            "specifically with your doctor."
        )


def calculate_fib4(age: int, ast: float, alt: float, platelets_10e9_l: float) -> float:
    """
    FIB-4 = (Age x AST) / (Platelets [10^9/L] x sqrt(ALT))
    Used as a non-invasive estimate of liver fibrosis risk.
    """
    return (age * ast) / (platelets_10e9_l * math.sqrt(alt))


def fib4_risk_tier(fib4: float, age: int) -> str:
    """
    Age-banded FIB-4 cutoffs per AASLD 2023 / EASL-EASD-EASO 2024 guidance:
      - Age < 65: low-risk <1.3, indeterminate 1.3-2.67, high-risk >2.67
      - Age >= 65: low-risk <2.0, indeterminate 2.0-2.67, high-risk >2.67
        (the standard 1.3 cutoff causes excess false positives over 65)
    High-risk threshold (>2.67) is constant across age groups.
    """
    low_cutoff = 2.0 if age >= 65 else 1.3
    high_cutoff = 2.67

    if fib4 < low_cutoff:
        return "GREEN"
    elif fib4 <= high_cutoff:
        return "AMBER"
    else:
        return "RED"


def fib4_age_reliability_note(age: int) -> str:
    """
    FIB-4 has known reduced reliability outside the 35-65 age band.
    """
    if age < 35:
        return (
            "FIB-4 is less reliable under age 35 — results here should be "
            "interpreted cautiously and are less likely to need further "
            "evaluation at this age."
        )
    elif age >= 65:
        return (
            "An adjusted, higher threshold has been used for your FIB-4 "
            "score since the standard threshold tends to over-flag risk "
            "in people over 65."
        )
    else:
        return ""


def calculate_egdr(waist_cm: float, has_hypertension: bool, hba1c_pct: float) -> float:
    """
    eGDR (Estimated Glucose Disposal Rate), mg/kg/min.
    eGDR = 21.158 - (0.09 x WC) - (3.407 x HTN) - (0.551 x HbA1c)
    Lower eGDR = greater insulin resistance. Validated against the
    hyperinsulinemic-euglycemic clamp (the gold-standard but invasive/
    impractical reference test for insulin resistance).
    """
    htn = 1 if has_hypertension else 0
    return 21.158 - (0.09 * waist_cm) - (3.407 * htn) - (0.551 * hba1c_pct)


def egdr_risk_tier(egdr: float) -> str:
    """
    eGDR < 8 mg/kg/min is the commonly cited insulin resistance threshold
    in the literature. Bands below split further for AMBER/RED.
    """
    if egdr >= 8.0:
        return "GREEN"
    elif egdr >= 6.0:
        return "AMBER"
    else:
        return "RED"


def egdr_age_note(age: int) -> str:
    """
    Brief note linking eGDR to age-related muscle mass decline
    (sarcopenia), which independently lowers insulin sensitivity.
    """
    if age < 40:
        return (
            "At your age, a low eGDR is more likely driven by excess weight, "
            "diet, or inactivity than by muscle loss."
        )
    elif age < 60:
        return (
            "From your 40s onward, gradual loss of muscle mass (which "
            "naturally accelerates with age) starts to contribute to lower "
            "insulin sensitivity alongside diet and activity factors."
        )
    else:
        return (
            "Age-related muscle mass decline (sarcopenia) becomes a more "
            "significant contributor to insulin resistance after 60 — "
            "resistance/strength exercise is especially valuable at this "
            "stage, both for eGDR and for preserving muscle mass itself."
        )


def sleep_tier(sleep_category: str) -> str:
    """Short and long sleep duration are both linked to adverse metabolic
    outcomes; mid-range is favourable."""
    mapping = {
        "Less than 5 hours": "RED",
        "5-6 hours": "AMBER",
        "7-8 hours": "GREEN",
        "More than 8 hours": "AMBER",
    }
    return mapping[sleep_category]


def activity_tier(activity_category: str) -> str:
    mapping = {
        "0 days": "RED",
        "1-2 days": "AMBER",
        "3-4 days": "AMBER",
        "5 or more days": "GREEN",
    }
    return mapping[activity_category]


def stress_tier(stress_category: str) -> str:
    mapping = {"Low": "GREEN", "Moderate": "AMBER", "High": "RED"}
    return mapping[stress_category]


def mood_energy_tier(mood_category: str) -> str:
    """
    Single-item screen on mood/energy/interest over the last 2 weeks,
    framed without clinical terminology. Mirrors PHQ-2 frequency response
    options but described in everyday language.
    """
    mapping = {
        "Not at all": "GREEN",
        "Several days": "AMBER",
        "More than half the days": "AMBER",
        "Nearly every day": "RED",
    }
    return mapping[mood_category]


def wellness_tier(sleep_t: str, activity_t: str, stress_t: str) -> str:
    """Combined lifestyle/wellness tier from sleep, activity, and stress
    (mood/energy is reported separately with its own supportive messaging)."""
    return overall_tier([sleep_t, activity_t, stress_t])


def overall_tier(tiers: list) -> str:
    if "RED" in tiers:
        return "RED"
    elif "AMBER" in tiers:
        return "AMBER"
    else:
        return "GREEN"


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

def render_metabolic_assessment():
    st.header("MetaWell — Metabolic Health & Wellness Check")
    st.caption(
        "A quick assessment covering metabolic risk, diet patterns, liver health, "
        "and everyday wellness — tailored for Indian populations."
    )

    st.markdown("### Your metabolic health doesn't wait for a birthday")
    st.write(
        "Type 2 diabetes is showing up in teenagers. Fatty liver disease - "
        "once seen mainly in older adults - is now common in people in "
        "their 20s and 30s. And across every age group in India, the same "
        "quiet drivers keep showing up: too much sugar and processed food, "
        "not enough movement, and rising belly fat that often hides behind "
        "a \"normal\" weight."
    )
    st.write(
        "The good news: most of this is preventable, and it's never too "
        "early - or too late - to start paying attention."
    )
    st.write(
        "MetaWell gives you a quick, personalized snapshot of where you "
        "stand, whether you're a student trying to build healthy habits "
        "early, a working professional juggling stress and screen time, or "
        "someone managing health in their 50s, 60s, and beyond. In just a "
        "few minutes, you can check:"
    )
    st.markdown(
        "- Your body composition and fat distribution (BMI, waist, waist-hip ratio)\n"
        "- Early signs of insulin resistance, even before blood sugar looks abnormal\n"
        "- Your heart disease risk over the next 10 years\n"
        "- How your liver is doing - fatty liver often has no symptoms until it's advanced\n"
        "- Everyday habits like sleep, activity, and stress that quietly shape "
        "your metabolic health"
    )
    st.write(
        "No needles, no waiting rooms - just answer a few questions, and "
        "get a clear, actionable picture of your health."
    )
    st.divider()


    # --- Q1: Ethnicity / Region ---
    st.subheader("1. Background")
    region = st.selectbox(
        "Which region best describes your background?",
        list(ETHNICITY_REGIONS.keys()),
    )

    # --- Q2: Demographics + Anthropometrics ---
    st.subheader("2. About you")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=18, max_value=100, value=40)
        sex = st.radio("Sex", ["male", "female"], horizontal=True)
        height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=165.0)
        weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    with col2:
        waist_cm = st.number_input("Waist circumference (cm)", min_value=40.0, max_value=200.0, value=85.0)
        hip_cm = st.number_input("Hip circumference (cm)", min_value=40.0, max_value=200.0, value=95.0)

    # --- Q3: Blood pressure + meds ---
    st.subheader("3. Blood pressure")
    col5, col6 = st.columns(2)
    with col5:
        sbp = st.number_input("Systolic BP (mmHg)", min_value=80.0, max_value=220.0, value=120.0)
    with col6:
        on_bp_meds = st.checkbox("On blood pressure medication")
    has_diabetes = st.checkbox("Diagnosed with diabetes")
    has_hypertension = on_bp_meds or sbp >= 140

    # --- Q4: Metabolic health (ASCVD, liver, insulin resistance/sensitivity) ---
    st.subheader("4. Metabolic health")
    st.caption(
        "Includes ASCVD score, liver health, insulin resistance, and "
        "insulin sensitivity. All values below are optional - fill in "
        "whatever you have available."
    )
    have_labs = st.checkbox("I have recent blood test results", value=True)
    fasting_glucose = total_chol = hdl = triglycerides = ldl = None
    if have_labs:
        colm1, colm2 = st.columns(2)
        with colm1:
            fasting_glucose = st.number_input("Fasting glucose (mg/dL) - if available", min_value=50.0, max_value=400.0, value=95.0)
            hdl = st.number_input("HDL (mg/dL) - if available", min_value=15.0, max_value=120.0, value=45.0)
            triglycerides = st.number_input("Triglycerides (mg/dL) - if available", min_value=30.0, max_value=1000.0, value=130.0)
        with colm2:
            ldl = st.number_input("LDL (mg/dL) - if available", min_value=30.0, max_value=400.0, value=100.0)
            total_chol = st.number_input("Total cholesterol (mg/dL) - if available", min_value=80.0, max_value=400.0, value=180.0)
        st.caption(
            "ALT, AST, platelets, and HbA1c are collected (under the "
            "eGDR and liver health checks) and will be included in "
            "your snapshot below."
        )

    st.markdown("**Insulin sensitivity check (optional)**")
    st.caption(
        "eGDR estimates how well your body responds to insulin - useful "
        "because it also reflects age-related muscle loss, which reduces "
        "insulin sensitivity independent of weight."
    )
    want_egdr = st.checkbox("I would like to check my eGDR (needs HbA1c)")
    hba1c = None
    if want_egdr:
        hba1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=15.0, value=5.5, key="hba1c_input")

    st.markdown("**Liver health check (optional)**")
    st.caption(
        "ALT and AST are standard liver function test (LFT) values, "
        "usually reported in U per L. Platelet count is from a CBC report "
        "and is optional but improves the estimate."
    )
    want_liver = st.checkbox("Would you like to check your metabolic liver health?")
    ast = alt = platelets = None
    have_platelets = False
    if want_liver:
        col_liver1, col_liver2 = st.columns(2)
        with col_liver1:
            ast = st.number_input("AST (U/L)", min_value=5.0, max_value=500.0, value=25.0, key="ast_input")
        with col_liver2:
            alt = st.number_input("ALT (U/L)", min_value=5.0, max_value=500.0, value=25.0, key="alt_input")
        have_platelets = st.checkbox("I also have my platelet count (from CBC)", key="have_platelets_check")
        if have_platelets:
            platelets = st.number_input("Platelet count (x10^9/L)", min_value=50.0, max_value=600.0, value=250.0, key="platelets_input")

    st.subheader("5. Diet and lifestyle")
    smoking_status = st.radio("Smoking status", ["Never", "Former", "Current"], horizontal=True)
    upf_frequency = st.selectbox(
        "How often do you eat packaged snacks, fried street food, sweets/desserts, or sugary drinks?",
        [
            "Rarely (few times a month)",
            "A few times a week",
            "Daily",
            "Multiple times daily",
        ],
    )
    salt_habit = st.radio(
        "Do you usually add extra salt at the table, or eat a lot of pickles/papad/processed foods?",
        ["Rarely", "Sometimes", "Often"],
        horizontal=True,
    )

    # --- Q6: Wellness check ---
    st.subheader("6. Wellness check")
    sleep_category = st.radio(
        "On average, how many hours do you sleep per night?",
        ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"],
        horizontal=True,
    )
    activity_category = st.radio(
        "How many days a week do you do at least 30 minutes of moderate activity "
        "(brisk walk, yoga, sports, etc.)?",
        ["0 days", "1-2 days", "3-4 days", "5 or more days"],
        horizontal=True,
    )
    stress_category = st.radio(
        "How would you rate your typical stress level?",
        ["Low", "Moderate", "High"],
        horizontal=True,
    )
    mood_category = st.radio(
        "Over the last 2 weeks, how often have you felt low on energy or "
        "interest in things you'd normally enjoy?",
        ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        horizontal=True,
    )

    submitted = st.button("Get my health & wellness snapshot")

    if not submitted:
        return

    # --- Calculations ---
    bmi = calculate_bmi(weight_kg, height_cm)
    whr = calculate_whr(waist_cm, hip_cm)["value"]
    whr_flag = whr_risk_flag(whr, sex)
    waist_flag = waist_risk_flag(waist_cm, sex)

    tiers = []
    diet_tier = diet_risk_tier(upf_frequency, salt_habit)
    tiers.append(diet_tier)

    adiposity_tier = "RED" if (whr_flag == "elevated" and waist_flag == "elevated") else \
                     "AMBER" if (whr_flag == "elevated" or waist_flag == "elevated") else "GREEN"
    tiers.append(adiposity_tier)

    tyg = None
    if fasting_glucose and triglycerides:
        tyg = calculate_tyg_index(fasting_glucose, triglycerides)
        tiers.append(tyg_risk_tier(tyg))

    egdr = None
    if want_egdr and hba1c:
        egdr = calculate_egdr(waist_cm, has_hypertension, hba1c)
        tiers.append(egdr_risk_tier(egdr))

    ascvd = None
    if all([total_chol, hdl, fasting_glucose]):
        ascvd = calculate_ascvd_risk(
            age=age, sex=sex, total_chol=total_chol, hdl=hdl,
            sbp=sbp, on_bp_meds=on_bp_meds, is_smoker=(smoking_status == "Current"),
            has_diabetes=has_diabetes,
        )
        tiers.append(ascvd_risk_tier(ascvd))

    ast_alt_ratio = None
    fib4 = None
    if want_liver and ast and alt:
        ast_alt_ratio = calculate_ast_alt_ratio(ast, alt)
        if have_platelets and platelets:
            fib4 = calculate_fib4(age, ast, alt, platelets)
            tiers.append(fib4_risk_tier(fib4, age))

    # Wellness tiers (sleep/activity/stress feed into overall tier;
    # mood/energy reported separately with supportive framing)
    sleep_t = sleep_tier(sleep_category)
    activity_t = activity_tier(activity_category)
    stress_t = stress_tier(stress_category)
    mood_t = mood_energy_tier(mood_category)

    wellness_t = wellness_tier(sleep_t, activity_t, stress_t)
    tiers.append(wellness_t)

    final_tier = overall_tier(tiers)

    # --- Output ---
    st.divider()
    tier_colors = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}
    st.subheader(f"{tier_colors[final_tier]} Overall health & wellness tier: {final_tier}")

    def bmi_classification(bmi_val):
        if bmi_val < 18.5:
            return "Underweight"
        elif bmi_val < 23.0:
            return "Normal range"
        elif bmi_val < 25.0:
            return "Overweight"
        else:
            return "Obese"

    st.markdown(f"**BMI:** {bmi:.1f} kg/m² ({bmi_classification(bmi)})")
    st.caption(
        "Standard (Asian cutoffs, used for India): under 18.5 underweight, "
        "18.5-22.9 normal, 23.0-24.9 overweight, 25.0 and above obese."
    )
    st.markdown(
        f"**Waist-Hip Ratio:** {whr:.2f} "
        f"({'elevated' if whr_flag == 'elevated' else 'within normal range'} "
        f"for South Asian cutoffs)"
    )
    st.caption(
        "Standard (South Asian cutoffs): above 0.90 for men, above 0.85 for "
        "women is considered elevated."
    )
    st.markdown(
        f"**Waist circumference:** {waist_cm:.0f} cm "
        f"({'elevated' if waist_flag == 'elevated' else 'within normal range'})"
    )
    st.caption(
        "Standard (South Asian cutoffs): 90 cm or above for men, 80 cm or "
        "above for women is considered elevated."
    )

    if ldl is not None:
        def ldl_classification(ldl_val):
            if ldl_val < 100:
                return "Optimal"
            elif ldl_val < 130:
                return "Near optimal"
            elif ldl_val < 160:
                return "Borderline high"
            elif ldl_val < 190:
                return "High"
            else:
                return "Very high"

        st.markdown(f"**LDL:** {ldl:.0f} mg/dL ({ldl_classification(ldl)})")
        st.caption(
            "Standard: under 100 optimal, 100-129 near optimal, 130-159 "
            "borderline high, 160-189 high, 190 and above very high (mg/dL)."
        )

    if tyg is not None:
        st.markdown(f"**TyG Index:** {tyg:.2f}")
        st.caption(
            "The TyG (Triglyceride-Glucose) index is a surrogate marker of "
            "**insulin resistance** — higher values indicate greater insulin "
            "resistance, an early driver of type 2 diabetes and metabolic "
            "syndrome, often detectable before fasting glucose itself becomes "
            "abnormal. Standard: below 8.5 is considered favourable, 8.5-9.0 "
            "is borderline, above 9.0 suggests insulin resistance."
        )
    else:
        st.info("Add fasting glucose and triglycerides to see your TyG index (insulin resistance marker).")

    if egdr is not None:
        st.markdown(f"**eGDR (estimated glucose disposal rate):** {egdr:.1f} mg/kg/min")
        st.caption(
            "eGDR estimates how efficiently your body clears glucose from the blood "
            "using insulin — lower values mean greater insulin resistance. "
            "Standard: 8 mg/kg/min or above is considered favourable; below "
            "8 is generally considered to indicate insulin resistance."
        )
        st.write(egdr_age_note(age))
    elif want_egdr:
        st.info("Add your HbA1c value above to see your eGDR result.")

    if ascvd is not None:
        def ascvd_classification(risk_val):
            if risk_val < 5.0:
                return "Low risk"
            elif risk_val < 7.5:
                return "Borderline risk"
            elif risk_val < 20.0:
                return "Intermediate risk"
            else:
                return "High risk"

        st.markdown(f"**10-year ASCVD risk:** {ascvd:.1f}% ({ascvd_classification(ascvd)})")
        st.caption(
            "Standard: below 5% low risk, 5-7.5% borderline, 7.5-20% "
            "intermediate risk, 20% and above high risk."
        )
        age_range_note = ""
        if age < 40 or age > 79:
            age_range_note = (
                "\n\n*This equation is formally validated only for ages 40-79; "
                "your age has been adjusted to the nearest validated boundary "
                "for this estimate, so treat the result as approximate.*"
            )
        st.caption(
            "ASCVD risk estimates your 10-year probability of a heart attack or stroke. "
            "It is used clinically to guide decisions on statin therapy, blood pressure "
            "targets, and how aggressively to pursue lifestyle changes — complementing "
            "(but distinct from) the insulin resistance signal from the TyG index.\n\n"
            "*Note: this estimate uses the published 2013 ACC/AHA Pooled Cohort Equations "
            "(reference coefficient set). These equations were derived from non-South Asian "
            "cohorts and may overestimate risk in South Asian populations — interpret "
            "alongside your TyG index and waist-based measures, and discuss with your "
            "doctor.*" + age_range_note
        )
    else:
        st.info("Add total cholesterol, HDL, and fasting glucose to see your ASCVD risk estimate.")

    st.divider()
    st.markdown("**Your background and diet pattern:**")
    st.write(ethnicity_diet_risk_note(region, diet_tier))

    if want_liver and ast_alt_ratio is not None:
        st.divider()
        st.markdown("**Liver health:**")
        st.markdown(f"**AST/ALT ratio:** {ast_alt_ratio:.2f}")
        st.write(ast_alt_interpretation(ast_alt_ratio))

        if fib4 is not None:
            st.markdown(f"**FIB-4 score:** {fib4:.2f}")
            fib4_tier = fib4_risk_tier(fib4, age)
            fib4_messages = {
                "GREEN": "Your FIB-4 score suggests a low likelihood of significant liver "
                         "fibrosis. Routine monitoring is generally sufficient.",
                "AMBER": "Your FIB-4 score is in an indeterminate range — this doesn't mean "
                         "there's a problem, but it's reasonable to mention this to your "
                         "doctor, who may suggest further evaluation.",
                "RED": "Your FIB-4 score is in a higher range associated with increased "
                       "likelihood of liver fibrosis. This is not a diagnosis, but it's "
                       "important to discuss this result with your doctor for further "
                       "assessment.",
            }
            st.write(fib4_messages[fib4_tier])
            age_note = fib4_age_reliability_note(age)
            if age_note:
                st.caption(age_note)
            st.caption(
                "FIB-4 is a screening tool based on age, AST, ALT, and platelet count. "
                "It estimates the likelihood of liver fibrosis but does not diagnose it — "
                "further tests (such as elastography) may be needed for confirmation."
            )
        else:
            st.info(
                "Add your platelet count (from a CBC report) to also see your FIB-4 "
                "score, which estimates liver fibrosis risk."
            )

        st.caption(
            "This liver check is for general awareness only and is not a substitute "
            "for medical advice. Please discuss any abnormal results with your doctor."
        )

    # --- Wellness snapshot ---
    st.divider()
    st.markdown(f"**Wellness snapshot:** {tier_colors[wellness_t]} {wellness_t}")

    sleep_messages = {
        "GREEN": "Your sleep duration is in a healthy range.",
        "AMBER": "Your sleep duration is a bit outside the ideal range — both "
                 "too little and too much sleep are linked with poorer "
                 "metabolic health over time.",
        "RED": "Getting too little sleep regularly is strongly linked with "
               "insulin resistance, weight gain, and increased appetite for "
               "high-sugar foods. Improving sleep is often one of the most "
               "impactful changes you can make.",
    }
    st.write(f"**Sleep:** {sleep_messages[sleep_t]}")

    activity_messages = {
        "GREEN": "You're meeting a good level of regular physical activity — "
                 "this helps improve insulin sensitivity and supports "
                 "healthy weight management.",
        "AMBER": "Increasing your activity frequency, even by one or two "
                 "more days a week, can meaningfully improve insulin "
                 "sensitivity and metabolic markers.",
        "RED": "Low physical activity is one of the most modifiable "
               "contributors to insulin resistance and weight gain. Even "
               "short, regular walks can make a real difference.",
    }
    st.write(f"**Physical activity:** {activity_messages[activity_t]}")

    stress_messages = {
        "GREEN": "Your stress levels seem manageable — that's good for "
                 "both your metabolic and overall health.",
        "AMBER": "Moderate stress is common, but chronic stress can affect "
                 "appetite, sleep, and blood sugar regulation. Simple "
                 "practices like short breaks, walks, or breathing "
                 "exercises can help.",
        "RED": "High stress levels can affect sleep, eating patterns, and "
               "blood sugar control. Consider building in regular "
               "stress-reduction practices, and talk to someone you trust "
               "if it feels overwhelming.",
    }
    st.write(f"**Stress:** {stress_messages[stress_t]}")

    mood_messages = {
        "GREEN": "Your energy and interest levels seem steady — that's a "
                 "good sign for overall wellbeing.",
        "AMBER": "It's normal to have some days with lower energy or "
                 "interest. If this continues or affects your daily life, "
                 "it may help to talk to someone you trust or a "
                 "healthcare professional.",
        "RED": "Feeling low on energy or interest most days can affect "
               "overall wellbeing and is worth discussing with a doctor or "
               "counsellor — support is available, and reaching out is a "
               "good first step.",
    }
    st.write(f"**Energy & interest:** {mood_messages[mood_t]}")

    st.caption(
        "This wellness snapshot is for general awareness and is not a "
        "diagnostic tool. If you have ongoing concerns about your mood, "
        "energy, sleep, or stress, please speak with a doctor or "
        "counsellor."
    )
