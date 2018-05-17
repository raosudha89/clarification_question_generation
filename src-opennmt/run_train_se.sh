#!/bin/bash

#SBATCH --job-name=train_simqs_candqs_copy_coverage_aus
#SBATCH --output=train_simqs_candqs_copy_coverage_aus
#SBATCH --qos=gpu-medium
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=10:00:00

SITENAME=askubuntu_unix_superuser
OPENNMT=/fs/clip-amr/OpenNMT-py
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
#SUFFIX=simqs
TRAIN_SUFFIX=simqs
TEST_SUFFIX=candqs

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

#python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data_${SUFFIX} \
#							-save_model $OPENNMT_DATA/opennmt_model_${SUFFIX} \
#							-gpuid 0 -epochs 20 \

python $OPENNMT/train.py 	-data $OPENNMT_DATA/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX}_copy \
							-save_model $OPENNMT_DATA/opennmt_model_${TRAIN_SUFFIX}_${TEST_SUFFIX}_copy_coverage \
							-gpuid 0 -epochs 20 \
							-copy_attn \
							-coverage_attn \

