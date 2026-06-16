with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        # --- Q3: Labs ---
        st.subheader("3. Recent lab values (if available)")
        have_labs = st.checkbox("I have recent blood test results", value=True)
        fasting_glucose = total_chol = hdl = triglycerides = None
        if have_labs:
            col3, col4 = st.columns(2)
            with col3:
                fasting_glucose = st.number_input("Fasting glucose (mg/dL)", min_value=50.0, max_value=400.0, value=95.0)
                total_chol = st.number_input("Total cholesterol (mg/dL)", min_value=80.0, max_value=400.0, value=180.0)
            with col4:
                hdl = st.number_input("HDL cholesterol (mg/dL)", min_value=15.0, max_value=120.0, value=45.0)
                triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=30.0, max_value=1000.0, value=130.0)

        # --- Q4: Blood pressure + meds ---
        st.subheader("4. Blood pressure")
        col5, col6 = st.columns(2)
        with col5:
            sbp = st.number_input("Systolic BP (mmHg)", min_value=80.0, max_value=220.0, value=120.0)
        with col6:
            on_bp_meds = st.checkbox("On blood pressure medication")
        has_diabetes = st.checkbox("Diagnosed with diabetes")
        has_hypertension = on_bp_meds or sbp >= 140'''

new = '''        # --- Q3: Blood pressure + meds ---
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
                "ALT, AST, platelets, and HbA1c are collected above (under the "
                "eGDR and liver health checks at the top of this page) and will "
                "be included in your snapshot below if provided."
            )'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: chunk 1 applied")
