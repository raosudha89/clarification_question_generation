#!/bin/bash

#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=4:00:00

METEOR=/fs/clip-software/user-supported/meteor-1.5
SITENAME=Sports_and_Outdoors
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
RESULTS_DIR=/fs/clip-amr/clarification_question_generation/results/amazon/$SITENAME
OLD_CQ_DATA_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/old_data_v3/amazon/$SITENAME
OLD_RESULTS_DIR=/fs/clip-scratch/raosudha/clarification_question_generation/old_results/amazon/$SITENAME

SUFFIX=lucene
#SUFFIX=candqs_template
#SUFFIX=simqs_candqs
#SUFFIX=candqs_template_copy_coverage
#SUFFIX=candqs_template_copy
#SUFFIX=simqs_template_candqs_template
#SUFFIX=simqs_template_candqs_template_copy
#SUFFIX=simqs_template_candqs_template_copy_coverage
REF_SUFFIX=candqs

java -Xmx2G -jar $METEOR/meteor-1.5.jar $CQ_DATA_DIR/test_pred_${SUFFIX}.txt \
										$CQ_DATA_DIR/test_ref_${REF_SUFFIX}_combined \
										-l en -norm -r 10 \
									> $RESULTS_DIR/test_pred_${SUFFIX}.meteor

#java -Xmx2G -jar $METEOR/meteor-1.5.jar $OLD_CQ_DATA_DIR/test_pred_${SUFFIX}.txt \
#										$OLD_CQ_DATA_DIR/test_ref_${REF_SUFFIX}_combined \
#										-l en -norm -r 20 \
#									> $OLD_RESULTS_DIR/test_pred_${SUFFIX}.meteor
