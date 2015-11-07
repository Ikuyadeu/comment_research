#!/bin/sh
python GetReviewersReliability2.py qt 1 > CSVdata_q_2/numOfPatchsets_1.csv
python GetReviewersReliability2.py qt 2 > CSVdata_q_2/numOfPatchsets_2.csv
python GetReviewersReliability2.py qt 3 > CSVdata_q_2/numOfPatchsets_3.csv

python GetReviewersReliability2.py Openstack 1 > CSVdata_o_2/numOfPatchsets_1.csv
python GetReviewersReliability2.py Openstack 2 > CSVdata_o_2/numOfPatchsets_2.csv
python GetReviewersReliability2.py Openstack 3 > CSVdata_o_2/numOfPatchsets_3.csv
