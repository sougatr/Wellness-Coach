with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    'Liver health check (optional)**")\n'
    '    st.caption(\n'
    '        "ALT and AST are standard liver function test (LFT) values, "\n'
    '        "usually reported in U per L. Platelet count is from a CBC report "\n'
    '        "and is optional but improves the estimate."\n'
    '    )\n'
)

new = (
    'Liver health check (optional)**")\n'
    '    st.caption(\n'
    '        "ALT and AST are enzymes made mainly in the liver. When liver "\n'
    '        "cells are stressed or damaged, these enzymes leak into the "\n'
    '        "bloodstream, so higher levels can be an early sign that the "\n'
    '        "liver needs attention. They are measured in U/L (units per "\n'
    '        "litre), a standard way labs report enzyme activity - you will "\n'
    '        "find these values on a routine liver function test (LFT). "\n'
    '        "Platelet count comes from a different test, a CBC (complete "\n'
    '        "blood count), and is included here because, combined with "\n'
    '        "ALT, AST, and your age, it helps estimate the risk of "\n'
    '        "long-term liver scarring (fibrosis) - something a single "\n'
    '        "liver enzyme value cannot tell you on its own."\n'
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
    print("SUCCESS: liver health explanation updated to layman language")

