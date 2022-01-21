/* eslint-disable prefer-object-spread */
import { reactive, ref, computed } from 'vue';

const CONFIG_KEY = '__STOCK-DETAIL-FORM__';

// export default {
//     mounted: (el) => {

//     }
// }
const formatNumber = (v) => {
  return Intl.NumberFormat("id-ID").format(v);
}

export const stateData = {
  id: 0,
  qty: 1,
  discount: 0,
  product_id: 0,
  content: 0,
  unit_id: 0,
  stock_id: 0,
  name: '',
  unit_name: '',
  price: 0,
  subtotal: 0,
};

// export const state = reactive({
//   data: { ...stateData },

//   detailId: computed({
//     get() {
//       return state.data.id;
//     },
//   }),

//   productId: computed({
//     get() {
//       return state.data.productId;
//     },
//     set(v) {
//       state.data.productId = v;
//     },
//   }),

//   unitId: computed({
//     get() {
//       return state.data.unitId;
//     },
//     set(v) {
//       state.data.unitId = v;
//     },
//   }),

//   name: computed({
//     get() {
//       return state.data.name;
//     },
//     set(v) {
//       state.data.name = v;
//     },
//   }),

//   unitName: computed({
//     get() {
//       return state.data.unitName;
//     },
//     set(v) {
//       state.data.unitName = v;
//     },
//   }),

//   qty: computed({
//     get() {
//       return state.data.qty;
//     },
//     set(v) {
//       if (state.data.qty !== v) {
//         state.data.qty = v;
//         state.data.subtotal = (state.data.price - state.data.discount) * v;
//       }
//     },
//   }),

//   price: computed({
//     get() {
//       return formatNumber(state.data.price);
//     },
//     set(v) {
//       if (state.data.price !== v) {
//         state.data.price = v;
//         state.data.subtotal = (v - state.data.discount) * state.data.qty;
//       }
//     },
//   }),

//   discount: computed({
//     get() {
//       return state.data.discount;
//     },
//     set(v) {
//       if (state.data.discount !== v) {
//         state.data.discount = v;
//         state.data.subtotal = (state.data.price - v) * state.data.qty;
//       }
//     },
//   }),

//   subtotal: computed({
//     get() {
//       return formatNumber(state.data.subtotal);
//     },
//   }),

// });
