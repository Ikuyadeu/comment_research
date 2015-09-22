# -*- coding: utf-8 -*-
#!/usr/bin/python3

import re
import sys
import csv
import time
import MySQLdb
from collections import defaultdict
from datetime import datetime
from Class import ReviewerClass

try:
    cnn = mysql
