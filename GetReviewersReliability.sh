#!/bin/sh
python GetReviewersReliability.py qt 1 > CSVdata_oss/numOfPatchsets_qt_1.csv
python GetReviewersReliability.py qt 2 > CSVdata_oss/numOfPatchsets_qt_2.csv
python GetReviewersReliability.py qt 3 > CSVdata_oss/numOfPatchsets_qt_3.csv

python GetReviewersReliability.py Openstack 1 > CSVdata_oss/numOfPatchsets_os_1.csv
python GetReviewersReliability.py Openstack 2 > CSVdata_oss/numOfPatchsets_os_2.csv
python GetReviewersReliability.py Openstack 3 > CSVdata_oss/numOfPatchsets_os_3.csv
