<template>
  <div class="dropdown" v-if="options">
    <!-- Dropdown Input -->
    <input
      class="dropdown-input"
      :class="{ 'dropdown-focus': optionsShown, 'dropdown-lost-focus': !optionsShown }"
      autocomplete="nope"
      :name="name"
      @focus="showOptions()"
      @blur="exit()"
      @click="showOptions()"
      @keyup.prevent="keyMonitor"
      @keydown.down.prevent.stop="selectedIndex++"
      @keydown.up.prevent.stop="selectedIndex--"
      @keydown.esc.prevent.stop="exit()"
      v-model="searchFilter"
      :disabled="disabled"
      :placeholder="placeholder"
    />
    <!-- Dropdown Menu -->
    <div class="dropdown-content" v-show="optionsShown">
      <div
        class="dropdown-item"
        @mousedown="selectOption(option, index)"
        v-for="(option, index) in filteredOptions"
        :key="index"
        ref="dropItem"
        :class="{ 'bg-emerald-100': selectedIndex === index }"
      >
        {{ option.name || option.id || "-" }}
      </div>
    </div>
  </div>
</template>

<script>
Array.prototype.indexOfObject = function (property, value) {
  for (let i = 0, len = this.length; i < len; i++) {
    if (this[i][property] === value) return i;
  }
  return -1;
};

export default {
  name: "Dropdown",
  template: "Dropdown",
  props: {
    selectedId: {
      type: Number,
      default: 0,
      required: true
    },
    name: {
      type: String,
      required: false,
      default: "dropdown",
      note: "Input name",
    },
    options: {
      type: Array,
      required: true,
      default: [],
      note: "Options of dropdown. An array of options with id and name",
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
      note: "Disable the dropdown",
    },
    maxItem: {
      type: Number,
      required: false,
      default: 6,
      note: "Max items showing",
    },
  },
  data() {
    return {
      selected: {},
      optionsShown: false,
      searchFilter: "",
      selIndex: 0,
    };
  },
  created() {
    if(this.selectedId > 0) this.selected = this.options[this.options.indexOfObject("id", this.selectedId)] || {};
  },
  computed: {
    selectedIndex: {
      get() {
        return this.selIndex;
      },
      set(value) {
        const length = this.filteredOptions ? this.filteredOptions.length - 1 : 0;
        const selMax = length > this.maxItem ? this.maxItem : length;
        this.selIndex = value === -1 ? 0 : value > selMax ? selMax : value;
      },
    },
    placeholder() {
      return this.selected.id ? this.selected.name : "Select one " + this.name;
    },
    filteredOptions() {
      const filtered = [];
      const regOption = new RegExp(this.searchFilter, "ig");
      for (const option of this.options) {
        if (this.searchFilter.length < 1 || option.name.match(regOption)) {
          if (filtered.length < this.maxItem) {
            filtered.push(option);
            this.selectedIndex = 0;
          }
        }
      }
      return filtered;
    },
  },
  methods: {
    selectOption(option, index) {
      this.selected = option;
      this.selectedIndex = index;
      this.optionsShown = false;
      this.searchFilter = this.selected.name;
      this.$emit("selected", this.selected);
    },
    showOptions() {
      if (!this.disabled) {
        this.searchFilter = "";
        this.optionsShown = true;
        this.selectedIndex = this.selected.id
          ? this.options.indexOfObject("id", this.selected.id)
          : 0;
      }
    },
    exit() {
      if (!this.selected.id) {
        this.selected = {};
        this.searchFilter = "";
      } else {
        this.searchFilter = this.selected.name;
      }
      // this.$emit("selected", this.selected);
      this.optionsShown = false;
    },
    // Selecting when pressing Enter
    keyMonitor: function (event) {
      //console.log(event.key);
      if ((event.key === "Enter" || event.key === "Escape") && this.filteredOptions[0]) {
        this.selectOption(this.filteredOptions[this.selIndex], 0);
        //this.selIndex = 0;
      } else this.optionsShown = true;
    },
  },
  //   watch: {
  //     searchFilter() {
  //       if (this.filteredOptions.length === 0) {
  //         this.selected = {};
  //       } else {
  //         this.selected = this.filteredOptions[0];
  //       }
  //       this.$emit("filter", this.searchFilter);
  //     },
  //   },
};
</script>

<style lscoped>
.dropdown {
  @apply relative inline-block min-h-[29px] w-full ml-[-2px];
}
.dropdown-focus {
  @apply border rounded-t-[6px] border-2 border-b-0 outline-none drop-shadow-xl
  ring-inset ring-0;
}
.dropdown-input {
  @apply text-[14px] placeholder:italic 
  border-emerald-500 py-0.5 px-2 flex-initial w-full self-start text-gray-700 z-[999];
}

.dropdown-lost-focus {
  @apply border outline-none border-emerald-500 rounded-[6px];
}
.dropdown-content {
  @apply absolute bg-white w-full flex flex-col rounded-b-[6px] drop-shadow-xl
 border-2 border-emerald-500 border-t-0 shadow overflow-auto z-[1000];
}
.dropdown-item {
  @apply text-gray-700 text-sm py-1 px-2 block cursor-pointer 
  hover:bg-emerald-700 hover:text-gray-100;
}
</style>
