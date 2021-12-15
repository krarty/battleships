# Dots And Boxes
[![Build Status](https://travis-ci.com/mantik-org/dots-and-boxes.svg?branch=main)](https://travis-ci.com/mantik-org/dots-and-boxes)
[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](/LICENSE) 

Battleship is a strategy type guessing game for single player.

## Description
The Battleship puzzle (sometimes called Bimaru, Yubotu, Solitaire Battleships or Battleship Solitaire) is a logic puzzle based on the Battleship guessing game. Battleship is played in a grid of squares that hides ships of different sizes. Numbers alongside the grid indicate how many squares in a row or column are occupied by part of a ship.

![Screenshot](/docs/images/screen01.png)

## Rules
The goal of the game is to place a certain number of ships of different sizes within the grid. Some battleships may be partially revealed. A battleship is a straight line of consecutive blocks. The number of the battleships from each size is shown in the legend below the grid. It’s not possible to place a ship in the neighborhood of another one.
The numbers outside the grid show the number of cells occupied by battleships on that row or column.

## Strategy
The basic solving strategy for a Battleship puzzle is to add segments to incomplete ships where appropriate, draw water in squares that are known not to contain a ship segment, and to complete ships in a row or column whose number is the same as the number of unsolved squares in that row or column, respectively. More advanced strategies include looking for places where the largest ship that has not yet been located can fit into the grid, and looking for rows and columns that are almost complete and determining if there is only one way to complete them.

## Sources
In this project, artificial intelligence was supported by [MiniZinc](https://www.minizinc.org/).  
MiniZinc is a free and open-source **constraint modeling language**. MiniZinc can be used to model constraint satisfaction and optimization problems in a high-level, solver-independent way, taking advantage of a large library of pre-defined constraints. The model is then compiled into FlatZinc, a solver input language that is understood by a wide range of solvers. MiniZinc is developed at Monash University in collaboration with Data61 Decision Sciences and the University of Melbourne.

Notable sources are:
- **Model**, [https://github.com/krarty/battleships-ai/blob/main/src/model/battleships.mzn](https://github.com/krarty/battleships-ai/blob/main/src/model/battleships.mzn) AI for calculate next move to complete the game.
- **Instance Generator**, [https://github.com/krarty/battleships-ai/blob/main/src/model/battleships-generator.mzn](https://github.com/krarty/battleships-ai/blob/main/src/model/battleships-generator.mzn) generate new random game instance.


## Build

To run Battleships, execute the following command:
```shell script
$ yarn 
$ yarn serve
```
**NOTE:** Building and running require [Python 3.x.x](https://www.python.org/) or greater.  

## Run
Open your web browser on http://localhost:8080 after successful build.  


## Third-Party Software
Battleships uses and depends on third-party open-source tools and libraries which are outside of this repository.
## License

Copyright (c) Krarty. All rights reserved.

Licensed under the [GPL-3.0](/LICENSE) license.
