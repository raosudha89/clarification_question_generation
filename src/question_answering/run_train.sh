#!/bin/bash

#SBATCH --job-name=train_qa_Home_and_Kitchen
#SBATCH --output=train_qa_Home_and_Kitchen
#SBATCH --qos=gpu-medium
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=12:00:00

SITENAME=Home_and_Kitchen
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/data/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/question_answering/opennmt-data/$SITENAME

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data \
							-save_model $OPENNMT_DATA/opennmt_model \
							-gpuid 0 -epochs 20 \
							-batch_size 128 \
