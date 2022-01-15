<template>
  <div>
    <h1>Sales</h1>
    <div class="message">
      Sales atau salesman atau salesmanship adalah orang dengan sebuah profesi dimana seseorang
      yang kerjanya berkeliling ke rumah-rumah, sok ramah tamah dan berniat menjual produknya ke
      konsumen dengan cara menghasut konsumen agar tertarik dan membeli produknya.
    </div>
    <div class="message">
        Konotasinya seperti buruk banget.. tapi Satu-satunya divisi yang menghasilkan Uang,
        dalam arti kata sebenarnya, adalah divisi sales. Divisi yang lain bisa menghemat biaya,
        tetapi tetap tidak bisa menciptakan aliran dana masuk. Fokus pada divisi <b>SALES</b>, dapat 
        memberikan pemasukan yang berkesinambungan bagi perusahaan Anda.
    </div>
    <div class="mt-4">
    <hr />
      <div v-for="(sales, index) in salesmans" v-bind:key="sales.id">
        <transition name="slide-fade">
          <div
            v-if="selectedIndex === index && selectedId === sales.id"
            class="sales-list"
          >
            <sales-form :salesProp="sales" @update="updateSales">
              <button
                type="button"
                class="btn-cancel rounded-md"
                @click="cancelForm()"
              >
                Cancel
              </button>
              <span class="flex-1"></span>
              <button @click="removeSales()" type="button" class="btn-remove" :disabled="sales.id === 0">
                Delete
              </button>
            </sales-form>
          </div>
          <div v-else class="sales-list">
            <div
              v-if="sales.id === 0"
              @click="supClick(index, sales.id)"
              class="span-link"
            >
              +
            </div>
            <div v-else class="sales-item">
              <div class="flex-none w-full md:w-2/5">
                <div @click="supClick(index, sales.id)" class="span-link">
                  {{ sales.name }}
                </div>
              </div>
              <div class="flex-1 w-full text-sm mt-2 md:mt-0">
                <div>{{ sales.street }} - {{ sales.city }}, {{ sales.zip }}</div>
                <div>Telp. {{ sales.phone }} / {{ sales.cell }}</div>
                <div>{{ sales.email }}</div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";
import SalesForm from "@/components/forms/SalesForm.vue";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
}

const new_sales = {
  id: 0,
  name: "",
  street: "",
  city: "",
  phone: "",
  cell: "",
  zip: "",
  email: "",
};

export default {
  name: "Sales",
  data() {
    return {
      salesmans: [{...new_sales}],
      selectedIndex: -1,
      selectedId: -1,
    };
  },
  components: {
    "tw-button": shallowRef(TwButton),
    "sales-form": SalesForm,
  },
  methods: {
    cancelForm() {
      const self = this;
      self.selectedId = -1;
      self.selectedIndex = -1;
    },
    async removeSales() {
      const self = this;
      const options = {
        "Content-Type": "application/json",
      };
      await axios
        .delete(`/api/salesmans/${self.selectedId}`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            const index = self.salesmans.indexOfObject("id", self.selectedId);
            self.salesmans.splice(index, 1);
            self.cancelForm();
          }
        });
    },
    supClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    updateSales(sales, id) {
      const self = this;
      let temp = self.salesmans;
      const index = self.salesmans.indexOfObject("id", id);
      temp[index] = sales;
      self.salesmans = temp;
      if (id === 0) {
        self.salesmans.push(new_sales);
      }
      self.cancelForm();
    },
  },
  async mounted() {
    const self = this;
    const options = {
      //      accept: "application/json",
      "Content-Type": "application/json",
    };
    await axios
      .get("/api/salesmans/", { headers: options })
      .then((res) => {
        const json = res.data;
        self.salesmans = [...json, new_sales];
      });
  },
  directives: {
    focus: {
      mounted(el) {
        // When the bound element is inserted into the DOM...
        setTimeout(() => {
          el.focus(); // Focus the element
          // el.select();
        }, 100);
      },
    },
  },
};
</script>

<style scoped>
.svg-icon {
  enable-background: new 0 0 64 64;
  display: inline;
  fill: #ff0000;
  /* margin-left: 12px; */
}
.span-link {
  @apply inline-block cursor-pointer font-bold text-emerald-400 hover:underline hover:text-emerald-700 hover:underline-offset-4;
}
h1 {
  font-weight: 700;
  font-size: 24px;
}

.sales-list {
  @apply py-4 border-b border-emerald-200;
}
.sales-item {
  @apply flex flex-col mt-1
  md:flex-row;
}

.message {
  margin-top: 12px;
  font-size: small;
}
.btn-cancel {
  @apply py-1 px-5 bg-orange-500 text-white font-semibold rounded-full shadow-md hover:bg-orange-700
  focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-75;
}
.btn-remove {
  @apply py-1 px-5 bg-red-700 text-white font-semibold rounded-full shadow-md hover:bg-red-800
  disabled:invisible
  focus:outline-none focus:ring-2 focus:ring-red-700 focus:ring-opacity-75;
}
.slide-fade-enter-active {
  transition: all 0.1s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(50px);
  opacity: 0;
}
</style>