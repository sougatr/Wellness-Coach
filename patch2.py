with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        # --- Q7: Wellness check ---
        st.subheader("7. Wellness check")'''

new = '''        # --- Q6: Wellness check ---
        st.subheader("6. Wellness check")'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: chunk 2 applied")
