#!/bin/bash

#SBATCH --qos=batch
#SBATCH --mem=4g
#SBATCH --time=4:00:00

SITENAME=Sports_and_Outdoors
DATA_DIR=/fs/clip-corpora/amazon_qa/$SITENAME
SCRIPT_DIR=/fs/clip-amr/clarification_question_generation/src/eval/
CQ_DATA_DIR=/fs/clip-amr/clarification_question_generation/data/amazon/$SITENAME
SUFFIX=simqs
REF_SUFFIX=simqs

python $SCRIPT_DIR/create_amazon_multi_refs.py 	--ques_dir $DATA_DIR/ques_docs \
                                                --test_ids_file $CQ_DATA_DIR/test_tgt_${SUFFIX}.txt.ids \
                                                --ref_prefix $CQ_DATA_DIR/test_ref_${REF_SUFFIX}
