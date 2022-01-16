<template>
  <div ref="test">
    <div
      class="mt-4 hidden text-[13px] w-full flex-row gap-x-0 font-medium md:flex bg-emerald-100"
    >
      <div class="w-[120px] px-1 py-1 border border-emerald-200">ID#</div>
      <div class="w-[200px] px-1 py-1 border border-emerald-200 border-l-0">NAMA</div>
      <div class="w-[300px] px-1 py-1 border border-emerald-200 border-l-0">BARCODE</div>
      <div class="w-[120px] px-1 py-1 border border-emerald-200 border-l-0 text-right">
        ISI
      </div>
      <div class="w-[250px] px-1 py-1 border border-emerald-200 border-l-0 text-right">
        HARGA BELI
      </div>
      <div class="w-[160px] px-1 py-1 border border-emerald-200 border-l-0 text-right">
        MARGIN
      </div>
      <div class="w-[250px] px-1 py-1 border border-emerald-200 border-l-0 text-right">
        HARGA JUAL
      </div>
      <div class="w-[225px] px-0 py-1 border border-emerald-200 border-l-0 text-center">
        DEFAULT
      </div>
      <div class="w-[270px] px-0 py-1 border border-emerald-200 border-l-0 text-center">
        COMMAND
      </div>
    </div>
    <div v-for="(unit, index) in units" v-bind:key="unit.id">
      <unit-form
        :selectedIndex="index"
        @change="onDefaultChanged($event, unit.id)"
        :unitProp="unit"
        :basePrice="$props.productPrice"
        @restoreData="restoreData"
        @update="updateUnit"
        @addNew="addUnit"
      >
        <template v-slot:default>
          <button
            class="btn border-transparent rounded-sm hover:bg-gray-200"
            type="button"
            tabindex="-1"
            :disabled="unit.id === 0"
            @click.prevent.stop="removeUnit(unit.id)"
          >
            <tw-icon
              name="mdi-light:delete"
              class="icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
              :class="{ 'text-red-700': unit.id > 0 }"
            />
          </button>
        </template>
      </unit-form>
    </div>
    <a href="#" @click.prevent.stop="addUnit">
      <tw-icon name="carbon:add-alt" class="icon w-5 h-5 mt-2 text-emerald-700" />
    </a>
  </div>
</template>

<script>
import axios from "axios";
import UnitForm from "./UnitForm.vue";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};

export default {
  name: "UnitList",

  props: {
    productId: {
      type: Number,
      default: 0,
    },
    update: {
      type: Function,
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
    changeFocus(value) {
      if (value !== this.focusName) {
        console.log(value);
      }
      this.focusName = value;
    },
    restoreData(unit) {
      const self = this;
      const index = self.units.indexOfObject("id", unit.id);
      if (unit.id === 0) {
        self.units.splice(index, 1);
      } else {
        self.units.splice(index, 1, { ...unit });
      }
    },
    onDefaultChanged(e, id) {
      for (let c = 0; c < this.units.length; c++) {
        this.units[c].is_default = this.units[c].id === id ? true : false;
      }
    },
    async removeUnit(id) {
      const self = this;
      const options = {
        "Content-Type": "application/json",
      };
      await axios
        .delete(`/api/units/${id}`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            const index = self.units.indexOfObject("id", id);
            self.units.splice(index, 1);
          }
        });
    },
    updateUnit(unit, id) {
      const self = this;
      //let temp = self.units;
      const index = self.units.indexOfObject("id", id);
      self.units.splice(index, 1, { ...unit });
      if (id === 0) {
        setTimeout(() => {
          self.addUnit();
        }, 0);
      }
    },
    addUnit() {
      const i = this.units.indexOfObject("id", 0);
      if (i < 0) {
        this.units.push({
          id: 0,
          name: "",
          barcode: "",
          content: 1,
          is_default: false,
          product_id: this.$props.productId,
          buy_price: this.$props.productPrice,
          margin: 0.0,
          price: this.$props.productPrice,
        });
      }
    },
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
            self.units = [...res.data];
          }
        })
        .catch((error) => {
          self.units = [];
        });
    },
  },
  async mounted() {
    await this.loadUnits();
    // this.$refs.test.querySelector("input").focus();
    //this.$refs.test.target.querySelector("*[autofocus]").focus();
  },
  computed: {
    focusName: {
      get() {
        return this.divFocus;
      },
      set(value) {
        if (value !== this.divFocus) {
          this.divFocus = value;
        }
      },
    },
  },
  data() {
    return {
      units: [],
      divFocus: "",
    };
  },
};
</script>

<style scoped></style>
