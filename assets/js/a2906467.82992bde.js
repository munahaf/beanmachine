"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[9048],{3905:function(e,n,r){r.r(n),r.d(n,{MDXContext:function(){return l},MDXProvider:function(){return u},mdx:function(){return h},useMDXComponents:function(){return f},withMDXComponents:function(){return m}});var t=r(67294);function o(e,n,r){return n in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var r=arguments[n];for(var t in r)Object.prototype.hasOwnProperty.call(r,t)&&(e[t]=r[t])}return e},i.apply(this,arguments)}function a(e,n){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);n&&(t=t.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),r.push.apply(r,t)}return r}function c(e){for(var n=1;n<arguments.length;n++){var r=null!=arguments[n]?arguments[n]:{};n%2?a(Object(r),!0).forEach((function(n){o(e,n,r[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(r,n))}))}return e}function s(e,n){if(null==e)return{};var r,t,o=function(e,n){if(null==e)return{};var r,t,o={},i=Object.keys(e);for(t=0;t<i.length;t++)r=i[t],n.indexOf(r)>=0||(o[r]=e[r]);return o}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(t=0;t<i.length;t++)r=i[t],n.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var l=t.createContext({}),m=function(e){return function(n){var r=f(n.components);return t.createElement(e,i({},n,{components:r}))}},f=function(e){var n=t.useContext(l),r=n;return e&&(r="function"==typeof e?e(n):c(c({},n),e)),r},u=function(e){var n=f(e.components);return t.createElement(l.Provider,{value:n},e.children)},p={inlineCode:"code",wrapper:function(e){var n=e.children;return t.createElement(t.Fragment,{},n)}},d=t.forwardRef((function(e,n){var r=e.components,o=e.mdxType,i=e.originalType,a=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),m=f(r),u=o,d=m["".concat(a,".").concat(u)]||m[u]||p[u]||i;return r?t.createElement(d,c(c({ref:n},l),{},{components:r})):t.createElement(d,c({ref:n},l))}));function h(e,n){var r=arguments,o=n&&n.mdxType;if("string"==typeof e||o){var i=r.length,a=new Array(i);a[0]=d;var c={};for(var s in n)hasOwnProperty.call(n,s)&&(c[s]=n[s]);c.originalType=e,c.mdxType="string"==typeof e?e:o,a[1]=c;for(var l=2;l<i;l++)a[l]=r[l];return t.createElement.apply(null,a)}return t.createElement.apply(null,r)}d.displayName="MDXCreateElement"},20242:function(e,n,r){r.r(n),r.d(n,{assets:function(){return m},contentTitle:function(){return s},default:function(){return p},frontMatter:function(){return c},metadata:function(){return l},toc:function(){return f}});var t=r(83117),o=r(80102),i=(r(67294),r(3905)),a=["components"],c={id:"programmable_inference",title:"Programmable Inference",sidebar_label:"Overview",slug:"/programmable_inference"},s=void 0,l={unversionedId:"framework_topics/mcmc_inference/custom_inference/programmable_inference",id:"framework_topics/mcmc_inference/custom_inference/programmable_inference",title:"Programmable Inference",description:"Programmable inference is a key feature of Bean Machine, and is achieved through three key techniques:",source:"@site/../docs/framework_topics/mcmc_inference/custom_inference/programmable_inference.md",sourceDirName:"framework_topics/mcmc_inference/custom_inference",slug:"/programmable_inference",permalink:"/docs/programmable_inference",draft:!1,editUrl:"https://github.com/facebookresearch/beanmachine/edit/main/website/../docs/framework_topics/mcmc_inference/custom_inference/programmable_inference.md",tags:[],version:"current",frontMatter:{id:"programmable_inference",title:"Programmable Inference",sidebar_label:"Overview",slug:"/programmable_inference"},sidebar:"someSidebar",previous:{title:"Newtonian Monte Carlo",permalink:"/docs/newtonian_monte_carlo"},next:{title:"Custom Proposers",permalink:"/docs/custom_proposers"}},m={},f=[],u={toc:f};function p(e){var n=e.components,r=(0,o.Z)(e,a);return(0,i.mdx)("wrapper",(0,t.Z)({},u,r,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Programmable inference is a key feature of Bean Machine, and is achieved through three key techniques:"),(0,i.mdx)("ul",null,(0,i.mdx)("li",{parentName:"ul"},"Compositional inference allows you to utilize distinct inference methods for different random variables when fitting a model. Bean Machines's single-site paradigm makes composeability possible as it allows you to modularly mix-and-match inference components to get the most out of your model."),(0,i.mdx)("li",{parentName:"ul"},"Block inference allows you to propose updates for several random variables jointly, which can be necessary when dealing with highly-correlated variables."),(0,i.mdx)("li",{parentName:"ul"},"Custom proposers allow you to leverage domain-specific transformations or custom proposers on a per-variable basis, which can be especially powerful to avoid worse edge-case performance when running inference over constrained random variables.")),(0,i.mdx)("p",null,"These techniques together, which we call ",(0,i.mdx)("em",{parentName:"p"},"programmable inference, "),"give the inference engine sufficient configurability for users to achieve efficient performance without writing a complete model-specific inference algorithm, and help close the performance gap between general-purpose and model-specific handwritten inference.  In the rest of this section we expand on each of these concepts."),(0,i.mdx)("p",null,"It is worth noting that supporting these techniques is facilitiated by Bean Machine's choice of declarative syntax, which explicates the statistical models' dependency structure, namely, the directed acyclic graph (DAG). Random variables are specified independently of the order in which they are sampled during inference and the inference engine has direct access to the code block defining each variable, and can execute these blocks in the order required by the inference algorithm."))}p.isMDXComponent=!0}}]);