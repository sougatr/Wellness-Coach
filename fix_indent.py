with open('metabolic_assessment.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1-indexed 532 to 560 => 0-indexed 531 to 559
for i in range(531, 560):
    if lines[i].strip() != '':
        lines[i] = '    ' + lines[i]

with open('metabolic_assessment.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS: re-indented eGDR/liver block")

