import json
import os
import sys


def convert_fasta_to_msa_json(input_file, output_file):
    """
    Converts a FASTA file into a JSON formatted for MSA.

    Args:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output JSON file.
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()

    msa_input = {
        "name": os.path.basename(input_file).split('.')[0].upper(),
        "modelSeeds": [1],
        "sequences": [],
        "dialect": "alphafold3",
        "version": 1
    }

    current_protein = None
    for line in lines:
        line = line.strip()
        if line.startswith('>'):
            if current_protein:
                msa_input["sequences"].append(current_protein)

            # Extract only the Uniprot accession ID (e.g., Q8BG89)
            protein_id = line.split('|')[1] if '|' in line else line.strip('>')

            current_protein = {"protein": {"id": protein_id, "sequence": ""}}
        else:
            if current_protein:
                current_protein["protein"]["sequence"] += line

    if current_protein:
        msa_input["sequences"].append(current_protein)

    with open(output_file, 'w') as f:
        json.dump(msa_input, f, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: script <input_file> <output_file>")
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]
    convert_fasta_to_msa_json(input_file, output_file)
