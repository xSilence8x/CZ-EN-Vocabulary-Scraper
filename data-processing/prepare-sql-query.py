import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
json_input_path = os.path.join(current_directory, "no-dupli-compl-vocabulary.json")
json_output_path = os.path.join(current_directory, "tuples.txt")

with open(json_input_path, "r") as file:
    data = json.load(file)

output = []
for line in data:
    czech = line.get("czech")
    english = line.get("english")
    output.append([czech, english])

for line in output:
    print(line)

with open(json_output_path, "w", encoding="utf-8") as file:
    for line in output:
        file.write(f"('{line[0]}', '{line[1]}'), ")