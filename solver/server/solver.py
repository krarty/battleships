#!/bin/env python3
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


import asyncio
import websockets
import logging
import json
import os
import requests
import re
import sys
import argparse
import random
import nest_asyncio

from minizinc import Instance, Model, Solver, Status


MOD_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'battleships.mzn')
GEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'battleships-generator.mzn')
DAT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
CCH_PATH = os.path.join(os.path.dirname(__file__), '..', 'cache')


parser = argparse.ArgumentParser(description='Run Battleships Solver')
parser.add_argument('--port', type=int, default=8765, help='Port to run the Battleships Solver on')
parser.add_argument('--model', type=str, default=MOD_PATH, help='Path to the Battleships solver model')
parser.add_argument('--generator', type=str, default=GEN_PATH, help='Path to the Battleships generator model')
parser.add_argument('--data', type=str, default=DAT_PATH, help='Path to the Battleships data')
parser.add_argument('--force', action='store_true', help='Force replacing of existing instances')
parser.add_argument('--fetch', action='store_true', help='Enable fetching and caching instances')
parser.add_argument('--cachedir', type=str, default=CCH_PATH, help='Path to the cached instances')
parser.add_argument('--debug', action='store_true', help='Run the Battleships Solver in debug mode')
parser.add_argument('--instances', type=int, default=10, help='Size of random instances of the Battleships data')
args = parser.parse_args()




async def dispatch(ws, message):

    if message['type'] == 'init':
        await init(ws, message)

    else:
        await ws.send(json.dumps({
            'type': 'error', 
            'message': 'unknown message type'
        }))


async def init(ws, message):


    if message['difficulty'] == 'random':
        return await generate_instance(ws)


    inst = random.randint(0, args.instances - 1)
    data = os.path.join(args.data, 'battleships-instance-%s-%d.dzn' % (message['difficulty'], inst))
    jsfd = os.path.join(args.data, 'battleships-instance-%s-%d.json' % (message['difficulty'], inst))
    cache = os.path.join(args.cachedir, 'battleships-instance-%s-%d.cache' % (message['difficulty'], inst))

    
    logging.info('Solving with difficulty %s and instance %s' % (message['difficulty'], inst))

    if not os.path.exists(data):
        await ws.send(json.dumps({
            'type': 'error', 
            'message': 'difficulty not available'
        }))



    solution = None

    if os.path.exists(cache):

        with open(cache) as fd:
            solution = '\n'.join(fd.readlines())

    else:

        m = Model()
        m.add_file(args.model)
        m.add_file(data)


        r = Instance(Solver.lookup('gecode'), m).solve(optimisation_level=5)

        if r.solution is None or  r.status == Status.UNSATISFIABLE:
            await ws.send(json.dumps({
                'type': 'error', 
                'message': 'no solution found'
            }))


        solution = str(r.solution)



    solution = solution.split('\n')
    solution = [x for x in solution if x != '']

    for i in range(len(solution)):

        solution[i] = solution[i].strip()
        solution[i] = re.sub('\s+', ',', solution[i])
        solution[i] = solution[i].split(',')
        solution[i] = [x for x in solution[i] if x != '']
        solution[i] = [int(x) for x in solution[i]]



    with open(jsfd) as fd:
        await ws.send(json.dumps({
            'type': 'run', 
            'solution': solution,
            'data': json.load(fd)
        }))



async def run(ws, path):

    async for message in ws:

        logging.info('Received message on path %s: %s' % (path, message))

        if path == '/':
            await dispatch(ws, json.loads(message))

        else:
            await ws.send(json.dumps({
                'type': 'error',
                'message': 'unknown path'
            }))



def fetch_instance(ships, size, instances, attempts=1, force=False):

    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'battleships-instance-%dx%d-%d.dzn' % (size[0], size[0], instances))

    if not force and not args.force and os.path.exists(path):
        return


    logging.info('Fetching instance %s %dx%d [%d] #%d' % (size[1], size[0], size[0], instances, attempts))

    r = requests.get('https://www.puzzle-battleships.com/?size=%s' % size[1])
    r = re.search('task\s= \'(.+)\';', r.text)
    r = r.group(1)
    r = r.split(';')


    # Parse Contraints section
    s = r[0].split(',')
    cols = s[:size[0]]
    rows = s[size[0]:]


    # Parse Hints section
    c = r[1]
    k = 0

    hints = []

    for i in range(len(c)):

        if str(c[i]).isdigit():

            if int(c[i]) > 0:

                row = (k // size[0]) + 1
                col = (k %  size[0]) + 1

                hints.append((row, col))

            else:
                return fetch_instance(ships, size, instances, attempts + 1, True)

            k += 1
        
        else:
            k += ord(c[i]) - 96

    
    with open(path, 'w') as f:
        
        f.write('%%\n')
        f.write('%% Autogenerated by %s, instance %s %dx%d [%d] #%d <%s>\n' % (__file__, size[1], size[0], size[0], instances, attempts, c))
        f.write('%% Source: https://www.puzzle-battleships.com/?size=%s\n' % size[1])
        f.write('%%\n\n')
        f.write('size = %d;\n' % size[0])
        f.write('hints_num = %d;\n' % len(hints))
        f.write('hints = [| ')
        f.write(' | '.join(['%d, %d' % (row, col) for row, col in hints]))
        f.write(' |];\n')
        f.write('ships_num = %d;\n' % len(ships[size[1]]))
        f.write('\n')
        f.write('constr_rows = [');
        f.write(', '.join(rows));
        f.write('];\n')
        f.write('constr_cols = [');
        f.write(', '.join(cols));
        f.write('];\n')
        f.write('\n')
        f.write('given_ships = [|\n')

        for ship in ships[size[1]][:-1]:
            f.write('<>, <>, <>, <>, %d, |\n' % ship)
        
        f.write('<>, <>, <>, <>, %d  |];\n' % ships[size[1]][-1])
        f.write('\n')

    
    with open(f'{path[:-4]}.json', 'w') as f:

        f.write(json.dumps({
            'size': size[0],
            'hints': hints,
            'constraints': {
                'rows': rows,
                'cols': cols
            },
            'ships': ships[size[1]]
        }))



    # Check and cache instance result

    m = Model()
    m.add_file(args.model)
    m.add_file(path)


    r = Instance(Solver.lookup('gecode'), m).solve(optimisation_level=5, all_solutions=True)


    if len(r) > 1:
        logging.error('Build %s: OVERFLOW' % path)

    elif r.solution is None or r.status == Status.UNSATISFIABLE:
        logging.error('Build %s: UNSATISFIABLE' % path)

    else:

        logging.info('Build %s: PASS' % path)

        with open(os.path.join(args.cachedir, 'battleships-instance-%dx%d-%d.cache' % (size[0], size[0], instances)), 'w') as f:
            f.write(str(r.solution[0]))


        return True


    return fetch_instance(ships, size, instances, attempts + 1, True)




def fetch_instances():

    logging.info('Fetching instances...')

    ships = {
        '0' : [1, 1, 1, 2, 2, 3],
        '2' : [1, 1, 1, 2, 2, 2, 3, 3, 4],
        '4' : [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    }

    for size in [(6, '0'), (8, '2'), (10, '4')]:
        for instances in range(args.instances):
            fetch_instance(ships, size, instances)


    logging.info('Fetching instances...OK')




async def generate_instance(ws, attempts=1):

    logging.info('Solving with difficulty random')
    logging.info('Generating instance... #%d' % attempts)


    size = (6, '0')
    path = os.path.join(os.path.dirname(args.generator), 'generator', 'battleships-generator-%dx%d.dzn' % (size[0], size[0]))


    m = Model()
    m.add_file(args.generator)
    m.add_file(path)


    r = Instance(Solver.lookup('gecode'), m).solve(optimisation_level=5, nr_solutions=30)

    if r.solution is None or r.status == Status.UNSATISFIABLE:
        return await generate_instance(ws, attempts + 1)


    logging.info('Generating instance...OK')


    inst = str(random.choice(r.solution))

    m = Model()
    m.add_file(args.model)
    m.add_string(inst)


    logging.info('Generating Hints...')

    r = Instance(Solver.lookup('gecode'), m).solve(optimisation_level=5, all_solutions=True)

    if r.solution is None or r.status == Status.UNSATISFIABLE:
        return await generate_instance(ws, attempts + 1)


    logging.info('Generated %d solutions' % len(r.solution))

    hints = []
    board = [0 for _ in range(size[0] * size[0])]
    owner = [0 for _ in range(size[0] * size[0])]

    ownerId = 1

    for s in r.solution:

        for k in str(s).split('\n'):

            if not k.strip():
                continue

            k = k.strip()
            k = re.sub(r'\s+', ' ', k)
            k = re.sub(r'\s+', ',', k)
            k = k.split(',')

            ra = int(k[0]) - 1
            ca = int(k[1]) - 1
            rb = int(k[2]) - 1
            cb = int(k[3]) - 1

            for i in range(ra, rb + 1):
                for j in range(ca, cb + 1):
                    board[i * size[0] + j] = board[i * size[0] + j] + 1
                    owner[i * size[0] + j] = ownerId

        ownerId = ownerId + 1



    ownerId = 0

    for i in range(size[0] * size[0]):
            
            if board[i] == 1:

                if ownerId == 0:
                    ownerId = owner[i]

                if owner[i] == ownerId:
                    hints.append((i // size[0] + 1, i % size[0] + 1))


    if hints == []:
        return await generate_instance(ws, attempts + 1)

    if len(hints) > 3:
        hints = random.sample(hints, 3)

    
    logging.info('Generating Hints...OK')
    
    solution = r.solution[ownerId - 1]
    solution = str(solution)
    solution = solution.split('\n')
    solution = [x for x in solution if x != '']

    for i in range(len(solution)):

        solution[i] = solution[i].strip()
        solution[i] = re.sub('\s+', ',', solution[i])
        solution[i] = solution[i].split(',')
        solution[i] = [x for x in solution[i] if x != '']
        solution[i] = [int(x) for x in solution[i]]



    rows = re.search(r'constr_rows\s+=\s+\[\s*(.*?)\s*\];', inst).group(1)
    rows = rows.split(',')
    rows = [x.strip() for x in rows]

    cols = re.search(r'constr_cols\s+=\s+\[\s*(.*?)\s*\];', inst).group(1)
    cols = cols.split(',')
    cols = [x.strip() for x in cols]


    logging.info('Generated random instance %dx%d with hints: %s, contraints: %s %s' % (size[0], size[0], hints, rows, cols))

    await ws.send(json.dumps({
        'type': 'run', 
        'solution': solution,
        'data': {
            'size': size[0],
            'hints': hints,
            'constraints': {
                'rows': rows,
                'cols': cols,
            },
            'ships': [1, 1, 1, 2, 2, 3]
        }
    }))
            



def main():

    nest_asyncio.apply()


    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


    if not os.path.exists(args.model):
        logging.error('Model path does not exist')
        sys.exit(1)

    if not os.path.exists(args.data):
        os.mkdir(args.data)

    if not os.path.exists(args.cachedir):
        os.mkdir(args.cachedir)

    if args.fetch:
        fetch_instances()
    else:
        logging.info('Skipping fetching instances')
    


    logging.info('Running Server on %s...' % args.port)
    server = websockets.serve(run, 'localhost', args.port)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

    return 0


if __name__ == '__main__':
    sys.exit(main())
