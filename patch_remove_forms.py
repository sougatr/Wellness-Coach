with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Convert to 0-indexed positions
# Line 478 (1-indexed) = index 477: "with st.form(...part1...):"
# Line 563 (1-indexed) = index 562: "with st.form(...part2...):"
# Line 606 (1-indexed) = index 605: submit button line

idx_form1 = 477
idx_form2 = 562
idx_submit = 605

assert 'with st.form("metabolic_assessment_form_part1")' in lines[idx_form1], f"Line {idx_form1+1} mismatch: {lines[idx_form1]!r}"
assert 'with st.form("metabolic_assessment_form_part2")' in lines[idx_form2], f"Line {idx_form2+1} mismatch: {lines[idx_form2]!r}"
assert 'st.form_submit_button' in lines[idx_submit], f"Line {idx_submit+1} mismatch: {lines[idx_submit]!r}"

# Replace submit button line with plain button (keep same indentation as original minus 4 spaces later)
lines[idx_submit] = lines[idx_submit].replace(
    'submitted = st.form_submit_button("Get my health & wellness snapshot")',
    'submitted = st.button("Get my health & wellness snapshot")'
)

# Remove the two 'with st.form(...)' lines entirely
# Process form2 first since it's the later index (so form1 index stays valid)
del lines[idx_form2]
del lines[idx_form1]

# Now de-indent lines that were between form1 and form2, and between form2 and submit
# After deletions:
#   - lines that were idx_form1+1 .. idx_form2-1 are now at idx_form1 .. idx_form2-2 (shifted by 1)
#   - lines that were idx_form2+1 .. idx_submit are now at idx_form2-1 .. idx_submit-2 (shifted by 2)
# Simplest robust approach: de-indent ALL lines from original idx_form1+1 through original idx_submit,
# accounting for the two line deletions that happened before/within that range.

# Since we deleted idx_form1 first... wait, we deleted idx_form2 first then idx_form1.
# After both deletions, the range that needs de-indenting is:
# from idx_form1 (now pointing to what was idx_form1+1) through idx_submit-2 (since 2 lines were removed before/within)

start = idx_form1  # after deleting idx_form1, this index now holds the old idx_form1+1 content
end = idx_submit - 2  # two lines removed total before this point

for i in range(start, end + 1):
    if lines[i].startswith('    '):
        lines[i] = lines[i][4:]

with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS: forms removed, content de-indented, submit button converted to plain button")

