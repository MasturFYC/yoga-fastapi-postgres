<template>
  <input
    type="text"
    autocomplete="off"
    :value="maskedValue"
    @change="change"
    @input="input"
    v-number="config"
    class="v-number"
    :name="name"
    v-bind="$attrs"
    ref="root"
  />
</template>

<script>
import { ref } from "vue";

import directive from './directive'
import options from './options'

export default {
  name: "number",
  inheritAttrs: false,
  props: {
    modelValue: {
      required: true
    },
    name: {
      type: String,
      required: false,
      default: "number",
      note: "Input name",
    },
    nullValue: {
      type: [Number, String],
      default: () => options.nullValue
    },
    masked: {
      type: Boolean,
      default: false
    },
    reverseFill: {
      type: Boolean,
      default: options.reverseFill
    },
    precision: {
      type: Number,
      default: () => options.precision
    },
    minimumFractionDigits: {
      type: [Number, Boolean],
      default: () => options.minimumFractionDigits
    },
    decimal: {
      type: String,
      default: () => options.decimal
    },
    separator: {
      type: String,
      default: () => options.separator
    },
    prefix: {
      type: String,
      default: () => options.prefix
    },
    suffix: {
      type: String,
      default: () => options.suffix
    }
  },
  directives: {
    number: directive
  },
  emits: ['update:modelValue'],
  data() {
    return {
      maskedValue: this.modelValue,
      unmaskedValue: null
    }
  },
  methods: {
    input({ target }) {
      this.maskedValue = target.value
      this.unmaskedValue = target.unmaskedValue
    },
    change() {
      this.$emit('update:modelValue', this.emittedValue)
    }
  },
  computed: {
    emittedValue() {
      return this.masked ? this.maskedValue : this.unmaskedValue
    },
    config() {
      return this.$props
    }
  },
  watch: {
    modelValue (val) {
      if (this.unmaskedValue !== val) {
        this.maskedValue = val
      }
    }
  },
  setup() {
    const root = ref(null);
    const getRef = () => root.value;
    return { root, getRef };
  },
}
</script>
