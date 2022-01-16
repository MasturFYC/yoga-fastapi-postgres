<template>
  <h1 class="text-emerald-700 text-[24px] font-bold">Pembelian</h1>
  <stock-form :stockProp="stock"> </stock-form>
</template>

<script>
import { computed, toRefs, reactive } from "vue";

import StockForm from "@/components/forms/stock/SrockForm.vue";
export default {
  name: "Pembelian",
  components: {
    "stock-form": StockForm,
  },
  setup() {
    const event = reactive({
      stock: {
        id: 0,
        invoice_number: "",
        total: 0,
        cash: 0,
        payment: 0,
        remain_payment: 0,
        created_at: new Date(),
        supplier_id: 0,
      },
    });
    return { ...toRefs(event) };
  },
};
</script>

<style scoped></style>
