import{_ as d}from"./TwCodePreviewEditor.5eb34a4b.js";import{g as u,f as m,o as n,e as a,n as w,Q as _,t as b,l as f,m as h,q as v,s as g,j as y,R as p,k as x,P as T}from"./vendor.d21eb4bc.js";import{_ as c}from"./index.38b9c37f.js";import{T as B}from"./TwButton.6252f860.js";import"./TwIcon.2bacb9f2.js";import"./index.6515b6d2.js";var S=`<tw-tooltip text="Awesome, you did it!">
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
</tw-tooltip>`;const j={name:"TwTooltip",props:{text:{type:String,required:!0},position:{type:String,default:"top",validator(t){return["top","bottom","left","right"].includes(t)}}},setup(t){const o=u(!1),s=m(()=>"position-"+t.position);return{show:o,position:s}}},$=t=>(v("data-v-74029bb2"),t=t(),g(),t),V=$(()=>y("span",{class:"absolute w-0 h-0 border-gray-800 border-opacity-95 arrow"},null,-1));function k(t,o,s,e,r,l){return n(),a("div",{class:"relative inline-block",onMouseover:o[0]||(o[0]=i=>e.show=!0),onMouseleave:o[1]||(o[1]=i=>e.show=!1)},[e.show?(n(),a("div",{key:0,class:w(["absolute z-40 bg-gray-800 bg-opacity-95 px-4 py-1 rounded-md text-xs text-white whitespace-nowrap transform",e.position])},[V,_(" "+b(s.text),1)],2)):f("",!0),h(t.$slots,"default",{},void 0,!0)],32)}var I=c(j,[["render",k],["__scopeId","data-v-74029bb2"]]);const N={name:"TooltipExample",data(){return{components:{"tw-tooltip":p(I),"tw-button":p(B)},codeBasicUsage:S}}},C={class:"page-example"},E=T('<h1>Tooltip</h1><p>Display prompt information for mouse hover.</p><h2 class="mt-8">Basic usage</h2><p>Hover to show the tooltip. Choose the best position for your needs, either <code>top</code>, <code>bottom</code>, <code>right</code> or <code>left</code>.</p>',4);function R(t,o,s,e,r,l){const i=d;return n(),a("div",C,[E,x(i,{source:r.codeBasicUsage,components:r.components},null,8,["source","components"])])}var P=c(N,[["render",R]]);export{P as default};
