with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_import = (
    'import math\n'
    'import streamlit as st\n'
)
new_import = (
    'import math\n'
    'import streamlit as st\n'
    'from usage_tracking import log_event\n'
)

count1 = content.count(old_import)
print("Import pattern found:", count1)
if count1 > 0:
    content = content.replace(old_import, new_import, 1)

old_def = 'def render_metabolic_assessment():\n'
new_def = (
    'def render_metabolic_assessment():\n'
    '    log_event("metawell_page_visited")\n'
)
count2 = content.count(old_def)
print("Function def pattern found:", count2)
if count2 > 0:
    content = content.replace(old_def, new_def, 1)

old_submit = '    submitted = st.button("Get my health & wellness snapshot")\n'
new_submit = (
    '    submitted = st.button("Get my health & wellness snapshot")\n'
    '    if submitted:\n'
    '        log_event("metawell_form_submitted")\n'
)
count3 = content.count(old_submit)
print("Submit button pattern found:", count3)
if count3 > 0:
    content = content.replace(old_submit, new_submit, 1)

with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE")

