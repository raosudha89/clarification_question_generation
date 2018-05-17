#!/bin/bash

#SBATCH --job-name=translate_onlycontext_Electronics
#SBATCH --output=translate_onlycontext_Electronics
#SBATCH --qos=batch
#SBATCH --mem=32g
#SBATCH --time=12:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
SUFFIX=onlycontext
#TRAIN_SUFFIX=onlycontext_template
#TEST_SUFFIX=onlycontext

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/translate.py    -model $OPENNMT_DATA/opennmt_model_${SUFFIX}_acc_*_e20.pt \
								-src $DATA_DIR/test_src_${SUFFIX}.txt \
								-output $DATA_DIR/test_pred_${SUFFIX}.txt \
								-replace_unk \
								#-gpu \

#python $OPENNMT/translate.py    -model $OPENNMT_DATA/opennmt_model_${TRAIN_SUFFIX}_${TEST_SUFFIX}_acc_*_e20.pt \
#								-src $DATA_DIR/test_src_${TEST_SUFFIX}.txt \
#								-output $DATA_DIR/test_pred_${TRAIN_SUFFIX}_${TEST_SUFFIX}.txt \
#								-replace_unk \
#								-gpu 0 \


