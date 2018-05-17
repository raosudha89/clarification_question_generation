#!/bin/bash

#SBATCH --job-name=preprocess_simqs_template_candqs_template_copy_Electronics
#SBATCH --output=preprocess_simqs_template_candqs_template_copy_Electronics
#SBATCH --qos=batch
#SBATCH --mem=16g
#SBATCH --time=4:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
#SUFFIX=simqs_template_candqs_template
TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs_template

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

#python $OPENNMT/preprocess.py 	-train_src $DATA_DIR/train_src_${SUFFIX}.txt \
#								-train_tgt $DATA_DIR/train_tgt_${SUFFIX}.txt \
#								-valid_src $DATA_DIR/tune_src_${SUFFIX}.txt \
#								-valid_tgt $DATA_DIR/tune_tgt_${SUFFIX}.txt \
#								-save_data $OPENNMT_DATA/opennmt_data_${SUFFIX} \
#								-src_seq_length 350 \
#								-tgt_seq_length 50 \

python $OPENNMT/preprocess.py 	-train_src $DATA_DIR/train_src_${TRAIN_SUFFIX}.txt \
								-train_tgt $DATA_DIR/train_tgt_${TRAIN_SUFFIX}.txt \
								-valid_src $DATA_DIR/tune_src_${TEST_SUFFIX}.txt \
								-valid_tgt $DATA_DIR/tune_tgt_${TEST_SUFFIX}.txt \
								-save_data $OPENNMT_DATA/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX}_copy \
								-src_seq_length 350 \
								-tgt_seq_length 50 \
								-dynamic_dict \

