with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''elif page == "Ask a Question":
    st.title("Ask a Question")
    p = st.session_state.get("profile")
    if p:
        st.caption(f"Answers personalised for {p.get('name', 'you')}, grounded in your guidelines.")
        with st.expander("Profile being used"):
            st.text(build_profile_summary(p))
    else:
        st.caption("General answers grounded in your guidelines.")

    engine = load_engine()
    question = st.text_input("Ask a question (e.g. 'suggest a workout for me', 'what diet suits me?'):")'''

new = '''elif page == "Ask a Question":
    st.title("Ask About Your Metabolic Health")
    p = st.session_state.get("profile")
    if p:
        st.caption(f"Answers personalised for {p.get('name', 'you')}, grounded in your guidelines.")
        with st.expander("Profile being used"):
            st.text(build_profile_summary(p))
    else:
        st.caption("General answers grounded in your guidelines.")

    st.markdown("**Try asking something specific, like:**")
    st.markdown(
        "- What do the Dietary Guidelines for India vis-\\u00e0-vis ADA medical nutrition "
        "therapy recommend for someone newly diagnosed with diabetes?\\n"
        "- What are good high-protein foods for older adults according to current "
        "guidelines? When should it be taken in the day?\\n"
        "- How does yoga affect sleep quality? Any other suggestions to improve sleep "
        "quality.\\n"
        "- What lifestyle changes help manage prediabetes? And what are the behaviour "
        "changes to improve long-term outcomes in diabetes management?\\n"
        "- What should women over 50 prioritize for their health? Suggest specific "
        "dietary and workout guidelines."
    )

    engine = load_engine()
    question = st.text_input("Type your question here:")'''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: title and example prompts added")

