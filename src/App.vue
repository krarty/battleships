<template>
  
    <div class="app">


        <div class="my-5">

            <div class="battleship-title">
                <h1 class="battleship-title-content">BATTLESHIPS</h1>
            </div>

            <div v-if="state === 'running'" class="message-flex">
                <h3 class="message-flex-text">Place your Ships</h3>
            </div>

            <div v-if="state === 'init'" class="message-flex">
                <h3 class="message-flex-text">Select your game difficulty</h3>
            </div>

            <div v-if="state === 'loading'" class='tetrominos my-5'>
                <div class='tetromino box1'></div>
                <div class='tetromino box2'></div>
                <div class='tetromino box3'></div>
                <div class='tetromino box4'></div>
            </div>

             <div v-if="state === 'error'" class="message-flex">
                <h3 class="message-flex-text error">There was an error...</h3>
            </div>

        </div>
        


        <div v-if="state === 'running'" class="battleship-playing-field">
            
             <div class="d-flex justify-content-between align-items-center pb-4">
                <div class="mx-5 px-2">
                    <button class="nav-button" title="Back" @click="back" :disabled="+hindex === +history.length">
                        <span class="mdi mdi-arrow-u-left-top-bold"></span>
                    </button>
                    <button class="nav-button" title="Forward" @click="forward" :disabled="+hindex === 0">
                        <span class="mdi mdi-arrow-u-right-top-bold"></span>
                    </button>
                </div>
                <div class="mx-5 px-5">
                    <h2 class="battleship-player-field-title">{{time}}</h2>
                </div>
                <div class="mx-5 px-2">
                    <button class="nav-button" title="Hint">
                        <span class="mdi mdi-lightbulb"></span>
                    </button>
                        <button class="nav-button" title="Help" @click="showHelp = true">
                        <span class="mdi mdi-help"></span>
                    </button>
                </div>
            </div>

        </div>


        <div v-if="state === 'running'" class="battleship-playing-field">

           
            <div class="placement-wrapper">

                <div class="fleet-button-wrapper">
                    <div v-for="(v, k) of placeableShips" :key="k">
                        <div v-if="v.size > 1" class="d-flex">
                            <div class="fleet-ship battleship-square-left">X</div>
                            <div v-for="(i, j) of (v.size - 2)" :key="j" class="fleet-ship">C</div>
                            <div class="fleet-ship battleship-square-right">X</div>
                        </div>
                        <div v-else>
                            <div class="fleet-ship battleship-square-circle">
                                <span class="mdi mdi-sail-boat mdi-24px"></span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            
            <div class="battleship-player-field">

                
                <div class="battleship-player-field-battleship-grid" :style="boardGrid">
                    <div v-for="v in boardSize" :key="v" @click="fire(v)" class="d-flex justify-content-center align-items-center"
                        :data-row="Math.ceil(v / boardWidth)" 
                        :data-col="Math.ceil(v % boardWidth)" 
                        :data-board="'player'" :class="boardChunk(+v)">

                        <span v-if="constraint(v, true)">{{constraints[v]}}</span>
                        <span v-if="locked(v)" class="mdi mdi-lock mdi-24px text-muted"></span>
                        
                    </div>
                </div>


                <div class="w-100 d-flex justify-content-center mb-5">
                    <button class="nav-button foo-button mx-3" title="Reset" @click="reset">
                        <span>Reset</span>
                    </button>
                    <button class="nav-button foo-button mx-3" title="Done" @click="done">
                        <span>Done</span>
                    </button>
                </div>

            </div>

        </div>

        <div v-if="state === 'init'">

            <div class="w-100 text-center">

                <div class="my-5">
                    <select v-model="difficulty" class="battleship-difficulty-select">
                        <option value="6x6">Easy</option>
                        <option value="8x8">Medium</option>
                        <option value="10x10">Hard</option>
                        <option value="random">Random</option>
                    </select>
                </div>

                <div class="my-5">
                    <button class="nav-button" @click="start">Start</button>
                </div>

            </div>

        </div>

        
        <div class="modal-help" v-show="showHelp">

            <div class="w-100 d-flex justify-content-end">
                <button class="nav-button" @click="showHelp = false">
                    <span class="mdi mdi-close-thick"></span>
                </button>
            </div>

            <div class="modal-help-body">

                <div class="battleship-title py-3">
                    <h1 class="battleship-title-content">RULES</h1>
                </div>

                <p>
                    The rules of Battleships are simple:<br>
                    You have to find the location of the battleships hidden in the grid. Some battleships may be partially revealed.
                    A battleship is a straight line of consecutive black cells.
                    The number of the battleships from each size is shown in the legend below the grid.
                    2 battleships cannot touch each other (even diagonally)
                    The numbers outside the grid show the number of cells occupied by battleships on that row/column.
                    The numbers outside the grid show the number of cells occupied by battleships on that row/column.
                </p>
            </div>

        </div>
    

    </div>

</template>


<script>

import '@/assets/css/style.css'
import AI from '@/assets/js/ai.js'

export default {
    
    data() {
        return {

            state: 'init',
            stopwatch: 0,

            boardWidth: 8 + 2,
            boardHeight: 8 + 2,

            shippedPlaces: [],
            placeableShips: [],
            constraints: [],
            lockedPlaces: [],

            history: [],
            hindex: 0,

            showHelp: false,


            difficulty: '6x6',

        }
    },

    computed: {

        boardSize() {
            return parseInt(this.boardWidth * this.boardHeight);
        },

        boardGrid() {
            return {
                'grid-template-columns' : `repeat(${this.boardWidth} , 1fr)`,
                'grid-template-rows'    : `repeat(${this.boardHeight}, 1fr)`,
            }
        },

        fleetGrid() {
            return {
                'grid-template-columns' : `repeat(${4}, 1fr)`,
                'grid-template-rows'    : `repeat(${this.placeableShips.length}, 1fr)`,
            }
        },

        time() {
            return `${(String(Math.floor(this.stopwatch / 60)).padStart(2, 0))}:${(String(Math.floor(this.stopwatch % 60)).padStart(2, 0))}`;
        }

    },

    methods: {

        locked(v) {
            return this.lockedPlaces.includes(v)
        },

        constraint(v, visible=false) {

            if(!visible) {
                
                return Math.ceil(+v % this.boardWidth) === 1                  ||
                       Math.ceil(+v / this.boardWidth) === 1                  ||
                       Math.ceil(+v % this.boardWidth) === 0                  ||
                       Math.ceil(+v / this.boardWidth) === this.boardHeight

            } else {
                
                return +v > 1                                                 &&
                       Math.ceil(+v % this.boardWidth) !== 0                  &&
                       Math.ceil(+v / this.boardWidth) !== this.boardHeight   &&
                      (Math.ceil(+v % this.boardWidth) === 1 || Math.ceil(v / this.boardWidth) === 1)
                       

            }
        },

        shipped(v) {
            return this.shippedPlaces.includes(v);
        },

        satisfied(v, exceeded=false) {

            if(Math.ceil(v % this.boardWidth) === 1) {

                if(exceeded)
                    return this.constraints[v] >= [...this.shippedPlaces.filter(i => Math.ceil(i / this.boardWidth) === Math.ceil(v / this.boardWidth))].length
                else
                    return this.constraints[v] === [...this.shippedPlaces.filter(i => Math.ceil(i / this.boardWidth) === Math.ceil(v / this.boardWidth))].length


            }

            if(Math.ceil(v / this.boardWidth) === 1) {

                if(exceeded)
                    return this.constraints[v] >= [...this.shippedPlaces.filter(i => Math.ceil(i % this.boardWidth) === Math.ceil(v % this.boardWidth))].length
                else
                    return this.constraints[v] === [...this.shippedPlaces.filter(i => Math.ceil(i % this.boardWidth) === Math.ceil(v % this.boardWidth))].length

            }


            return true;
            
        },

        wrong(v, visited=[]) {

            return !this.shippedPlaces.every(i => {
               
                if(i === v)
                    return true
                
                if(visited.includes(i))
                    return true

                if(Math.abs(i - v) === 1)
                    return !this.wrong(i, [...visited, i])

                if(Math.abs(i - v) === this.boardWidth)
                    return !this.wrong(i, [...visited, i])

                if(Math.abs(i - v) === this.boardWidth - 1)
                    return false

                return Math.abs(i - v) !== this.boardWidth + 1;

            })

        },

        fire(v, pushHistory=true) {

            if(!this.constraint(v) && !this.locked(v)) {
                
                if(pushHistory) {
                    this.history = [v, ...this.history.slice(this.hindex)]
                    this.hindex = 0
                }

                if(this.shipped(v))
                    this.shippedPlaces.splice(this.shippedPlaces.indexOf(v), 1);
                else
                    this.shippedPlaces.push(v);

            }
        },

        prow(v) {

            if(!this.shipped(v))
                return false


            let empty = 4
            let direction = ''

            if(this.shippedPlaces.includes(v + 1)) {
                empty--
                direction = 'L'
            }

            if(this.shippedPlaces.includes(v - 1)) {
                empty--
                direction = 'R'
            }

            if(this.shippedPlaces.includes(v + this.boardWidth)) {
                empty--
                direction = 'U'
            }

            if(this.shippedPlaces.includes(v - this.boardWidth)) {
                empty--
                direction = 'D'
            }


            if(empty < 3)
                return ''

            if(empty === 4)
                return 'C'

            return direction

        },

        boardChunk(v) {
            return { 
                'battleship-square battleship-square-empty'     : !this.constraint(v) && !this.shipped(v),
                'battleship-square battleship-square-ship'      : !this.constraint(v) &&  this.shipped(v) && !this.wrong(v),
                'battleship-square battleship-square-ship-hit'  : !this.constraint(v) &&  this.shipped(v) &&  this.wrong(v),
                'battleship-square battleship-square-const'     :  this.constraint(v),
                'unsatisfied'                                    :  this.constraint(v) && !this.satisfied(v, true),
                'satisfied'                                      :  this.constraint(v) &&  this.satisfied(v),
                'battleship-square battleship-square-circle'     :  this.prow(v) === 'C',
                'battleship-square battleship-square-left'       :  this.prow(v) === 'L',
                'battleship-square battleship-square-right'      :  this.prow(v) === 'R',
                'battleship-square battleship-square-up'         :  this.prow(v) === 'U',
                'battleship-square battleship-square-down'       :  this.prow(v) === 'D',
            }
        },

        back() {
       
            if(this.hindex < this.history.length)
                this.fire(this.history[this.hindex++], false)
        
        },

        forward() {
            
            if(this.hindex > 0)
                this.fire(this.history[--this.hindex], false)
        
        },


        reset() {
            this.shippedPlaces = this.shippedPlaces.filter(i => this.locked(i))
            this.hindex = 0
            this.history = []
            this.stopwatch = 0
        },

        done() {
            
        },

        run(msg) {

            this.boardWidth = msg.data.constraints.cols.length + 2
            this.boardHeight = msg.data.constraints.rows.length + 2

            this.constraints = new Array(this.boardWidth * this.boardHeight)
            this.constraints = this.constraints.fill(0)

            this.lockedPlaces = new Array(this.boardWidth * this.boardHeight)
            this.lockedPlaces = this.lockedPlaces.fill(0)


            console.log(msg)

            msg.data.constraints.cols.forEach((e, i) => this.constraints[(i + 2)] = Number(e))
            msg.data.constraints.rows.forEach((e, i) => this.constraints[(i + 1) * this.boardWidth + 1] = Number(e))

            msg.data.hints.forEach(e => this.shippedPlaces.push(e[0] * this.boardWidth + e[1] + 1))
            msg.data.hints.forEach(e => this.lockedPlaces.push(e[0] * this.boardWidth + e[1] + 1))


            ;[...new Set(msg.data.ships)].forEach(i => {
                this.placeableShips.push({
                    size: i,
                    count: msg.data.ships.filter(j => j === i).length
                })
            })


            this.state = 'running'

        },

        start() {

            this.state = 'loading'

            AI('localhost', 8765,

                (ws) => {

                    ws.send(JSON.stringify({
                        type: 'init',
                        difficulty: this.difficulty,
                    }))

                },

                (ws, msg) => {

                    switch(msg.type) {
                        case 'run':
                            this.run(msg)
                            break
                        case 'error':
                            this.state = 'error'
                            break
                    }

                },

                () => {
                    this.state = 'error'
                },

            )

        }

    },

    mounted() {

        setInterval(() => {
            this.stopwatch += 1;
        }, 1000);


        this.constraints = [...Array(this.boardSize).keys()]
            .map(() => Math.floor(Math.random() * 5))
        
        
    },
}


</script>