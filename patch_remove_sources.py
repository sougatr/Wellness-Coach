with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        st.subheader("Answer")
        st.write(str(answer))
        st.subheader("Sources used")
        for i, node in enumerate(answer.source_nodes):
            st.markdown(f"**Source {i + 1}** (relevance: {node.score:.2f})")
            st.write(node.node.get_content()[:300] + "...")
        if p:'''

new = '''        st.subheader("Answer")
        st.write(str(answer))
        if p:'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: sources display removed")
