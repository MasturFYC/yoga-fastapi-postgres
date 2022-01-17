<template>
  <form @submit="formSubmit">
    <div class="data-form border">
      <div class="flex-1 flex flex-col gap-y-2 self-start w-full">
        <label class="label-group">
          <span class="label-title">Invoice</span>
          <input class="control" type="text" v-model.lazy="invoiceNumber" />
        </label>
        <label class="label-group">
          <span class="label-title">Tanggal</span>
          <input class="control" type="date"
          placeholder="mm-dd-yyyy" format="MM-DD-YYYY"
          v-model.lazy="createdAt" />
        </label>
        <label class="label-group">
          <span class="label-title">Supplier</span>
          <v-dropdown
            v-if="suppliers.length"
            :options="suppliers"
            :selectedId="supplierId"
            v-on:selected="validateSelection"
            :disabled="false"
            name="supplier"
            :maxItem="8"
          />
        </label>
      </div>

      <div class="flex-1 flex flex-col gap-y-2 w-full">
        <label class="label-group">
          <span class="label-title">Total</span>
          <number
            class="control-disabled md:text-right"
            v-model="total"
            v-bind="inputNumber"
            tabindex="-1"
            placeholder="0"
            readonly
          />
        </label>
        <label class="label-group">
          <span class="label-title">Cash</span>
          <number
            class="control md:text-right"
            v-model="cash"
            v-bind="inputNumber"
            placeholder="0"
          />
        </label>
        <label class="label-group">
          <span class="label-title">Payment</span>
          <number
            class="control-disabled md:text-right"
            v-model="payment"
            v-bind="inputNumber"
            tabindex="-1"
            placeholder="0"
            readonly
          />
        </label>
      </div>
    </div>
    <div class="flex flex-row gap-2 my-5">
      <button type="submit" class="btn-primary" :disabled="!enableSubmit">Save</button>
      <button type="button" class="btn-cancel" @click="cancelChange">Cancel</button>
      <button type="button" class="btn-remove hidden" :class="{'flex': stockId > 0}" @click="removeData">Save</button>
    </div>
    <hr />
        <div>time {{ createdAt }}</div>

  </form>
</template>

<script>
import { computed, toRefs, reactive, onMounted } from "vue";
import Dropdown from "@/components/FycDropdown.vue";
import axios from "axios";
import dayjs from 'dayjs';

export default {
  name: "StockForm",

  components: {
    "v-dropdown": Dropdown,
  },

  props: {
    stockProp: {
      type: Object,
      required: true,
      default: {},
    },
  },

  setup(props, {emit}) {
    const formSubmit = (e) => {
      e.preventDefault();
      saveChange();
    };

    const loadSupplier = async () => {
      const opt = {
        accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios.get("/api/suppliers/", { headers: opt }).then((res) => {
        const json = res.data;
        event.supplierList = json;
      });
    };

    const validateSelection = (e) => {
      event.supplierId = e.id;
    };

    const event = reactive({
      stock: props.stockProp,
      supplierList: [],
      dirty: false,

      suppliers: computed(() => {
        return event.supplierList;
      }),

      stockId: computed(() => event.stock.id),

      invoiceNumber: computed({
        get() {
          return event.stock.invoice_number;
        },
        set(value) {
          if (value !== event.stock.invoice_number) {
            event.stock.invoice_number = value;
            event.hashDirty = true;
          }
        },
      }),

      hashDirty: computed({
        get () { return event.dirty },
        set (value) { event.dirty = value },
      }),

      total: computed({
        get() {
          return event.stock.total;
        },
        set(value) {
          if (value !== event.stock.total) {
            event.stock.total = value;
            event.hashDirty = true;
          }
        },
      }),

      cash: computed({
        get() {
          return event.stock.cash;
        },
        set(value) {
          if (value !== event.stock.cash) {
            event.stock.cash = value;
            event.hashDirty = true;
          }
        },
      }),

      payment: computed({
        get() {
          return event.stock.payment;
        },
        set(value) {
          if (value !== event.stock.payment) {
            event.stock.payment = value;
            event.hashDirty = true;
          }
        },
      }),

      remainPayment: computed({
        get() {
          return event.stock.remain_payment;
        },
        set(value) {
          if (value !== event.stock.remain_payment) {
            event.stock.remain_payment = value;
          }
        },
      }),

      supplierId: computed({
        get() {
          return event.stock.supplier_id;
        },
        set(value) {
          if (value !== event.stock.supplier_id) {
            event.stock.supplier_id = value;
            event.hashDirty = true;
            //console.log('supplier id hashChanged', value)
          }
        },
      }),

      createdAt: computed({
        get() {          
          return dayjs(event.stock.created_at).format('YYYY-MM-DD');
        },
        set(value) {
          
          if (value !== event.stock.created_at) {
            event.stock.created_at = setDatetime(value);
            event.hashDirty = true;
          }
        },
      }),

      inputNumber: computed(() => {
        return {
          decimal: ",",
          separator: ".",
          suffix: "",
          precision: 2,
          masked: false,
        };
      }),
    });

    const setDatetime = (v) => {
        const time = dayjs(); //);        
        const date = dayjs(v)
        .set("hour", time.get("hour"))
        .set("minute", time.get("minute"))
        .set("second", time.get("second"))
        .set("millisecond", time.get("millisecond"));
        return date;
      };


    const enableSubmit = computed(() => {
      const isInvoiceValid = event.invoiceNumber.trim().length > 0;
      const isSupplierIdValid = event.supplierId > 0;

      // console.log({
      //   'isInvoiceValid': isInvoiceValid,
      //   'isSupplierIdValid': isSupplierIdValid, 'supid':event.supplierId
      // })
      const test = isInvoiceValid && isSupplierIdValid;
    //console.log('test',test)
      return (test);
    });

    onMounted(async () => {
      await loadSupplier();
    });

    const cancelChange = () => emit("cancelChange");
    const saveChange = () => emit("saveChange", event.stock);
    const removeData = () => emit("removeData", event.stock.id);

    return {
      ...toRefs(event),
      formSubmit,
      enableSubmit,
      validateSelection,
      cancelChange,
      saveChange,
      removeData,
      setDatetime
    };
  },
};
</script>
<style scoped>
.control {
  @apply rounded-[6px] py-0.5 px-2 flex-initial w-full self-start text-gray-700
  border border-emerald-400 placeholder:italic
  focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500;
}

.label-title {
  @apply font-medium text-gray-400 w-[150px] self-center text-left md:text-right;
}
.label-group {
  @apply flex flex-1 flex-row text-[14px] gap-x-3;
}
.control-disabled {
  @apply rounded-[6px] py-0.5 px-2 flex-initial w-full self-start
  text-gray-400 border border-gray-400 focus:border-gray-400
  placeholder:italic focus:outline-none focus:ring-0;
}
.data-form {
  @apply flex w-full flex-col md:flex-row gap-x-0 gap-y-2 p-2 md:p-4 mt-4 md:gap-x-4 rounded-lg;
}

.btn-cancel {
  @apply py-1 px-5 bg-orange-500 text-white text-sm font-semibold rounded-full shadow-md hover:bg-orange-700
  focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75;
}
.btn-remove {
  @apply py-1 px-5 bg-red-700 text-white  text-sm font-semibold rounded-full shadow-md hover:bg-red-800
  disabled:invisible
  focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-opacity-75;
}
.btn-primary {
  @apply py-1 px-5 bg-blue-500 text-white text-sm font-semibold rounded-full shadow-md hover:bg-blue-700
  focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75
  disabled:text-gray-600 disabled:bg-gray-200;
}

</style>
