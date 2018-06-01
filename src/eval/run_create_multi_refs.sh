#!/bin/bash

SITENAME=askubuntu_unix_superuser
DATA_DIR=/fs/clip-amr/ranking_clarification_questions/data/$SITENAME
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src/eval/
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME
UPWORK_DIR=/fs/clip-amr/question_generation/upwork/$SITENAME

python $SCRIPT_DIR/create_multi_refs.py --qa_data_tsvfile $DATA_DIR/qa_data.tsv \
                                        --human_annotations $UPWORK_DIR/human_annotations \
                                        --test_ids_file $DATA_DIR/test_ids \
                                        --ref_prefix $CQ_DATA_DIR/test_new_ref