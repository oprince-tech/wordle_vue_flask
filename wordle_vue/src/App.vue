<template charset="utf-8">
  <meta charset="UTF-8">
  <div class="container">
    <Board @updateKeys="updateKeys" ref="board"/>
    <Keyboard ref="keyboard"/>
    <SubmitClear @submitAction="submitLetters" @clearAction="clearKeys"/>
    <div id="loading" v-if="loading">
      <p>Loading...</p>
    </div>
    <Matches :matches="matches" ref="matchesRef"/>
  </div>
</template>

<script>
import Board from './components/Board.vue'
import Keyboard from './components/Keyboard.vue'
import SubmitClear from './components/SubmitClear.vue'
import Matches from './components/Matches.vue'

export default {
  name: 'App',
  components: {
    Board,
    Keyboard,
    SubmitClear,
    Matches,
  },
  methods: {
    async submitLetters() {
      this.loading = true
      const keyboardLetters = this.$refs.keyboard.letters
      const boardLetters = this.$refs.board.tiles
      this.misses = keyboardLetters.filter(x => x.state === 'miss')
      this.hits = boardLetters.filter(x => x.state === 'yellow' || x.state ==='green')
      const req = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': 'http://localhost:3000'
        },
        body: JSON.stringify({hits: this.hits, misses: this.misses})
      }
      const res = await fetch("http://localhost:5000/api", req)
      const matches = await res.json();
      this.matches = matches.matches
      this.loading = false
    },
    clearKeys() {
      const letters = this.$refs.keyboard.letters
      const tiles = this.$refs.board.tiles
      letters.forEach(x => x.state = '')
      tiles.forEach(x => x.text = '')
      tiles.forEach(x => x.state = '')
    },
    updateKeys(tile) {
      const keyboardLetters = this.$refs.keyboard.letters
      const letter = keyboardLetters.filter(x => x.text === tile.text.toUpperCase())
      if (letter[0]) {
        letter[0].state = tile.state
      }
    }
  },
  data() {
    return {
      matches: this.matches,
      loading: this.loading
    }
  },
}
</script>

<style>
:root {
  --bg-color: #121213;
  --button-primary: #0275d8;
  --button-danger: #d9534f;
  --text-color: #d7dadc;
  --error-color: #dc3545;
  --light-grey: #818384;
  --dark-grey: #3a3a3c;
  --custom-yellow: #b59f3b;
  --custom-green: #538d4e;
}

html body {
  background-color: var(--bg-color);
  margin: 0;
  padding: 0;
}

input:focus {
  outline: none;
}
.container {
  background-color: var(--bg-color);
  margin: 0 auto;
  padding: 0;
  max-width: 480px !important;
  justify-content: center;
  position: relative;
}

#loading {
  color: var(--text-color);
  font-size: 1.25rem;
  font-family: monospace;
  padding-top: 15px;
  text-align: center;

}
</style>
