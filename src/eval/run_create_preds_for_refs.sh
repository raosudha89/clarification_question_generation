#!/bin/bash

#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=05:00:00

#SUFFIX=onlycontext
#SUFFIX=nocontext_candqs
#SUFFIX=lucene
#SUFFIX=candqs
#SUFFIX=candqs_template
SUFFIX=simqs
#SUFFIX=simqs_template_moreqs
#SUFFIX=candqs_copy
#SUFFIX=candqs_coverage
#SUFFIX=candqs_copy_coverage
#SUFFIX=candqs_template_copy
#SUFFIX=candqs_template_coverage
#SUFFIX=candqs_template_copy_coverage
#SUFFIX=simqs_candqs
#SUFFIX=simqs_candqs_copy
#SUFFIX=simqs_candqs_copy_coverage
#SUFFIX=simqs_template
#SUFFIX=simqs_template_candqs_template
#SUFFIX=simqs_template_candqs_template_copy
#SUFFIX=simqs_template_candqs_template_copy_coverage

SITENAME=askubuntu_unix_superuser
DATA_DIR=/fs/clip-amr/ranking_clarification_questions/data/$SITENAME
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src/eval/
UPWORK=/fs/clip-amr/question_generation/upwork/$SITENAME

python $SCRIPT_DIR/create_preds_for_refs.py	--qa_data_tsvfile $DATA_DIR/qa_data.tsv \
  											--test_ids_file $DATA_DIR/test_ids \
										 	--human_annotations $UPWORK/human_annotations \
					  						--model_output_file $CQ_DATA_DIR/test_pred_${SUFFIX}.txt \

