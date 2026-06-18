with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    'Insulin sensitivity check (optional)**")\n'
    '    st.caption(\n'
    '        "eGDR estimates how well your body responds to insulin - useful "\n'
    '        "because it also reflects age-related muscle loss, which reduces "\n'
    '        "insulin sensitivity independent of weight."\n'
    '    )\n'
)

new = (
    'Insulin sensitivity check (optional)**")\n'
    '    st.caption(\n'
    '        "eGDR is a simple way to estimate how well your body uses "\n'
    '        "insulin to manage blood sugar. As we age, we naturally lose "\n'
    '        "some muscle mass, and muscle is where a lot of blood sugar "\n'
    '        "gets used up - so less muscle can mean your body has to work "\n'
    '        "harder with insulin, even if your weight hasn\'t changed."\n'
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
    print("SUCCESS: eGDR explanation updated to layman language")

