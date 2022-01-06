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
            />
            <tw-button type="default" size="sm" round :components="components">
              <svg
                version="1.1"
                id="Layer_1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                x="0px"
                y="0px"
                width="16"
                viewBox="0 0 64 64"
                class="svg-icon"
                xml:space="preserve"
              >
                <path
                  d="M59.68,55.978c2.29,2.27-1.25,5.81-3.54,3.53c-2.11-2.1-4.23-4.2-6.35-6.31c-5.93-5.89-11.86-11.78-17.79-17.68
	c-2.2,2.19-4.4,4.37-6.6,6.56c-5.84,5.81-11.69,11.62-17.54,17.43c-2.29,2.28-5.82-1.26-3.54-3.53c2.12-2.1,4.23-4.21,6.35-6.31
	c5.93-5.89,11.85-11.78,17.78-17.67c-2.19-2.18-4.39-4.36-6.58-6.54c-5.85-5.81-11.7-11.63-17.55-17.44
	c-2.29-2.27,1.25-5.8,3.54-3.53c2.11,2.1,4.23,4.2,6.35,6.31c5.93,5.89,11.86,11.79,17.79,17.68c2.2-2.19,4.4-4.37,6.6-6.56
	c5.85-5.81,11.7-11.62,17.54-17.43c2.29-2.27,5.83,1.26,3.54,3.53c-2.12,2.11-4.23,4.21-6.35,6.31
	c-5.93,5.89-11.85,11.78-17.78,17.67c2.19,2.18,4.39,4.36,6.58,6.54C47.98,44.358,53.83,50.168,59.68,55.978z"
                /></svg
            ></tw-button></form
        ></span>
        <span v-else class="span-link" @click="catClick(index, cat.id)">{{
          cat.id === 0 ? "+" : cat.name
        }}</span>
      </li>
    </ol>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";

export default {
  name: "Category",
  data() {
    return {
      categories: [],
      selectedIndex: -1,
      selectedId: 0,
      components: {
        "tw-button": TwButton,
      },
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
      if (cat && cat.id > 0) {
        await this.updatCatgory(cat.name, cat.id);
      } else {
        await this.insertCategory(cat.name, 0);
      }
    },
    async insertCategory(name, id) {
      const self = this;
      await axios
        .post(
          `http://localhost:8080/categories/`,
          JSON.stringify({ name: name }),
          {
            headers: {
              accept: "application/json",
              "Content-Type": "application/json",
            },
          }
        )
        .then((res) => {
          const json = res.data;
          let temp = self.categories;
          const index = self.categories.findIndex((item) => item.id === id);
          temp[index] = json;
          self.categories = temp;
          self.categories.push({ id: 0, name: "" });
          this.selectedIndex = -1;
        });
    },
    async updatCatgory(name, id) {
      const self = this;
      await axios
        .put(
          `http://localhost:8080/categories/${id}/`,
          JSON.stringify({ name: name }),
          {
            headers: {
              accept: "application/json",
              "Content-Type": "application/json",
            },
          }
        )
        .then((res) => {
          const json = res.data;
          let temp = self.categories;
          const index = self.categories.findIndex((item) => item.id === id);
          temp[index] = json;
          self.categories = temp;
          this.selectedIndex = -1;
        });
    },
  },
  async mounted() {
    const self = this;
    const options = {
      //      accept: "application/json",
      "Content-Type": "application/json",
    };
    await axios
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
.svg-icon {
  enable-background: new 0 0 64 64;
  display: inline;
  fill: #ff0000;
  /* margin-left: 12px; */
}
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