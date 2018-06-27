#!/bin/bash

#SBATCH --job-name=translate_qa_Home_and_Kitchen
#SBATCH --output=translate_qa_Home_and_Kitchen
#SBATCH --qos=gpu-short
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=2:00:00

SITENAME=Home_and_Kitchen
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/data/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/opennmt-data/$SITENAME

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/translate.py    -model $OPENNMT_DATA/opennmt_model_acc_*_e20.pt \
								-src $DATA_DIR/test_contexts.txt \
								-output $DATA_DIR/test_pred_answers.txt \
								-replace_unk \
								-gpu 0\


