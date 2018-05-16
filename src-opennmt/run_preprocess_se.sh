#!/bin/bash

#SBATCH --job-name=preprocess_nocontext_candqs_aus
#SBATCH --output=preprocess_nocontext_candqs_aus
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=askubuntu_unix_superuser
OPENNMT=/fs/clip-amr/OpenNMT-py
OPENNMT_DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/opennmt-data/$SITENAME
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME
#TRAIN_SUFFIX=simqs_template
#TEST_SUFFIX=candqs_template
SUFFIX=nocontext_candqs

source /fs/clip-amr/gpu_virtualenv/bin/activate
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python $OPENNMT/preprocess.py 	-train_src $CQ_DATA_DIR/train_src_${SUFFIX}.txt \
								-train_tgt $CQ_DATA_DIR/train_tgt_${SUFFIX}.txt \
								-valid_src $CQ_DATA_DIR/tune_src_${SUFFIX}.txt \
								-valid_tgt $CQ_DATA_DIR/tune_tgt_${SUFFIX}.txt \
								-save_data $OPENNMT_DATA_DIR/opennmt_data_${SUFFIX} \
								-src_seq_length 350 \
								-tgt_seq_length 50 \

#python $OPENNMT/preprocess.py 	-train_src $CQ_DATA_DIR/train_src_${TRAIN_SUFFIX}.txt \
#								-train_tgt $CQ_DATA_DIR/train_tgt_${TRAIN_SUFFIX}.txt \
#								-valid_src $CQ_DATA_DIR/tune_src_${TEST_SUFFIX}.txt \
#								-valid_tgt $CQ_DATA_DIR/tune_tgt_${TEST_SUFFIX}.txt \
#								-save_data $OPENNMT_DATA_DIR/opennmt_data_${TRAIN_SUFFIX}_${TEST_SUFFIX}_copy \
#								-src_seq_length 350 \
#								-tgt_seq_length 50 \
#								-dynamic_dict \

