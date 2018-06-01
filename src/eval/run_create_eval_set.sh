#!/bin/bash

#SBATCH --job-name=create_eval_set_Home_and_Kitchen
#SBATCH --output=create_eval_set_Home_and_Kitchen
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=Home_and_Kitchen
CORPORA_DIR=/fs/clip-corpora/amazon_qa
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python src/eval/create_eval_set.py   --qa_data_fname $CORPORA_DIR/qa_${SITENAME}.json.gz \
                                --metadata_fname $CORPORA_DIR/meta_${SITENAME}.json.gz \
                                --test_ids $DATA_DIR/test_ids \
                                --csv_file $DATA_DIR/evaluation_set.csv \
                                --lucene_model $DATA_DIR/test_pred_lucene.txt \
                                --lucene_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                --nocontext_model $DATA_DIR/test_pred_nocontext_candqs.txt \
                                --nocontext_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                --onlycontext_model $DATA_DIR/test_pred_onlycontext.txt \
                                --onlycontext_model_test_ids $DATA_DIR/test_tgt_onlycontext.txt.ids \
                                --candqs_model $DATA_DIR/test_pred_candqs_copy_coverage.txt \
                                --candqs_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                --candqs_template_model $DATA_DIR/test_pred_candqs_template_copy_coverage.txt \
                                --candqs_template_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
