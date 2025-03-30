import json
import itertools
import os
import sys
from copy import deepcopy

def create_pairwise_msa(input_file, output_dir):
     # Load the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Extract sequences
    sequences = data['sequences']
    # Set paired_Msa to an empty string for all sequences
    for sequence in sequences:
        sequence['protein']['pairedMsa'] = ''
    # Generate all possible pairs of sequences
    pairs = list(itertools.combinations(sequences, 2))

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    #create output_pairs directory
    output_dir = os.path.join(output_dir, 'msa_pairs')
    os.makedirs(output_dir, exist_ok=True)
    # Save each pair as a separate JSON file
    for seq1, seq2 in pairs:
        seq_a = deepcopy(seq1)
        seq_b = deepcopy(seq2)
        seq_a['protein']['id'], seq_b['protein']['id'] = "A", "B"
        seq_a_name = seq1['protein']['id']
        seq_b_name = seq2['protein']['id']
        pair_name = f'{seq_a_name}_{seq_b_name}'
        pair_data =  {
            'name': pair_name,
            'modelSeeds': [1],
            'sequences': [seq_a, seq_b],
            'dialect': "alphafold3",
            'version': 1,
        }
        output_file = os.path.join(output_dir, f'{pair_name}.json')
        with open(output_file, 'w') as f:
            json.dump(pair_data, f, indent=4)
            print(f'Saved {output_file}')



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: script <INPUT_JSON_PATH>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Determine the output directory based on the input file's directory
    input_dir = os.path.dirname(input_file)
    output_dir = os.path.join(input_dir, 'output_pairs')
    
    create_pairwise_msa(input_file, output_dir)
