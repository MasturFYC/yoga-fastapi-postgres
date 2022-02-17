<template>
  <div class="fyc-table">
    <div class="fyc-header">
      <div class="fyc-row">
        <div class="fyc-cell"><div class="px-1">#ID</div></div>
        <div class="fyc-cell"><div class="px-1">NAMA BARANG</div></div>
        <div class="fyc-cell w-16 text-right"><div class="px-1">QTY</div></div>
        <div class="fyc-cell w-20"><div class="px-1">UNIT</div></div>
        <div class="fyc-cell"><div class="text-right px-1">HARGA</div></div>
        <div class="fyc-cell w-24 text-right"><div class="px-1">DISCOUNT</div></div>
        <div class="fyc-cell"><div class="text-right px-1">SUBTOTAL</div></div>
        <div class="fyc-cell"><div class="text-center px-1">COMMAND</div></div>
      </div>
    </div>
    <div class="fyc-body">
      <detail-form
        v-for="(item, index) in details"
        :detail="item"
        :key="item.id"
        :products="products"
        @update="updateDetail"
        @insert="insertDetail"
        @add="addNewDetail"
        @remove="removeDetail"
        @next="selectNetRow"
        :ref="
          (el) => {
            if (el) list[index] = el?.getRef();
          }
        "
      />
    </div>
    <div ref="divScroll" class="mt-[250px]"></div>
  </div>
</template>
<script>
import {
  toRefs,
  ref,
  onBeforeUpdate,
  onMounted,
  reactive,
  computed,
  nextTick,
} from "vue";

import axios from "axios";
import StockDetailForm from "@/components/forms/stock/detail-form";
import { stateData as detailData } from "../detail-form/directive";

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

Array.prototype.getItem = function (id) {
  const i = this.indexOfObject("id", id);
  return i === -1 ? null : this[i];
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
    "detail-form": StockDetailForm,
  },

  setup(props, { emit }) {
    const divScroll = ref(null);
    const state = reactive({
      curId: 0,
      list: ref([]),
      stockDetails: [],
      dataProducts: [],
      stockId: computed({
        get() {
          return props.stockId;
        },
      }),
      details: computed({
        get() {
          return state.stockDetails;
        },
        set(v) {
          state.stockDetails = v;
        },
      }),
      products: computed({
        get() {
          return state.dataProducts;
        },
        set(v) {
          state.dataProducts = v;
        },
      }),
    });

    const loadProducts = async () => {
      await axios
        .get(`/api/products/with-units`, {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.products = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const loadStockDetails = async () => {
      await axios
        .get(`/api/stockdetails/stock/${state.stockId}`, {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.stockDetails = [...res.data, { ...detailData }];
        })
        .catch((error) => {
          console.log(error);
        });
    };

    onMounted(async () => {
      await loadProducts();
      await loadStockDetails();
    });

    onBeforeUpdate(() => {
      state.list.value = [];
    });

    function selectNetRow(id) {
      const i = state.details.indexOfObject("id", id) + 1;

      const ep = state.list[i];
      if (ep) {
        const el = ep.querySelectorAll("input");
        if (el) {
          nextTick(() => {
            el[0].focus();
          });
        }
      }
    }

    function addNewDetail() {
      const l = state.details.length;
      state.details.push({ ...detailData });
      nextTick(() => {
        const el = state.list[l];
        el.querySelector("input").focus();
        el.scrollIntoView({ behavior: "smooth" });
      });
    }

    const insertDetail = async (e, callback) => {
      const { qty, content, unit_name, price, discount, product_id, unit_id } = e;
      const data = {
        'qty': qty,
        'content': content,
        'unit_name': unit_name,
        'price': price,
        'discount': discount,
        'stock_id': state.stockId,
        'product_id': product_id,
        'unit_id': unit_id,
      };

      await axios
        .post(`/api/stockdetails`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.details.update(res.data, 0);
          callback(true);
          console.log(res.data.subtotal)
          emit("update", 'post', props.stockId, res.data.subtotal);
        })
        .catch((error) => {
          callback(false);
        });
    };

    const updateDetail = async (e, id, callback) => {

      const { qty, content, unit_name, price, discount, product_id, unit_id } = e;
      const data = {
        'qty': qty,
        'content': content,
        'unit_name': unit_name,
        'price': price,
        'discount': discount,
        'stock_id': state.stockId,
        'product_id': product_id,
        'unit_id': unit_id,
      };

      await axios
        .put(`/api/stockdetails/${id}`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          const item = state.details.getItem(id);
          state.details.update(res.data, id);
          callback(true);
          emit("update", 'put', props.stockId, item.subtotal - res.data.subtotal);
        })
        .catch((error) => {
          console.log(error);
          callback(false);
        });
    };


    const removeDetail = async (e) => {
      await axios
        .delete(`/api/stockdetails/${e}`, {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          const item = state.details.getItem(e);
          state.details.remove(e);
          emit("update", 'delete', props.stockId, item.subtotal);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return {
      ...toRefs(state),
      updateDetail,
      insertDetail,
      addNewDetail,
      selectNetRow,
      removeDetail,
    };
  },
};
</script>

<style scoped>
.v-number {
  @apply w-full py-0.5 rounded-sm outline-none border border-transparent bg-transparent px-1
  focus:bg-white focus:outline-none focus:border-emerald-400;
}

.fyc-table {
  @apply md:table w-full border-0 md:border-gray-300 rounded-t-md text-[13px];
}
.fyc-header {
  @apply hidden border-b border-gray-400 bg-gray-200 text-[13px] uppercase
  md:table-header-group h-9 font-medium;
}
.fyc-footer {
  @apply flex flex-col border-b border-gray-400 bg-gray-100
  md:table-footer-group h-9 font-medium;
}
.fyc-header .fyc-cell:first-child {
  @apply rounded-tl-md border-l-0;
}
.fyc-header .fyc-cell:last-child {
  @apply rounded-tr-md;
}
.fyc-header .fyc-cell {
  @apply align-middle border-b;
}
.fyc-body {
  @apply flex flex-col md:table-header-group;
}
.fyc-row {
  @apply flex flex-col mt-4 md:mt-0 md:table-row text-[13px];
}
.fyc-body .fyc-row {
  @apply hover:bg-gray-100;
}
.fyc-cell {
  @apply table-cell py-0 px-4 text-base md:text-sm md:px-1 md:py-1 text-[13px]
  border-0 border-l border-gray-300;
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
