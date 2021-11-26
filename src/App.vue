<template>
  
    <div>

        <br>
        <br>
        <br>

        <div class="battleship-title">
            <h1 class="battleship-title__content">BATTLESHIPS</h1>
        </div>

        <div class="message-flex">
            <h3 class="message-flex__text">Place your Ships</h3>
        </div>

        <br>
        <br>
        <br>
        
        <div class="battleship-playing-field">

            <!-- <div class="placement-wrapper">

                <div class="fleet-button-wrapper" :style="fleetGrid">
                    <button v-for="(v, k) in placeableShips" :key="k" class="fleet-button-wrapper__button" :style="`grid-column: 1 / span ${v.size};`" :data-index="k" :title="v.name"></button>
                </div>

                <button class="placement-wrapper__rotate-button">DONE</button>
                <button class="placement-wrapper__rotate-button">RESET</button>

            </div> -->

            
            <div class="battleship-player-field">

                <div class="w-100 d-flex justify-content-between align-items-center pb-4">
                    <div>
                        <button class="nav-button" title="Back" @click="back" :disabled="hindex == history.length">
                            <span class="mdi mdi-arrow-u-left-top-bold"></span>
                        </button>
                        <button class="nav-button" title="Forward" @click="forward" :disabled="hindex == 0">
                            <span class="mdi mdi-arrow-u-right-top-bold"></span>
                        </button>
                    </div>
                    <div>
                        <h2 class="battleship-player-field__title">{{time}}</h2>
                    </div>
                    <div>
                        <button class="nav-button" title="Hint">
                            <span class="mdi mdi-lightbulb"></span>
                        </button>
                         <button class="nav-button" title="Help" @click="showHelp = true">
                            <span class="mdi mdi-help"></span>
                        </button>
                    </div>
                </div>

                
                <div class="battleship-player-field__battleship-grid" :style="boardGrid">
                    <div v-for="v in boardSize" :key="v" @click="fire(v)" 
                        :data-row="Math.ceil(v / boardWidth)" 
                        :data-col="Math.ceil(v % boardWidth)" 
                        :data-board="'player'" :class="boardChunk(+v)">

                        <span v-if="constraint(v, true)">{{constraints[v]}}</span>
                        
                    </div>
                </div>


                <div class="w-100 d-flex justify-content-center">
                    <button class="nav-button foo-button mx-3" title="Reset" @click="reset">
                        <span>Reset</span>
                    </button>
                    <button class="nav-button foo-button mx-3" title="Done" @click="done">
                        <span>Done</span>
                    </button>
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
                    <h1 class="battleship-title__content">RULES</h1>
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

export default {
    
    data() {
        return {

            stopwatch: 0,

            boardWidth: 8 + 2,
            boardHeight: 8 + 2,

            shippedPlaces: [],
            constraints: [],

            history: [],
            hindex: 0,

            showHelp: false,

            placeableShips: [
                {
                    size: 3,
                    count: 1,
                    name: 'Carrier',
                },
                {
                    size: 2,
                    count: 2,
                    name: 'Cruiser',
                },
                                {
                    size: 1,
                    count: 3,
                    name: 'Destroyer',
                },
            ],

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

        constraint(v, visible=false) {

            if(!visible) {
                
                return Math.ceil(+v % this.boardWidth) == 1                  || 
                       Math.ceil(+v / this.boardWidth) == 1                  ||
                       Math.ceil(+v % this.boardWidth) == 0                  || 
                       Math.ceil(+v / this.boardWidth) == this.boardHeight

            } else {
                
                return +v > 1                                                &&
                       Math.ceil(+v % this.boardWidth) != 0                  &&
                       Math.ceil(+v / this.boardWidth) != this.boardHeight   &&
                      (Math.ceil(+v % this.boardWidth) == 1 || Math.ceil(v / this.boardWidth) == 1)
                       

            }
        },

        shipped(v) {
            return this.shippedPlaces.includes(v);
        },

        satisfied(v, exceded=false) {

            if(Math.ceil(v % this.boardWidth) == 1) {

                if(exceded)
                    return this.constraints[v] >= [...this.shippedPlaces.filter(i => Math.ceil(i / this.boardWidth) == Math.ceil(v / this.boardWidth))].length
                else
                    return this.constraints[v] == [...this.shippedPlaces.filter(i => Math.ceil(i / this.boardWidth) == Math.ceil(v / this.boardWidth))].length


            }

            if(Math.ceil(v / this.boardWidth) == 1) {

                if(exceded)
                    return this.constraints[v] >= [...this.shippedPlaces.filter(i => Math.ceil(i % this.boardWidth) == Math.ceil(v % this.boardWidth))].length
                else
                    return this.constraints[v] == [...this.shippedPlaces.filter(i => Math.ceil(i % this.boardWidth) == Math.ceil(v % this.boardWidth))].length

            }


            return true;
            
        },

        wrong(v, visited=[]) {

            return !this.shippedPlaces.every(i => {
               
                if(i == v)
                    return true
                
                if(visited.includes(i))
                    return true

                if(Math.abs(i - v) == 1)
                    return !this.wrong(i, [...visited, i])

                if(Math.abs(i - v) == this.boardWidth)
                    return !this.wrong(i, [...visited, i])

                if(Math.abs(i - v) == this.boardWidth - 1)
                    return false

                if(Math.abs(i - v) == this.boardWidth + 1)
                    return false

                return true

            })

        },

        fire(v, pushHistory=true) {

            if(!this.constraint(v)) {
                
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

            if(empty == 4)
                return 'C'

            return direction

        },

        boardChunk(v) {
            return { 
                'battleship-square battleship-square--empty'     : !this.constraint(v) && !this.shipped(v),
                'battleship-square battleship-square--ship'      : !this.constraint(v) &&  this.shipped(v) && !this.wrong(v),
                'battleship-square battleship-square--ship-hit'  : !this.constraint(v) &&  this.shipped(v) &&  this.wrong(v),
                'battleship-square battleship-square--const'     :  this.constraint(v),
                'unsatisfied'                                    :  this.constraint(v) && !this.satisfied(v, true),
                'satisfied'                                      :  this.constraint(v) &&  this.satisfied(v),
                'battleship-square battleship-square-circle'     :  this.prow(v) == 'C',
                'battleship-square battleship-square-left'       :  this.prow(v) == 'L',
                'battleship-square battleship-square-right'      :  this.prow(v) == 'R',
                'battleship-square battleship-square-up'         :  this.prow(v) == 'U',
                'battleship-square battleship-square-down'       :  this.prow(v) == 'D',
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
            this.shippedPlaces = []
            this.hindex = 0
            this.history = []
            this.stopwatch = 0
        },

        done() {
            
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