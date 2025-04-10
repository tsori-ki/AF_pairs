#!/bin/bash

#SBATCH --cpus-per-task=8
#SBATCH --mem=40G
#SBATCH --time=2-00:00:00

#SBATCH --mail-type=END
#SBATCH --mail-user=tsori.kislev@gmail.com

#SBATCH --exclude=sm-01,sm-16

#SBATCH --output=slurms_outs/msa/%j.out

export XLA_FLAGS="--xla_disable_hlo_passes=custom-kernel-fusion-rewriter"

# Documentation:
# This script runs the MSA (Multiple Sequence Alignment) process for a given input JSON file.
# Usage:
#   ./msa.sh <INPUT_JSON_PATH> <OUTPUT_DIR>
# Arguments:
#   <INPUT_JSON_PATH>: Path to the input JSON file.
#   <OUTPUT_DIR>: Directory where the output will be saved.

export PATH="/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/bin:$PATH"
. "/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/etc/profile.d/conda.sh"
conda activate /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3-conda

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <INPUT_JSON_PATH> <OUTPUT_DIR>"
  exit 1
fi

JSON_PATH=$1
OUTPUT_DIR=$2

# Validate input JSON file
if [ ! -f "$JSON_PATH" ]; then
  echo "Error: Input JSON file '$JSON_PATH' does not exist."
  exit 1
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Run MSA with input JSON: $JSON_PATH"

cd /cs/labs/dina/tsori/af3_example/

python /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3/run_alphafold.py \
  --jackhmmer_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/jackhmmer \
  --db_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/databases \
  --model_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/models \
  --hmmbuild_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmbuild \
  --hmmsearch_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmsearch \
  --norun_inference \
  --output_dir "$OUTPUT_DIR" \
  --json_path "$JSON_PATH"

OUTPUT_JSON_PATH="$OUTPUT_DIR/$(basename "$JSON_PATH" .json)_data.json"
python msa_to_pairwise.py "$JSON_PATH" "$OUTPUT_JSON_PATH"
