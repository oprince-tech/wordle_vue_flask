<template>

  <div id="board">
    <div v-for="(tile, index) in tiles" :key="tile.id" class="tile">
      <input ref="inp" @input="targetNext(index)" v-model="tile.text" class="letterInput" :class="[tile.state]" maxlength="1" type="text">
      <span @click="appendTile(tile.id)" class="underscore"></span>
    </div>
  </div>

</template>

<script>

  export default {
    methods: {
      appendTile(id) {
        let tile = this.tiles[id]
        if (tile.state === '') {
          tile.state = 'yellow'
        } else if (tile.state === 'yellow') {
          tile.state = 'green'
        } else if (tile.state === 'green') {
          tile.state = 'miss'
        } else if (tile.state === 'miss') {
          tile.state = ''
        }
        this.$emit('updateKeys', tile)
      },
      targetNext(i) {
        if (i + 1 < this.tiles.length) {
          this.$refs.inp[i + 1].focus()
        }
      }
    },
    name: 'Board',
    emits: ['updateKeys'],
    data() {
      return {
        tiles: [
          { id: 0, text: '', state: '' },
          { id: 1, text: '', state: '' },
          { id: 2, text: '', state: '' },
          { id: 3, text: '', state: '' },
          { id: 4, text: '', state: '' }
        ]
      }
    }
  }

</script>

<style scoped>

  #board {
    padding-top: 50px;
    width: 100%;
    margin: auto;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .tile {
    width: 80px;
    position: relative;
    height: 72px;
    justify-content: space-between;
    padding: 0;
  }

  .letterInput {
    text-decoration: none;
    color: var(--text-color);
    background-color: var(--bg-color);
    border: none;
    text-transform: uppercase;
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    border-style: none;
    width: 100%;
    min-height: 64px;
    padding: 0;
  }

  .letterInput.miss {
    background-color: var(--dark-grey) !important;
  }
  .letterInput.yellow {
    background-color: var(--custom-yellow) !important;
  }
  .letterInput.green {
    background-color: var(--custom-green) !important;
  }

  .underscore {
    position: absolute;
    width: 100%;
    padding: 0;
    left: 0;
    bottom: 0;
    margin: 0;
    height: 0.5rem;
    background-color: #dddddd;
  }

</style>
