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
          <input class="control" type="date" v-model.lazy="createdAt" />
        </label>
        <label class="label-group">
          <span class="label-title">Supplier</span>
          <v-dropdown
            :options="suppliers"
            v-on:selected="validateSelection"
            :disabled="false"
            name="zipcode"
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
  </form>
</template>

<script>
import { computed, toRefs, reactive, onMounted } from "vue";
import Dropdown from "@/components/FycDropdown.vue";
import axios from "axios";

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

  setup(props) {
    const formSubmit = (e) => {
      e.preventDefault();
    };

    const loadSupplier = async () => {
      const options = {
        accept: "application/json",
        "Content-Type": "application/json",
      };
      await axios.get("/api/categories/", { headers: options }).then((res) => {
        const json = res.data;
        console.log(json);
        event.supplierList = json;
      });
    };

    const validateSelection = (e) => {
      console.log(e);
    };

    const event = reactive({
      stock: props.stockProp,
      supplierList: [],

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
          }
        },
      }),

      total: computed({
        get() {
          return event.stock.total;
        },
        set(value) {
          if (value !== event.stock.total) {
            event.stock.total = value;
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
          }
        },
      }),

      createdAt: computed({
        get() {
          return event.stock.created_at;
        },
        set(value) {
          if (value !== event.stock.created_at) {
            event.stock.created_at = value;
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

    onMounted(async () => {
      await loadSupplier();
    });

    return {
      ...toRefs(event),
      formSubmit,
      validateSelection,
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
  @apply flex w-full flex-col md:flex-row gap-x-0 gap-y-2 p-2 md:p-4 mt-4 md:gap-x-4;
}
</style>
