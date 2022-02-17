<template>
  <div>
    <form @submit="formSubmit">
    <div class="flex flex-col md:flex-row gap-x-4">
      <label for="sup-name" class="flex-label">
        <span class="flex-span">Nama:</span>
        <input
          v-focus
          maxlength="50"
          id="sup-name"
          type="text"
          class="flex-input"
          :class="{'input-disable': nameValid}"
          v-model="supplier.name"
          placeholder="e.g. PT. Mandiri Perkasa"
        />
      </label>
      <label for="sales-name" class="flex-label">
        <span class="flex-span">Sales:</span>
        <input
          id="sales-name"
          type="text"
          maxlength="50"
          class="flex-input"
          :class="{'input-disable': salesValid}"
          v-model="supplier.sales_name"
          placeholder="e.g. Mr. Junaedi"
        />
      </label>
    </div>
    <div class="flex flex-col md:flex-row gap-x-4">
      <label for="street" class="flex-label">
        <span class="flex-span">Alamat:</span>
        <textarea
          id="street"
          maxlength="128"
          class="flex-input"
          :class="{'input-disable': streetValid}"
          v-model="supplier.street"
          placeholder="e.g. Jl. Jenderal Sudirman No. 155 Kel. Lemahmekar"
        />
      </label>
      <label for="city" class="flex-label">
        <span class="flex-span">Kota:</span>
        <input
          id="city"
          maxlength="50"
          class="flex-input self-start"
          :class="{'input-disable': cityValid}"
          type="text"
          v-model="supplier.city"
          placeholder="e.g. Indramayu"
        />
      </label>
    </div>
    <div class="flex flex-col md:flex-row gap-x-4">
      <label for="phone" class="flex-label">
        <span class="flex-span">Telp.:</span>
        <input
          id="phone"
          maxlength="25"
          class="flex-input"
          :class="{'input-disable': phoneValid}"
          type="text"
          v-model="supplier.phone"
          placeholder="e.g. 02342775"
        />
      </label>
      <label for="cellular" class="flex-label">
        <span class="flex-span">Cellular:</span>
        <input
          id="cellular"
          maxlength="25"
          class="flex-input"
          type="text"
          v-model="supplier.cell"
          placeholder="e.g. 0856 6598 2366"
        />
      </label>
    </div>
    <div class="flex flex-col md:flex-row gap-x-4">
      <label for="zip" class="flex-label">
        <span class="flex-span">Kode pos:</span>
        <input
          id="zip"
          maxlength="8"
          class="flex-input"
          type="text"
          v-model="supplier.zip"
          placeholder="e.g. 45212"
        />
      </label>
      <label for="email" class="flex-label">
        <span class="flex-span">e-mail:</span>
        <input
          id="email"
          maxlength="128"
          class="flex-input"
          type="text"
          v-model="supplier.email"
          placeholder="e.g. somepne@gmail.com"
        />
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
  name: "SupplierForm",

  props: {
    update: {
      type: Function
    },
    supplierProp: {
      type: Object,
      default: {
        id: 0,
        name: "",
        sales_name: "",
        street: "",
        city: "",
        phone: "",
        cell: "",
        zip: "",
      },
    },
  },
  data() {
    return {
      supplier: { ...this.$props.supplierProp }
    };
  },
  methods: {
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      if (self.supplier.id > 0) {
        await self.updateSupplier(self.supplier, self.supplier.id);
      } else {
        await self.insertSupplier(self.supplier);
      }
    },
    async insertSupplier(supplier) {
      const self = this;
      const data = { ...supplier };
      delete data.id;

      await axios
        .post(`/api/suppliers`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit('update', res.data, 0)
        });
    },
    async updateSupplier(supplier, id) {
      const self = this;
      const data = { ...supplier };
      delete data.id;
      await axios
        .put(`/api/suppliers/${id}`, JSON.stringify(data), {
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
    enableSubmit () { return this.nameValid || this.salesValid || this.streetValid || this.cityValid || this.phoneValid },
    nameValid() { return this.supplier.name.trim().length === 0},
    salesValid() {return this.supplier.sales_name.trim().length === 0},
    streetValid () {return this.supplier.street.trim().length === 0},
    cityValid () {return this.supplier.city.trim().length === 0},
    phoneValid () {return this.supplier.phone.trim().length === 0}
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
.flex-span {
  @apply flex-none w-20 text-[13px] font-medium text-gray-600 py-1 md:text-right md:mr-3;
}
.flex-label {
  @apply flex flex-initial w-full mt-2 md:flex-1 md:w-1/2;
}
.flex-input {
  @apply rounded-[4px] py-1 px-2 flex-initial w-full self-start border 
  border-emerald-400 text-[14px] placeholder:italic
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