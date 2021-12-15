%                                                                      
% GPL3 License 
%
% Author(s):                                                              
%      Antonino Natale  <ntlnnn97r06e041t@studenti.unical.it>
%      Giuseppe Agresta <grsgpp99m01c352f@studenti.unical.it>
%      Matteo Perfidio  <prfmtt98e07f537p@studenti.unical.it>
% 
% 
% Copyright (C) 2021 Krarty
%
% This file is part of Battleships AI.
%
% Battleships AI is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% Battleships AI is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with Battleships AI.  If not, see <https://www.gnu.org/licenses/>.
%


%%
%% Input Data
%%

% Size of board
int: size;

% Number of ships
int: ships_num;

% Range of indices for each cell of matrix board
set of int: mat_indices = 1..size;

% Range of indices for each placeable ship
set of int: ships_indices = 1..ships_num;

% Set of placeable ships in the board
array[ships_indices, 1..5] of opt mat_indices: given_ships; 




%%
%% Input Validation
%%

% Size validation
constraint assert (size > 0, "Value error! Size must be non negative");


% Ships validation
constraint assert (

    forall(i in ships_indices, j in 1..5) (

        if occurs(given_ships[i, j]) then 
            given_ships[i, j] > 0 /\ given_ships[i, j] <= size
        else
            j != 5
        endif
  ), 
  "Value error! Ships coordinate must be in the board"

);




%%
%% Decision Variables
%%

% Set of placed ships in the board
array[ships_indices, 1..5] of var mat_indices: ships;





%%
%% Constraints
%%

%
% Copy the ship size from input in ships decision variable set
%
constraint forall(i in ships_indices, j in 1..5) (

    if occurs(given_ships[i, j]) then 
        given_ships[i, j] = ships[i, j] 
    else 
        true
    endif

);


%
% Forall ships in the board, check if ship size constraints are satisfied horizontally or vertically
%
constraint forall(i in ships_indices) (
    (
        ships[i, 1] == ships[i, 3] /\ 
        ships[i, 2] <= ships[i, 4] /\ 
        ships[i, 5] == ships[i, 4] - ships[i, 2] + 1
    ) \/ (
        ships[i, 2] == ships[i, 4] /\ 
        ships[i, 1] <= ships[i, 3] /\ 
        ships[i, 5] == ships[i, 3] - ships[i, 1] + 1
    )
);

%
% Forall ships in the board, check if another ship is a invalid neighbor
%
constraint forall(i in ships_indices) (
    not exists(j in ships_indices) ( 
        (

            exists(r in ships[j, 1]..ships[j, 3], 
                   c in ships[j, 2]..ships[j, 4]) (
               
                r >= ships[i, 1] - 1 /\ 
                r <= ships[i, 3] + 1 /\
                c >= ships[i, 2] - 1 /\ 
                c <= ships[i, 4] + 1

            )

        ) /\ j != i
    )
);



%
% Forall ships in the board, check if ships are placed in ordered way on the
% solution to avoid different combinations of the same result
%
constraint forall(i in 1..ships_num - 1) (

    if ships[i, 5] == ships[i + 1, 5] then 
        
        if ships[i, 1] == ships[i + 1, 1] then 
            ships[i, 2] <= ships[i + 1, 2]
        else 
            ships[i, 1] <= ships[i + 1, 1]
        endif

    else 
        ships[i, 5] <= ships[i + 1, 5]
    endif

);


%%
%% Output
%%

solve satisfy;

output [
    "size = " ++ show_int(1, size) ++ ";\n"
];

output [
    "ships_num = " ++ show_int(1, ships_num) ++ ";\n"
];

output [
    "given_ships = [|\n"
];

output [
 "<>, <>, <>, <>, " ++ show_int(1, ships[i, 5]) ++ if i == ships_num then " |];\n" else " |\n" endif | i in ships_indices 
];

output [
    "constr_cols = ["
];

output [
    show_int(2, sum(j in ships_indices) (
        if i in ships[j, 1]..ships[j, 3] then 
            ships[j, 4] - ships[j, 2] + 1
        else 
            0
        endif
    )) ++ if i == size then " ];\n" else "," endif | i in mat_indices
];



output [
    "constr_rows = ["
];

output [
    show_int(2, sum(j in ships_indices) (
        if i in ships[j, 2]..ships[j, 4] then 
            ships[j, 3] - ships[j, 1] + 1
        else 
            0 
        endif
    )) ++ if i == size then " ];\n" else "," endif | i in mat_indices
];

output [
    "hints_num = 0;\n"
];

output [
    "hints = [];\n"
];
