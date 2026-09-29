/* Exact rationals govern browser state. Numbers appear only at the SVG boundary. */
const CC = (() => {
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;}
  class Rational {
    constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw new Error('Zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
    static from(x){if(x instanceof Rational)return x;if(typeof x==='object')return new Rational(x.num,x.den);if(typeof x==='string'&&x.includes('/'))return new Rational(...x.split('/'));return new Rational(x);}
    add(x){x=Rational.from(x);return new Rational(this.n*x.d+x.n*this.d,this.d*x.d);}
    sub(x){x=Rational.from(x);return this.add(new Rational(-x.n,x.d));}
    mul(x){x=Rational.from(x);return new Rational(this.n*x.n,this.d*x.d);}
    div(x){x=Rational.from(x);return new Rational(this.n*x.d,this.d*x.n);}
    cmp(x){x=Rational.from(x);const v=this.n*x.d-x.n*this.d;return v<0n?-1:v>0n?1:0;}
    floor(){return this.n>=0n?this.n/this.d:-((-this.n+this.d-1n)/this.d);}
    frac(){return this.sub(this.floor());}
    number(){return Number(this.n)/Number(this.d);}
    toString(){return this.d===1n?String(this.n):`${this.n}/${this.d}`;}
  }
  const R=x=>Rational.from(x), min=(a,b)=>a.cmp(b)<=0?a:b;
  const el=id=>document.getElementById(id);
  function svg(tag,attrs={},text){const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v)));if(text!==undefined)n.textContent=text;return n;}
  function add(parent,tag,attrs,text){const n=svg(tag,attrs,text);parent.append(n);return n;}
  function clearSVG(node,height){const width=Math.max(220,Math.round(node.getBoundingClientRect().width));node.replaceChildren();node.setAttribute('viewBox',`0 0 ${width} ${height}`);return width;}
  function physical(q,t){const speeds=[1,q,q+1,2*q+1,3*q+1,3*q+2,5*q+2];return speeds.map(speed=>{const raw=t.mul(speed),phase=raw.frac();return{speed,lap:raw.floor(),phase,distance:min(phase,R(1).sub(phase))};});}
  return {R,Rational,min,el,svg,add,clearSVG,physical};
})();
