import { createApp  } from 'vue';
//import { createI18n } from 'vue-i18n';
import App from './App.vue'
import router from '@/router'
import VueSelect from 'vue-next-select';
import Cleave from 'vue-cleave-component';
import '@/styles/app.css'
import '@/styles/page-example-common-style.css'
import 'vue-next-select/dist/index.min.css';

import '@purge-icons/generated'


const app = createApp(App);
// app.use(
//   createI18n({
//     locale: 'id-ID',
//     messages,
//   })
// );
app.use(router);
app.component('v-select', VueSelect);
app.component('v-number', Cleave);
app.mount('#app')
