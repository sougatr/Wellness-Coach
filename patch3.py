with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    if tyg is not None:
        st.markdown(f"**TyG Index:** {tyg:.2f}")'''

new = '''    if ldl is not None:
        st.markdown(f"**LDL:** {ldl:.0f} mg/dL")

    if tyg is not None:
        st.markdown(f"**TyG Index:** {tyg:.2f}")'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: chunk 3 applied")
