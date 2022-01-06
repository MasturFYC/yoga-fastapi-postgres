<template>
  <div>Nama:</div>
  <div>
    <input type="text" v-model="name" placeholder="e.g. PT. Mandiri Perkasa" />
  </div>
  <div>Sales:</div>
  <div>
    <input type="text" v-model="sales_name" placeholder="e.g. Mr. Junaedi" />
  </div>
  <label for="city" class="flex">
    <span class="flex-none w-20">Alamat:</span>
    <textarea
      class="flex-initial w-64"
      id="city"
      v-model="city"
      placeholder="e.g. Indramayu"
    />
  </label>

  <label for="city" class="flex">
    <span class="flex-none w-20">Kota:</span>
    <input
      class="flex-initial w-64"
      type="text"
      v-model="street"
      placeholder="e.g. Jl. Jenderal Sudirman No. 155 Kel. Lemahmekar"
    />
  </label>
  <label for="phone" class="flex">
    <span class="flex-none w-20">Telp.:</span>
    <input
      class="flex-initial w-64"
      type="text"
      id="phone"
      v-model="phone"
      placeholder="e.g. 02342775"
    />
  </label>
  <label for="cellular" class="flex">
    <span class="flex-none w-20">Cellular:</span>
    <input
      class="flex-initial w-64"
      type="text"
      id="cellular"
      v-model="cell"
      placeholder="e.g. 0856 6598 236ee96s"
    />
  </label>
  <label for="zip" class="flex">
    <span class="flex-none w-20">Kode pos:</span>
    <input
      class="flex-initial w-64"
      type="text"
      id="zip"
      v-model="zip"
      placeholder="e.g. 45212"
    />
  </label>
  <div>
    <label for="email" class="flex">
      <span class="flex-none w-20">e-mail:</span>
      <input
        class="flex-initial w-64"
        type="text"
        id="email"
        v-model="email"
        placeholder="e.g. somepne@gmail.com"
      />
    </label>
  </div>
</template>

<script>
export default {
  name: "SupplierForm",

  props: {
    name: {
      type: String,
      default: "",
    },
    sales_name: {
      type: String,
      default: "------",
    },
    street: {
      type: String,
      default: "",
    },
    city: {
      type: String,
      default: "",
    },
    phone: {
      type: String,
      default: "",
    },
    cell: {
      type: String,
      default: "",
    },
    zip: {
      type: String,
      default: "",
    },
    email: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    return {};
  },
};
</script>
<style scoped>
input[type="text"] {
  border: 1px solid #cecece;
  padding: 0 6px;
}
textarea {
  border: 1px solid #cecece;
  padding: 0 6px;
}
label {
  margin-top: 6px;
}
</style>