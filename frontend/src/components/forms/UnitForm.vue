<template>
  <form
    @submit.prevent="getButtonName"
    :id="'myform' + unit.id"
    @keydown.down.prevent.stop="onKeyDown"
    @keydown.up.prevent.stop="onKeyDown"
    class="
      text-[13px]
      w-full
      flex flex-col
      gap-x-0
      md:flex-row
      py-4
      md:py-0
      gap-y-1
      md:gap-y-0
    "
    @keydown.esc="cancelEdit"
  >
    <div
      class="
        flex
        w-full
        md:w-[120px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-t-0
      "
    >
      <span class="label-title self-center">ID#:</span>
      <span class="my-input self-center">{{ unit.id }}</span>
    </div>
    <label
      class="
        flex
        w-full
        md:w-[500px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
      ><span class="label-title">Unit</span
      ><input
        class="my-input"
        v-focus
        type="text"
        @keydown.enter="focusNext"
        v-model.lazy="unit.name"
        @focus="onBlur(0)"
        maxlength="6"
        @change="setDirty"
    /></label>
    <label
      class="
        flex
        w-full
        md:w-[120px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
      ><span class="label-title">Isi</span
      ><number
        ref="contentEl"
        class="my-input text-left md:text-right"
        v-model.lazy="unit.content"
        @keydown.enter="focusNext"
        @focus="onBlur(1)"
        v-bind="inputNumber"
        @change="contentChanged($event)"
        placeholder="0"
    /></label>
    <label
      class="
        flex
        w-full
        md:w-[250px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
      ><span class="label-title">Harga Beli</span
      ><number
        class="my-input text-left text-gray-400 md:text-right"
        @keydown.enter="focusNext"
        v-model="buyPrice"
        @focus="onBlur(2)"
        v-bind="inputNumber"
        placeholder="0"
        readonly
    /></label>
    <label
      class="
        flex
        w-full
        md:w-[160px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
      ><span class="label-title">Margin</span
      ><number
        class="my-input text-left md:text-right"
        v-model.lazy="unit.margin"
        @keydown.enter="focusNext"
        @focus="onBlur(3)"
        v-bind="inputPercent"
        @change="marginChanged($event)"
        placeholder="0"
    /></label>
    <label
      class="
        flex
        w-full
        md:w-[250px]
        px-0
        md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
      ><span class="label-title">Harga Jual</span
      ><number
        class="my-input text-left md:text-right"
        v-model.lazy="unit.price"
        @keydown.enter="focusNext"
        @focus="onBlur(4)"
        v-bind="inputNumber"
        @change="priceChanged($event)"
        placeholder="0"
    /></label>
    <label
      class="
        flex
        w-full
        md:w-[225px]
        px-0
        md:px-1
        border-0
        mt-2
        md:mt-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
    >
      <input
        type="checkbox"
        v-model.lazy="unit.is_default"
        class="self-center"
        @keydown.enter="focusNext"
        @focus="onBlur(5)"
        @change="setDirty"
      />
      <span class="px-1 md:hidden self-center">Default ?</span>
    </label>
    <div
      class="
        flex flex-row
        w-[270px]
        gap-x-0
        py-1
        px-0
        mt-4
        md:mt-0 md:px-1
        border-0
        md:border md:border-indigo-200 md:border-l-0 md:border-t-0
      "
    >
      <button
        type="button"
        @click.prevent.stop="formSubmit"
        :disabled="!isDirty"
        class="btn border-transparent rounded-sm hover:bg-gray-200"
        :class="{ 'disabled hover:bg-transparent': !isDirty }"
      >
        <tw-icon
          name="mdi:check"
          class="flex-1 icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
          :class="{ 'text-green-700': isDirty }"
        />
      </button>
      <button
        type="button"
        :disabled="!isDirty && unit.id !== 0"
        @click.prevent.stop="cancelEdit"
        class="btn border-transparent rounded-sm hover:bg-gray-200"
        :class="{ 'disabled hover:bg-transparent': !isDirty }"
      >
        <tw-icon
          name="mdi-light:cancel"
          class="icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
          :class="{ 'text-orange-700': isDirty || unit.id === 0 }"
        />
      </button>
      <slot></slot>
    </div>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: "UnitForm",
  props: {
    basePrice: {
      type: Number,
      default: 0,
    },
    unitProp: {
      type: Object,
    },
    addNew: {
      type: Function
    }
  },
  methods: {
    onBlur(e) {
      this.iBlur = e;
    },
    getButtonName(e) {
      this.clickedButton = e.submitter.name;
    },
    onKeyDown(e) {

      // if(this.isDirty) {
      //   this.formSubmit(e)
      // }

      const forms = Array.from(
        e.target.parentElement.parentElement.parentElement.querySelectorAll(
          "form"
        )
      );

      const index = forms.indexOf(e.target.form);
      const length = forms.length - 1;

      const i =
        e.key === "ArrowUp"
          ? index === 0
            ? length
            : index - 1
          : index === length
          ? 0
          : index + 1;
      const f = forms[i];

      const inputs = f.querySelectorAll("input");
      const el = inputs[this.getBlurIndex];

      el.focus();
      if (this.getBlurIndex < 5) {
        setTimeout(() => {
          el.setSelectionRange(0, el.value.length);
        }, 50);
      }
    },
    focusNext(e) {
      const inputs = Array.from(e.target.form.querySelectorAll("input"));
      const index = inputs.indexOf(e.target);
      const length = inputs.length;

      if (index < length) {
        const i = index === 1 ? index + 1 : index;
        if (index === length - 1) {
          if(this.isDirty) {
            this.formSubmit(e);            
          }
        } else {
          const el = inputs[i + 1];
          el.focus();
          if (el.type === "text") {
            setTimeout(() => {
              el.setSelectionRange(0, el.value.length);
            }, 50);
          } else {
            if(this.isDirty) {
              this.formSubmit(e); 
            }
            this.$emit('addNew');
            inputs[0].focus();
          }
        }
      }
    },
    setDirty() {
      this.formChanged = true;
    },
    contentChanged(e) {
      const content = this.unit.content;
      this.unit.price = this.buyPrice + this.buyPrice * this.margin;
      this.formChanged = true;
    },
    marginChanged(e) {
      // const margin = this.unit.margin;
      this.unit.price = this.buyPrice + this.buyPrice * this.margin;
      this.formChanged = true;
    },
    priceChanged(e) {
      this.unit.margin =
        ((this.unit.price - this.buyPrice) / this.buyPrice) * 100.0;
      this.formChanged = true;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();
      if (self.unit.id > 0) {
        await self.updateUnit(self.unit, self.unit.id);
      } else {
        await self.insertUnit(self.unit);
      }
    },
    cancelEdit() {
      if (this.unit.id === 0) {
        this.$emit("update", this.unit, -1);
      } else {
        this.unit = { ...this.oldUnit };
      }
      this.formChanged = false;
    },
    async insertUnit(sales) {
      const self = this;
      const data = { ...sales };
      delete data.id;

      await axios
        .post(`/api/units/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit("update", res.data, 0);
          self.oldUnit = res.data;
          self.formChanged = false;
          self.unit = { ...this.$props.unitProp };
        });
    },
    async updateUnit(sales, id) {
      const self = this;
      const data = { ...sales };
      delete data.id;
      await axios
        .put(`/api/units/${id}/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          self.$emit("update", res.data, id);
          this.oldUnit = res.data;
          this.formChanged = false;
        });
    },
  },
  data() {
    return {
      iBlur: 0,
      clickedButton: null,
      formChanged: false,
      oldUnit: { ...this.$props.unitProp },
      unit: { ...this.$props.unitProp },
    };
  },
  computed: {
    getBlurIndex() {
      return this.iBlur;
    },
    isDirty() {
      return this.formChanged;
    },
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
    buyPrice() {
      return this.unit.content * this.$props.basePrice;
    },
    margin() {
      return this.unit.margin / 100.0;
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
};
</script>

<style scoped>
.my-input {
  @apply w-full outline-none border-0 md:border-0;
}
.label-title {
  @apply w-[200px] md:hidden md:w-0 border-0 border-b border-b-indigo-200;
}
</style>
