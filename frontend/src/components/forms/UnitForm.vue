<template>
  <form
    class="
      text-[13px]
      w-full
      flex
      flex-col
      gap-x-0
      md:flex-row
      py-2
      md:py-0
    "
  >
    <div class="flex w-full md:w-[120px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-t-0">
      <span class="label-title">ID#:</span>
      <span class="my-input">{{ unit.id }}</span>
    </div>
    <label class="flex w-full md:w-[500px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0"
      ><span class="label-title">Unit</span
      ><input
        class="my-input"
        v-focus
        type="text"
        v-model.lazy="unit.name"
        maxlength="6"
    /></label>
    <label class="flex w-full md:w-[120px]  py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0"
      ><span class="label-title">Isi</span
      ><number
        class="my-input text-left md:text-right"
        v-model.lazy="unit.content"
        v-bind="inputNumber"
        @change="contentChanged($event)"
        placeholder="0"
    /></label>
    <label class="flex w-full md:w-[250px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0"
      ><span class="label-title">Harga Beli</span
      ><number
        class="my-input text-left md:text-right"
        v-model="buyPrice"
        v-bind="inputNumber"
        placeholder="0"
        readonly
    /></label>
    <label class="flex w-full md:w-[155px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0"
      ><span class="label-title">Margin</span
      ><number
        class="my-input text-left md:text-right"
        v-model.lazy="unit.margin"
        v-bind="inputPercent"
        @change="marginChanged($event)"
        placeholder="0"
    /></label>
    <label class="flex w-full md:w-[250px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0"
      ><span class="label-title">Harga Jual</span
      ><number
        class="my-input text-left md:text-right"
        v-model.lazy="unit.price"
        v-bind="inputNumber"
        @change="priceChanged($event)"
        placeholder="0"
    /></label>
    <label class="flex w-full md:w-[250px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0">
      <input type="checkbox" v-model.lazy="unit.is_default" class="self-center" />
      <span class="px-1 label-title self-center">Default ?</span>
    </label>
    <div class="w-[250px] py-1 px-0 md:px-1 border-0  md:border md:border-indigo-400 md:border-l-0 md:border-t-0">-</div>
  </form>
</template>

<script>

export default {
  name: "UnitForm",
  props: {
    basePrice: {
      type: Number,
      default: 0
    },
    unitProp: {
      type: Object,
    },
  },
  methods: {
    contentChanged(e) {
      const content = this.unit.content;
      this.unit.price = this.buyPrice + (this.buyPrice * this.margin)
    },
    marginChanged(e) {
     // const margin = this.unit.margin;
      this.unit.price = this.buyPrice + (this.buyPrice * this.margin)
    },
    priceChanged(e) {
      this.unit.margin = ((this.unit.price - this.buyPrice) / this.buyPrice) * 100.0;
    },
  },
  data() {
    return {
      unit: { ...this.$props.unitProp },
    };
  },
  computed: {
    inputNumber: {
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
    inputPercent: {
      get() {
        return {
          decimal: ",",
          separator: ".",
          suffix: " %",
          precision: 2,
          masked: false,
        };
      },
    },
    buyPrice() { return this.unit.content * this.$props.basePrice; },
    margin() { return this.unit.margin / 100.0; }
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
.my-input {
  @apply w-full outline-none border-0 md:border-0;
}
.label-title {
  @apply w-[100px] md:hidden md:w-0 md:border-0;
}
</style>
