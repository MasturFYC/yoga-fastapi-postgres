import{_ as u}from"./TwCodePreviewEditor.5eb34a4b.js";import{R as d,e as i,k as s,j as t,Q as o,o as r}from"./vendor.d21eb4bc.js";import{T as a}from"./TwButton.6252f860.js";import{_ as c}from"./index.38b9c37f.js";import"./TwIcon.2bacb9f2.js";import"./index.6515b6d2.js";var b=`<div>
  <tw-button>Default</tw-button>
  <tw-button type="primary">Primary</tw-button>
  <tw-button type="success">Success</tw-button>
  <tw-button type="warning">Warning</tw-button>
  <tw-button type="danger">Danger</tw-button>
</div>
<div class="mt-3">
  <tw-button round>Default</tw-button>
  <tw-button type="primary" round>Primary</tw-button>
  <tw-button type="success" round>Success</tw-button>
  <tw-button type="warning" round>Warning</tw-button>
  <tw-button type="danger" round>Danger</tw-button>
</div>`,l=`<div>
  <tw-button size="lg">Large</tw-button>
  <tw-button size="md">Medium</tw-button>
  <tw-button size="sm">Small</tw-button>
</div>
<div class="mt-3">
  <tw-button size="lg" round>Large</tw-button>
  <tw-button size="md" round>Medium</tw-button>
  <tw-button size="sm" round>Small</tw-button>
</div>`,w=`<div>
  <tw-button disabled>Default</tw-button>
  <tw-button type="primary" disabled>Primary</tw-button>
  <tw-button type="success" disabled>Success</tw-button>
  <tw-button type="warning" disabled>Warning</tw-button>
  <tw-button type="danger" disabled>Danger</tw-button>
</div>
<div class="mt-3">
  <tw-button round disabled>Default</tw-button>
  <tw-button type="primary" round disabled>Primary</tw-button>
  <tw-button type="success" round disabled>Success</tw-button>
  <tw-button type="warning" round disabled>Warning</tw-button>
  <tw-button type="danger" round disabled>Danger</tw-button>
</div>`;const m={name:"ButtonExample",data(){return{components:{"tw-button":d(a)},codeBasicUsage:b,codeSizes:l,codeDisabled:w}}},p={class:"page-example"},_=t("h1",null,"Button",-1),g=t("p",null,"Commonly used button.",-1),y=t("h2",{class:"mt-8"},"Basic usage",-1),v=t("h2",{class:"mt-8"},"Sizes",-1),f=t("p",null,[o("Button component provides three sizes, large "),t("code",null,"lg"),o(", medium "),t("code",null,"md"),o(" and small "),t("code",null,"sm"),o(". Medium is the default size.")],-1),h=t("h2",{class:"mt-8"},"Disabled",-1),B=t("p",null,[o("The "),t("code",null,"disabled"),o(" attribute determines if the button is disabled.")],-1);function z(D,S,x,j,e,T){const n=u;return r(),i("div",p,[_,g,y,s(n,{source:e.codeBasicUsage,components:e.components},null,8,["source","components"]),v,f,s(n,{source:e.codeSizes,components:e.components},null,8,["source","components"]),h,B,s(n,{source:e.codeDisabled,components:e.components},null,8,["source","components"])])}var U=c(m,[["render",z]]);export{U as default};
