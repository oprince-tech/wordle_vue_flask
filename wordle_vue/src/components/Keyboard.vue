<template>

  <div id="keyboard">
    <button v-for="(letter, index) in letters" :item="letter" :key="letter.id" :class="[letter.state]" @click="cycleKey(letter.id)">{{letter.text}}</button>
  </div>

</template>

<script>

  export default {
    components: {},
    methods: {
      cycleKey(id) {
        let letter = this.letters[id]
        if (letter.state !== 'miss') {
          letter.state = 'miss'
        } else {
          letter.state = ''
        }
        this.$emit('updateTiles', letter)
      }
    },
    emits: ['updateTiles'],
    data() {
      return {
        letters: [
          { id: 0, text: 'Q', state: '' },
          { id: 1, text: 'W', state: '' },
          { id: 2, text: 'E', state: '' },
          { id: 3, text: 'R', state: '' },
          { id: 4, text: 'T', state: '' },
          { id: 5, text: 'Y', state: '' },
          { id: 6, text: 'U', state: '' },
          { id: 7, text: 'I', state: '' },
          { id: 8, text: 'O', state: '' },
          { id: 9, text: 'P', state: '' },
          { id: 10, text: 'A', state: '' },
          { id: 11, text: 'S', state: '' },
          { id: 12, text: 'D', state: '' },
          { id: 13, text: 'F', state: '' },
          { id: 14, text: 'G', state: '' },
          { id: 15, text: 'H', state: '' },
          { id: 16, text: 'J', state: '' },
          { id: 17, text: 'K', state: '' },
          { id: 18, text: 'L', state: '' },
          { id: 19, text: 'Z', state: '' },
          { id: 20, text: 'X', state: '' },
          { id: 21, text: 'C', state: '' },
          { id: 22, text: 'V', state: '' },
          { id: 23, text: 'B', state: '' },
          { id: 24, text: 'N', state: '' },
          { id: 25, text: 'M', state: '' }
        ],
        misses: [],
        yellows: [],
        greens: []
      }
    }
  }

</script>

<style scoped>

  #keyboard {
    display: grid;
    grid-template-columns: repeat(20, minmax(auto, 1em));
    grid-auto-rows: 3em;
    gap: 0.3em;
    justify-content: center;
    padding-top: 40px;
  }

  button:nth-child(11) {
    grid-column: 2 / 4;
  }

  button:nth-child(20) {
    grid-column: 4/6;
  }

  button.miss {
    background-color: var(--dark-grey) !important;
  }
  button.yellow {
    background-color: var(--custom-yellow) !important;
  }
  button.green {
    background-color: var(--custom-green) !important;
  }

  button {
    font-size: inherit;
    grid-column: span 2;
    color: white;
    background-color: var(--light-grey);
    font-size: 16px;
    font-weight: 500;
    align-items: center;
    border: none;
    border-radius: 0.2em;
    cursor: pointer;
  }

  #submitContainer {
    padding-top: 1em;
  }

</style>
