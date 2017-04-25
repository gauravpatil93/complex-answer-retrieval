#!/bin/bash


echo "============================================================="
echo "Generating cache for entity linking ..............           "
echo "============================================================="

python tc_generate_document_cache.py $1 $2 $3 enhanced


echo "============================================================="
echo "Generating results file with entity linking............      "
echo "============================================================="


python tc_generate_entitylinking_results.py $1 $2 $3 enhanced

echo "============================================================="
echo "Running evaluation framework on results with entity linking  "
echo "============================================================="

python eval_framework.py $4 $5
