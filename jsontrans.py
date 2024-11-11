import json

# Path to your COCO JSON file
input_json_path = 'D:/program/dataset/carclasscoco/valid/annotations/valid.json'
output_json_path = 'D:/program/dataset/carclasscoco/valid/annotations/transvalid.json'

# Load the JSON data
with open(input_json_path, 'r') as file:
    data = json.load(file)

# Define the category ID for "car"
car_category_id = None

# Check if "car" already exists in the categories, or add it
for category in data['categories']:
    if category['name'] == 'car':
        car_category_id = category['id']
        break

# If "car" was not found, add it to categories
if car_category_id is None:
    car_category_id = max([cat['id'] for cat in data['categories']]) + 1
    data['categories'].append({
        "id": car_category_id,
        "name": "car",
        "supercategory": "vehicle"
    })

# Update all annotations to use the car_category_id
for annotation in data['annotations']:
    annotation['category_id'] = car_category_id

# Save the modified JSON data
with open(output_json_path, 'w') as file:
    json.dump(data, file, indent=2)

print(f"All classes updated to 'car' with category_id {car_category_id}")
