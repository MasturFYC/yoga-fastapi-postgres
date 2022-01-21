<template>
  <div class="fyc-row" @keydown.enter.prevent="gotoNextCell" ref="root">
    
    <div class="fyc-cell">
      {{ detailId }}
    </div>

    <div class="fyc-cell">
      <v-dropdown
        :options="products"
        :selectedId="productId"
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
        :options="units"
        :selectedId="unitId"
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
</template>

<script>
import { toRefs, onBeforeUpdate, reactive, ref, computed } from "vue";

//import axios from "axios";
import Dropdown from "@/components/DropdownNonBorder.vue";
//import { state as detailData } from "./directive";


Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};

const formatNumber = (v) => {
  return Intl.NumberFormat("id-ID").format(v);
}


export default {
  name: "StockDetailForm",
  props: {
    products: {
      type: Object,
      require: true,
      default: [],
    },
    detail: {
      type: Object,
      require: true,
      default: {},
    },
  },
  components: {
    "v-dropdown": Dropdown,
  },

  setup(props, { emit }) {
    // const state = detailData;
    // state.data = {...props.detail};
    const root = ref(null);
    const getRef = () => root.value;
    
    const state = reactive({
      productUnits: [],
      cell: 0,
      cells: ref([]),
      dirty: false,

      data: { ...props.detail },

      detailId: computed({
        get() {
          return state.data.id;
        },
        set(v) {
          state.data.id = v;
        },
      }),

      productId: computed({
        get() {
          return state.data.product_id;
        },
        set(v) {
          if(v !== state.data.product_id) {
            state.data.product_id = v;
            state.isDirty = true;
          }
        },
      }),

      unitId: computed({
        get() {
          return state.data.unit_id;
        },
        set(v) {
          if(v !== state.data.unit_id) {
            state.data.unit_id = v;
            state.isDirty = true;
          }
        },
      }),

      name: computed({
        get() {
          return state.data.name;
        },
        set(v) {
          state.data.name = v;
        },
      }),

      unitName: computed({
        get() {
          return state.data.unit_name;
        },
        set(v) {
          state.data.unit_name = v;
        },
      }),

      qty: computed({
        get() {
          return state.data.qty;
        },
        set(v) {
          if (state.data.qty !== v) {
            state.data.qty = v;
            state.data.subtotal = (state.data.price - state.data.discount) * v;
            state.isDirty = true;
          }
        },
      }),


      content: computed({
        get() {
          return state.data.content;
        },
        set(v) {
          if (state.data.content !== v) {
            state.data.content = v;
          }
        },
      }),      

      price: computed({
        get() {
          return formatNumber(state.data.price);
        },
        set(v) {
          if (state.data.price !== v) {
            state.data.price = v;
            state.data.subtotal = (v - state.data.discount) * state.data.qty;
          }
        },
      }),

      discount: computed({
        get() {
          return state.data.discount;
        },
        set(v) {
          if (state.data.discount !== v) {
            state.data.discount = v;
            state.data.subtotal = (state.data.price - v) * state.data.qty;
            state.isDirty = true;
          }
        },
      }),

      subtotal: computed({
        get() {
          return formatNumber(state.data.subtotal);
        },
      }),

      isDirty: computed({
        get() {
          return state.dirty;
        },
        set(v) {
          state.dirty = v;
        },
      }),

      products: computed({
        get() {return props.products}
      }),

      units: computed({
        get() {
          const i = state.products.indexOfObject("id", state.productId)
          
          if(i >= 0) {
            const res =  state.products[i];
            if(res) {
              return res.units
            }
          }
          return [];
        }
      }),

      inputNumber: computed({
        get() {
          return {
            decimal: ",",
            separator: ".",
            suffix: "",
            precision: 2,
            masked: false,
          };
        },
      }),
    });

    const gotoNextCell = () => {
      const shouldUpdate = state.cell === 3;
      const shouldInsert = state.data.id === 0;
      state.cell = state.cell === 3 ? 0 : state.cell + 1;
      // console.log(`index-${state.cell}`,state.cells[state.cell])
      // if(state.cell === 1) state.cells['qty'].focus();

      if (shouldUpdate) {
        
        if(state.isDirty) {

          setTimeout(()=> {
          if (state.data.id === 0) {        
            emit("insert", state.data);
          } else {
            emit("update", state.data, state.data.id);
          }}, 1);

          if(shouldInsert) {
            emit("add");
        };

        state.isDirty = false;
        } else {
          emit("next",state.data.id);
        }
      
     } else {
        state.cells[state.cell].focus();
     }

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
      state.content = e.content;
      state.unitName = e.name;
      state.price = e.price;
    };

    onBeforeUpdate(() => {
      state.cells.value = [];
    });
  

    return {
      //...toRefs(state),
      ...toRefs(state),
      gotoNextCell,
      root,
      getRef,
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

.fyc-cell {
  @apply align-middle border-b;
}
.fyc-cell:first-child {
  @apply md:pl-2;
}
.fyc-cell:last-child {
  @apply md:pr-2;
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
</style>
