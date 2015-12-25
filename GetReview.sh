#!/bin/sh
python GetReview.py qt 1 > CSVdata_oss/Review_qt_1.csv
python GetReview.py qt 2 > CSVdata_oss/Review_qt_2.csv
python GetReview.py qt 3 > CSVdata_oss/Review_qt_3.csv

python GetReview.py Openstack 1 > CSVdata_oss/Review_os_1.csv
python GetReview.py Openstack 2 > CSVdata_oss/Review_os_2.csv
python GetReview.py Openstack 3 > CSVdata_oss/Review_os_3.csv
