<template>
  <div class="fyc-table">
    <div class="fyc-header">
      <div class="fyc-row">
        <div class="fyc-cell">#ID</div>
        <div class="fyc-cell">NAMA BARANG</div>
        <div class="fyc-cell w-16 text-right">QTY</div>
        <div class="fyc-cell w-16">UNIT</div>
        <div class="fyc-cell text-right">HARGA</div>
        <div class="fyc-cell w-24 text-right">DISCOUNT</div>
        <div class="fyc-cell text-right">SUBTOTAL</div>
      </div>
    </div>
    <div class="fyc-body">
      <div
        class="fyc-row"
        @keydown.left.prevent.stop="gotoPrevCell"
        @keydown.right.prevent.stop="gotoNextCell"
        @keydown.enter.prevent="gotoNextCell"
      >
        <div class="fyc-cell">
          {{ 0 }}
        </div>
        <div class="fyc-cell">
          <v-dropdown
            :options="[
              { id: 1, name: 'test' },
              { id: 2, name: 'Minyak' },
            ]"
            :selectedId="0"
            v-on:selected="validateSelection"
            :disabled="false"
            name="product"
            :maxItem="8"
            @focus="setCurrentCell(0)"
            :ref="(el) => (cells[0] = el.getRef())"
          />
        </div>
        <div class="fyc-cell text-right">
          <input
            type="text"
            class="text-right w-16"
            @focus="setCurrentCell(1)"
            :ref="(el) => (cells[1] = el)"
          />
        </div>
        <div class="fyc-cell w-16">
          <v-dropdown
            :options="[
              { id: 1, name: 'kg' },
              { id: 2, name: 'cm' },
            ]"
            :selectedId="0"
            v-on:selected="validateSelection"
            :disabled="false"
            name="unit"
            :maxItem="8"
            @focus="setCurrentCell(2)"
            :ref="(el) => (cells[2] = el.getRef())"
          />
        </div>
        <div class="fyc-cell text-right">{{ 0 }}</div>
        <div class="fyc-cell text-right">
          <input
            title="Discount"
            type="text"
            class="w-24 text-right"
            @focus="setCurrentCell(3)"
            :ref="(el) => (cells[3] = el)"
          />
        </div>
        <div class="fyc-cell text-right">{{ 0 }}</div>
      </div>
    </div>
  </div>
</template>
<script>
import { computed, onMounted, reactive, toRefs, ref, onBeforeUpdate } from "vue";
import axios from "axios";
import Dropdown from "@/components/DropdownNonBorder.vue";

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
    const state = reactive({
      cell: 0,
      cells: ref([]),
      stockDetails: [],
      dirty: false,
      details: computed({
        get() {
          return state.stockDetails;
        },
        set(v) {
          state.stockDetails = v;
        },
      }),
    });

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
      state.cells[state.cell].focus();
    };

    const gotoPrevCell = () => {
      state.cell = state.cell === 0 ? 3 : state.cell - 1;
      state.cells[state.cell].focus();
    };

    const setCurrentCell = (i) => {
      state.cell = i;
    };

    const validateSelection = (e) => {};

    onBeforeUpdate(() => {
      state.cells.value = [];
    });

    return {
      ...toRefs(state),
      gotoNextCell,
      gotoPrevCell,
      setCurrentCell,
      validateSelection,
    };
  },
};
</script>
<style scoped>
.fyc-table {
  @apply md:table w-full border-0 md:border rounded-t-xl text-[13px];
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
