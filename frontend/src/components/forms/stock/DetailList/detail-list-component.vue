<template>
  <div class="fyc-table">
    <div class="fyc-header">
      <div class="fyc-row">
        <div class="fyc-cell px-2">#ID</div>
        <div class="fyc-cell px-2">NAMA BARANG</div>
        <div class="fyc-cell w-16 text-right px-2">QTY</div>
        <div class="fyc-cell w-16 px-2">UNIT</div>
        <div class="fyc-cell text-right px-2">HARGA</div>
        <div class="fyc-cell w-24 text-right px-2">DISCOUNT</div>
        <div class="fyc-cell text-right px-2">SUBTOTAL</div>
      </div>
    </div>
    <div class="fyc-body">
      <div class="fyc-row" @keydown.enter.prevent="gotoNextCell">
        <div class="fyc-cell">
          {{ detailId }}
        </div>
        <div class="fyc-cell">
          <v-dropdown
            :options="[
              { id: 1, name: 'test' },
              { id: 2, name: 'Minyak' },
            ]"
            :selectedId="0"
            v-on:selected="validateName"
            :disabled="false"
            name="product"
            :maxItem="8"
            @focus="setCurrentCell(0)"
            :ref="
              (el) => {
                if (el) cells[0] = el?.getRef();
              }
            "
          />
        </div>
        <div class="fyc-cell text-right">
          <number
            class="my-input w-16 text-left md:text-right"
            v-model.lazy="qty"
            v-bind="inputNumber"
            placeholder="0"
            name="qty"
            @focus="setCurrentCell(1)"
            :ref="
              (el) => {
                if (el) cells[1] = el?.getRef();
              }
            "
          />
        </div>
        <div class="fyc-cell w-16">
          <v-dropdown
            :options="[
              { id: 1, name: 'kg', price: 2500 },
              { id: 2, name: 'cm', price: 1000 },
            ]"
            :selectedId="0"
            v-on:selected="validateUnit"
            :disabled="false"
            name="unit"
            :maxItem="8"
            @focus="setCurrentCell(2)"
            :ref="
              (el) => {
                if (el) cells[2] = el?.getRef();
              }
            "
          />
        </div>
        <div class="fyc-cell text-right px-2">{{ price }}</div>
        <div class="fyc-cell text-right">
          <number
            class="my-input text-left md:text-right"
            v-model.lazy="discount"
            v-bind:options="inputNumber"
            name="discount"
            placeholder="0"
            @focus="setCurrentCell(3)"
            :ref="
              (el) => {
                if (el) cells[3] = el?.getRef();
              }
            "
          />
        </div>
        <div class="fyc-cell text-right px-2">{{ subtotal }}</div>
      </div>
    </div>
  </div>
</template>
<script>
import { onMounted, toRefs, onBeforeUpdate } from "vue";

import axios from "axios";
import Dropdown from "@/components/DropdownNonBorder.vue";
import { state as detailData } from "./directive";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};
Array.prototype.insert = function (index, item) {
  this.splice(index, 0, item);
};
Array.prototype.update = function (item, id) {
  const i = this.indexOfObject("id", id);
  if (i >= 0) {
    this.splice(i, 1, item);
  }
};
Array.prototype.remove = function (id) {
  const i = this.indexOfObject("id", id);
  if (i >= 0) {
    this.splice(i, 1);
  }
};
export default {
  name: "StockDetailList",
  props: {
    stockId: {
      type: Number,
      require: true,
      default: 0,
    },
  },
  components: {
    "v-dropdown": Dropdown,
  },

  setup(props, { emit }) {
    const state = detailData;

    const loadStockDetails = async () => {
      await axios
        .get(`/api/stockdetails/stock/${props.stockId}`, {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.details = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    onMounted(async () => {
      await loadStockDetails();
    });

    const gotoNextCell = () => {
      state.cell = state.cell === 3 ? 0 : state.cell + 1;
      // console.log(`index-${state.cell}`,state.cells[state.cell])
      // if(state.cell === 1) state.cells['qty'].focus();
      state.cells[state.cell].focus();
    };

    // const gotoPrevCell = () => {
    //   state.cell = state.cell === 0 ? 3 : state.cell - 1;
    //   //state.cells[state.cell].focus();
    // };

    const setCurrentCell = (i) => {
      state.cell = i;
    };

    const validateName = (e) => {
      state.productId = e.id;
      state.name = e.name;
    };
    const validateUnit = (e) => {
      state.unitId = e.id;
      state.unitName = e.name;
      state.price = e.price;
    };

    onBeforeUpdate(() => {
      state.cells.value = [];
    });

    return {
      ...toRefs(state),
      gotoNextCell,
      //      gotoPrevCell,
      setCurrentCell,
      validateName,
      validateUnit,
    };
  },
};
</script>
<style scoped>
.v-number {
  @apply w-full py-0.5 rounded-sm outline-none border border-transparent bg-transparent px-2
  focus:bg-white focus:outline-none focus:border-emerald-400;
}

.fyc-table {
  @apply md:table w-full border-0 md:border-gray-300 rounded-t-xl text-[13px];
}
.fyc-header {
  @apply hidden border-b border-gray-400 bg-gray-200
  md:table-header-group h-9 font-medium;
}
.fyc-footer {
  @apply flex flex-col border-b border-gray-400 bg-gray-100
  md:table-footer-group h-9 font-medium;
}
.fyc-header .fyc-cell:first-child {
  @apply rounded-tl-xl pl-2;
}
.fyc-header .fyc-cell:last-child {
  @apply rounded-tr-xl pr-2;
}
.fyc-header .fyc-cell {
  @apply align-middle border-b;
}
.fyc-body .fyc-cell:first-child {
  @apply md:pl-2;
}
.fyc-body .fyc-cell:last-child {
  @apply md:pr-2;
}
.fyc-body {
  @apply flex flex-col md:table-header-group;
}
.fyc-row {
  @apply flex flex-col mt-4 md:mt-0 md:table-row;
}
.fyc-body .fyc-row {
  @apply hover:bg-gray-100;
}
.fyc-cell {
  @apply table-cell py-0 px-4 text-base md:text-sm md:px-1 md:py-1;
}
.btn-add {
  @apply py-1 px-5 bg-emerald-600 text-white font-semibold rounded-full shadow-md hover:bg-emerald-700
  focus:bg-emerald-900 focus:outline-none
  disabled:text-gray-600 disabled:bg-gray-200;
}
.cell-link {
  @apply cursor-pointer;
}
</style>
