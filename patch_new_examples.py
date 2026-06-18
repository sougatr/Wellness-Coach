with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '\n    st.markdown("**Try asking something specific, like:**")\n'
    '    st.markdown(\n'
    '        "- What do the Dietary Guidelines for India vis-\\u00e0-vis ADA medical nutrition "\n'
    '        "therapy recommend for someone newly diagnosed with diabetes?\\n"\n'
    '        "- What are good high-protein foods for older adults according to current "\n'
    '        "guidelines? When should it be taken in the day?\\n"\n'
    '        "- How does yoga affect sleep quality? Any other suggestions to improve sleep "\n'
    '        "quality.\\n"\n'
    '        "- What lifestyle changes help manage prediabetes? And what are the behaviour "\n'
    '        "changes to improve long-term outcomes in diabetes management?\\n"\n'
    '        "- What should women over 50 prioritize for their health? Suggest specific "\n'
    '        "dietary and workout guidelines."\n'
    '    )\n'
)

new = (
    '\n    st.markdown("**Try asking something specific, like:**")\n'
    '    st.markdown(\n'
    '        "- What is the difference between being overweight and being "\n'
    '        "metabolically unhealthy?\\n"\n'
    '        "- How is insulin resistance different from diabetes?\\n"\n'
    '        "- What lifestyle changes reverse insulin resistance fastest?\\n"\n'
    '        "- My cholesterol is high but I feel fine - should I be worried?\\n"\n'
    '        "- What is a good eating pattern for managing high triglycerides?\\n"\n'
    '        "- Can losing weight improve insulin resistance?\\n"\n'
    '        "- What Indian foods are good for managing insulin resistance?\\n"\n'
    '        "- How much exercise do I actually need to improve my metabolic health?\\n"\n'
    '        "- What should women focus on for heart health after 50?"\n'
    '    )\n'
)

count = content.count(old)
print("Occurrences found:", count)
if count == 0:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: example prompts replaced with new 9 questions")

