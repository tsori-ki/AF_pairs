# Protein Structure Analysis Toolkit

A collection of tools for preparing and analyzing protein sequences for AlphaFold 3 structure predictions.

## Tools

### Data Preparation
- `txt_to_msa.py`: Converts FASTA-like text files to AlphaFold 3 MSA JSON format
- `subunits_to_msa_input.py`: Converts subunit JSON files to AlphaFold 3 MSA JSON format
- `cut_chains.py`: Splits protein chains at specified positions into multiple subchains

### Analysis
- `msa_to_pairwise.py`: Creates pairwise combinations of protein sequences for interaction analysis

### Execution Scripts
- `msa.sh`: Runs the MSA generation step of AlphaFold 3
- `run_af.sh`: Runs AlphaFold 3 structure prediction on prepared data

## Usage

### Converting Sequences
```bash
# Convert text file to MSA JSON format
python txt_to_msa.py input.txt output.json

# Convert subunits file to MSA JSON format
python subunits_to_msa_input.py input.json output_dir
```

### Cutting Protein Chains
```bash
# Edit cut_chains.py to specify your chains and cut positions
# Then run:
python cut_chains.py
```

### Creating Pairwise Combinations
```bash
python msa_to_pairwise.py COMPLEX_NAME
```

### Running AlphaFold
```bash
# Run MSA generation
sbatch msa.sh COMPLEX_NAME

# Run AlphaFold prediction
sbatch run_af.sh COMPLEX_NAME
# Or for a specific JSON file
sbatch run_af.sh -j path/to/pair.json
```

## Dependencies
- Python 3
- AlphaFold 3 environment