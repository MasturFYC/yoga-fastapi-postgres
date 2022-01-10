<template>
  <form>
    <div class="flex flex-col w-full text-sm gap-2 md:flex-row">
      <div class="w-1/6">{{ unit.id }}</div>
      <label class="flex flex-row gap-0"
        ><span class="label-unit">Unit</span
        ><input class="my-input" type="text" v-model="unit.name" maxlength="6"
      /></label>
      <label class="flex w-full flex-row"
        ><span class="label-unit flex-1 border">Isi</span
        ><input
          class="my-input flex-1 w-1/6 text-right"
          type="text"
          v-model="unit.content"
      /></label>
      <label class="inline w-full"
        ><span class="label-unit">Harga Beli</span
        ><input class="my-input w-2/6 text-right" type="text" v-model="unit.buy_price"
      /></label>
      <label class="inline w-full"
        ><span class="label-unit">Margin</span
        ><input class="my-input w-2/6 text-right" type="text" v-model="unit.margin"
      /></label>
      <label class="inline w-full"
        ><span class="label-unit">Harga Jual</span
        ><input class="my-input w-2/6 text-right" type="text" v-model="unit.price"
      /></label>
      <label class="w-2/6 inline w-full">
        <input type="checkbox" v-model="unit.is_default" />
        <span class="ml-2">?</span>
      </label>
      <div class="w-2/6"></div>
    </div>
  </form>
</template>

<script>
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
  name: "UnitForm",

  props: {
    unit: {
      type: Object,
      default: initUnit,
    },
  },
  methods: {
    data() {
      return {
        unit: { ...this.$props.unit },
      };
    },
  },
};
</script>

<style scoped>
.my-input {
  @apply border-none outline-none inline;
}
.label-unit {
  @apply flex-initial w-1/4 md:hidden;
}
</style>
