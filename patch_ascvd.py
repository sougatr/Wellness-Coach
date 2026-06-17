with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '10-year ASCVD risk:** {ascvd:.1f}%")\n'
    '        age_range_note = ""\n'
)

new = (
    'def ascvd_classification(risk_val):\n'
    '            if risk_val < 5.0:\n'
    '                return "Low risk"\n'
    '            elif risk_val < 7.5:\n'
    '                return "Borderline risk"\n'
    '            elif risk_val < 20.0:\n'
    '                return "Intermediate risk"\n'
    '            else:\n'
    '                return "High risk"\n'
    '\n'
    '        st.markdown(f"**10-year ASCVD risk:** {ascvd:.1f}% ({ascvd_classification(ascvd)})")\n'
    '        st.caption(\n'
    '            "Standard: below 5% low risk, 5-7.5% borderline, 7.5-20% "\n'
    '            "intermediate risk, 20% and above high risk."\n'
    '        )\n'
    '        age_range_note = ""\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: ASCVD classification and standard added")

