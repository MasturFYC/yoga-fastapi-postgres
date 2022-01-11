<template>
  <div
    class="mt-4 hidden text-[13px] w-full flex flex-row gap-x-0 font-medium md:flex bg-indigo-100"
  >
    <div class="w-[120px] px-1 py-1 border border-indigo-400">ID#</div>
    <div class="w-[500px] px-1 py-1 border border-indigo-400 border-l-0">NAMA</div>
    <div class="w-[120px] px-1 py-1 border border-indigo-400 border-l-0 text-right">
      ISI
    </div>
    <div class="w-[250px] px-1 py-1 border border-indigo-400 border-l-0 text-right">
      HARGA BELI
    </div>
    <div class="w-[155px] px-1 py-1 border border-indigo-400 border-l-0 text-right">
      MARGIN
    </div>
    <div class="w-[250px] px-1 py-1 border border-indigo-400 border-l-0 text-right">
      HARGA JUAL
    </div>
    <div class="w-[225px] px-1 py-1 border border-indigo-400 border-l-0">DEFAULT</div>
    <div class="w-[270px] px-1 py-1 border border-indigo-400 border-l-0">COMMAND</div>
  </div>
  <template v-for="unit in units" :key="unit.id">
    <unit-form :unitProp="unit" :basePrice="$props.productPrice" @update="updateUnit">
      <template v-slot:default>
        <button
          class="btn border-transparent rounded-sm hover:bg-gray-200"
          type="button"
          :disabled="unit.id === 0"
          @click="removeUnit(unit.id)"
        >
          <tw-icon
            name="mdi-light:delete"
            class="icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
            :class="{ 'text-red-700': unit.id > 0 }"
          />
        </button>
      </template>
    </unit-form>
  </template>
  <a href="#" @click.prevent.stop="addUnit">+</a>
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
      let temp = self.units;
      const index = self.units.indexOfObject("id", id);
      if (id === -1) {
        if (unit.id === 0) {
          self.units.splice(index, 1);
        }
      } else {
        //temp[index] = unit;
        self.units[index] = unit;
        if (id === 0) {
          self.addUnit();
        }
      }
    },
    addUnit() {
      const i = this.units.indexOfObject("id", 0);
      if (i < 0) {
        this.units.push({
          id: 0,
          name: "",
          content: 1,
          is_default: false,
          product_id: this.$props.productId,
          buy_price: this.$props.productPrice,
          margin: 30.0,
          price: this.$props.productPrice + this.$props.productPrice * (30.0 / 100.0),
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
  },
  data() {
    return {
      units: [],
    };
  },
};
</script>

<style scoped></style>
