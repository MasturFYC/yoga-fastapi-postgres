<template>
  <form @submit.prevent.stop="getButtonName" :id="'myform-' + unit.id">
    <div
      class="text-[13px] w-full flex flex-col gap-x-0 md:flex-row py-4 md:py-0 gap-y-1 md:gap-y-0"
      @keydown.enter.prevent.stop="focusNext"
      @keydown.down.prevent.stop="onKeyDown"
      @keydown.up.prevent.stop="onKeyDown"
      @keydown.esc.prevent.stop="cancelEdit"
    >
      <div
        class="flex w-full md:w-[120px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-t-0"
      >
        <span class="label-title self-center">ID#:</span>
        <span class="my-input self-center text-gray-400">{{ unit.id }}</span>
      </div>
      <label
        class="flex w-full md:w-[200px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Unit</span>
        <input
          class="my-input"
          v-focus
          type="text"
          v-model.lazy="unitName"
          @focus.prevent.stop="onFocus(0)"
          maxlength="6"
        />
      </label>
      <label
        class="flex w-full md:w-[300px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Barcode</span>
        <input
          class="my-input"
          type="text"
          v-model.lazy="barcode"
          @focus.prevent.stop="onFocus(1)"
          maxlength="25"
        />
      </label>
      <label
        class="flex w-full md:w-[120px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Isi</span>
        <number
          ref="contentEl"
          class="my-input text-left md:text-right"
          v-model.lazy="unitContent"
          @focus.prevent.stop="onFocus(2)"
          v-bind="inputNumber"
          placeholder="0"
        />
      </label>
      <label
        class="flex w-full md:w-[250px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Harga Beli</span>
        <number
          class="my-input text-left text-gray-400 md:text-right"
          v-model="buyPrice"
          @focus.prevent.stop="onFocus(3)"
          v-bind="inputNumber"
          placeholder="0"
          readonly
        />
      </label>
      <label
        class="flex w-full md:w-[160px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Margin</span>
        <number
          class="my-input text-left md:text-right"
          v-model.lazy="unitMargin"
          @focus.prevent.stop="onFocus(4)"
          v-bind="inputPercent"
          placeholder="0"
        />
      </label>
      <label
        class="flex w-full md:w-[250px] px-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <span class="label-title">Harga Jual</span>
        <number
          class="my-input text-left md:text-right"
          v-model.lazy="salePrice"
          @focus.prevent.stop="onFocus(5)"
          v-bind="inputNumber"
          placeholder="0"
        />
      </label>
      <label
        class="flex w-full md:w-[225px] px-0 md:px-1 border-0 mt-2 md:mt-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
      >
        <input
          type="checkbox"
          v-model.lazy="unitDefault"
          class="mx-0 md:mx-auto self-center"
          @focus.prevent.stop="onFocus(6)"
        />
        <span class="px-1 md:hidden self-center text-gray-500">Default ?</span>
      </label>
      <div
        class="flex flex-row w-[270px] gap-x-0 py-1 px-0 mt-4 md:mt-0 md:px-1 border-0 md:border md:border-indigo-200 md:border-l-0 md:border-t-0"
        :class="{ 'bg-green-100': isDirty }"
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
    </div>
    <div
      v-if="isInvalidPrice"
      class="border-0 text-sm md:border md:border-indigo-200 p-2 text-red-700 flex-none w-full md:border-t-0"
    >
      Harga jual tidak boleh lebih kecil dari harga beli.
    </div>
    <div
      v-if="isDuplicate"
      class="border-0 text-sm md:border md:border-indigo-200 p-2 text-red-700 flex-none w-full md:border-t-0"
    >
      Nama unit atau barcode sudah digunakan.
    </div>
  </form>
</template>

<script>
import axios from "axios";

export default {
  name: "UnitForm",
  props: {
    basePrice: { type: Number, default: 0 },
    unitProp: { type: Object },
    addNew: { type: Function },
    //changeDefault: { type: Function },
  },
  methods: {
    onFocus(e) {
      this.iBlur = e;
    },
    getButtonName(e) {
      this.clickedButton = e.submitter.name;
    },
    onKeyDown(e) {
      // if(this.isDirty) {
      //   this.formSubmit(e)
      // }

      const forms = Array.from(e.target.form.parentElement.querySelectorAll("form"));

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
      if (el.type === "text" && el.value.length > 0) {
        setTimeout(() => {
          el.setSelectionRange(0, el.value.length);
        }, 0);
      }
    },
    focusNext(e) {
      const inputs = Array.from(e.target.form.querySelectorAll(["input", "button"]));
      const index = inputs.indexOf(e.target);
      // const length = inputs.length;
      const max = 6;

      if (index < max) {
        const i = index === 2 ? index + 1 : index;
        const el = inputs[i + 1];
        el.focus();
        if (el.type === "text") {
          setTimeout(() => {
            el.setSelectionRange(0, el.value.length);
          }, 0);
        }
        return;
      }

      if (this.isInvalidPrice) {
        return;
      }

      if (this.isDirty) {
        this.formSubmit(e);
      }

      this.gotoNextRow(e.target.form);

      //}
    },
    gotoNextRow(e) {
      //console.log(e.name);

      const forms = Array.from(e.parentElement.querySelectorAll("form"));

      let index = forms.indexOf(e);
      const length = forms.length - 1;

      if (index === length) {
        this.$emit("addNew");
        index--;
      }
      const f = forms[index + 1];

      const inputs = f.querySelectorAll("input");
      const el = inputs[0];

      el.focus();
      if (el.value.length > 0) {
        setTimeout(() => {
          el.setSelectionRange(0, el.value.length);
        }, 0);
      }
    },
    setDirty() {
      this.formChanged = true;
    },
    async formSubmit(e) {
      const self = this;
      e.preventDefault();

      if (this.isInvalidPrice) {
        return;
      }

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
      this.isDuplicate = false;
    },
    async insertUnit(unit) {
      const self = this;
      const data = { ...unit };
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
          self.isDuplicate = false;
          self.unit = res.data;
        })
        .catch((error) => {
          self.isDuplicate = true;
        });
    },
    async updateUnit(unit, id) {
      const self = this;
      const data = { ...unit };
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
          self.isDuplicate = false;
        })
        .catch((error) => {
          this.isDuplicate = true;
        });
    },
  },
  data() {
    return {
      iBlur: 0,
      isDuplicate: false,
      clickedButton: null,
      formChanged: false,
      oldUnit: { ...this.$props.unitProp },
      unit: { ...this.$props.unitProp },
    };
  },
  computed: {
    salePrice: {
      get() {
        return this.unit.price;
      },
      set(value) {
        if (value !== this.unit.price) {
          this.formChanged = true;
          this.unit.price = value;
          this.unit.margin = ((this.unit.price - this.buyPrice) / this.buyPrice) * 100.0;
        }
      },
    },

    unitName: {
      get() {
        return this.unit.name;
      },
      set(value) {
        if (value !== this.unit.name) {
          this.formChanged = true;
          this.unit.name = value;
        }
      },
    },
    barcode: {
      get() {
        return this.unit.barcode;
      },
      set(value) {
        if (value !== this.unit.barcode) {
          this.formChanged = true;
          this.unit.barcode = value;
        }
      },
    },
    unitContent: {
      get() {
        return this.unit.content;
      },
      set(value) {
        if (value !== this.unit.content) {
          this.formChanged = true;
          this.unit.content = value;
          this.unit.price = this.buyPrice + this.buyPrice * this.margin;
        }
      },
    },

    unitMargin: {
      get() {
        return this.unit.margin;
      },
      set(value) {
        if (value !== this.unit.margin) {
          this.formChanged = true;
          this.unit.margin = value;
          this.unit.price = this.buyPrice + this.buyPrice * this.margin;
        }
      },
    },

    unitDefault: {
      get() {
        return this.unit.is_default;
      },
      set(value) {
        if (value !== this.unit.is_default) {
          this.formChanged = true;
          this.unit.is_default = value;
          //this.$emit('changeDefault', this.unit.id);
        }
      },
    },

    isInvalidPrice() {
      return this.unit.price < this.buyPrice;
    },

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
      mounted: function (el) {
        // When the bound element is inserted into the DOM...
        setTimeout(() => {
          el.focus(); // Focus the element
          //          }
          // el.select();
        }, 0);
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
  @apply w-[200px]  text-gray-500 md:hidden md:w-0 border-0 border-b border-b-indigo-200;
}
</style>
