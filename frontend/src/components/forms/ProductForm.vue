<template>
  <div>
    <form @submit="formSubmit">
      <div class="flex flex-col md:flex-row gap-x-4">
        <label for="prod-name" class="flex-label">
          <span class="flex-span">Nama Produk:</span>
          <input
            v-focus
            maxlength="50"
            id="prod-name"
            type="text"
            class="flex-input"
            :class="{ 'input-disable': nameValid }"
            v-model="product.name"
            placeholder="e.g. Gula Pasir"
          />
        </label>
        <label for="prod-spec" class="flex-label">
          <span class="flex-span">Spek:</span>
          <input
            id="prod-spec"
            type="text"
            maxlength="50"
            class="flex-input"
            v-model="product.spec"
            placeholder="e.g. 1 zax @ 25kg"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label for="base-unit" class="flex-label">
          <span class="flex-span">Unit (terkecil):</span>
          <input
            id="base-unit"
            maxlength="6"
            type="text"
            class="flex-input"
            :class="{ 'input-disable': base_unitValid }"
            v-model="product.base_unit"
            placeholder="e.g. kg"
          />
        </label>
        <label for="base-weight" class="flex-label">
          <span class="flex-span">Berat (terkecil):</span>
          <v-number
            id="base-weight"
            class="flex-input"
            :options="inputNumeral"
            :class="{ 'input-disable': base_weightValid }"
            v-model="product.base_weight"
            placeholder="e.g. 2.5"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label for="base-price" class="flex-label">
          <span class="flex-span">Harga Beli (terkecil):</span>
          <v-number
            id="base-price"
            class="flex-input"
            :options="inputNumeral"
            :class="{ 'input-disable': base_priceValid }"
            v-model="product.base_price"
            placeholder="e.g. 12,500"
          />
        </label>
        <label for="first-stock" class="flex-label">
          <span class="flex-span">Stock awal:</span>
          <v-number
            id="first-stock"
            readonly
            class="flex-input-readonly"
            :options="inputNumeral"
            v-model="product.first_stock"
          />
        </label>
      </div>
      <div class="flex flex-col md:flex-row gap-x-4">
        <label for="stock" class="flex-label">
          <span class="flex-span">Sisa Stock:</span>
          <v-number
            id="stock"
            readonly
            class="flex-input-readonly"
            :options="inputNumeral"
            v-model="product.stock"
          />
        </label>
        <label for="category-id" class="flex-label">
          <span class="flex-span">Kategori:</span>
          <v-select
            id="category-id"
            label="category-id"
            v-model="categoryId"
            :options="categories"
            label-by="name"
            value-by="id"
            class="flex-select"
            :class="{ 'input-disable': categoryValid }"
            searchable
            close-on-select
            clear-on-close
            placeholder="Pilih kategori"
            @selected="setSelected"
          ></v-select>
        </label>
      </div>
      <div class="my-4">
      <label for="is-active" class="py-2 flex-1 w-full">
        <input
          id="is-active"
          type="checkbox"
          v-model="product.is_active"
        />
        <span class="flex-span ml-2">Aktif ?</span>
      </label>
      <label for="is-sale" class="py-2 flex-1 w-full">
        <input
          id="is-sale"
          type="checkbox"
          v-model="product.is_sale"
        />
        <span class="flex-span ml-2">Produk untuk dijual</span>
      </label>
      </div>
      <div class="flex flex-row gap-2 mt-5">
        <button type="submit" class="btn-primary" :disabled="enableSubmit">Save</button>
        <slot />
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
      type: Function
    },
    categoriesProp: {
      type: Array,
      default: [{ id: 0, name: 'Pilih kategori' }]
    },
    productProp: {
      type: Object,
      default: {
        id: 0, name: "", spec: "", base_unit: "", base_weight: 0,
        base_price: 0, first_stock: 0, stock: 0, is_active: true, category_id: 0
      },
    },
  },
  methods: {
    setSelected(o) {
      this.categoryId = o.id;
      this.product.category_id = o.id;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      if (self.product.id > 0) {
        await self.updateProduct(self.product, self.product.id);
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
          self.$emit('update', res.data, 0)
        });
    },
    async updateProduct(product, id) {
      const self = this;
      const data = { ...product };
      delete data.id;
      await axios
        .put(`/api/products/${id}/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit('update', res.data, id)
        });
    },
  },
  computed: {
    enableSubmit() { return this.nameValid || this.base_unitValid || this.base_weightValid || this.base_priceValid || this.categoryValid },
    nameValid() { return this.product.name.trim().length === 0 },
    base_unitValid() { return this.product.base_unit.trim().length === 0 },
    base_weightValid() { return this.product.base_weight < 0 },
    base_priceValid() { return this.product.base_price <= 0 },
    categoryValid() { return this.product.category_id === 0 },
    categories: {
      get() {
        return this.$props.categoriesProp;
      }
    },
    inputNumeral: {
      get() {
        return {
          numeralPositiveOnly: true,
          noImmediatePrefix: true,
          rawValueTrimPrefix: true,
          numeralIntegerScale: 9,
          numeralDecimalScale: 2,
          numeral: true,
        }
      }
    }
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
    self.categoryId = self.product.category_id;
  },
  data() {
    return {
      product: { ...this.$props.productProp },
      categoryId: 0, //this.$props.productProp.category_id, //{id: 0, name: 'Pilih kategori', products: []},
      searchInput: '',
    };
  },

};
</script>
<style scoped>
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
  @apply rounded-[4px] py-0 px-1 flex-initial w-full self-start text-black
  border border-indigo-400 text-[14px] placeholder:italic 
  hover:outline-none hover:border-indigo-500 hover:ring-1 hover:ring-indigo-500;
}
.flex-input {
  @apply rounded-[4px] py-0.5 px-2 flex-initial w-full self-start text-gray-700
  border border-indigo-400 text-[14px] placeholder:italic
  focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500;
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