<template>
  <div
    class="fyc-row"
    @keydown.enter.prevent="gotoNextCell"
    @keydown.esc.prevent="restoreData"
    ref="root"
    :id="'id-' + detailId"
  >
    <div class="fyc-cell">
      <span class="text-gray-500">{{ detailId }}</span>
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
        :key="productId"
      >
      <template v-slot:default="{option: {name, spec}}">
        <span class="block w-full py-1 px-2 text-gray-700 hover:text-gray-100">{{name}}{{spec ? ', ' + spec : ''}}</span>
      </template>
      </v-dropdown>
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

    <div class="fyc-cell w-full md:w-20">
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
        :key="unitId"
      >
      <template v-slot:default="{option: {name, price}}">
        <span class="block w-full py-1 px-2 text-gray-700 hover:text-gray-100">{{name}} {{ FormatNumber(price) }}</span>
      </template>
      </v-dropdown>
    </div>

    <div class="fyc-cell text-right"><span class="px-1 text-gray-500">{{ price }}</span></div>

    <div class="fyc-cell text-right">
      <number
        class="my-input text-left md:text-right"
        v-model.lazy="discount"
        :options="inputNumber"
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

    <div class="fyc-cell text-right">
      <div
        class="px-1 font-bold text-gray-500"
        tabindex="0"
        @focus="setCurrentCell(4)"
        :class="{'text-red-700':subtotal<0}"
        :ref="
          (el) => {
            if (el) cells[4] = el;
          }
        "
      >
        {{ subtotal }}
      </div>
    </div>
    <div class="fyc-cell text-center" :class="{ 'bg-red-100 text-white': isDirty }">
      <div class="flex flex-row gap-x-2 self-center">
        <button
          type="button"
          :disabled="!isDirty"
          class="flex-1 flex btn border rounded-sm hover:bg-gray-200"
          :class="{ 'disabled hover:bg-transparent': !isDirty }"
          @click="saveDetail"
          ref="saveButton"
        >
          <tw-icon
            name="mdi:check"
            class="flex-1 icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
            :class="{ 'text-green-700': isDirty }"
          />
        </button>
        <button
          type="button"
          :disabled="!isDirty && detailId !== 0"
          class="flex-1 flex btn border rounded-sm hover:bg-gray-200"
          :class="{
            'disabled hover:bg-transparent': !isDirty,
            hidden: !isDirty && detailId === 0,
          }"
          @click.prevent.stop="restoreData"
        >
          <tw-icon
            name="mdi-light:cancel"
            class="flex-1 icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
            :class="{ 'text-orange-700': isDirty || detailId === 0 }"
          />
        </button>
        <button
          class="flex-1 flex btn border rounded-sm hover:bg-gray-200"
          :class="{ hidden: detailId === 0 }"
          type="button"
          tabindex="-1"
          :disabled="detailId === 0"
          @click.prevent.stop="removeDetail"
        >
          <tw-icon
            name="mdi-light:delete"
            class="flex-1 icon w-5 h-5 text-gray-400 group-hover:text-gray-500"
            :class="{ 'text-red-700': detailId > 0 }"
          />
        </button>
      </div>
    </div>
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
};

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
    const saveButton = ref(null);
    const root = ref(null);
    const getRef = () => root.value;

    const state = reactive({
      oldData: { ...props.detail },
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
          if (v !== state.data.product_id) {
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
          if (v !== state.data.unit_id) {
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
            const {price, discount} = state.data
            state.data.subtotal = (price - discount) * v;
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
            const {qty, discount} = state.data
            state.data.subtotal = (v - discount) * qty;
          }
        },
      }),

      discount: computed({
        get() {
          return state.data.discount;
        },
        set(v) {
          if (state.data.discount !== v) {
            state.isDirty = true;
            state.data.discount = v;
            const {qty, price} = state.data
            state.data.subtotal = (price - v) * qty;
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
          if (state.dirty !== v) {
            state.dirty = v;
          }
        },
      }),

      products: computed({
        get() {
          return props.products;
        },
      }),

      units: computed({
        get() {
          const i = state.products.indexOfObject("id", state.productId);

          if (i >= 0) {
            const res = state.products[i];
            if (res) {
              return res.units;
            }
          }
          return [];
        },
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
      const shouldUpdate = state.cell === 5;
      const shouldInsert = state.data.id === 0;
      state.cell = state.cell === 5 ? 0 : state.cell + 1;
      // console.log(`index-${state.cell}`,state.cells[state.cell])
      // if(state.cell === 1) state.cells['qty'].focus();

      if (shouldUpdate) {
        if (state.isDirty) {
          if (state.data.id === 0) {
            emit("insert", state.data, (x) => {
              state.isDirty = !x;
              if (x) {
                state.oldData = { ...state.data };
                setTimeout(() => {
                  emit("add");
                }, 1);
              }
            });
          } else {
            emit("update", state.data, state.data.id, (x) => {
              state.isDirty = !x;
              if (x && shouldInsert) {
                state.oldData = { ...state.data };
                setTimeout(() => {
                  emit("add");
                }, 1);
              } else {
                emit("next", state.data.id);
              }
            });
          }
        } else emit("next", state.data.id);
      } else {
        if (state.cell === 5) {
          if (state.isDirty) {
            saveButton.value.click(); //.focus();
          }
          emit("next", state.data.id);
        } else {
          const el = state.cells[state.cell];
          el.focus();
          if (el.type === "text") {
            el.setSelectionRange(0, el.value.length);
          }
        }
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
      const {id, name} = e;
      state.productId = id;
      state.name = name;
      const unit = state.units.filter((c) => c.is_default)[0] || state.units[0];
      if (unit) {
        state.unitId = unit.id;
        state.price = unit.price;
      }
    };

    const validateUnit = (e) => {
      const {id, content, name, price} = e;
      state.unitId = id;
      state.content = content;
      state.unitName = name;
      state.price = price;
    };

    onBeforeUpdate(() => {
      state.cells.value = [];
    });

    const removeDetail = () => {
      emit("remove", state.detailId);
    };

    const restoreData = () => {
      state.data = { ...state.oldData };
      state.isDirty = false;
    };

    const saveDetail = () => {
      if (state.data.id === 0) {
        emit("insert", state.data, (x) => {
          state.isDirty = !x;
          if (x) {
            state.oldData = { ...state.data };
            setTimeout(() => {
              emit("add");
            }, 1);
          }
        });
      } else {
        emit("update", state.data, state.data.id, (x) => {
          state.isDirty = !x;
          if (x) {
            state.oldData = { ...state.data };
          }
        });
      }
    };

    const FormatNumber = (x) => {
      return formatNumber(x)
    }

    return {
      //...toRefs(state),
      ...toRefs(state),
      gotoNextCell,
      root,
      saveButton,
      getRef,
      //      gotoPrevCell,
      setCurrentCell,
      validateName,
      validateUnit,
      restoreData,
      saveDetail,
      removeDetail,
      FormatNumber
    };
  },
};
</script>

<style scoped>
.v-number {
  @apply w-full py-0.5 rounded-sm outline-none border border-transparent bg-transparent px-1
  focus:bg-white focus:outline-none focus:border-emerald-400;
}

.fyc-cell {
  @apply align-middle border-b;
}
.fyc-cell:first-child {
  @apply md:pl-2 border-l-0;
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
  @apply table-cell py-0 px-4 text-base md:text-sm md:px-1 md:py-1
  border-0 md:border-l border-b border-gray-300;
}
</style>
