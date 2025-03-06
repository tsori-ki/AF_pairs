#!/bin/bash

#SBATCH --cpus-per-task=8
#SBATCH --mem=40G
#SBATCH --time=1-00:00:00

#SBATCH --mail-type=END
#SBATCH --mail-user=tsori.kislev@gmail.com

#SBATCH --output=slurms_outs/msa/%j.out



export PATH="/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/bin:$PATH"
. "/sci/labs/dina/bshor/projects/af_combdock/tools/conda_install/miniconda3/etc/profile.d/conda.sh"
conda activate /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3-conda


if [ -z "$1" ]; then
  echo "Usage: $0 <COMPLEX>"
  exit 1
fi

JSON_PATH="msa_inputs/$1.json"
OUTPUT_DIR="$(pwd)"

echo "Run MSA on $1"

cd /cs/labs/dina/tsori/af3_example/

python /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/alphafold3/run_alphafold.py --jackhmmer_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/jackhmmer --db_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/databases --model_dir /cs/usr/bshor/sci/installations/af3_variations/deepmind/models --hmmbuild_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmbuild --hmmsearch_binary_path /cs/usr/bshor/sci/installations/af3_variations/deepmind/localalphafold3/hmmer/bin/hmmsearch --norun_inference  --output_dir $OUTPUT_DIR --json_path $JSON_PATH