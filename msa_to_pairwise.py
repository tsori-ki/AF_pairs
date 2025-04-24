import json
import itertools
import os
import sys
from copy import deepcopy


def create_pairwise_msa(msa_folder: str, mapping_file: str, subunits_info_file: str, output_dir: str) -> None:
    """
    Create pairwise MSA files with self-pairs only for multi-chain originals
    """
    # Load mapping and subunit info
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)

    with open(subunits_info_file, 'r') as f:
        subunits_info = json.load(f)

    # Get list of MSA files
    msa_files = [f for f in os.listdir(msa_folder) if f.endswith('.json')]
    subunits = [f.split('.')[0] for f in msa_files]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate combinations without self-pairs
    pairs = list(itertools.combinations(subunits, 2))

    # Add self-pairs for multi-chain originals
    for subunit in subunits:
        original_name = mapping.get(subunit)
        if original_name and len(subunits_info.get(original_name, {}).get('chain_names', [])) > 1:
            pairs.append((subunit, subunit))

    # Create pair files
    for pair in pairs:
        sub1, sub2 = pair
        with open(os.path.join(msa_folder, f"{sub1}.json")) as f1, \
                open(os.path.join(msa_folder, f"{sub2}.json")) as f2:
            seq1 = json.load(f1)
            seq2 = json.load(f2)

        seq_a = deepcopy(seq1)
        seq_b = deepcopy(seq2)

        # Format pair data
        seq_a['protein']['id'] = "A"
        seq_b['protein']['id'] = "B"
        seq_a['protein']['pairedMsa'] = ''
        seq_b['protein']['pairedMsa'] = ''

        pair_name = f"{sub1}_{sub2}"
        output_path = os.path.join(output_dir, f"{pair_name}.json")

        with open(output_path, 'w') as f:
            json.dump({
                'name': pair_name,
                'modelSeeds': [1],
                'sequences': [seq_a, seq_b],
                'dialect': "alphafold3",
                'version': 1
            }, f, indent=4)

        print(f"Created {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: script.py <MSA_FOLDER> <MAPPING_JSON> <SUBUNITS_INFO_JSON>")
        sys.exit(1)

    msa_folder = sys.argv[1]
    mapping_file = sys.argv[2]
    subunits_info_file = sys.argv[3]
    output_dir = os.path.join(os.path.dirname(msa_folder), 'msa_pairs')

    create_pairwise_msa(msa_folder, mapping_file, subunits_info_file, output_dir)
