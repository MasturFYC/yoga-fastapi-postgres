<template>
  <div>
    <form @submit="formSubmit">
      <div class="flex flex-col md:flex-row gap-x-4">
        <label class="flex-label">
          <span class="flex-span">Nama Produk:</span>
          <input
            v-focus
            maxlength="50"
            type="text"
            class="flex-input"
            :class="{ 'input-disable': nameValid }"
            v-model.lazy="productName"
            placeholder="e.g. Gula Pasir"
          />
        </label>
        <label class="flex-label">
          <span class="flex-span">Spek:</span>
          <input
            type="text"
            maxlength="50"
            class="flex-input"
            v-model.lazy="productSpec"
            placeholder="e.g. 1 zax @ 25kg"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label class="flex-label">
          <span class="flex-span">Unit (terkecil):</span>
          <input
            maxlength="6"
            type="text"
            class="flex-input"
            :class="{ 'input-disable': baseUnitValid }"
            v-model.lazy="baseUnit"
            placeholder="e.g. kg"
          />
        </label>
        <label class="flex-label">
          <span class="flex-span">Berat (terkecil):</span>
          <number
            class="flex-input"
            v-bind="inputNumeral"
            :class="{ 'input-disable': baseWeightValid }"
            v-model.lazy="baseWeight"
            placeholder="e.g. 2.5"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label class="flex-label">
          <span class="flex-span">Harga Beli (terkecil):</span>
          <number
            class="flex-input"
            v-bind="inputNumeral"
            :class="{ 'input-disable': basePriceValid }"
            v-model.lazy="basePrice"
            placeholder="e.g. 12,500"
          />
        </label>
        <label class="flex-label">
          <span class="flex-span">Stock awal:</span>
          <number
            readonly
            class="flex-input-readonly"
            v-bind="inputNumeral"
            placeholder="0"
            v-model.lazy="firstStock"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label class="flex-label">
          <span class="flex-span">Sisa Stock:</span>
          <number
            placeholder="0"
            readonly
            class="flex-input-readonly"
            v-bind="inputNumeral"
            v-model.lazy="productStock"
          />
        </label>
        <label class="flex-label">
          <span class="flex-span">Kategori:</span>
          <v-select
            id="myselect"
            ref="myselect"
            :options="categories"
            label="name"
            v-model.lazy="productCategoryId"
            class="style-chooser"
            :class="{ 'input-disable': categoryValid }"
            :reduce="(cat) => cat.id"
          >
            <template v-slot:list-header>
              <li style="text-align: center">Pilih kategori</li>
            </template>
            <template v-slot:selected-option="{ name }">
              <div style="color: #555; display: flex; align-items: baseline; margin: 0px">
                <span class="font-medium font-[13px]">{{ name }}</span>
                <!-- em style="margin-left: 0.5rem">by {{ name }}</!-->
              </div>
            </template>
            <template v-slot:selection="{ item }">
              <span class="font-bold">{{ item }}</span>
            </template>
            <template v-slot:option="{ name }">
              <span>{{ name }}</span>
            </template>
            <template v-slot:no-options="{ search, searching }">
              <template v-if="searching">
                Kategori tidak ditemukan
                <em>{{ search }}</em
                >.
              </template>
              <em v-else style="opacity: 0.5">Ketikkan untuk mulai mencari kategori.</em>
            </template>
          </v-select>
        </label>
      </div>
      <div class="my-4">
        <label class="py-2 flex-1 w-full mr-4">
          <input type="checkbox" v-model.lazy="product.isActive" />
          <span class="flex-span ml-2">Aktif ?</span>
        </label>
        <label class="py-2 flex-1 w-full">
          <input type="checkbox" v-model.lazy="product.isSale" />
          <span class="flex-span ml-2">Produk untuk dijual</span>
        </label>
      </div>
      <div class="flex flex-row gap-2 mt-5">
        <button type="submit" class="btn-primary" :disabled="enableSubmit">Save</button>
        <slot></slot>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProductForm",

  props: {
    update: {
      type: Function,
    },
    categoriesProp: {
      type: Array,
      default: [{ id: 0, name: "Pilih kategori" }],
    },
    productProp: {
      type: Object,
      default: {
        id: 0,
        name: "",
        spec: "",
        baseUnit: "",
        baseWeight: 0,
        basePrice: 0,
        firstStock: 0,
        stock: 0,
        isActive: true,
        isSale: false,
        categoryId: 0,
      },
    },
  },
  methods: {
    dropdownShouldOpen(VueSelect) {
      if (this.productCategoryId !== 0) {
        return VueSelect.open;
      }

      return VueSelect.search.length !== 0 && VueSelect.open;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      if (self.productId > 0) {
        await self.updateProduct(self.product, self.productId);
      } else {
        await self.insertProduct(self.product);
      }
    },
    async insertProduct(product) {
      const self = this;
      const data = { ...product };
      delete data.id;

      await axios
        .post(`/api/products/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit("update", res.data, 0);
        });
    },
    async updateProduct(product, id) {
      const self = this;
      const data = { ...product };
      // delete data.id;
      await axios
        .put(`/api/products/${id}/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit("update", res.data, id);
        });
    },
  },
  computed: {
    productId() {
      return this.product.id;
    },
    productName: {
      get() {
        return this.product.name;
      },
      set(value) {
        if (value !== this.product.name) {
          this.product.name = value;
        }
      },
    },
    productSpec: {
      get() {
        return this.product.spec;
      },
      set(value) {
        if (value !== this.product.spec) {
          this.product.spec = value;
        }
      },
    },
    baseWeight: {
      get() {
        return this.product.baseWeight;
      },
      set(value) {
        if (value !== this.product.baseWeight) {
          this.product.baseWeight = value;
        }
      },
    },
    basePrice: {
      get() {
        return this.product.basePrice;
      },
      set(value) {
        if (value !== this.product.basePrice) {
          this.product.basePrice = value;
        }
      },
    },
    baseUnit: {
      get() {
        return this.product.baseUnit;
      },
      set(value) {
        if (value !== this.product.baseUnit) {
          this.product.baseUnit = value;
        }
      },
    },
    firstStock: {
      get() {
        return this.product.firstStock;
      },
      set(value) {
        if (value !== this.product.firstStock) {
          this.product.firstStock = value;
        }
      },
    },
    productStock: {
      get() {
        return this.product.stock;
      },
      set(value) {
        if (value !== this.product.stock) {
          this.product.stock = value;
        }
      },
    },
    productCategoryId: {
      get() {
        return this.product.categoryId;
      },
      set(value) {
        if (value !== this.product.categoryId) {
          this.product.categoryId = value === null ? 0 : value;
        }
      },
    },
    enableSubmit() {
      return (
        this.nameValid ||
        this.baseUnitValid ||
        this.baseWeightValid ||
        this.basePriceValid ||
        this.categoryValid
      );
    },
    nameValid() {
      return this.product.name.trim().length === 0;
    },
    baseUnitValid() {
      return this.product.baseUnit.trim().length === 0;
    },
    baseWeightValid() {
      return this.product.baseWeight < 0;
    },
    basePriceValid() {
      return this.product.basePrice <= 0;
    },
    categoryValid() {
      return this.product.categoryId === 0 || this.product.categoryId === null;
    },
    categories: {
      get() {
        return this.$props.categoriesProp;
      },
    },
    inputNumeral: {
      get() {
        return {
          decimal: ",",
          separator: ".",
          suffix: "",
          precision: 2,
          masked: false,
        };
      },
    },
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
  async mounted() {
    const self = this;
    self.categoryId = self.productCategoryId;
  },
  data() {
    return {
      product: { ...this.$props.productProp },
      categoryId: 0, //this.$props.productProp.categoryId, //{id: 0, name: 'Pilih kategori', products: []},
      searchInput: "",
    };
  },
};
</script>

<style scoped>
.style-chooser .vs__dropdown-toggle,
.vs--searchable .vs__dropdown-toggle,
.style-chooser {
  @apply flex flex-1 w-full text-[13px] border-2 border-red-700;
}

div[role="combobox"] {
  @apply flex flex-1 w-full text-[13px] border-2 border-red-700;
}
/* 
.style-chooser,
.style-chooser .vs__search::placeholder,
.style-chooser .vs__dropdown-toggle,
.style-chooser .vs__dropdown-menu {
  background: #dfe5fb;
  border: none;
  color: #394066;
  text-transform: lowercase;
  font-variant: small-caps;
}

.vs--searchable,
.vs__dropdown-toggle,
.style-chooser .vs__dropdown-menu .vs--searchable,
.vs__dropdown-toggle,
.vs--searchable .vs__dropdown-toggle,
#vs2__combobox,
.style-chooser .vs__dropdown-toggle,
.vs__dropdown-toggle,
.style-chooser .vs__dropdown-menu {
  border: none; /* 3px solid #cfcfcf; 
}

.style-chooser .vs__clear,
.style-chooser .vs__open-indicator {
  fill: #394066;
} */

.flex-span {
  @apply flex-none w-[130px] text-[13px] font-medium text-gray-600 py-1 md:text-right md:mr-3;
}
.flex-label {
  @apply flex flex-initial w-full mt-2 md:flex-1 md:w-1/2;
}

.flex-input-readonly {
  @apply rounded-[4px] py-0.5 px-2 flex-initial w-full self-start text-gray-600
  border border-gray-400 text-[14px] placeholder:italic
  focus:outline-none focus:border-gray-500 focus:ring-0 focus:ring-gray-500;
}
.flex-select {
  @apply rounded-[4px] py-0 px-0 flex-initial w-full self-start text-[14px]
  border-emerald-400 placeholder:italic
  focus:border-solid focus:outline-emerald-500 focus:ring-2 focus:ring-emerald-500;
  /*  hover:outline-none hover:border-emerald-500 hover:ring-1 hover:ring-emerald-500;*/
}
.flex-input {
  @apply rounded-[4px] py-0.5 px-2 flex-initial w-full self-start text-gray-700
  border border-emerald-400 text-[14px] placeholder:italic
  focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500;
}

.input-disable {
  @apply border-red-400 focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500;
}
.btn-primary {
  @apply py-1 px-5 bg-blue-500 text-white font-semibold rounded-full shadow-md hover:bg-blue-700
  focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75
  disabled:text-gray-600 disabled:bg-gray-200;
}

::placeholder {
  font-size: small;
}
</style>
