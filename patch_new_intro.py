with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    st.markdown("### Your metabolic health doesn't wait for a birthday")
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

    st.warning('''

new = '''    st.markdown("### Is Your Metabolic Health Really Normal?")
    st.write(
        "You got your blood work done. Fasting glucose, lipids, liver "
        "tests - all came back normal. You moved on."
    )
    st.write(
        "But \\"normal\\" on one test doesn't always mean your metabolic "
        "health is fine. Insulin resistance, early fatty liver, and rising "
        "heart risk often build quietly for years. They show up when "
        "numbers are looked at together - long before any single test "
        "flags a problem."
    )
    st.write(
        "MetaWell is built for exactly this. Whether you're checking in "
        "after a routine annual test, or keeping an eye on things because "
        "of extra weight, this tool looks at your numbers as a whole - "
        "not just one at a time."
    )
    st.write(
        "In a few minutes, using values you likely already have, you can check:"
    )
    st.markdown(
        "- Early signs of insulin resistance, even when blood sugar looks normal\\n"
        "- Your 10-year heart disease risk\\n"
        "- How your liver is doing - fatty liver often has no symptoms until it's advanced\\n"
        "- How sleep and stress are quietly shaping your metabolism, often "
        "more than diet alone"
    )
    st.write(
        "No needles, no waiting rooms. Just answer a few questions, and "
        "see what your own results have been telling you all along."
    )

    st.warning('''

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: intro replaced with sharper framing")

