#!/bin/bash

#SBATCH --qos=batch
#SBATCH --job-name=create_we_Home_and_Kitchen
#SBATCH --output=create_we_Home_and_Kitchen
#SBATCH --mem=32g
#SBATCH --time=12:00:00 

SITENAME=Home_and_Kitchen
EMB_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/data/embeddings/$SITENAME
SCRIPTS_DIR=/fs/clip-amr/clarification_question_generation/src/embedding_generation

python $SCRIPTS_DIR/create_we_vocab.py $EMB_DIR/vectors.txt $EMB_DIR/word_embeddings.p $EMB_DIR/vocab.p

