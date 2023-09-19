import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

json_directory = os.path.join(parent_directory, "vocabulary")
json_output_path = os.path.join(current_directory, "complete-vocabulary.json")
combined_data = []

for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            combined_data.extend(data)

file_path = os.path.join(json_directory, json_output_path)
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(combined_data, file, indent=4)
