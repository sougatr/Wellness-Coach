with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'st.markdown(f"**LDL:** {ldl:.0f} mg/dL")'

new = '''def ldl_classification(ldl_val):
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
        )'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: LDL classification added")

