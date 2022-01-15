<template>
  <div>
    <h1>Customer</h1>
    <div class="message">
      Secara umum, arti customer adalah seseorang atau organisasi yang membeli suatu
      barang atau jasa dari sebuah toko atau bisnis tertentu. Pendapat lain mengatakan
      pengertian customer adalah pelanggan, yaitu individu, rumah tangga, atau perusahaan,
      yang membeli suatu produk, baik itu ide, barang, atau jasa, dari penjual atau
      pemasok tertentu.
    </div>
    <div class="message">
      Dalam hal ini, customer tidak selalu berarti konsumen karena bisa saja pelanggan
      tersebut membeli suatu produk bukan untuk digunakan sendiri tapi untuk dijual atau
      diberikan kepada orang lain.
    </div>
    <div class="mt-4">
      <hr />
      <div v-for="(customer, index) in customers" v-bind:key="customer.id">
        <transition name="slide-fade">
          <template
            v-if="selectedIndex === index && selectedId === customer.id"
            class="customer-list"
          >
            <customer-form :customerProp="customer" @update="updateCustomer">
              <button type="button" class="btn-cancel rounded-md" @click="cancelForm()">
                Cancel
              </button>
              <span class="flex-1"></span>
              <button
                @click="removeCustomer()"
                type="button"
                class="btn-remove"
                :disabled="customer.id === 0"
              >
                Delete
              </button>
            </customer-form>
          </template>
          <template v-else class="customer-list">
            <a
              href="#"
              v-if="customer.id === 0"
              @click.prevent="supClick(index, customer.id)"
              class="span-link"
            >
              +
            </a>
            <div v-else class="customer-item" href="#">
              <div class="flex-none w-full md:w-2/5">
                <a
                  href="#"
                  @click.prevent="supClick(index, customer.id)"
                  class="span-link"
                >
                  {{ customer.name }}
                </a>
              </div>
              <div class="flex-1 w-full text-sm mt-2 md:mt-0">
                <div>{{ customer.street }} - {{ customer.city }}, {{ customer.zip }}</div>
                <div>Telp. {{ customer.phone }} / {{ customer.cell }}</div>
                <div>{{ customer.email }}</div>
              </div>
            </div>
          </template>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { shallowRef } from "vue";
import axios from "axios";
import TwButton from "@/components/TwButton.vue";
import CustomerForm from "@/components/forms/CustomerForm.vue";

Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};

const new_customer = {
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
  name: "Customer",
  data() {
    return {
      customers: [{ ...new_customer }],
      selectedIndex: -1,
      selectedId: -1,
    };
  },
  components: {
    "tw-button": shallowRef(TwButton),
    "customer-form": CustomerForm,
  },
  methods: {
    cancelForm() {
      const self = this;
      self.selectedId = -1;
      self.selectedIndex = -1;
    },
    async removeCustomer() {
      const self = this;
      const options = {
        "Content-Type": "application/json",
      };
      await axios
        .delete(`/api/customers/${self.selectedId}`, {
          headers: options,
        })
        .then((res) => {
          if (res.status === 200) {
            const index = self.customers.indexOfObject("id", self.selectedId);
            self.customers.splice(index, 1);
            self.cancelForm();
          }
        });
    },
    supClick(index, catId) {
      const self = this;
      self.selectedId = catId;
      self.selectedIndex = index;
    },
    updateCustomer(customer, id) {
      const self = this;
      let temp = self.customers;
      const index = self.customers.indexOfObject("id", id);
      temp[index] = customer;
      self.customers = temp;
      if (id === 0) {
        self.customers.push(new_customer);
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
    await axios.get("/api/customers/", { headers: options }).then((res) => {
      const json = res.data;
      self.customers = [...json, new_customer];
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

.customer-list {
  @apply py-4 border-b border-emerald-200;
}
.customer-item {
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
