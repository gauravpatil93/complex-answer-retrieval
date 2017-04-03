#!/bin/bash

echo "============================================================="
echo "Generating results file with BM25 (Baseline approach)........"
echo "============================================================="

python tc_generate_entitylinking_results.py all.test200.cbor.outlines all.test200.cbor.paragraphs output_baseline.run notenhanced

echo "============================================================="
echo "Running evaluation framework on results                      "
echo "============================================================="

python eval_framework.py all.test200.cbor.hierarchical.qrels output_baseline.run
