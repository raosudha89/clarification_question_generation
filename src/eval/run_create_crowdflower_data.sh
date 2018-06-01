#!/bin/bash

#SBATCH --job-name=create_crowdflower_HK
#SBATCH --output=create_crowdflower_HK
#SBATCH --qos=batch
#SBATCH --mem=36g
#SBATCH --time=24:00:00

SITENAME=Home_and_Kitchen
CORPORA_DIR=/fs/clip-corpora/amazon_qa
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
CROWDFLOWER_DIR=/fs/clip-amr/clarification_question_generation/crowdflower_eval

export PATH="/fs/clip-amr/anaconda2/bin:$PATH"

python src/eval/create_crowdflower_data.py --qa_data_fname $CORPORA_DIR/qa_${SITENAME}.json.gz \
                                            --metadata_fname $CORPORA_DIR/meta_${SITENAME}.json.gz \
                                            --test_ids $DATA_DIR/test_ids \
                                            --csv_file $CROWDFLOWER_DIR/HK_crowdflower_3models_v4.csv \
                                            --old_aggregate_results $CROWDFLOWER_DIR/HK_aggregate_3models.csv \
                                            --lucene_model $DATA_DIR/test_pred_lucene.txt \
                                            --lucene_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
                                            #--simcandqs_model $DATA_DIR/test_pred_simqs_candqs.txt \
                                            #--simcandqs_model_test_ids $DATA_DIR/test_tgt_candqs.txt.ids \
