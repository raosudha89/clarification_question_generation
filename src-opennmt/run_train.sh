#!/bin/bash

#SBATCH --job-name=train_simcandqs_template_Electronics
#SBATCH --output=train_simcandqs_template_Electronics
#SBATCH --qos=gpu-medium
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=64g
#SBATCH --time=10:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs_template

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX} \
							-save_model $OPENNMT_DATA/opennmt_model_${TRAIN_SUFFIX}_${TEST_SUFFIX} \
							-gpuid 0 -epochs 15 -batch_size 128 \
							#-copy_attn \
							#-coverage_attn \

#python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data \
#							-save_model $OPENNMT_DATA/opennmt_model \
#							-gpuid 0 -epochs 15 -batch_size 128 \

