with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''f"({'elevated' if waist_flag == 'elevated' else 'within normal range'})"
    )'''

new = '''f"({'elevated' if waist_flag == 'elevated' else 'within normal range'})"
    )
    st.caption(
        "Standard (South Asian cutoffs): 90 cm or above for men, 80 cm or "
        "above for women is considered elevated."
    )'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: waist circumference standard added")

