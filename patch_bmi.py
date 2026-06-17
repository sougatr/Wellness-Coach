with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'st.markdown(f"**BMI:** {bmi:.1f} kg/m\u00b2")'

new = '''def bmi_classification(bmi_val):
        if bmi_val < 18.5:
            return "Underweight"
        elif bmi_val < 23.0:
            return "Normal range"
        elif bmi_val < 25.0:
            return "Overweight"
        else:
            return "Obese"

    st.markdown(f"**BMI:** {bmi:.1f} kg/m\u00b2 ({bmi_classification(bmi)})")
    st.caption(
        "Standard (Asian cutoffs, used for India): under 18.5 underweight, "
        "18.5-22.9 normal, 23.0-24.9 overweight, 25.0 and above obese."
    )'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: BMI classification added")

