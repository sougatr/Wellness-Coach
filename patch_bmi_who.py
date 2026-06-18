with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    'def bmi_classification(bmi_val):\n'
    '        if bmi_val < 18.5:\n'
    '            return "Underweight"\n'
    '        elif bmi_val < 23.0:\n'
    '            return "Normal range"\n'
    '        elif bmi_val < 25.0:\n'
    '            return "Overweight"\n'
    '        else:\n'
    '            return "Obese"\n'
    '\n'
    '    st.markdown(f"**BMI:** {bmi:.1f} kg/m\u00b2 ({bmi_classification(bmi)})")\n'
    '    st.caption(\n'
    '        "Standard (Asian cutoffs, used for India): under 18.5 underweight, "\n'
    '        "18.5-22.9 normal, 23.0-24.9 overweight, 25.0 and above obese."\n'
    '    )\n'
)

new = (
    'def bmi_classification(bmi_val):\n'
    '        if bmi_val < 18.5:\n'
    '            return "Underweight"\n'
    '        elif bmi_val < 25.0:\n'
    '            return "Normal range"\n'
    '        elif bmi_val < 30.0:\n'
    '            return "Overweight"\n'
    '        else:\n'
    '            return "Obese"\n'
    '\n'
    '    st.markdown(f"**BMI:** {bmi:.1f} kg/m\u00b2 ({bmi_classification(bmi)})")\n'
    '    st.caption(\n'
    '        "Standard (WHO classification): under 18.5 underweight, "\n'
    '        "18.5-24.9 normal, 25.0-29.9 overweight, 30.0 and above obese."\n'
    '    )\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: BMI classification updated to WHO standard")

