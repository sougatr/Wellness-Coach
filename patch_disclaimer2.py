with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '"**Prototype for demonstration purposes.** MetaWell is not a "\n'
    '        "substitute for professional medical advice, diagnosis, or "\n'
    '        "treatment. Data entered here is not stored securely - please "\n'
    '        "avoid entering identifying personal information. Always consult "\n'
    '        "a qualified healthcare provider about your individual health."\n'
)

new = (
    '"**Prototype for demonstration purposes.** MetaWell is not a "\n'
    '        "substitute for professional medical advice, diagnosis, or "\n'
    '        "treatment. As this is a prototype, use only laboratory values "\n'
    '        "and avoid personal identifiers. Consult a qualified healthcare "\n'
    '        "provider about your individual health."\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: disclaimer updated")

