#!/bin/bash

#SBATCH --job-name=train_simqs_template_candqs_template_Electronics
#SBATCH --output=train_simqs_template_candqs_template_Electronics
#SBATCH --qos=gpu-long
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=12:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
#SUFFIX=candqs_template
TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs_template

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

#python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data_${SUFFIX} \
#							-save_model $OPENNMT_DATA/opennmt_model_${SUFFIX} \
#							-gpuid 0 -epochs 20 -batch_size 128 \
#							#-src_word_vec_size 200 \
#							#-tgt_word_vec_size 200 \

python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX} \
							-save_model $OPENNMT_DATA/opennmt_model_${TRAIN_SUFFIX}_${TEST_SUFFIX} \
							-gpuid 0 -epochs 20 -batch_size 128 \
							#-copy_attn \
							#-coverage_attn \

