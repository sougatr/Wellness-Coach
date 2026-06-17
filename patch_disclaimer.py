with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        "No needles, no waiting rooms - just answer a few questions, and "
        "get a clear, actionable picture of your health."
    )
    st.divider()'''

new = '''        "No needles, no waiting rooms - just answer a few questions, and "
        "get a clear, actionable picture of your health."
    )

    st.warning(
        "**Prototype for demonstration purposes.** MetaWell is not a "
        "substitute for professional medical advice, diagnosis, or "
        "treatment. Data entered here is not stored securely - please "
        "avoid entering identifying personal information. Always consult "
        "a qualified healthcare provider about your individual health."
    )

    st.divider()'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: disclaimer added")

