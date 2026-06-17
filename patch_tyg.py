with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    'TyG Index:** {tyg:.2f}")\n'
    '        st.caption(\n'
    '            "The TyG (Triglyceride-Glucose) index is a marker of **insulin resistance** \u2014 "\n'
    '            "higher values indicate greater insulin resistance, an early driver of "\n'
    '            "type 2 diabetes and metabolic syndrome, often detectable before fasting "\n'
    '            "glucose itself becomes abnormal."\n'
    '        )\n'
)

new = (
    'TyG Index:** {tyg:.2f}")\n'
    '        st.caption(\n'
    '            "The TyG (Triglyceride-Glucose) index is a surrogate marker of "\n'
    '            "**insulin resistance** \u2014 higher values indicate greater insulin "\n'
    '            "resistance, an early driver of type 2 diabetes and metabolic "\n'
    '            "syndrome, often detectable before fasting glucose itself becomes "\n'
    '            "abnormal. Standard: below 8.5 is considered favourable, 8.5-9.0 "\n'
    '            "is borderline, above 9.0 suggests insulin resistance."\n'
    '        )\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: TyG caption updated with surrogate marker wording and standard")

