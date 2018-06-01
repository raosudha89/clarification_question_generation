#!/bin/bash

#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=4:00:00

METEOR=/fs/clip-software/user-supported/meteor-1.5
SITENAME=askubuntu_unix_superuser
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/$SITENAME
RESULTS_DIR=/fs/clip-amr/clarification_question_generation/results/$SITENAME
SUFFIX=simqs_template_candqs_template

java -Xmx2G -jar $METEOR/meteor-1.5.jar $CQ_DATA_DIR/test_pred_${SUFFIX}.txt.hasrefs \
										$CQ_DATA_DIR/test_ref_combined \
										-l en -norm -r 6 \
									> $RESULTS_DIR/test_pred_${SUFFIX}.meteor
