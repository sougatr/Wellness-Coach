with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def render_metabolic_assessment():
    st.header("MetaWell — Metabolic Health & Wellness Check")
    st.caption(
        "A quick assessment covering metabolic risk, diet patterns, liver health, "
        "and everyday wellness — tailored for Indian populations."
    )'''

new = '''def render_metabolic_assessment():
    st.header("MetaWell — Metabolic Health & Wellness Check")
    st.caption(
        "A quick assessment covering metabolic risk, diet patterns, liver health, "
        "and everyday wellness — tailored for Indian populations."
    )

    st.markdown("### Your metabolic health doesn't wait for a birthday")
    st.write(
        "Type 2 diabetes is showing up in teenagers. Fatty liver disease - "
        "once seen mainly in older adults - is now common in people in "
        "their 20s and 30s. And across every age group in India, the same "
        "quiet drivers keep showing up: too much sugar and processed food, "
        "not enough movement, and rising belly fat that often hides behind "
        "a \\"normal\\" weight."
    )
    st.write(
        "The good news: most of this is preventable, and it's never too "
        "early - or too late - to start paying attention."
    )
    st.write(
        "MetaWell gives you a quick, personalized snapshot of where you "
        "stand, whether you're a student trying to build healthy habits "
        "early, a working professional juggling stress and screen time, or "
        "someone managing health in their 50s, 60s, and beyond. In just a "
        "few minutes, you can check:"
    )
    st.markdown(
        "- Your body composition and fat distribution (BMI, waist, waist-hip ratio)\\n"
        "- Early signs of insulin resistance, even before blood sugar looks abnormal\\n"
        "- Your heart disease risk over the next 10 years\\n"
        "- How your liver is doing - fatty liver often has no symptoms until it's advanced\\n"
        "- Everyday habits like sleep, activity, and stress that quietly shape "
        "your metabolic health"
    )
    st.write(
        "No needles, no waiting rooms - just answer a few questions, and "
        "get a clear, actionable picture of your health."
    )
    st.divider()'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: intro added")
