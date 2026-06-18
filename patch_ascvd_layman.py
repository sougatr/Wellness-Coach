with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '            "ASCVD risk estimates your 10-year probability of a heart attack or stroke. "\n'
    '            "It is used clinically to guide decisions on statin therapy, blood pressure "\n'
    '            "targets, and how aggressively to pursue lifestyle changes \u2014 complementing "\n'
    '            "(but distinct from) the insulin resistance signal from the TyG index.\\n\\n"\n'
)

new = (
    '            "ASCVD risk tells you the chance, out of 100, that someone with your "\n'
    '            "specific risk profile will have a heart attack or stroke in the next "\n'
    '            "10 years. For example, a 5% risk means about 5 out of 100 people with "\n'
    '            "similar numbers would be expected to have one of these events in that "\n'
    '            "time. Doctors use this estimate to decide how urgently to focus on "\n'
    '            "things like blood pressure, cholesterol, and lifestyle changes. This "\n'
    '            "complements (but is distinct from) the insulin resistance signal from "\n'
    '            "the TyG index.\\n\\n"\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: ASCVD explanation updated to layman language")

