<template>
<div class="flex flex-row">
  <div class="flex-1 w-full">
    <h1 class="text-emerald-700 text-[24px] font-bold">Pembelian</h1>
    <div class="my-4">
      <button href="#" class="btn-add" @click="addNewStock">
        <tw-icon name="carbon:add-alt" class="flex-1 icon w-5 h-5" />
      </button>
    </div>
    <div v-if="!showForm">
      <div class="fyc-table">
        <div class="fyc-table-row-header">
          <div class="fyc-table-row">
            <div class="fyc-table-cell">ID#</div>
            <div class="fyc-table-cell">INVOICE</div>
            <div class="fyc-table-cell text-center">TANGGAL</div>
            <div class="fyc-table-cell">SUPPLIER</div>
            <div class="fyc-table-cell text-right">TOTAL</div>
            <div class="fyc-table-cell text-right">CASH</div>
            <div class="fyc-table-cell text-right">ANGSURAN</div>
            <div class="fyc-table-cell text-right">SISA BAYAR</div>
          </div>
        </div>
        <div class="fyc-table-row-group">
          <div
            class="fyc-table-row"
            v-for="(item, index) in stocks"
            :key="item.id"
            :class="{
              'bg-gray-50': index % 2 !== 0,
              'bg-emerald-700 text-white': selectedIndex === index,
            }"
            @click="selectedIndex = index"
          >
            <div class="fyc-table-cell">{{ item.id }}</div>
            <div class="fyc-table-cell cell-link" @click="editStock(item)">
              {{ item.invoice_number }}
            </div>
            <div class="fyc-table-cell md:text-center">
              {{ formatDate(item.created_at) }}
            </div>
            <div class="fyc-table-cell">
              {{ getSupplierName(item.supplier_id) }}
            </div>
            <div class="fyc-table-cell text-right">
              {{ format(item.total) }}
            </div>
            <div class="fyc-table-cell text-right">{{ format(item.cash) }}</div>
            <div class="fyc-table-cell text-right">
              {{ format(item.payment) }}
            </div>
            <div class="fyc-table-cell text-right font-bold">
              {{ item.remain_payment }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <stock-form
      v-if="showForm"
      :stockProp="selectedStock"
      :suppliers="suppliers"
      :isLoaded="childLoaded"
      @cancelChange="cancelChange"
      @saveChange="saveChange"
      @removeData="removeData"
      :key="counter"
    ></stock-form>
    <div v-if="showForm" :key="selectedStock.id">
      <stock-detail 
        :stockId="selectedStock.id"
        @update="updateLocalStock"
        />
    </div>
  </div>
  <div class="hidden md:block md:w-[250px] p-2">
    <code class="text-xs whitespace-pre">{{ selectedStock.id === 0 ? stocks : selectedStock }}</code>
  </div>
  </div>
</template>

<script>
import { computed, toRefs, reactive, onMounted } from "vue";
import dayjs from "dayjs";
import axios from "axios";
import StockForm from "@/components/forms/stock/StockForm.vue";
import StockDetailList from "@/components/forms/stock/DetailList";

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
  name: "Pembelian",
  components: {
    "stock-form": StockForm,
    "stock-detail": StockDetailList,
  },

  setup() {
    const new_stock = {
      id: 0,
      invoice_number: "",
      total: 0,
      cash: 0,
      payment: 0,
      remain_payment: 0,
      created_at: dayjs(),
      supplier_id: 0,
    };

    // const dateOptions = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
    const indoNumberFormatter = new Intl.NumberFormat("id-ID");
    // const indoDateFormatter = new Intl.DateTimeFormat("id-ID", dateOptions);

    const state = reactive({
      childLoaded: false,
      counter: 0,
      isEdit: false,
      stock: { ...new_stock },
      stocks: [],
      suppliers: [],
      selIndex: 0,
      selectedIndex: computed({
        get() {
          return state.selIndex;
        },
        set(v) {
          state.selIndex = v;
        },
      }),
      showForm: computed({
        get: () => {
          return state.isEdit;
        },
        set: (v) => {
          state.isEdit = v;
        },
      }),
      selectedStock: computed({
        get: () => {
          return state.stock;
        },
        set: (v) => {
          state.stock = v;
        },
      }),
    });

    const addNewStock = () => {
      //setTimeout(() => {
      state.counter++;
      state.childLoaded = false;
        state.selectedStock = { ...new_stock };
      //}, 100);
      state.showForm = true;
    };

    const editStock = (item) => {
      state.childLoaded = false;
      state.selectedStock = item;
      // setTimeout(() => {
      state.showForm = true;
      // }, 2000);
    };

    function cancelChange() {
      state.showForm = false;
      state.selectedStock = { ...new_stock };
    }

    const formatDate = (date) => {
      return dayjs(date).format("DD-MM-YYYY");
    };

    const getSupplierName = (id) => {
      const i = state.suppliers.indexOfObject("id", id);
      const test = state.suppliers[i];
      return test ? test.name : "-";
    };

    const loadSupplier = async () => {
      const opt = {
        accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios.get("/api/suppliers/", { headers: opt }).then((res) => {
        const json = res.data;
        state.suppliers = json;
      });
    };

    const loadAllStock = async () => {
      await axios
        .get("/api/stocks/", {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.stocks = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const format = (num) => {
      return indoNumberFormatter.format(num);
    };

    const insertStock = async (stock) => {
      const data = { ...stock };
      delete data.id;

      await axios
        .post("/api/stocks/", JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          state.showForm = false;
          state.stocks.insert(0, res.data);
          //state.selectedStock = { ...new_stock };
          state.selectedIndex = 0;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const updateStock = async (stock, id) => {
      const data = { ...stock };
      delete data.id;

      await axios
        .put(`/api/stocks/${id}/`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          const id = res.data.id;
          const index = state.stocks.update(res.data, id);
          //state.selectedStock = { ...new_stock };
          state.selectedIndex = 0;
          state.showForm = false;
        });
    };

    const removeData = async (id) => {
      await axios.delete(`/api/stocks/${id}/`).then((res) => {
        if (res.status === 200) {
          state.stocks.remove(id);
          //state.selectedStock = { ...new_stock };
          state.showForm = false;
        }
      });
    };

    const saveChange = async (stock) => {
      if (stock.id === 0) {
        await insertStock(stock);
      } else {
        await updateStock(stock, stock.id);
      }
    };

    const updateLocalStock = (method, id, total) => {
      
      const item = state.stocks.getItem(id);
      if(method === 'delete') {
        item.total -= total; 
      } else {
        item.total += total;
      }
      item.remain_payment = item.total - (item.cash + item.payment)
      state.childLoaded = true;
      state.stocks.update(item, id)
      state.selectedStock = item;
      state.counter++;
    }

    onMounted(async () => {
      await loadSupplier();
      await loadAllStock();
    });

    return {
      ...toRefs(state),
      formatDate,
      getSupplierName,
      cancelChange,
      saveChange,
      removeData,
      format,
      editStock,
      addNewStock,
      updateLocalStock
    };
  },
};
</script>

<style scoped>
.fyc-table {
  @apply md:table w-full border rounded-t-md;
}

.fyc-table-row-header {
  @apply hidden border-b border-gray-400 bg-gray-100
  md:table-header-group h-9 font-medium;
}
.fyc-table-row-header .fyc-table-cell:first-child {
  @apply rounded-tl-md pl-2;
}
.fyc-table-row-header .fyc-table-cell:last-child {
  @apply rounded-tr-md pr-2;
}

.fyc-table-row-header .fyc-table-cell {
  @apply align-middle border-b;
}

.fyc-table-row-group .fyc-table-cell:first-child {
  @apply md:pl-2;
}
.fyc-table-row-group .fyc-table-cell:last-child {
  @apply md:pr-2;
}

.fyc-table-row-group {
  @apply flex flex-col md:table-header-group;
}
.fyc-table-row {
  @apply flex flex-col mt-4 md:mt-0 md:table-row;
}
.fyc-table-row-group .fyc-table-row {
  @apply hover:bg-emerald-700 hover:text-white;
}
.fyc-table-cell {
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
