<template>
  <div
    class="invisible border text-[13px] font-medium w-full flex flex-row gap-x-2 md:visible"
  >
    <div class="w-1/6">ID#</div>
    <div class="w-full">NAMA</div>
    <div class="w-1/6 text-right">ISI</div>
    <div class="w-2/6 text-right">HARGA BELI</div>
    <div class="w-2/6 text-right">MARGIN</div>
    <div class="w-2/6 text-right">HARGA JUAL</div>
    <div class="w-2/6">DEFAULT</div>
    <div class="w-2/6">COMMAND</div>
  </div>
  <template v-for="unit in units" :key="unit.id">
    <unit-form :unit="unit" />
  </template>
</template>

<script>
import axios from "axios";
import UnitForm from "./UnitForm.vue";

const initUnit = {
  id: 0,
  product_id: 0,
  name: "",
  content: 0,
  buy_price: 0,
  margin: 0,
  price: 0,
  is_default: false,
};

export default {
  name: "UnitList",

  props: {
    productId: {
      type: Number,
      default: 0,
    },
    productPrice: {
      type: Number,
      default: 0,
    },
  },
  components: {
    "unit-form": UnitForm,
  },
  methods: {
    async loadUnits() {
      const self = this;

      await axios
        .get(`/api/units/product/${self.$props.productId}`, {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          if (res.status === 200) {
            self.units = [...res.data, { ...initUnit }, { ...initUnit, id: 1 }];
          }
        })
        .catch((error) => {
          self.units = [{ ...initUnit }];
        });
    },
  },
  async mounted() {
    await this.loadUnits();
  },
  data() {
    return {
      units: [],
    };
  },
};
</script>

<style scoped>
table {
  @apply w-full;
}
.v-select.style-chooser {
  @apply rounded-[4px] py-0 px-0 flex-initial w-full text-[14px];
}
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
  border-indigo-400 placeholder:italic
  focus:border-solid focus:outline-indigo-500 focus:ring-2 focus:ring-indigo-500;
  /*  hover:outline-none hover:border-indigo-500 hover:ring-1 hover:ring-indigo-500;*/
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
