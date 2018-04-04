#!/bin/bash

#SBATCH --job-name=qg_au_prnn
#SBATCH --output=qg_au_prnn
#SBATCH --qos=gpu-long
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --time=24:00:00
#SBATCH --mem=32g

SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src
#DATA_DIR=/fs/clip-amr/question_generation/data_v9/unix.stackexchange.com
DATA_DIR=/fs/clip-amr/question_generation/data_v9/askubuntu.com
OLD_DATA_DIR=/fs/clip-amr/question_generation/datasets/stackexchange_v9/askubuntu.com
#DATA_DIR=/fs/clip-amr/question_generation/data_v9/superuser.com
EMB_DIR=/fs/clip-amr/question_generation/datasets/embeddings

python $SCRIPT_DIR/main.py --post_data_tsvfile $DATA_DIR/post_data.tsv \
							--qa_data_tsvfile $DATA_DIR/qa_data.tsv \
							--sim_ques_fname $OLD_DATA_DIR/lucene_similar_questions.txt \
							--word_vec_fname $EMB_DIR/vectors_200.txt			
