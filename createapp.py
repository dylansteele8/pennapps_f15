#!/usr/bin/env python

import os
import sys

PROJECT_NAME = 'pennapps_f15'

if len(sys.argv) <= 1:
    print "You must supply an app name."
    print "run 'python createapp.py [APP_NAME]'"
    sys.exit(1)

print "Creating %s App..." % sys.argv[1]
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(PROJECT_ROOT, 'pennapps_f15/apps'))
if (os.system('python ../../manage.py startapp %s' % sys.argv[1]) == 0):
  print "App %s created!" % sys.argv[1]
else:
  print "Oops, it failed. Please try again!"
