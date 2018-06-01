#!/bin/bash

#SBATCH --job-name=create_equal_no_of_preds
#SBATCH --output=create_equal_no_of_preds
#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=4:00:00

SITENAME=Home_and_Kitchen
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
SUFFIX=lucene
ID_SUFFIX=candqs
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src

export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python ${SCRIPT_DIR}/eval/create_equal_no_of_preds.py   --model_outputs $DATA_DIR/test_pred_${SUFFIX}.txt \
                                                        --model_test_ids $DATA_DIR/test_tgt_${ID_SUFFIX}.txt.ids \
                                                        --new_model_outputs $DATA_DIR/test_pred_${SUFFIX}_equalno.txt \

