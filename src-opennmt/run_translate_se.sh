#!/bin/bash

#SBATCH --job-name=translate_nocontext_candqs_aus
#SBATCH --output=translate_nocontext_candqs_aus
#SBATCH --qos=gpu-medium
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=10:00:00

SITENAME=askubuntu_unix_superuser
OPENNMT=/fs/clip-amr/OpenNMT-py
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
SUFFIX=nocontext_candqs
#TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/translate.py	-model $OPENNMT_DATA/opennmt_model_${SUFFIX}_acc_*_e20.pt \
							 	-src $CQ_DATA_DIR/test_src_${TEST_SUFFIX}.txt \
								-output $CQ_DATA_DIR/test_pred_${SUFFIX}.txt \
								-replace_unk -gpu 0 \
							 	#-src $CQ_DATA_DIR/test_src_${SUFFIX}.txt \

#python $OPENNMT/translate.py	-model $OPENNMT_DATA/opennmt_model_${TRAIN_SUFFIX}_${TEST_SUFFIX}_acc_*_e20.pt \
#							 	-src $CQ_DATA_DIR/test_src_${TEST_SUFFIX}.txt \
#								-output $CQ_DATA_DIR/test_pred_${TRAIN_SUFFIX}_${TEST_SUFFIX}.txt \
#								-replace_unk -gpu 0 \


