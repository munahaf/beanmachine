"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6656],{3905:function(e,n,t){t.r(n),t.d(n,{MDXContext:function(){return d},MDXProvider:function(){return c},mdx:function(){return h},useMDXComponents:function(){return p},withMDXComponents:function(){return s}});var a=t(67294);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(){return i=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&(e[a]=t[a])}return e},i.apply(this,arguments)}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function m(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},i=Object.keys(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)t=i[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var d=a.createContext({}),s=function(e){return function(n){var t=p(n.components);return a.createElement(e,i({},n,{components:t}))}},p=function(e){var n=a.useContext(d),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},c=function(e){var n=p(e.components);return a.createElement(d.Provider,{value:n},e.children)},f={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},u=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,i=e.originalType,o=e.parentName,d=m(e,["components","mdxType","originalType","parentName"]),s=p(t),c=r,u=s["".concat(o,".").concat(c)]||s[c]||f[c]||i;return t?a.createElement(u,l(l({ref:n},d),{},{components:t})):a.createElement(u,l({ref:n},d))}));function h(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var i=t.length,o=new Array(i);o[0]=u;var l={};for(var m in n)hasOwnProperty.call(n,m)&&(l[m]=n[m]);l.originalType=e,l.mdxType="string"==typeof e?e:r,o[1]=l;for(var d=2;d<i;d++)o[d]=t[d];return a.createElement.apply(null,o)}return a.createElement.apply(null,t)}u.displayName="MDXCreateElement"},49452:function(e,n,t){t.r(n),t.d(n,{contentTitle:function(){return m},default:function(){return c},frontMatter:function(){return l},metadata:function(){return d},toc:function(){return s}});var a=t(87462),r=t(63366),i=(t(67294),t(3905)),o=["components"],l={id:"compositional_inference",title:"Compositional Inference",sidebar_label:"Compositional Inference",slug:"/compositional_inference"},m=void 0,d={unversionedId:"framework_topics/custom_inference/compositional_inference",id:"framework_topics/custom_inference/compositional_inference",title:"Compositional Inference",description:'Sometimes it might be hard to pick a single algorithm that performs well on the entire model. For example, while gradient-based algorithms such as No-U-Turn Sampler and Newtonian Monte Carlo generally yield high number of effective samples, they can only handle random variables with continuous support. On the other hand, while single site algorithms make it easier to update high-dimensional models by proposing only one node at a time, they might have trouble updating models with highly correlated random variables. Fortunately, Bean Machine supports composable inference through the CompositionalInference class, which allows us to use different inference methods to update different subset of nodes and to "block" multiple nodes together so that they are accepted/rejected jointly by a single Metropolis-Hastings step. In this doc, we will cover the basics of CompositionalInference and how to mix-and-match different inference algorithms. To learn about how to do "block inference" with CompositionalInference, see Block Inference.',source:"@site/../docs/framework_topics/custom_inference/compositional_inference.md",sourceDirName:"framework_topics/custom_inference",slug:"/compositional_inference",permalink:"/docs/compositional_inference",editUrl:"https://github.com/facebookresearch/beanmachine/edit/main/website/../docs/framework_topics/custom_inference/compositional_inference.md",tags:[],version:"current",frontMatter:{id:"compositional_inference",title:"Compositional Inference",sidebar_label:"Compositional Inference",slug:"/compositional_inference"},sidebar:"someSidebar",previous:{title:"Custom Proposers",permalink:"/docs/custom_proposers"},next:{title:"Block Inference",permalink:"/docs/block_inference"}},s=[{value:"Default Inference Methods",id:"default-inference-methods",children:[],level:2},{value:"Configuring Your Own Inference",id:"configuring-your-own-inference",children:[{value:"Choosing different inference methods for different random variable families",id:"choosing-different-inference-methods-for-different-random-variable-families",children:[],level:3},{value:"Overriding default inference method",id:"overriding-default-inference-method",children:[],level:3}],level:2}],p={toc:s};function c(e){var n=e.components,t=(0,r.Z)(e,o);return(0,i.mdx)("wrapper",(0,a.Z)({},p,t,{components:n,mdxType:"MDXLayout"}),(0,i.mdx)("p",null,"Sometimes it might be hard to pick a single algorithm that performs well on the entire model. For example, while gradient-based algorithms such as ",(0,i.mdx)("a",{parentName:"p",href:"/docs/no_u_turn_sampler"},"No-U-Turn Sampler")," and ",(0,i.mdx)("a",{parentName:"p",href:"/docs/newtonian_monte_carlo"},"Newtonian Monte Carlo")," generally yield high number of effective samples, they can only handle random variables with continuous support. On the other hand, while single site algorithms make it easier to update high-dimensional models by proposing only one node at a time, they might have trouble updating models with highly correlated random variables. Fortunately, Bean Machine supports composable inference through the ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference"),' class, which allows us to use different inference methods to update different subset of nodes and to "block" multiple nodes together so that they are accepted/rejected jointly by a single Metropolis-Hastings step. In this doc, we will cover the basics of ',(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference"),' and how to mix-and-match different inference algorithms. To learn about how to do "block inference" with ',(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference"),", see ",(0,i.mdx)("a",{parentName:"p",href:"/docs/block_inference"},"Block Inference"),"."),(0,i.mdx)("h2",{id:"default-inference-methods"},"Default Inference Methods"),(0,i.mdx)("p",null,"By default, Compositional Inference will pick a single site algorithm to update each of the latent variable in the model based on its support:"),(0,i.mdx)("table",null,(0,i.mdx)("thead",{parentName:"table"},(0,i.mdx)("tr",{parentName:"thead"},(0,i.mdx)("th",{parentName:"tr",align:null},"Support"),(0,i.mdx)("th",{parentName:"tr",align:null},"Algorithm"))),(0,i.mdx)("tbody",{parentName:"table"},(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},"real"),(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"SingleSiteNewtonianMonteCarlo")," (real space proposer)")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},"greater than"),(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"SingleSiteNewtonianMonteCarlo")," (half space proposer)")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},"simplex"),(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"SingleSiteNewtonianMonteCarlo")," (simplex space proposer)")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},"finite discrete"),(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"SingleSiteUniformMetropolisHastings"))),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},"everything else"),(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"SingleSiteAncestralMetropolisHastings"))))),(0,i.mdx)("p",null,"To run ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference")," with these default inference methods, simply leave the inference argument empty:"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-py"},"CompositionalInference().infer(\n    queries,\n    observations,\n    num_samples,\n    num_chains,\n    num_adaptive_samples,\n)\n")),(0,i.mdx)("p",null,"The parameters to ",(0,i.mdx)("inlineCode",{parentName:"p"},"infer")," are described below:"),(0,i.mdx)("table",null,(0,i.mdx)("thead",{parentName:"table"},(0,i.mdx)("tr",{parentName:"thead"},(0,i.mdx)("th",{parentName:"tr",align:null},"Name"),(0,i.mdx)("th",{parentName:"tr",align:null},"Usage"))),(0,i.mdx)("tbody",{parentName:"table"},(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"queries")),(0,i.mdx)("td",{parentName:"tr",align:null},"A ",(0,i.mdx)("inlineCode",{parentName:"td"},"List")," of ",(0,i.mdx)("inlineCode",{parentName:"td"},"@bm.random_variable")," targets to fit posterior distributions for.")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"observations")),(0,i.mdx)("td",{parentName:"tr",align:null},"The ",(0,i.mdx)("inlineCode",{parentName:"td"},"Dict")," of observations. Each key is a random variable, and its value is the observed value for that random variable.")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"num_samples")),(0,i.mdx)("td",{parentName:"tr",align:null},"Number of samples to build up distributions for the values listed in ",(0,i.mdx)("inlineCode",{parentName:"td"},"queries"),".")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"num_chains")),(0,i.mdx)("td",{parentName:"tr",align:null},"Number of separate inference runs to use. Multiple chains can be used by diagnostics to verify inference ran correctly.")),(0,i.mdx)("tr",{parentName:"tbody"},(0,i.mdx)("td",{parentName:"tr",align:null},(0,i.mdx)("inlineCode",{parentName:"td"},"num_adaptive_samples")),(0,i.mdx)("td",{parentName:"tr",align:null},"The integer number of samples to spend before ",(0,i.mdx)("inlineCode",{parentName:"td"},"num_samples")," on tuning the inference algorithm for the ",(0,i.mdx)("inlineCode",{parentName:"td"},"queries"),".")))),(0,i.mdx)("h2",{id:"configuring-your-own-inference"},"Configuring Your Own Inference"),(0,i.mdx)("p",null,(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference")," also takes an optional dictionary, namely, the ",(0,i.mdx)("inlineCode",{parentName:"p"},"inference_dict"),", which can be used to override the default behavior.\nIn the following sections, assume that we're working with a toy model with three random variable families, ",(0,i.mdx)("inlineCode",{parentName:"p"},"foo"),", ",(0,i.mdx)("inlineCode",{parentName:"p"},"bar"),", and ",(0,i.mdx)("inlineCode",{parentName:"p"},"baz"),":"),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-py"},"@bm.random_variable\ndef foo(i):\n    return dist.Beta(2.0, 2.0)\n\n@bm.random_variable\ndef bar(i):\n    return dist.Bernoulli(foo(i))\n\n@bm.random_variable\ndef baz(j):\n    return dist.Normal(0.0, 1.0)\n")),(0,i.mdx)("h3",{id:"choosing-different-inference-methods-for-different-random-variable-families"},"Choosing different inference methods for different random variable families"),(0,i.mdx)("p",null,"To select an inference algorithm for a particular random variable family, pass the random variable family as the key and an instance of the inference algorithm as value.\nFor example, the following snippet tells ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference")," to use ",(0,i.mdx)("inlineCode",{parentName:"p"},"SingleSiteNoUTurnSampler()")," to update all instances of ",(0,i.mdx)("inlineCode",{parentName:"p"},"foo")," and ",(0,i.mdx)("inlineCode",{parentName:"p"},"SingleSiteHamiltonianMonteCarlo(1.0)")," to update all instance of ",(0,i.mdx)("inlineCode",{parentName:"p"},"baz"),".\nNodes that are not specified, such as instances of ",(0,i.mdx)("inlineCode",{parentName:"p"},"bar"),", will fall back to the default inference methods mentioned above."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-py"},"bm.CompositionalInference({\n    foo: bm.SingleSiteNoUTurnSampler(),\n    baz: bm.SingleSiteHamiltonianMonteCarlo(trajectory_length=1.0),\n}).infer(**args) # same parameters as shown above\n")),(0,i.mdx)("p",null,'You may notice that we are using what we referred to as "random variable families" like ',(0,i.mdx)("inlineCode",{parentName:"p"},"foo")," as keys, which are essentially functions that generates the random variables, instead of using instances of random variables such as ",(0,i.mdx)("inlineCode",{parentName:"p"},"foo(0)")," and ",(0,i.mdx)("inlineCode",{parentName:"p"},"foo(1)"),". This is because often times the number of random variable is not known ahead of time until an inference starts with some data (you can even have unbounded number of nodes in some model). By using random variable family in the config, we no longer need to explicitly spell out all every instance in a huge dictionary."),(0,i.mdx)("h3",{id:"overriding-default-inference-method"},"Overriding default inference method"),(0,i.mdx)("p",null,"If your model has a large number of nodes and you want to override the default inference method for all of them without listing them all, you can use Python's ",(0,i.mdx)("inlineCode",{parentName:"p"},"Ellipsis")," literal, or equivalently, ",(0,i.mdx)("inlineCode",{parentName:"p"},"...")," (three dots), as a key to specify the default inference method for nodes that are not specified in the dictionary. For example, the following code snippet tells ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference")," to use ",(0,i.mdx)("inlineCode",{parentName:"p"},"SingleSiteUniformMetropolisHastings()")," to update all instances of ",(0,i.mdx)("inlineCode",{parentName:"p"},"bar")," (which are discrete), and use ",(0,i.mdx)("inlineCode",{parentName:"p"},"SingleSiteNoUTurnSampler()")," to update the rest of nodes (which are all continuous)."),(0,i.mdx)("pre",null,(0,i.mdx)("code",{parentName:"pre",className:"language-py"},"bm.CompositionalInference({\n    bar: bm.SingleSiteUniformMetropolisHastings(),\n    ...: bm.SingleSiteNoUTurnSampler(),\n}).infer(**args) # same parameters as shown above\n")),(0,i.mdx)("p",null,"Bean Machine provides a great variety of inference methods under ",(0,i.mdx)("a",{parentName:"p",href:"https://beanmachine.org/api/beanmachine.ppl.inference.html"},(0,i.mdx)("inlineCode",{parentName:"a"},"beanmachine.ppl.inference"))," that can be used with the ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference")," API. To learn more about what else can be done with ",(0,i.mdx)("inlineCode",{parentName:"p"},"CompositionalInference"),", see ",(0,i.mdx)("a",{parentName:"p",href:"/docs/block_inference"},"Block Inference"),"."))}c.isMDXComponent=!0}}]);