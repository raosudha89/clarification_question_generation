#!/bin/bash

#SBATCH --job-name=preprocess_simcandqs_template_Electronics
#SBATCH --output=preprocess_simcandqs_template_Electronics
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=Electronics
OPENNMT=/fs/clip-amr/OpenNMT-py
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OPENNMT_DATA=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
TRAIN_SUFFIX=simqs_template
TEST_SUFFIX=candqs_template

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/preprocess.py 	-train_src $DATA_DIR/train_src_${TRAIN_SUFFIX}.txt \
								-train_tgt $DATA_DIR/train_tgt_${TRAIN_SUFFIX}.txt \
								-valid_src $DATA_DIR/tune_src_${TEST_SUFFIX}.txt \
								-valid_tgt $DATA_DIR/tune_tgt_${TEST_SUFFIX}.txt \
								-save_data $OPENNMT_DATA/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX} \
								-src_seq_length 350 \
								-tgt_seq_length 50 \

#python $OPENNMT/preprocess.py 	-train_src $DATA_DIR/train_src.txt \
#								-train_tgt $DATA_DIR/train_tgt.txt \
#								-valid_src $DATA_DIR/tune_src.txt \
#								-valid_tgt $DATA_DIR/tune_tgt.txt \
#								-save_data $OPENNMT_DATA/opennmt_data \
#								-src_seq_length 350 \
#								-tgt_seq_length 50 \
