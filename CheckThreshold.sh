#!/bin/sh
python CheckThreshold.py qt 1 0.8897 0.8872 0.8782 1
python CheckThreshold.py qt 1 0.8894 0.8861 0.8782 -1
python CheckThreshold.py qt 2 0.6768 0.6682 0.6572 1 1
python CheckThreshold.py qt 2 0.6805 0.6703 0.4 1 -1
python CheckThreshold.py qt 2 0.6756 0.6675 0.6575 -1 1
python CheckThreshold.py qt 2 0.6755 0.6677 0.6583 -1 -1

python CheckThreshold.py Openstack 1 0.8362 0.7789 0.6730 1
python CheckThreshold.py Openstack 1 0.8597 0.8178 0.6909 -1
python CheckThreshold.py Openstack 2 0.8162 0.7555 0.625 1 1
python CheckThreshold.py Openstack 2 0.8207 0.7714 0.5833 1 -1
python CheckThreshold.py Openstack 2 0.8049 0.7638 0.6364 -1 1
python CheckThreshold.py Openstack 2 0.8157 0.7759 0.6 -1 -1
