<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>

#app {
  min-height: 100vh;
}

body, html {
  margin: 0;
  width: 100%;
  min-height: 100vh;
}

body {
  background: url("./assets/background.jpg") no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  overflow: hidden;
}

</style>
