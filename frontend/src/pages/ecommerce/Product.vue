<template>
  <div>
    <h1>Product</h1>
    <div class="message">
      Dalam bisnis, produk adalah barang atau jasa yang dapat diperjualbelikan. Dalam
      marketing, produk adalah apapun yang bisa ditawarkan ke sebuah pasar dan bisa
      memuaskan sebuah keinginan atau kebutuhan. Dalam tingkat pengecer, produk sering
      disebut sebagai merchandise. Dalam manufaktur, produk dibeli dalam bentuk barang
      mentah dan dijual sebagai barang jadi. Produk yang berupa barang mentah seperti
      metal atau hasil pertanian sering pula disebut sebagai komoditas.
    </div>
    <div class="mt-4">
      <hr />
      <div v-for="(prod, index) in products" v-bind:key="prod.id">
        <transition name="slide-fade">
          <template v-if="selectedIndex === index && selectedId === prod.id">
            <div class="product-list">
              <product-form
                :productProp="prod"
                :categoriesProp="categories"
                @update="updateData"
              >
                <template v-slot:default>
                  <button
                    type="button"
                    class="btn-cancel rounded-md"
                    @click="cancelForm()"
                  >
                    Cancel
                  </button>
                  <span class="flex-1"></span>
                  <button
                    @click="deleteForm()"
                    type="button"
                    class="btn-remove"
                    :disabled="prod.id === 0"
                  >
                    Delete
                  </button>
                </template>
              </product-form>
            </div>
          </template>
          <template v-else>
            <div class="product-list">
              <a
                href="#"
                v-if="prod.id === 0"
                @click.prevent.stop="itemClick(index, prod.id)"
                class="span-link"
              >
                +
              </a>
              <div v-else class="product-item">
                <div class="flex-none w-full md:w-2/5">
                  <a
                    href="#"
                    @click.prevent.stop="itemClick(index, prod.id)"
                    class="span-link"
                  >
                    {{ prod.name }}
                  </a>
                  <div class="text-sm">
                    <div>Spek: {{ prod.spec }}</div>
                  </div>
                  <div>
                    <label>
                      <input
                        type="checkbox"
                        :checked="units.includes(prod.id)"
                        @change="unitChecked($event.target.checked, prod.id)"
                      /><span class="ml-2 text-sm">Tampilkan untis</span></label
                    >
                  </div>
                </div>
                <div class="flex-1 w-full text-sm mt-0">
                  <div>Kategori: {{ categoryName(prod.category_id) }}</div>
                  <div>Berat: {{ formatNumber(prod.base_weight) }} kg</div>
                  <div>{{ prod.is_active ? "Masih Aktif" : "Tidak Aktif" }}</div>
                </div>
                <div class="flex-1 w-full text-sm mt-0">
                  <div>Harga: {{ formatNumber(prod.base_price) }}</div>
                  <div>Unit: {{ prod.base_unit }}</div>
                  <div>
                    {{ prod.is_sale ? "Produk untuk dijual" : "Tidak untuk dijual" }}
                  </div>
                </div>
              </div>
              <template v-if="units.includes(prod.id)">
                <unit-list :productId="prod.id" :key="prod.id"></unit-list>
              </template>
            </div>
          </template>
        </transition>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";
import ProductForm from "@/components/forms/ProductForm.vue";
import UnitList from "@/components/forms/UnitList.vue";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};

const new_product = {
  id: 0,
  name: "",
  spec: "",
  base_unit: "",
  base_weight: 0,
  base_price: 0,
  first_stock: 0,
  stock: 0,
  is_active: true,
  category_id: 0,
};

export default {
  name: "Product",
  components: {
    "tw-button": shallowRef(TwButton),
    "product-form": ProductForm,
    "unit-list": UnitList,
  },
  methods: {
    unitChecked(checked, id) {
      let i = this.units.indexOf(id);
      if (checked) {
        if (i < 0) {
          this.units.push(id);
        }
      } else {
        if (i >= 0) {
          this.units.splice(i, 1);
        }
      }
      console.log(this.units);
    },
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
        .delete(`/api/products/${self.selectedId}`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            const index = self.products.indexOfObject("id", self.selectedId);
            self.products.splice(index, 1);
            self.cancelForm();
          }
        });
    },
    itemClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    updateData(product, id) {
      const self = this;
      let temp = self.products;
      const index = self.products.indexOfObject("id", id);
      temp[index] = product;
      self.products = temp;
      if (id === 0) {
        self.products.push(new_product);
      }
      self.cancelForm();
    },
    async loadCategories() {
      const self = this;
      const options = {
        //      accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios
        .get("/api/categories/", { headers: options })
        .then((res) => {
          const json = res.data;
          self.loadedCategories = json; //[{id: 0, name: 'Pilih kategori'}, ...json];
        })
        .catch((error) => {
          self.loadedCategories = [];
        });
    },
    async loadProducts() {
      const self = this;
      const options = {
        //      accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios.get("/api/products/", { headers: options }).then((res) => {
        const json = res.data;
        self.products = [...json, new_product];
      });
    },
  },
  async mounted() {
    await this.loadCategories();
    await this.loadProducts();
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
  computed: {
    categories() {
      return this.loadedCategories;
    },
    formatNumber() {
      return (value) => Intl.NumberFormat("id-ID").format(value);
    },
    categoryName() {
      return (catId) => {
        const cat = this.loadedCategories.filter((c) => c.id === catId)[0];
        if (cat) {
          return cat.name;
        }
        return "";
      };
    },
  },
  data() {
    return {
      loadedCategories: [],
      products: [],
      units: [],
      selectedIndex: -1,
      selectedId: -1,
    };
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
  @apply inline-block cursor-pointer font-bold text-indigo-400 hover:underline hover:text-indigo-700 hover:underline-offset-4;
}
h1 {
  font-weight: 700;
  font-size: 24px;
}

.product-list {
  @apply py-4;
}
.product-item {
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
