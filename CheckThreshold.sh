#!/bin/sh
python CheckThreshold.py qt 1 0.6058 0.5975 0.5757  1
python CheckThreshold.py qt 1 0.606 0.6006 0.5632 -1
python CheckThreshold.py qt 2 0.607 0.6008 0.5556 1 1
python CheckThreshold.py qt 2 0.6308 0.6038 0.4 1 -1
python CheckThreshold.py qt 2 0.6073 0.6011 0.56 -1 1
python CheckThreshold.py qt 2 0.6186 0.5982 0.5 -1 -1

python CheckThreshold.py Openstack 1 0.565 0.5553 0.4919 1
python CheckThreshold.py Openstack 1 0.5617 0.552 0.5035 -1
python CheckThreshold.py Openstack 2 0.5744 0.5551 0.48 1 1
python CheckThreshold.py Openstack 2 0.5818 0.5522 0.2748 1 -1
python CheckThreshold.py Openstack 2 0.563 0.5517 0.4857 -1 1
python CheckThreshold.py Openstack 2 0.5692 0.5513 0.4194 -1 -1
