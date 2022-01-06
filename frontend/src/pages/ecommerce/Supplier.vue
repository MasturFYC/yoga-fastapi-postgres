<template>
  <div>
    <h1>Supplier</h1>
    <div class="message">
      Suplier adalah orang atau perusahaan yang menjual bahan yang akan diolah
      perusahaan lain menjadi produk siap jual. Umumnya suplier menjual produk
      dalam bentuk mentah atau bahan baku. Rumah produksi atau pabriklah yang
      kemudian menggunakan bahan mentah tadi untuk digunakan sebagai bagian dari
      proses penciptaan produk tertentu. Misalnya, supplier kelapa yang
      menyetorkan beberapa ton kelapa setiap bulan untuk mencukupi kebutuhan
      pembuatan minyak goreng kelapa yang dihasilkan si pabrik.
    </div>
    <div>
      <ol start="1">
        <li v-for="(sup, index) in suppliers" v-bind:key="sup.id">
          <div v-if="selectedIndex === index && selectedId === sup.id">
              <SupplierForm />
          </div>
          <div v-else class="span-link" @click="supClick(index, sup.id)">
            <div v-if="sup.id === 0">+</div>
            <div v-else>
              Nama: {{ sup.id === 0 ? "+" : sup.name }} Sales:
              {{ sup.sales_name }}
            </div>
          </div>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";
import SupplierForm from "@/components/SupplierForm.vue"

const new_supplier = {
  id: 0,
  name: "",
  sales_name: "",
  street: "",
  city: "",
  phone: "",
  cell: "",
  zip: "",
  email: "",
};

export default {
  name: "Supplier",
  data() {
    return {
      suppliers: [],
      selectedIndex: -1,
      selectedId: -1,
    }
  },
  components: {
    'tw-button': shallowRef(TwButton),
    SupplierForm,
  },
  methods: {
    supClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      const sup = self.suppliers.filter((c) => c.id === self.selectedId)[0];
      if (sup && sup.id > 0) {
        await this.updatCatgory(sup.name, sup.id);
      } else {
        await this.insertCategory(sup.name, 0);
      }
    },
    async insertCategory(name, id) {
      const self = this;
      await axios
        .post(
          `http://localhost:8080/suppliers/`,
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
          let temp = self.suppliers;
          const index = self.suppliers.findIndex((item) => item.id === id);
          temp[index] = json;
          self.suppliers = temp;
          self.suppliers.push(new_supplier);
          this.selectedIndex = -1;
        });
    },
    async updatCatgory(name, id) {
      const self = this;
      await axios
        .put(
          `http://localhost:8080/suppliers/${id}/`,
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
          let temp = self.suppliers;
          const index = self.suppliers.findIndex((item) => item.id === id);
          temp[index] = json;
          self.suppliers = temp;
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
      .get("http://localhost:8080/suppliers/", { headers: options })
      .then((res) => {
        console.log("-----------", res);
        const json = res.data;

        self.suppliers = [...json, new_supplier];
      });
  },
  //   async created() {
  //       const self = this;
  //       const res = await fetch("http://localhost:8080/suppliers/");
  //       const json = await res.json();
  //       self.suppliers = [...json, {id: 0, name: ''}];
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