<template>
  <div>
    <h1>Product Category</h1>
    <div class="message">
      Kategorisasi produk adalah penempatan dan pengorganisasian produk ke dalam
      kategori masing-masing untuk mempermudah dalam pengelompokkan produk.
      Dalam hal ini, kedengarannya sederhana: pilih departemen yang tepat untuk
      suatu produk. Namun, proses ini diperumit oleh banyaknya produk di banyak
      platform e-commerce.
    </div>
    <div class="message">
      Berikut di bawah ini adalah daftar nama kategori untuk mengelompokkan
      beberapa produk berdasarkan fungsi dan manfaatnya. Click nama kategori
      untuk mengeditnya, untuk membuat kategori baru klik tanda <b>+</b> paling
      bawah dari daftar nama kategori.
    </div>
    <ol start="1">
      <li v-for="(cat, index) in categories" v-bind:key="cat.id">
        <span v-if="selectedIndex === index && selectedId === cat.id">
          <form @submit="formSubmit">
            <input
              type="text"
              v-focus
              v-model.lazy="cat.name"
              placeholder="e.g. Bahan baku"
            /></form
        ></span>
        <span v-else class="span-link" @click="catClick(index, cat.id)">{{
          cat.id === 0 ? "+" : cat.name
        }}</span>
      </li>
    </ol>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Category",
  data() {
    return {
      categories: [],
      selectedIndex: -1,
      selectedId: 0,
    };
  },
  methods: {
    catClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      const cat = self.categories.filter((c) => c.id === self.selectedId)[0];
      if (cat) {

        const res = await fetch(
          `http://localhost:8080/categories/${self.selectedId}/`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: cat.name }),
          }
        );
        const json = await res.json();
        let temp = self.categories;
        const index = self.categories.findIndex(item => item.id === self.selectedId);
        temp[index] = json;
        self.categories = temp;
        this.selectedIndex = -1;
      }
    },
  },
  async mounted() {
    const self = this;
    const options = {
      accept: "application/json",
      "Content-Type": "application/json",
    };
    const res = await axios
      .get("http://localhost:8080/categories/", { headers: options })
      .then((res) => {
        const json = res.data;
        self.categories = [...json, { id: 0, name: "" }];
      });
  },
  //   async created() {
  //       const self = this;
  //       const res = await fetch("http://localhost:8080/categories/");
  //       const json = await res.json();
  //       self.categories = [...json, {id: 0, name: ''}];
  //   },
  directives: {
    focus: {
      mounted(el) {
        // When the bound element is inserted into the DOM...
        setTimeout(() => {
          el.focus(); // Focus the element
          // el.select();
        }, 100);
      },
    },
  },
};
</script>

<style scoped>
input[type="text"] {
  border: 1px solid #cecece;
  border-radius: 4px;
  padding-left: 6px;
  padding-right: 6px;
  width: 50%;
}
.span-link {
  cursor: pointer;
}
h1 {
  font-weight: 700;
  font-size: 24px;
}
ol {
  margin-top: 24px;
  margin-left: 24px;
}
li {
  margin-top: 6px;
}

.message {
  margin-top: 12px;
  font-size: small;
}
</style>