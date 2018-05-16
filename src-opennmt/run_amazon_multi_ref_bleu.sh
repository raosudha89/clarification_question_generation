#!/bin/bash

#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=05:00:00

#SUFFIX=onlycontext
#SUFFIX=nocontext_candqs_diffcandqs
#SUFFIX=candqs_diffcand
#SUFFIX=candqs_template_diffcand
#SUFFIX=candqs_copy_diffcandqs
#SUFFIX=candqs_copy_coverage_diffcandqs
#SUFFIX=simqs_candqs_diffcandqs
#SUFFIX=simqs_template_candqs_template_diffcandqs
#SUFFIX=simqs_moreqs
SUFFIX=simqs_template_moreqs

SITENAME=Electronics
DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
BLEU_SCRIPT=/fs/clip-software/user-supported/mosesdecoder/3.0/scripts/generic/multi-bleu.perl
RESULTS_DIR=/fs/clip-amr/clarification_question_generation/results/amazon/$SITENAME
#REF_PREFIX=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME/test_ref
#REF_PREFIX=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME/test_ref_candqs
REF_PREFIX=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME/test_ref_simqs

wc -l ${REF_PREFIX}0
wc -l $DATA_DIR/test_pred_${SUFFIX}.txt

perl $BLEU_SCRIPT $REF_PREFIX < $DATA_DIR/test_pred_${SUFFIX}.txt > $RESULTS_DIR/${SUFFIX}.score

#python $SCRIPT_DIR/amazon_multi_ref_bleu.py	--ques_dir $CORPORA_DIR/ques_docs \
#											--model_output_file $DATA_DIR/test_pred_${SUFFIX}.txt \
#											--model_name $SUFFIX \
#											--test_ids_file $DATA_DIR/test_tgt.txt.ids \
#											> $RESULTS_DIR/${SUFFIX}.score
#											#--test_ids_file $DATA_DIR/test_tgt_candqs.txt.ids \
#											#--test_ids_file $DATA_DIR/test_tgt_simqs.txt.ids \
