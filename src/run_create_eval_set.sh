#!/bin/bash

#SBATCH --job-name=read_amazon_Electronics
#SBATCH --output=read_amazon_Electronics
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

#SITENAME=Automotive
SITENAME=Electronics
#SITENAME=Home_and_Kitchen
CORPORA_DIR=/fs/clip-corpora/amazon_qa
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OLD_DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/old_data/amazon/$SITENAME
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python src/create_eval_set.py   --qa_data_fname $CORPORA_DIR/qa_${SITENAME}.json.gz \
                                --metadata_fname $CORPORA_DIR/meta_${SITENAME}.json.gz \
                                --test_ids $DATA_DIR/test_ids \
                                --csv_file $DATA_DIR/evaluation_set.csv \
                                --onlycontext_model $OLD_DATA_DIR/test_pred_onlycontext.txt \
                                --onlycontext_model_test_ids $OLD_DATA_DIR/test_tgt.txt.ids \
                                --simcandqs_model $OLD_DATA_DIR/test_pred_simqs_candqs_diffcandqs.txt \
                                --simcandqs_model_test_ids $OLD_DATA_DIR/test_tgt_candqs.txt.ids \
                                --simcandqs_template_model $OLD_DATA_DIR/test_pred_simqs_template_candqs_template_diffcandqs.txt \
                                --simcandqs_template_model_test_ids $OLD_DATA_DIR/test_tgt_candqs.txt.ids \