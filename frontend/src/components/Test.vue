<template>
  <h1>{{ pesan }}</h1>
  <button @click="buttonClick">Test</button>
    <ul id="v-for-object" class="demo">
    <li v-for="cat in categories" v-bind:key="cat.id">
        {{ cat.name }}
    </li>
    </ul>  

</template>

<script>

export default {
    name: 'Test',
    props: ['pesan'],
    emits:['setPesan'],
    data() {
        return {
            categories: []
        }
    },
    methods : {
        async buttonClick() {
            const res = await fetch("http://localhost:8080/categories/");
            const json = await res.json();
            this.categories = json
            this.$emit("setPesan", this.categories[0].name);
        }
    }
}
</script>


<style scoped>
h1 {
  color: red;
}
</style>
