<template>

  <div id="matchesContainer">
    <table>
      <tbody>
        <tr v-for="match in matches" :key="matches">
          <td>{{ match }}</td>
        </tr>
      </tbody>
    </table>
  </div>

</template>

<script>

  export default {
    name: 'Matches',
    props: {
      matches: Object,
      loading: Boolean
    }
  }

</script>

<style scoped>

  #matchesContainer {
    color: var(--text-color);
    font-size: 20px;
    font-family: monospace;
    padding-top: 15px;
  }
  #matchesContainer table {
    margin: 0 auto;
  }

</style>
