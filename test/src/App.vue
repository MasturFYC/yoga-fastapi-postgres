<script>
import { defineComponent } from "vue";
import HelloWorld from './components/HelloWorld.vue'
import Test from './components/Test.vue'
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup

export default defineComponent({
  name: 'App',
  data() {
    return {
      www: 'Welcome'
    }
  },
  components: {    
    HelloWorld,
    Test
  },
  methods: {
    woiii(e) {
      this.www = e
    }
  },
})


</script>

<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld msg="Hello Vue 3 + Vite" />
  <Test :pesan="www" @setPesan="woiii" />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
