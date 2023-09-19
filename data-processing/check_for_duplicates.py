import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
json_input_path = os.path.join(current_directory, "complete-vocabulary.json")
json_output_path = os.path.join(current_directory, "no-dupli-compl-vocabulary.json")

with open(json_input_path, "r") as file:
    data = json.load(file)

unique_items = set()
duplicate_items = []

for line in data:
    czech = line.get("czech")
    english = line.get("english")

    words_tuple = (czech, english)
    if words_tuple in unique_items:
        duplicate_items.append(words_tuple)
    else:
        unique_items.add(words_tuple)

for line in duplicate_items:
    print(line)

print(f"data {len(data)}, set {len(unique_items)}, duplicates {len(duplicate_items)}")

vocabulary = []
for element in unique_items:
    czech, english = element
    vocabulary.append({"czech": czech, "english": english})

with open(json_output_path, "w", encoding="utf-8") as file:
    json.dump(vocabulary, file, indent=4)