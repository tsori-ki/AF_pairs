import json
import string
import itertools
import os

def generate_labels():
    """Generate labels A-Z, then AA, AB, AC... up to ZZ if needed."""
    alphabet = string.ascii_uppercase
    for letter in alphabet:
        yield letter
    for pair in itertools.product(alphabet, repeat=2):
        yield ''.join(pair)

def rename_protein_ids(msa_data, output_file, mapping_file_path):
    """
    Renames protein IDs in the given MSA JSON structure and saves the mapping in a json file.

    Args:
        msa_data (dict): The MSA JSON data.
        mapping_file_path (str): Path to save the mapping JSON file.

    """
    protein_map = {}
    label_generator = generate_labels()

    for seq in msa_data.get("sequences", []):
        original_id = seq["protein"]["id"]
        if original_id not in protein_map:
            protein_map[original_id] = next(label_generator)
        seq["protein"]["id"] = protein_map[original_id]

    # Save mapping
    with open(mapping_file_path, 'w') as file:
        json.dump(protein_map, file, indent=4)

    with open(output_file, 'w') as f:
        json.dump(msa_data, f, indent=4, separators=(',', ': '))
