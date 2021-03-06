<template>
  <div>
    <h1 class="text-emerald-700">Product</h1>
    <div class="message">
      Dalam bisnis, produk adalah barang atau jasa yang dapat diperjualbelikan. Dalam
      marketing, produk adalah apapun yang bisa ditawarkan ke sebuah pasar dan bisa
      memuaskan sebuah keinginan atau kebutuhan. Dalam tingkat pengecer, produk sering
      disebut sebagai merchandise. Dalam manufaktur, produk dibeli dalam bentuk barang
      mentah dan dijual sebagai barang jadi. Produk yang berupa barang mentah seperti
      metal atau hasil pertanian sering pula disebut sebagai komoditas.
    </div>
    <div class="flex flex-row justify-center items-center mt-4 gap-x-4">
      <v-select
        class="flex-1 w-1/2 style-chooser"
        :options="[{ id: 0, name: 'All...' }, ...categories]"
        label="name"
        v-model="categoryId"
        :reduce="(cat) => cat.id"
      >
        <template v-slot:selected-option="{ name }">
          <div style="color: #555; display: flex; align-items: baseline; margin: 0px">
            <span class="font-medium font-[13px]">{{ name }}</span>
            <!-- em style="margin-left: 0.5rem">by {{ name }}</!-->
          </div>
        </template>
      </v-select>
      <input
        type="text"
        class="flex-1 w-1/2 border border-emerald-600 py-1 px-4 text-sm md:w-80 rounded-md placeholder:italic focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-600"
        placeholder="Search for product name"
        @keydown.enter.prevent.stop="searchProduct"
        maxlength="50"
        v-model="searchText"
      />
    </div>
    <div class="mt-4">
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
              <button
                href="#"
                v-if="prod.id === 0"
                @click.prevent.stop="itemClick(index, prod.id)"
                class="btn-add"
              >
                <tw-icon name="carbon:add-alt" class="flex-1 icon w-5 h-5" />
              </button>
              <div v-else class="product-item text-sm">
                <div class="flex-none w-full flex-col md:w-2/5">
                  <a
                    href="#"
                    @click.prevent.stop="itemClick(index, prod.id)"
                    class="span-link flex-1"
                    >{{ prod.name }}</a
                  >
                  <div class="w-full flex flex-row">
                    <div class="w-1/3 text-gray-400">Spek:</div>
                    <div class="flex-1">{{ prod.spec }}</div>
                  </div>
                  <div class="flex-1">
                    <label>
                      <input
                        type="checkbox"
                        :checked="units.includes(prod.id)"
                        @change="unitChecked($event.target.checked, prod.id)"
                      />
                      <span class="ml-2">Lihat units</span>
                    </label>
                  </div>
                </div>
                <div class="flex-1 flex flex-col mt-0">
                  <div class="flex-1 flex flex-row">
                    <div class="w-1/3 text-gray-400">Kategori:</div>
                    <div class="flex-1">{{ categoryName(prod.categoryId) }}</div>
                  </div>
                  <div class="flex-1 flex flex-row">
                    <div class="w-1/3 text-gray-400">Berat:</div>
                    <div class="flex-1">{{ formatNumber(prod.baseWeight) }} kg</div>
                  </div>
                  <div class="flex-1 flex flex-row">
                    <div class="w-1/3 text-gray-400">Aktif ?</div>
                    <div class="flex-1">{{ prod.isActive ? "Ya" : "Tidak" }}</div>
                  </div>
                </div>
                <div class="flex-1 flex flex-col mt-0">
                  <div class="flex-1 flex flex-row">
                    <div class="w-1/3 text-gray-400">Harga:</div>
                    <div class="flex-1">{{ formatNumber(prod.basePrice) }}</div>
                  </div>
                  <div class="flex-1 flex flex-row">
                    <div class="w-1/3 text-gray-400">Unit:</div>
                    <div class="flex-1">{{ prod.baseUnit }}</div>
                  </div>
                  <div class="flex-1">
                    {{ prod.isSale ? "Produk ini untuk dijual" : "Tidak untuk dijual" }}
                  </div>
                </div>
              </div>
              <template v-if="units.includes(prod.id)">
                <unit-list
                  :productId="prod.id"
                  :productPrice="prod.basePrice"
                  :key="prod.id"
                ></unit-list>
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

const newProduct = {
  id: 0,
  name: "",
  spec: "",
  baseUnit: "",
  baseWeight: 0,
  basePrice: 0,
  firstStock: 0,
  stock: 0,
  isActive: true,
  categoryId: 0,
};

export default {
  name: "Product",
  components: {
    "tw-button": shallowRef(TwButton),
    "product-form": shallowRef(ProductForm),
    "unit-list": shallowRef(UnitList),
  },
  methods: {
    validateSelection(e) {
      console.log("--1---", e);
    },
    async searchProduct(e) {
      const self = this;

      if (self.searchText.length > 2) {
        const options = {
          //      accept: "application/json",
          "Content-Type": "application/json",
        };
        await axios
          .get(`/api/products/search/${self.searchText}/`, { headers: options })
          .then((res) => {
            const json = res.data;
            self.products = [newProduct, ...json];
          }).catch(err => {
            console.log(err)
          });
      }
    },
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
      //console.log(this.units)
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
        .delete(`/api/products/${self.selectedId}/`, {
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
        self.products.push(newProduct);
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
        self.products = [newProduct, ...json];
      });
    },
    async loadProductsByCategory() {
      const self = this;
      const options = {
        //      accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios
        .get(`/api/products/category/${this.categoryId}/`, {
          headers: options,
        })
        .then((res) => {
          const json = res.data;
          self.products = [newProduct, ...json];
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
    productList() {
      return this.products.map((o) => ({ id: o.id, name: o.name }));
    },
    categories() {
      return this.loadedCategories;
    },
    formatNumber() {
      return (value) => Intl.NumberFormat("id-ID").format(value);
    },
    categoryId: {
      get: function () {
        return this.catId;
      },
      set: function (value) {
        if (this.catId !== value) {
          this.catId = value === null ? 0 : value;
          this.loadProductsByCategory();
        }
      },
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
      searchText: "",
      catId: 0,
    };
  },
};
</script>

<style scoped>
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

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
}

.svg-icon {
  enable-background: new 0 0 64 64;
  display: inline;
  fill: #ff0000;
  /* margin-left: 12px; */
}
.span-link {
  @apply inline-block cursor-pointer font-bold text-emerald-700 hover:underline hover:text-emerald-900 hover:underline-offset-4;
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
.v-select.style-chooser {
  @apply rounded-md text-sm py-0 px-0;
}
.btn-add {
  @apply py-1 px-5 bg-emerald-600 text-white font-semibold rounded-full shadow-md hover:bg-emerald-700
  focus:bg-emerald-900 focus:outline-none 
  disabled:text-gray-600 disabled:bg-gray-200;
}
</style>
