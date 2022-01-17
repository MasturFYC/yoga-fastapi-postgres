<template>
  <div>
    <h1 class="text-emerald-700 text-[18px] font-bold">Pembelian #{{ stock.id }}</h1>
    <stock-form
      v-if="stock.id > 0"
      :stockProp="stock"
      @cancelChange="cancelChange"
      @saveChange="saveChange"
      @removeData="removeData"
    ></stock-form>
  </div>
</template>

<script>
import { computed, toRefs, reactive, onMounted } from "vue";
import dayjs from "dayjs";
import axios from "axios";

import StockForm from "@/components/forms/stock/SrockForm.vue";
export default {
  name: "Pembelian",
  components: {
    "stock-form": StockForm,
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

    const event = reactive({
      isEdit: true,
      showForm: computed(() => event.isEdit),
      stock: new_stock,
    });

    function cancelChange() {
      event.isEdit = false;
    }

    const loadStock = async () => {
      await axios
        .get("/api/stocks/3/", {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          //console.log(res.data);
          event.stock = res.data;
        })
        .catch((error) => {
          console.log(error);
        });      
    }
    const insertStock = async (stock) => {


      const data = { ...stock};
      delete data.id;

      await axios
        .post("/api/stocks/", JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          console.log(res.data);
          event.stock = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const updateStock = async (stock, id) => {
      const data = { ...stock};
      delete data.id;

      await axios
        .put(`/api/stocks/${id}`, JSON.stringify(data), {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          console.log(res.data);
          event.stock = res.data;
        });
    };

    async function removeData(id) {
      await axios
        .delete(`/api/stocks/${id}`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            //const index = self.products.indexOfObject("id", self.selectedId);
            //self.products.splice(index, 1);
            //self.cancelForm();
            event.stock = new_stock;
          }
        });
    }

    const saveChange = async (stock) => {
      if (stock.id === 0) {
        await insertStock(stock);
      } else {
        await updateStock(stock, stock.id);
      }
    };

    onMounted(async () => {
      await loadStock();
    });


    return { ...toRefs(event), cancelChange, saveChange, removeData };
  },
};
</script>

<style scoped></style>
