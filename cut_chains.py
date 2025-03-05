import json


def cut_chain(msa_input, chain_id, cuts):
    """
    Cut the chain at the specified positions, cut it into multiple chains

    Parameters
    ----------
    msa_input : dict with keys 'sequences' that is list of dicts,
    each has key 'protein':dict with keys 'id', 'sequence'
        The input MSA data
    chain_id : str
        The chain ID to cut
    cuts : list
        The positions to cut the sequence
    """
    new_sequences = []
    for seq in msa_input['sequences']:
        if seq['protein']['id'] == chain_id:
            sequence = seq['protein']['sequence']
            cuts = [0] + cuts + [len(sequence)]
            for i in range(len(cuts) - 1):
                new_chain_id = f"{chain_id}_{chr(65 + i)}"
                new_sequence = sequence[cuts[i]:cuts[i + 1]]
                new_sequences.append({"protein": {"id": new_chain_id, "sequence": new_sequence}})
        else:
            new_sequences.append(seq)

    msa_input['sequences'] = new_sequences


if __name__ == '__main__':
    # open the json msa_input file
    with open('MLL4.json', 'r') as f:
        msa_input = json.load(f)
        cut_chain(msa_input, 'MLL', [200, 800])
        cut_chain(msa_input, 'UTX', [460, 840])
        cut_chain(msa_input, 'NCOA', [650, 1300])
        cut_chain(msa_input, 'PTIP', [200, 560])
        cut_chain(msa_input, 'CBP', [500, 1000, 1900])
        # Save the modified msa_input to a new file
        with open('MLL4_cut.json', 'w') as out_f:
            json.dump(msa_input, out_f, indent=4)