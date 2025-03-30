import json
import os
import sys

# Documentation:
# This script converts a text file containing protein sequences into a JSON file formatted for MSA (Multiple Sequence Alignment).
# Usage:
#   python txt_to_msa.py <input_file> <output_file>
# Arguments:
#   <input_file>: Path to the input text file containing protein sequences in FASTA-like format.
#   <output_file>: Path to the output JSON file where the converted data will be saved.
# Output:
#   A JSON file containing the protein sequences formatted for MSA.

def convert_txt_to_msa_json(input_file, output_file):
    """
    Converts a text file containing protein sequences into a JSON file formatted for MSA.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to the output JSON file.

    The input file should contain protein sequences in a FASTA-like format:
    - Lines starting with '>' indicate a new protein, with the protein ID following the '>'.
    - Subsequent lines contain the protein sequence.

    The output JSON file will contain:
    - A "name" field derived from the input file name.
    - A "sequences" list, where each sequence is represented as a dictionary with "id" and "sequence".
    - Additional metadata fields such as "modelSeeds", "dialect", and "version".
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
            protein_id = line.split('-')[0].strip('>')
            protein_id = ''.join([c for c in protein_id if c.isupper()])

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
    convert_txt_to_msa_json(input_file, output_file)