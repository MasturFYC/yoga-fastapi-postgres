<template>
  <div>
    <h1 class="h1">Product Category</h1>
    <p>Product Category adalah data induk dari data product </p>
    <table width='100%'>
        <tbody v-for="cat in categories" :key="cat.id">
        <tr>
            <td>{{cat.id}}</td>
            <td>{{cat.name}}</td>
        </tr>
        </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'Category',
  data() {
      return {
          categories: []
      }
  },
  methods: {
      async loadCategories() {
          const self = this;
          const res = await fetch('http://localhost:8080/categories/');
          const json = await res.json();
          self.categories = json;
      }
  },
  mounted() {
      const self = this;
      self.loadCategories();
  }
}
</script>

<style scoped>
td {
    padding-left: 4px;
}
</style>