#!/bin/bash

SITENAME=Home_and_Kitchen
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
SUFFIX=candqs_template_copy_coverage
ID_SUFFIX=candqs

export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python src/eval/create_pred_perid.py --test_ids $DATA_DIR/test_ids \
                                --model_outputs $DATA_DIR/test_pred_${SUFFIX}.txt \
                                --model_test_ids $DATA_DIR/test_tgt_${ID_SUFFIX}.txt.ids \
                                --model_outputs_perid $DATA_DIR/test_pred_${SUFFIX}_perid.txt \

