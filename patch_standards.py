with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    st.markdown(f"**BMI:** {bmi:.1f} kg/m²")
    st.markdown(
        f"**Waist-Hip Ratio:** {whr:.2f} "
        f"({'elevated' if whr_flag == 'elevated' else 'within normal range'} "
        f"for South Asian cutoffs)"
    )
    st.markdown(
        f"**Waist circumference:** {waist_cm:.0f} cm "
        f"({'elevated' if waist_flag == 'elevated' else 'within normal range'})"
    )

    if ldl is not None:
        st.markdown(f"**LDL:** {ldl:.0f} mg/dL")

    if tyg is not None:
        st.markdown(f"**TyG Index:** {tyg:.2f}")
        st.caption(
            "The TyG (Triglyceride-Glucose) index is a marker of **insulin resistance** - "
            "higher values indicate greater insulin resistance, an early driver of "
            "type 2 diabetes and metabolic syndrome, often detectable before fasting "
            "glucose itself becomes abnormal."
        )
    else:
        st.info("Add fasting glucose and triglycerides to see your TyG index (insulin resistance marker).")

    if egdr is not None:
        st.markdown(f"**eGDR (estimated glucose disposal rate):** {egdr:.1f} mg/kg/min")
        st.caption(
            "eGDR estimates how efficiently your body clears glucose from the blood "
            "using insulin - lower values mean greater insulin resistance. Values "
            "below 8 are generally considered to indicate insulin resistance."
        )
        st.write(egdr_age_note(age))
    elif want_egdr:
        st.info("Add your HbA1c value above to see your eGDR result.")

    if ascvd is not None:
        st.markdown(f"**10-year ASCVD risk:** {ascvd:.1f}%")'''

new = '''    def bmi_classification(bmi_val):
        if bmi_val < 18.5:
            return "Underweight"
        elif bmi_val < 23.0:
            return "Normal range"
        elif bmi_val < 25.0:
            return "Overweight"
        else:
            return "Obese"

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

    def ascvd_classification(risk_val):
        if risk_val < 5.0:
            return "Low risk"
        elif risk_val < 7.5:
            return "Borderline risk"
        elif risk_val < 20.0:
            return "Intermediate risk"
        else:
            return "High risk"

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
        st.markdown(f"**LDL:** {ldl:.0f} mg/dL ({ldl_classification(ldl)})")
        st.caption(
            "Standard: under 100 optimal, 100-129 near optimal, 130-159 "
            "borderline high, 160-189 high, 190 and above very high (mg/dL)."
        )

    if tyg is not None:
        st.markdown(f"**TyG Index:** {tyg:.2f}")
        st.caption(
            "The TyG (Triglyceride-Glucose) index is a surrogate marker of "
            "**insulin resistance** - higher values indicate greater insulin "
            "resistance, an early driver of type 2 diabetes and metabolic "
            "syndrome, often detectable before fasting glucose itself "
            "becomes abnormal. Standard: below 8.5 is considered favourable, "
            "8.5-9.0 is borderline, above 9.0 suggests insulin resistance."
        )
    else:
        st.info("Add fasting glucose and triglycerides to see your TyG index (insulin resistance marker).")

    if egdr is not None:
        st.markdown(f"**eGDR (estimated glucose disposal rate):** {egdr:.1f} mg/kg/min")
        st.caption(
            "eGDR estimates how efficiently your body clears glucose from the blood "
            "using insulin - lower values mean greater insulin resistance. "
            "Standard: 8 mg/kg/min or above is considered favourable; below "
            "8 is generally considered to indicate insulin resistance."
        )
        st.write(egdr_age_note(age))
    elif want_egdr:
        st.info("Add your HbA1c value above to see your eGDR result.")

    if ascvd is not None:
        st.markdown(f"**10-year ASCVD risk:** {ascvd:.1f}% ({ascvd_classification(ascvd)})")
        st.caption(
            "Standard: below 5% low risk, 5-7.5% borderline, 7.5-20% "
            "intermediate risk, 20% and above high risk."
        )'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: standards added for BMI, WHR, waist, LDL, TyG, eGDR, ASCVD")

