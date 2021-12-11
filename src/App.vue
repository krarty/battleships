<template>

    <div class="app">

        <div class="my-4">

            <div class="battleship-title">
                <h1 class="battleship-title-content" v-if="state === 'init'">BATTLESHIPS</h1>
                <h5 class="battleship-title-content animate__animated animate__backInDown message-flex" v-if="state === 'running'">
                    <span class="animated-pulse">BATTLESHIPS</span>
                </h5>
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
            
             <div class="d-flex justify-content-between align-items-baseline pb-4">
                <div class="mx-5 px-2 animate__animated animate__backInLeft">
                    <button class="nav-button mr-3" title="Reset" @click="reset">
                        <span class="mdi mdi-delete"></span>
                    </button>
                    <button class="nav-button" title="Back" @click="back" :disabled="+hindex === +history.length">
                        <span class="mdi mdi-arrow-u-left-top-bold"></span>
                    </button>
                    <button class="nav-button" title="Forward" @click="forward" :disabled="+hindex === 0">
                        <span class="mdi mdi-arrow-u-right-top-bold"></span>
                    </button>
                </div>
                <div class="mx-5 px-5 animate__animated animate__zoomIn">
                    <h2 class="battleship-player-field-title">{{time}}</h2>
                </div>
                <div class="mx-5 px-2 animate__animated animate__backInRight">
                    <button class="nav-button" title="Done" @click="showDone = true">
                        <span class="mdi mdi-check-bold"></span>
                    </button>
                    <button class="nav-button" title="Hint" @click="hint">
                        <span class="mdi mdi-lightbulb"></span>
                    </button>
                    <button class="nav-button ml-3" title="Help" @click="showHelp = true">
                        <span class="mdi mdi-help"></span>
                    </button>
                </div>
            </div>

        </div>


        <div v-if="state === 'running'" class="battleship-playing-field animate__animated animate__backInUp">

            
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


                <div class="battleship-goals">
                
                    <p v-for="(v, k) in placeableShips" :key="k" class="mt-2">
                        <del  v-if="goal(v)" class="text-muted">{{k + 1}}) You have to place exactly {{v.count}} ships of size {{v.size}}</del>
                        <span v-if="!goal(v)">{{k + 1}}) You have to place exactly {{v.count}} ships of size {{v.size}}</span>
                    </p>

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

        
        <div class="modal-help animate__animated animate__zoomIn" v-show="showHelp">

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


        <div class="modal-help animate__animated animate__zoomIn" v-show="showDone">

            <div class="w-100 d-flex justify-content-end">
                <button class="nav-button" @click="showDone = false">
                    <span class="mdi mdi-close-thick"></span>
                </button>
            </div>

            <div v-if="!errors && difference === 0" class="modal-help-body">

                <div class="battleship-title py-3">
                    <h1 class="battleship-title-modal">You Win!</h1>
                </div>

                <p class="text-center">

                    <button class="nav-button" @click="reset">
                        <span>Rematch</span>
                    </button>
                    <button class="nav-button" @click="reload">
                        <span>Start menu</span>
                    </button>

                </p>

            </div>

            <div v-if="!errors && difference !== 0" class="modal-help-body">

                <div class="battleship-title py-3">
                    <h1 class="battleship-title-modal">You're almost done!</h1>
                </div>

                <p class="text-center">
                    You have to solve the puzzle! So far good, {{difference}} to go!
                </p>

            </div>

            <div v-if="errors" class="modal-help-body">

                <div class="battleship-title py-3">
                    <h1 class="battleship-title-modal">Try again!</h1>
                </div>

                <p class="text-center">
                    You have errors in your solution!
                </p>

            </div>

        </div>
    
       
    </div>

</template>


<script>

import '@/assets/css/style.css'
import 'animate.css'
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

            solution: [],
            hints: [],

            history: [],
            hindex: 0,

            showHelp: false,
            showDone: false,

            difficulty: '6x6',

        }
    },

    computed: {

        boardSize() {
            return parseInt(this.boardWidth * this.boardHeight)
        },

        boardGrid() {
            return {
                'grid-template-columns' : `repeat(${this.boardWidth} , 1fr)`,
                'grid-template-rows'    : `repeat(${this.boardHeight}, 1fr)`,
            }
        },

        time() {
            return `${(String(Math.floor(this.stopwatch / 60)).padStart(2, 0))}:${(String(Math.floor(this.stopwatch % 60)).padStart(2, 0))}`
        },

        difference() {
            return Math.abs(this.shippedPlaces.length - this.solution.reduce((a, b) => a + b, 0))
        },

        errors() {
            
            for(let i = 0; i < this.boardSize; i++) {

                if(this.solution[i] === 0 && this.shipped(i))
                    return true

            }

            return false

        },

    },

    methods: {

        locked(v) {
            return this.lockedPlaces.includes(v)
        },

        hinted(v) {
            return this.hints[v] === 1
        },

        hint() {

            const candidates = this.solution.map((e, i) => (e === 1 && !this.shipped(i)) || (e === 0 && this.shipped(i)) ? i : 0).filter(e => e !== 0)

            if(candidates.length === 0)
                return

            
            if(this.shippedPlaces.length === 0) {

                if(!this.hints.includes(candidates[0]))
                    this.hints.push(candidates[0])

            } else {

                const distances = []
                
                for(const s of this.shippedPlaces) {

                    const sr = Math.floor(s / this.boardWidth)
                    const sc = Math.floor(s % this.boardWidth)

                    for(const c of candidates) {

                        const cr = Math.floor(c / this.boardWidth)
                        const cc = Math.floor(c % this.boardWidth)
                        
                        distances.push({
                            candidate: c,
                            distance: Math.sqrt(Math.pow(sr - cr, 2) + Math.pow(sc - cc, 2))
                        })

                    }

                }
                

                distances.sort((a, b) => a.distance - b.distance)
                
                this.hints.push(distances[0].candidate)


            }

            
            

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

        goal(v) {

            if(v.size === 1) {

                return this.shippedPlaces.filter(i => {

                    return !(
                        this.shippedPlaces.includes(i + 1)               ||
                        this.shippedPlaces.includes(i - 1)               ||
                        this.shippedPlaces.includes(i + this.boardWidth) ||
                        this.shippedPlaces.includes(i - this.boardWidth)
                    )

                }).length === v.count

            } else {

                const q = []

                return this.shippedPlaces.sort((a, b) => a - b).filter(i => {

                    if(q.includes(i))
                        return false


                    const searchIn = (i) => {

                        if(!this.shippedPlaces.includes(i))
                            return false

                        q.push(i)
                        return true

                    }


                    const searchRight = () => {
                        
                        for(let start = i; start <= i + v.size - 1; start++) {

                            if(!searchIn(start))
                                return false
                        
                        }

                        return !searchIn(i + v.size)

                    }

                    const searchLeft = () => {
                        
                        for(let start = i; start >= i - v.size + 1; start--) {

                            if(!searchIn(start))
                                return false
                        
                        }

                        return !searchIn(i - v.size)
                        
                    }


                    const searchUp = () => {
                        
                        for(let start = i; start >= i - (v.size + 1) * this.boardWidth; start -= this.boardWidth) {

                            if(!searchIn(start))
                                return false
                        
                        }

                        return !searchIn(i - v.size * this.boardWidth)
                        
                    }


                    const searchDown = () => {
                        
                        for(let start = i; start <= i + (v.size - 1) * this.boardWidth; start += this.boardWidth) {

                            if(!searchIn(start))
                                return false
                        
                        }

                        return !searchIn(i + v.size * this.boardWidth)
                        
                    }


                    if(searchRight() || searchLeft() || searchUp() || searchDown())
                        return true

                }).length === v.count

            }
            
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
                'battleship-square battleship-square-empty'      : !this.constraint(v) && !this.shipped(v),
                'battleship-square battleship-square-ship'       : !this.constraint(v) &&  this.shipped(v) && !this.wrong(v),
                'battleship-square battleship-square-ship-hit'   : !this.constraint(v) &&  this.shipped(v) &&  this.wrong(v),
                'battleship-square battleship-square-const'      :  this.constraint(v),
                'unsatisfied'                                    :  this.constraint(v) && !this.satisfied(v, true),
                'satisfied'                                      :  this.constraint(v) &&  this.satisfied(v),
                'battleship-square battleship-square-circle'     :  this.prow(v) === 'C',
                'battleship-square battleship-square-left'       :  this.prow(v) === 'L',
                'battleship-square battleship-square-right'      :  this.prow(v) === 'R',
                'battleship-square battleship-square-up'         :  this.prow(v) === 'U',
                'battleship-square battleship-square-down'       :  this.prow(v) === 'D',
                'battleship-square battleship-square-hints-add'  : !this.shipped(v) && this.hints.includes(v) && this.solution[v] === 1,
                'battleship-square battleship-square-hints-rm'   :  this.shipped(v) && this.hints.includes(v) && this.solution[v] === 0,
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
            this.hints = []
            this.stopwatch = 0
            this.showHelp = false
            this.showDone = false
        },

        reload() {
            window.location.reload()
        },

        run(msg) {

            this.boardWidth = msg.data.constraints.cols.length + 2
            this.boardHeight = msg.data.constraints.rows.length + 2

            this.constraints = new Array(this.boardWidth * this.boardHeight)
            this.constraints = this.constraints.fill(0)

            this.lockedPlaces = new Array(this.boardWidth * this.boardHeight)
            this.lockedPlaces = this.lockedPlaces.fill(0)

            this.solution = [...new Array(this.boardSize)].map((e, i) => {

                const row = Math.ceil(i / this.boardWidth)
                const col = Math.ceil(i % this.boardWidth)

                for(const s of msg.solution) {

                    if(row >= (s[0] + 1) && row <= (s[2] + 1) && col >= (s[1] + 1) && col <= (s[3] + 1))
                        return 1

                }

                return 0

            })


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