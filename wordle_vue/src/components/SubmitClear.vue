<template>

  <div id="submitContainer">
    <button id="submitButton" @click="submitAction">Run</button>
    <button id="clearButton" @click="clearAction">Clear</button>
  </div>

</template>

<script>

  export default {
    methods: {
      submitAction() {
        this.$emit('submitAction')
      },
      clearAction() {
        this.$emit('clearAction')
      }
    },
    emits: ['submitAction', 'clearAction']
  }

</script>

<style>

  #submitContainer {
    display: flex;
    justify-content: center;
    padding-top: 20px;
    color: var(--text-color);
    font-weight: bold;
  }

  #submitContainer button {
    border: none;
    width: 4em;
    height: 2.5em;
    border-radius: 0.3rem;
    margin: 0 10px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
  }

  #submitButton {
    color: var(--text-color);
    background-color: var(--button-primary);
  }
  #clearButton {
    color: var(--text-color);
    background-color: var(--button-danger);
  }

</style>
