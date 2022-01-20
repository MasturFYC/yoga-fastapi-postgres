import { createApp  } from 'vue';
//import { createI18n } from 'vue-i18n';
import App from './App.vue'
import router from '@/router'
//import VueSelect from 'vue-next-select';
import vSelect from 'vue-select';
//import Cleave from 'vue-cleave-component';
//import VueClickAway from 'vue3-click-away';

import '@/styles/app.css'
import '@/styles/page-example-common-style.css'
// import 'vue-next-select/dist/index.min.css';
import 'vue-select/dist/vue-select.css';

import '@purge-icons/generated'
import vNumber from './components/vue-number-format'


const app = createApp(App);
// app.use(
//   createI18n({
//     locale: 'id-ID',
//     messages,
//   })
// );
app.use(router);
app.component('v-select', vSelect);
app.use(vNumber, {precision: 4});
//app.use(VueClickAway);
app.mount('#app')
