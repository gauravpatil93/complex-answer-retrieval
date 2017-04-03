#!/bin/bash

echo "============================================================="
echo "Generating results file with tagme enchanced queries........."
echo "============================================================="

python tc_generate_entitylinking_results.py all.test200.cbor.outlines all.test200.cbor.paragraphs output_entitylinking.run enhanced

echo "============================================================="
echo "Running evaluation framework on results on tagme enhanced results"
echo "============================================================="

python eval_framework.py all.test200.cbor.hierarchical.qrels output_entitylinking.run
