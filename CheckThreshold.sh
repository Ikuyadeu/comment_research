#!/bin/sh
python CheckThreshold.py qt 1 0.8903 0.8876 0.8794 1
python CheckThreshold.py qt 1 0.8901 0.8872 0.8795 -1
python CheckThreshold.py qt 2 0.6775 0.6735 0.6613 1 1
python CheckThreshold.py qt 2 0.6808 0.6747 0.4286 1 -1
python CheckThreshold.py qt 2 0.6772 0.6731 0.6604 -1 1
python CheckThreshold.py qt 2 0.6765 0.6724 0.6583 -1 -1

python CheckThreshold.py Openstack 1 0.8698 0.8402 0.75 1
python CheckThreshold.py Openstack 1 0.8672 0.8317 0.7143 -1
python CheckThreshold.py Openstack 2 0.8257 0.7947 0.6863 1 1
python CheckThreshold.py Openstack 2 0.8265 0.7832 0.6364 1 -1
python CheckThreshold.py Openstack 2 0.8131 0.7771 0.6667 -1 1
python CheckThreshold.py Openstack 2 0.8235 0.7834 0.6154 -1 -1
