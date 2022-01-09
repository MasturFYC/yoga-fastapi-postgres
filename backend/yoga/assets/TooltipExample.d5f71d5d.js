import{_ as d}from"./TwCodePreviewEditor.e5be2ab4.js";import{g as u,f as m,o as n,e as a,n as w,N as _,t as f,k as b,l as h,p as v,q as g,i as y,L as p,j as x,P as T}from"./vendor.b08dc4ec.js";import{_ as c}from"./index.86c095c3.js";import{T as B}from"./TwButton.c3ff6f91.js";import"./TwIcon.c7fe7a3e.js";import"./index.01e0c1c7.js";var S=`<tw-tooltip text="Awesome, you did it!">
  <tw-button type="primary">Hover me!</tw-button>
</tw-tooltip>
<tw-tooltip class="ml-2" text="Very beautiful!" position="bottom">
  <tw-button type="success">Bottom</tw-button>
</tw-tooltip>
<tw-tooltip class="ml-2" text="Yes, that's right!" position="right">
  <tw-button type="warning">Right</tw-button>
</tw-tooltip>
<tw-tooltip class="ml-2" text="You must be happy!" position="left">
  <tw-button type="danger">Left</tw-button>
</tw-tooltip>`;const j={name:"TwTooltip",props:{text:{type:String,required:!0},position:{type:String,default:"top",validator(t){return["top","bottom","left","right"].includes(t)}}},setup(t){const o=u(!1),s=m(()=>"position-"+t.position);return{show:o,position:s}}},$=t=>(v("data-v-74029bb2"),t=t(),g(),t),N=$(()=>y("span",{class:"absolute w-0 h-0 border-gray-800 border-opacity-95 arrow"},null,-1));function V(t,o,s,e,i,l){return n(),a("div",{class:"relative inline-block",onMouseover:o[0]||(o[0]=r=>e.show=!0),onMouseleave:o[1]||(o[1]=r=>e.show=!1)},[e.show?(n(),a("div",{key:0,class:w(["absolute z-40 bg-gray-800 bg-opacity-95 px-4 py-1 rounded-md text-xs text-white whitespace-nowrap transform",e.position])},[N,_(" "+f(s.text),1)],2)):b("",!0),h(t.$slots,"default",{},void 0,!0)],32)}var k=c(j,[["render",V],["__scopeId","data-v-74029bb2"]]);const I={name:"TooltipExample",data(){return{components:{"tw-tooltip":p(k),"tw-button":p(B)},codeBasicUsage:S}}},C={class:"page-example"},E=T('<h1>Tooltip</h1><p>Display prompt information for mouse hover.</p><h2 class="mt-8">Basic usage</h2><p>Hover to show the tooltip. Choose the best position for your needs, either <code>top</code>, <code>bottom</code>, <code>right</code> or <code>left</code>.</p>',4);function U(t,o,s,e,i,l){const r=d;return n(),a("div",C,[E,x(r,{source:i.codeBasicUsage,components:i.components},null,8,["source","components"])])}var P=c(I,[["render",U]]);export{P as default};
