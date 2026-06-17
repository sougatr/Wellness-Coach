with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        if p:
            summary = build_profile_summary(p)
            full_query = (
                "You are a wellness coach. Answer the user's question using ONLY the provided "
                "wellness guidelines, personalised to this person's profile. If the guidelines "
                "do not cover it, say so rather than inventing advice.\\n\\n"
                f"PERSON'S PROFILE:\\n{summary}\\n\\n"
                f"QUESTION: {question}"
            )
        else:
            full_query = question'''

new = '''        guidance_note = (
            "You are a wellness coach. Answer the user's question using ONLY the provided "
            "wellness guidelines. If multiple documents are relevant, prefer India-specific "
            "guidance (such as the Dietary Guidelines for India) when the question relates to "
            "Indian diets, food patterns, or population-specific recommendations, and use "
            "general/international guidance to supplement where India-specific guidance is "
            "not available. If the guidelines do not cover the question, say so rather than "
            "inventing advice."
        )
        if p:
            summary = build_profile_summary(p)
            full_query = (
                f"{guidance_note} Personalise your answer to this person's profile.\\n\\n"
                f"PERSON'S PROFILE:\\n{summary}\\n\\n"
                f"QUESTION: {question}"
            )
        else:
            full_query = f"{guidance_note}\\n\\nQUESTION: {question}"'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: query guidance instruction added")
