#!/bin/bash

echo "============================================================="
echo "Generating results file with entity linking............      "
echo "============================================================="

python tc_generate_entitylinking_results.py all.test200.cbor.outlines all.test200.cbor.paragraphs output_entitylinking.run enhanced

echo "============================================================="
echo "Running evaluation framework on results with entity linking  "
echo "============================================================="

python eval_framework.py all.test200.cbor.hierarchical.qrels output_entitylinking.run
