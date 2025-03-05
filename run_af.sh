#!/bin/bash

#SBATCH --mem=40G
#SBATCH --time=72:00:00
#SBATCH --gres=gpu:1,vmem:20g
#SBATCH --exclude=creek-01,creek-02,firth-02,firth-01

#SBATCH --mail-type=END
#SBATCH --mail-user=tsori.kislev@gmail.com


export PATH="/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/bin:$PATH"
. "/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/etc/profile.d/conda.sh"
conda activate /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3-conda

cd /cs/labs/dina/tsori/af3_example/

if [ -z "$1" ]; then
  echo "Usage: $0 [-j] <pair/folder>"
  exit 1
fi

if [ "$1" == "-j" ]; then
  PAIR="$2"
  if [ -z "$PAIR" ]; then
    echo "Usage: $0 -j <pair.json>"
    exit 1
  fi
  OUTPUT_DIR=$(dirname "$(dirname "$PAIR")")
  echo "Run AF3 on file: $PAIR"
  echo "Output directory: $OUTPUT_DIR"
    python /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3/run_alphafold.py --jackhmmer_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/jackhmmer --db_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/databases --model_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/models --hmmbuild_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmbuild --hmmsearch_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmsearch --norun_data_pipeline --output_dir $OUTPUT_DIR --json_path $PAIR
  
  
  
else
  COMPLEX="$1"
  INPUT_DIR="$COMPLEX/msa_pairs"
  echo "Run AF3 on $COMPLEX"
  echo "input dir $INPUT_DIR"
  python /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3/run_alphafold.py --jackhmmer_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/jackhmmer --db_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/databases --model_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/models --hmmbuild_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmbuild --hmmsearch_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmsearch --norun_data_pipeline --output_dir $COMPLEX --input_dir $INPUT_DIR  
  
fi

