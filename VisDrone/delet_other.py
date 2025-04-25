import json

INPUT_FILE = "D:/program/dataset/VisDrone/VisDrone2019-DET-test/annotations/test.json"
OUTPUT_FILE = 'output_filtered.json'

CATEGORY_TO_REMOVE = 11

# Load original JSON
def load_coco_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Filter annotations
def filter_annotations(data, category_id_to_remove):
    original_count = len(data['annotations'])
    data['annotations'] = [anno for anno in data['annotations'] if anno['category_id'] != category_id_to_remove]
    removed_count = original_count - len(data['annotations'])
    print(f"Removed {removed_count} annotations with category_id = {category_id_to_remove}")
    return data

# Save new JSON
def save_coco_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    coco_data = load_coco_json(INPUT_FILE)
    filtered_data = filter_annotations(coco_data, CATEGORY_TO_REMOVE)
    save_coco_json(filtered_data, OUTPUT_FILE)
    print(f"Filtered COCO annotations saved to {OUTPUT_FILE}")
