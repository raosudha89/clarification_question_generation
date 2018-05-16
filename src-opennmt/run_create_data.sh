#!/bin/bash

#SITENAME=askubuntu.com
SITENAME=askubuntu_unix_superuser
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src-opennmt
DATA_DIR=/fs/clip-amr/ranking_clarification_questions/data/$SITENAME
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME

python $SCRIPT_DIR/create_data.py --post_data_tsvfile $DATA_DIR/post_data.tsv \
							--qa_data_tsvfile $DATA_DIR/qa_data.tsv \
							--train_ids_file $DATA_DIR/train_ids \
							--tune_ids_file $DATA_DIR/tune_ids \
							--test_ids_file $DATA_DIR/test_ids \
							--train_src_fname $CQ_DATA_DIR/train_src \
							--train_tgt_fname $CQ_DATA_DIR/train_tgt \
							--tune_src_fname $CQ_DATA_DIR/tune_src \
							--tune_tgt_fname $CQ_DATA_DIR/tune_tgt \
							--test_src_fname $CQ_DATA_DIR/test_src \
							--test_tgt_fname $CQ_DATA_DIR/test_tgt \
							--sim_ques_fname $DATA_DIR/lucene_similar_questions.txt \
							--candqs True \
							--nocontext True \
							#--simqs True \
							#--template True \
							#--onlycontext True \
