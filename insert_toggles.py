with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        "and everyday wellness — tailored for Indian populations."
    )

    with st.form("metabolic_assessment_form"):'''

new = '''        "and everyday wellness — tailored for Indian populations."
    )

    st.markdown("**Insulin sensitivity check (optional)**")
    st.caption(
        "eGDR estimates how well your body responds to insulin — useful "
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

    st.divider()

    with st.form("metabolic_assessment_form"):'''

if old not in content:
    print("ERROR: insertion point not found")
else:
    content = content.replace(old, new)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: eGDR and liver toggles inserted before the form")
