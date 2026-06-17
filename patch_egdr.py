with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '.1f} mg/kg/min")\n'
    '        st.caption(\n'
    '            "eGDR estimates how efficiently your body clears glucose from the blood "\n'
    '            "using insulin \u2014 lower values mean greater insulin resistance. Values "\n'
    '            "below 8 are generally considered to indicate insulin resistance."\n'
    '        )\n'
)

new = (
    '.1f} mg/kg/min")\n'
    '        st.caption(\n'
    '            "eGDR estimates how efficiently your body clears glucose from the blood "\n'
    '            "using insulin \u2014 lower values mean greater insulin resistance. "\n'
    '            "Standard: 8 mg/kg/min or above is considered favourable; below "\n'
    '            "8 is generally considered to indicate insulin resistance."\n'
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
    print("SUCCESS: eGDR standard added")

