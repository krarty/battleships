#!/bin/env python
#                                                                      
# GPL3 License 
#
# Author(s):                                                              
#      Antonino Natale  <ntlnnn97r06e041t@studenti.unical.it>
#      Giuseppe Agresta <grsgpp99m01c352f@studenti.unical.it>
#      Matteo Perfidio  <prfmtt98e07f537p@studenti.unical.it>
# 
# 
# Copyright (C) 2021 Krarty
#
# This file is part of Battleships AI.
#
# Battleships AI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Battleships AI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Battleships AI.  If not, see <https://www.gnu.org/licenses/>.
#


import os
import subprocess

M = os.path.join(os.path.dirname(__file__), '..', 'model', 'battleships.mzn')



def run_test(test_name):

    #print('Running test: ' + test_name)

    # Run the test
    out = subprocess.check_output(['minizinc', '-O5', M, os.path.join(os.path.dirname(__file__), '..', 'data', test_name) ])

    # Check the results
    out = out.decode('utf-8')

    if '=====UNSATISFIABLE=====' in out:
        print('Test %s: UNSATISFIABLE' % test_name)
    elif '----------' in out:
        print('Test %s: PASS' % test_name)
    else:
        print('Test %s: FAIL' % test_name)
        print(out)
    


for t in sorted(os.listdir(os.path.join(os.path.dirname(__file__), '..', 'data'))):
    if '6x6' in t and not '.json' in t:
        run_test(t)

for t in sorted(os.listdir(os.path.join(os.path.dirname(__file__), '..', 'data'))):
    if '8x8' in t and not '.json' in t:
        run_test(t)

for t in sorted(os.listdir(os.path.join(os.path.dirname(__file__), '..', 'data'))):
    if '10x10' in t and not '.json' in t:
        run_test(t)