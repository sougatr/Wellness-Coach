with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '"provider about your individual health."\n'
    '    )\n'
    '\n'
    '    st.divider()\n'
)

new = (
    '"provider about your individual health."\n'
    '    )\n'
    '\n'
    '    st.markdown("#### What is metabolic health and insulin resistance?")\n'
    '    st.write(\n'
    '        "Metabolic health is how well your body manages energy - turning "\n'
    '        "food into fuel, storing fat properly, and keeping blood sugar, "\n'
    '        "blood pressure, and cholesterol in healthy ranges. Insulin "\n'
    '        "resistance is an early, common breakdown in this system: insulin "\n'
    '        "helps move sugar from your blood into your cells, but when cells "\n'
    '        "stop responding well, your body produces more and more insulin "\n'
    '        "just to keep up. Left unchecked, this can lead to type 2 "\n'
    '        "diabetes, fatty liver, and heart disease - often years before "\n'
    '        "symptoms appear. Caught early, it is largely reversible through "\n'
    '        "diet, activity, sleep, and weight management."\n'
    '    )\n'
    '\n'
    '    st.divider()\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: metabolic health explainer added")

