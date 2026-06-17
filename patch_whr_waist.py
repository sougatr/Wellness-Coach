with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''f"for South Asian cutoffs)"
    )'''

new = '''f"for South Asian cutoffs)"
    )
    st.caption(
        "Standard (South Asian cutoffs): above 0.90 for men, above 0.85 for "
        "women is considered elevated."
    )'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: WHR standard added")

