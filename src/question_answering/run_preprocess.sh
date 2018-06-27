#!/bin/bash

#SBATCH --job-name=preprocess_qa_Home_and_Kitchen
#SBATCH --output=preprocess_qa_Home_and_Kitchen
#SBATCH --qos=batch
#SBATCH --mem=32g
#SBATCH --time=6:00:00

SITENAME=Home_and_Kitchen
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/data/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/opennmt-data/$SITENAME

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/preprocess.py 	-train_src $DATA_DIR/train_contexts.txt \
								-train_tgt $DATA_DIR/train_answers.txt \
								-valid_src $DATA_DIR/tune_contexts.txt \
								-valid_tgt $DATA_DIR/tune_answers.txt \
								-save_data $OPENNMT_DATA/opennmt_data \
								-src_seq_length 300 \
								-tgt_seq_length 50 \

