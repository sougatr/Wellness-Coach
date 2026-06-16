with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                "ALT, AST, platelets, and HbA1c are collected above (under the "
                "eGDR and liver health checks at the top of this page) and will "
                "be included in your snapshot below if provided."
            )'''

new = '''                "ALT, AST, platelets, and HbA1c are collected (under the "
                "eGDR and liver health checks) and will be included in "
                "your snapshot below."
            )'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: caption text updated")
