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
    <div class="mt-4">
    <hr />
      <div v-for="(sup, index) in suppliers" v-bind:key="sup.id">
        <transition name="slide-fade">
          <div
            v-if="selectedIndex === index && selectedId === sup.id"
            class="supplier-list"
          >
            <supplier-form :supplierProp="sup" @update="updateData">
              <button
                type="button"
                class="btn-cancel rounded-md"
                @click="cancelForm()"
              >
                Cancel
              </button>
              <span class="flex-1"></span>
              <button @click="deleteForm()" type="button" class="btn-remove" :disabled="sup.id === 0">
                Delete
              </button>
            </supplier-form>
          </div>
          <div v-else class="supplier-list">
            <div
              v-if="sup.id === 0"
              @click="supClick(index, sup.id)"
              class="span-link"
            >
              +
            </div>
            <div v-else class="supplier-item">
              <div class="flex-none w-full md:w-2/5">
                <div @click="supClick(index, sup.id)" class="span-link">
                  {{ sup.name }}
                </div>
                <div>Sales: {{ sup.sales_name }}</div>
              </div>
              <div class="flex-1 w-full text-sm mt-2 md:mt-0">
                <div>{{ sup.street }} - {{ sup.city }}, {{ sup.zip }}</div>
                <div>Telp. {{ sup.phone }} / {{ sup.cell }}</div>
                <div>{{ sup.email }}</div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";
import SupplierForm from "@/components/forms/SupplierForm.vue";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
}

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
      suppliers: [{...new_supplier}],
      selectedIndex: -1,
      selectedId: -1,
    };
  },
  components: {
    "tw-button": shallowRef(TwButton),
    "supplier-form": SupplierForm,
  },
  methods: {
    cancelForm() {
      const self = this;
      self.selectedId = -1;
      self.selectedIndex = -1;
    },
    async deleteForm() {
      const self = this;
      const options = {
        "Content-Type": "application/json",
      };
      await axios
        .delete(`/api/suppliers/${self.selectedId}/`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            const index = self.suppliers.indexOfObject("id", self.selectedId);
            self.suppliers.splice(index, 1);
            self.cancelForm();
          }
        });
    },
    supClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    updateData(supplier, id) {
      const self = this;
      let temp = self.suppliers;
      const index = self.suppliers.indexOfObject("id", id);
      temp[index] = supplier;
      self.suppliers = temp;
      if (id === 0) {
        self.suppliers.push(new_supplier);
      }
      self.cancelForm();
    },
  },
  async mounted() {
    const self = this;
    const options = {
      //      accept: "application/json",
      "Content-Type": "application/json",
    };
    await axios
      .get("/api/suppliers/", { headers: options })
      .then((res) => {
        const json = res.data;
        self.suppliers = [...json, new_supplier];
      });
  },
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
.span-link {
  @apply inline-block cursor-pointer font-bold text-emerald-400 hover:underline hover:text-emerald-700 hover:underline-offset-4;
}
h1 {
  font-weight: 700;
  font-size: 24px;
}

.supplier-list {
  @apply py-4 border-b border-emerald-200;
}
.supplier-item {
  @apply flex flex-col mt-1
  md:flex-row;
}

.message {
  margin-top: 12px;
  font-size: small;
}
.btn-cancel {
  @apply py-1 px-5 bg-orange-500 text-white font-semibold rounded-full shadow-md hover:bg-orange-700
  focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75;
}
.btn-remove {
  @apply py-1 px-5 bg-red-700 text-white font-semibold rounded-full shadow-md hover:bg-red-800
  disabled:invisible
  focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-opacity-75;
}
.slide-fade-enter-active {
  transition: all 0.1s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(50px);
  opacity: 0;
}
</style>