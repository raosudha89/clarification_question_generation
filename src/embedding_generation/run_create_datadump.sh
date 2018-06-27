#!/bin/bash

#SBATCH --job-name=datadump_Home_and_Kitchen
#SBATCH --output=datadump_Home_and_Kitchen
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=Home_and_Kitchen
DATA_DIR=/fs/clip-corpora/amazon_qa
SCRATCH_DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/data/amazon
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src/embedding_generation

export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $SCRIPT_DIR/create_datadump.py	 	--qa_data_fname $DATA_DIR/qa_${SITENAME}.json.gz \
											--metadata_fname $DATA_DIR/meta_${SITENAME}.json.gz \
											--datadump_fname $SCRATCH_DATA_DIR/$SITENAME/datadump.txt \
