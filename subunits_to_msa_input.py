import json
import sys
import os

def convert_subunits_to_msa_input(input_file, output_dir):
    # Load the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Initialize the output data structure
    msa_input = {
        "name": input_file.split('/')[-1].split('.')[0],
        "modelSeeds": [1],
        "sequences": [],
        "dialect": "alphafold3",
        "version": 1
    }

    # Extract and format the sequences
    for subunit in data.values():
        sequence_info = {
            "id": subunit["chain_names"][0].upper(),
            "sequence": subunit["sequence"]
        }
        msa_input["sequences"].append({"protein": sequence_info})

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Save the output JSON file
    # Get the filename without the directory
    filename = os.path.basename(input_file)

    # Join the filename with the output directory
    output_file = os.path.join(output_dir, filename)
    with open(output_file, 'w') as f:
        json.dump(msa_input, f, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: script <input_file> <output_dir> ")
        sys.exit(1)
    input_file, output_dir = sys.argv[1], sys.argv[2]
    convert_subunits_to_msa_input(input_file, output_dir)
