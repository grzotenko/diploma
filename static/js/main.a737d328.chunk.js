(this.webpackJsonpfront=this.webpackJsonpfront||[]).push([[0],{17:function(e,a,t){e.exports=t.p+"static/media/vk.ce6a386d.svg"},18:function(e,a,t){e.exports=t.p+"static/media/search.ecef733a.svg"},19:function(e,a,t){e.exports=t.p+"static/media/youtube.0f519090.svg"},20:function(e,a,t){e.exports=t.p+"static/media/facebook.d99368ca.svg"},21:function(e,a,t){e.exports=t.p+"static/media/instagram.5b23a837.svg"},22:function(e,a,t){e.exports=t(45)},27:function(e,a,t){},45:function(e,a,t){"use strict";t.r(a);var c=t(0),n=t.n(c),s=t(15),l=t.n(s),i=t(2),o=t(3),r=t(5),m=t(4),u=(t(27),t(16)),h=t.n(u),d=function(){return h.a.get("http://127.0.0.1:8000/api/common/",{headers:{Accept:"application/json","Content-Type":"application/json","Access-Control-Allow-Origin":"*"}})},p=t(17),f=t.n(p),_=t(18),b=t.n(_),g=t(19),E=t.n(g),v=t(20),k=t.n(v),N=t(21),j=t.n(N),w=function(e){Object(r.a)(t,e);var a=Object(m.a)(t);function t(){return Object(i.a)(this,t),a.apply(this,arguments)}return Object(o.a)(t,[{key:"render",value:function(){return console.log(this.props.data&&this.props.data.menu),n.a.createElement("div",{className:"header pos-fixed w-full",id:"anchorTop"},n.a.createElement("div",{className:"social-block dis-flex"},n.a.createElement("button",{className:"social-block__search"},n.a.createElement("img",{className:"social-block__search-img",width:"18",height:"18",src:b.a,alt:""})),n.a.createElement("div",{className:"social-block__elems dis-flex m-l-5"},n.a.createElement("a",{href:"#",className:"social-block__elem"},n.a.createElement("img",{className:"social-block__elem-img",width:"20",height:"20",src:f.a,alt:""})),n.a.createElement("a",{href:"#",className:"social-block__elem m-l-5"},n.a.createElement("img",{className:"social-block__elem-img",width:"20",height:"20",src:k.a,alt:""})),n.a.createElement("a",{href:"#",className:"social-block__elem m-l-5"},n.a.createElement("img",{className:"social-block__elem-img",width:"20",height:"20",src:j.a,alt:""})),n.a.createElement("a",{href:"#",className:"social-block__elem m-l-5"},n.a.createElement("img",{className:"social-block__elem-img",width:"20",height:"20",src:E.a,alt:""})))),n.a.createElement("div",{className:"m-t-5 header-menu"},n.a.createElement("nav",{className:"menu"},n.a.createElement("ul",{className:"menu__list"},this.props.data.menu&&this.props.data.menu.map((function(e){return n.a.createElement("li",{key:e.id,className:"menu__group"},n.a.createElement("a",{href:"{item.url}",className:"menu__link"},e.title))}))))))}}]),t}(n.a.Component);w.defaultProps={data:{}};var x=function(e){Object(r.a)(t,e);var a=Object(m.a)(t);function t(e){var c;return Object(i.a)(this,t),(c=a.call(this,e)).state={data:{}},c}return Object(o.a)(t,[{key:"componentDidMount",value:function(){var e=this;d().then((function(a){console.log(a),e.setState({data:a.data})})).catch((function(e){alert(e)}))}},{key:"render",value:function(){return n.a.createElement("div",{className:"wrapper dis-flex"},n.a.createElement(w,this.state),n.a.createElement("div",null,this.state.data.main&&this.state.data.main.banner))}}]),t}(n.a.Component);l.a.render(n.a.createElement(x,null),document.getElementById("root"))}},[[22,1,2]]]);
//# sourceMappingURL=main.a737d328.chunk.js.map