#!/bin/bash

#SBATCH --job-name=create_ranking_5models_v2_Home_and_Kitchen
#SBATCH --output=create_ranking_5models_v2_Home_and_Kitchen
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=Home_and_Kitchen
CORPORA_DIR=/fs/clip-corpora/amazon_qa
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
OLD_DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/old_data_v3/amazon/$SITENAME
CROWDFLOWER_DATA_DIR=/fs/clip-amr/clarification_question_generation/crowdflower_eval
export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python src/eval/create_ranking_3models.py --qa_data_fname $CORPORA_DIR/qa_${SITENAME}.json.gz \
                                            --metadata_fname $CORPORA_DIR/meta_${SITENAME}.json.gz \
                                            --test_ids $DATA_DIR/test_ids \
                                            --csv_file $CROWDFLOWER_DATA_DIR/HK_ranking_5models_v2.csv \
                                            --lucene_model $DATA_DIR/test_pred_lucene.txt \
                                            --lucene_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                            --context_model $DATA_DIR/test_pred_onlycontext.txt \
                                            --context_model_test_ids $DATA_DIR/test_tgt_onlycontext.txt.ids \
                                            --candqs_model $DATA_DIR/test_pred_candqs.txt \
                                            --candqs_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                            --candqs_template_model $DATA_DIR/test_pred_candqs_template.txt \
                                            --candqs_template_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
