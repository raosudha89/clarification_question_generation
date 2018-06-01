#!/bin/bash

SITENAME=Home_and_Kitchen
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
SUFFIX=candqs
ID_SUFFIX=candqs

export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

for i in {0..19}
do
    python src/eval/create_equal_no_of_preds.py --model_outputs $DATA_DIR/test_ref_${SUFFIX}$i \
                                                --model_test_ids $DATA_DIR/test_tgt_${ID_SUFFIX}.txt.ids \
                                                --new_model_outputs $DATA_DIR/test_ref_equalno_${SUFFIX}$i \
                                        
done 