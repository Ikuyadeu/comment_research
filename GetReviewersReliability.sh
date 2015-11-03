#!/bin/sh
python GetReviewersReliability.py qt 1 > CSVdata_q/numOfPatchsets_1.csv
python GetReviewersReliability.py qt 2 > CSVdata_q/numOfPatchsets_2.csv
python GetReviewersReliability.py qt 3 > CSVdata_q/numOfPatchsets_3.csv

python GetReviewersReliability.py Openstack 1 > CSVdata_o/numOfPatchsets_1.csv
python GetReviewersReliability.py Openstack 2 > CSVdata_o/numOfPatchsets_2.csv
python GetReviewersReliability.py Openstack 3 > CSVdata_o/numOfPatchsets_3.csv
