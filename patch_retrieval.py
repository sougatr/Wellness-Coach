with open('wellness_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    return index.as_query_engine(
    similarity_top_k=5,
    response_mode="tree_summarize",
)'''

new = '''    return index.as_query_engine(
    similarity_top_k=10,
    response_mode="tree_summarize",
)'''

if old not in content:
    print("ERROR: pattern not found")
else:
    content = content.replace(old, new, 1)
    with open('wellness_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: similarity_top_k increased to 10")
