#!/bin/bash

#SBATCH --job-name=translate_simcandqs_template_diffcandqs_Electronics
#SBATCH --output=translate_simcandqs_template_diffcandqs_Electronics
#SBATCH --qos=gpu-medium
#SBATCH --partition=gpu
#SBATCH --gres=gpu
#SBATCH --mem=32g
#SBATCH --time=10:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs_template

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

#python $OPENNMT/translate.py	-model /fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/Electronics/opennmt_model_simqs_candqs_acc_36.54_ppl_26.05_e15.pt \
python $OPENNMT/translate.py	-model /fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/Electronics/opennmt_model_simqs_template_candqs_template_acc_36.55_ppl_26.05_e15.pt \
								-src $DATA_DIR/test_src_${TEST_SUFFIX}.txt \
								-output $DATA_DIR/test_pred_${TRAIN_SUFFIX}_${TEST_SUFFIX}_diffcandqs.txt \
								-replace_unk \
								-gpu 0 \

#python $OPENNMT/translate.py	-model $OPENNMT_DATA/opennmt_model_acc_*_e15.pt \
#							 	-src $DATA_DIR/test_src.txt \
#								-output $DATA_DIR/test_pred_onlycontext.txt \
#								-replace_unk -gpu 0

