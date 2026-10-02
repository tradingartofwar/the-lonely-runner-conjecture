/* Exact finite explorer over the pinned atlas. Floating point is for drawing only. */
function createExplorerModel(CC,geometry,examples){
 'use strict';
 const {R,min}=CC,max=(a,b)=>a.cmp(b)>=0?a:b,ceil=v=>-R(v).mul(-1).floor();
 const rows=[[1,0],[0,1],[1,1],[2,1],[3,1],[3,2],[5,2]],floor=R('1/8');
 const pointKey=p=>p.map(String).join(','),unique=points=>[...new Map(points.map(p=>[pointKey(p),p])).values()];
 const dot=(a,b)=>a.reduce((s,v,i)=>s.add(R(v).mul(b[i])),R(0));
 const range=values=>values.length?[values.reduce(min),values.reduce(max)]:null;
 const blend=(a,b,r)=>a.map((v,i)=>R(v).add(R(b[i]).sub(v).mul(r)));
 function poly(raw,id){return{...raw,id,vertices:raw.vertices.map(p=>p.map(R)),constraints:raw.constraints?.map(([name,n,b])=>[name,n.map(R),R(b)])};}
 const parents=geometry.parent_child.parents.map((p,i)=>poly(p,`P${i}`));
 const cells=geometry.parent_child.children.map((p,i)=>poly(p,`C${i}`));
 const caps=geometry.top_caps.map(c=>({...poly(c,c.id),dimension:3,edges:[[0,1],[0,2],[0,3],[1,2],[2,3],[3,1]],faces:[[0,1,2],[0,2,3],[0,3,1],[1,2,3]]}));
 const segments=examples.selector_visual.segments.map(s=>({...s,id:s.segment,dimension:1,vertices:s.endpoints.map(p=>p.map(R)),edges:[[0,1]],labels:s.torus_laps}));
 const shapes=count=>count===6?parents:cells;
 function validate(ray,q,count){if(!['A','B'].includes(ray)||!Number.isInteger(q)||q<2||q>60||![6,7].includes(count))throw Error('Use ray A or B, integer q=2…60, and six or seven forms.');}
 function orbit(ray,q,p){return ray==='A'?R(p[0]).mul(q).sub(p[1]):R(p[0]).sub(R(p[1]).mul(q));}
 const time=(ray,p)=>R(p[ray==='A'?0:1]);
 function speeds(ray,q,count=7){return (ray==='A'?[1,q,q+1,q+2,q+3,2*q+3,2*q+5]:[1,q,q+1,2*q+1,3*q+1,3*q+2,5*q+2]).slice(0,count);}
 function physical(ray,q,t,count=7){
  t=R(t);const runners=speeds(ray,q).map((speed,i)=>{const raw=t.mul(speed),phase=raw.frac();return{speed,lap:raw.floor().toString(),phase,distance:min(phase,R(1).sub(phase)),required:i<count};});
  return{time:t,minimum:runners.slice(0,count).map(r=>r.distance).reduce(min),runners};
 }
 // Intersect certified edges with one plane; vertices include equality.
 function section(shape,functional,target){
  target=R(target);const points=shape.vertices.filter(p=>functional(p).cmp(target)===0);
  for(const [i,j]of shape.edges){const a=shape.vertices[i],b=shape.vertices[j],fa=functional(a),fb=functional(b);if(fa.sub(target).cmp(0)*fb.sub(target).cmp(0)<0)points.push(blend(a,b,target.sub(fa).div(fb.sub(fa))));}
  return unique(points);
 }
 // All chords preserve the convex section; extrema of this set give its exact line intersection.
 function slice(points,functional,target){return section({vertices:points,edges:points.flatMap((_,i)=>points.slice(i+1).map((__,j)=>[i,i+j+1]))},functional,target);}
 const horizontal=(shape,z)=>section(shape,p=>p[2],z);
 function integerValues(interval){if(!interval)return[];const result=[];for(let h=ceil(interval[0]);h<=interval[1].floor();h++)result.push(Number(h));return result;}
 function contacts(shape,ray,q){
  const interval=range(shape.vertices.map(p=>orbit(ray,q,p))),result=[];
  for(const h of integerValues(interval)){const points=section(shape,p=>orbit(ray,q,p),h);for(const point of points)result.push({shape:shape.id,h,point,time:time(ray,point),height:point[2]});}
  return result.sort((a,b)=>b.height.cmp(a.height)||a.time.cmp(b.time)||a.h-b.h);
 }
 function merge(intervals){
  const sorted=intervals.map(p=>p.map(R)).sort((a,b)=>a[0].cmp(b[0])||a[1].cmp(b[1])),result=[];
  for(const [a,b]of sorted){const last=result.at(-1);if(last&&a.cmp(last[1])<=0)last[1]=max(last[1],b);else result.push([a,b]);}return result;
 }
 function safeSet(ray,q,count,z){
  validate(ray,q,count);z=R(z);if(z.cmp(floor)<0||z.cmp('1/2')>0)throw Error('The atlas supports thresholds from 1/8 to 1/2.');
  const records=[];
  for(const shape of shapes(count)){
   const points=horizontal(shape,z),interval=range(points.map(p=>orbit(ray,q,p)));
   for(const h of integerValues(interval)){
    const common=slice(points,p=>orbit(ray,q,p),h),times=range(common.map(p=>time(ray,p)));if(times)records.push({shape:shape.id,h,interval:times,points:common});
   }
  }
  const intervals=merge(records.flatMap(r=>[r.interval,[R(1).sub(r.interval[1]),R(1).sub(r.interval[0])]]));
  return{threshold:z,intervals,records,duration:intervals.reduce((s,[a,b])=>s.add(b.sub(a)),R(0))};
 }
 function selector(q){
  const trials=segments.map(s=>{const interval=range(s.vertices.map(p=>orbit('A',q,p))),h=Number(ceil(interval[0])),accepted=R(h).cmp(interval[1])<=0;return{segment:s.id,interval,h,accepted,point:accepted?slice(s.vertices,p=>orbit('A',q,p),h)[0]:null};});
  const selected=trials.find(t=>t.accepted);return{trials,selected};
 }
 const cache=new Map();
 function analyze(ray,q,count=7){
  validate(ray,q,count);const key=[ray,q,count].join(':');if(cache.has(key))return cache.get(key);
  const all=shapes(count).flatMap(s=>contacts(s,ray,q));if(!all.length)throw Error('No atlas witness; recover a richer model before claiming a global optimum.');
  const best=all.map(c=>c.height).reduce(max),winners=all.filter(c=>c.height.cmp(best)===0);
  const times=[...new Map(winners.flatMap(c=>[c.time,R(1).sub(c.time)]).map(t=>[String(t),t])).values()].sort((a,b)=>a.cmp(b));
  for(const t of times)if(physical(ray,q,t,count).minimum.cmp(best)!==0)throw Error('Orbit/physical optimum mismatch');
  const selected=ray==='A'&&count===7?selector(q).selected:null;
  const witness=selected?{point:selected.point,time:selected.point[0],shape:selected.segment,h:selected.h,height:floor}:winners[0];
  if(physical(ray,q,witness.time,count).minimum.cmp(floor)<0)throw Error('Witness below atlas floor');
  const result={ray,q,count,speeds:speeds(ray,q,count),maximum:best,times,winners,witness,safe:safeSet(ray,q,count,floor)};
  cache.set(key,result);return result;
 }
 function inspect(shape,ray,q,z,h,position=0){
  z=R(z);const points=horizontal(shape,z),interval=range(points.map(p=>orbit(ray,q,p))),integers=integerValues(interval);
  const common=slice(points,p=>orbit(ray,q,p),h).sort((a,b)=>time(ray,a).cmp(time(ray,b)));
  const endpoints=common.length?[common[0],common.at(-1)]:[],point=endpoints.length?blend(endpoints[0],endpoints[1],R(position).div(100)):null;
  return{shape:shape.id,height:z,h,section:points,interval,integers,common:endpoints,point,time:point?time(ray,point):null};
 }
 function contains(shape,p){if(shape.constraints)return shape.constraints.every(([,n,b])=>dot(n,p).cmp(b)<=0);if(shape.id.startsWith('E')){const [a,b]=shape.vertices,r=R(p[0]).sub(a[0]).div(b[0].sub(a[0]));return r.cmp(0)>=0&&r.cmp(1)<=0&&blend(a,b,r).every((v,i)=>v.cmp(p[i])===0);}return contains(cells[shape.cell],p)&&R(p[2]).cmp('1/7')>=0;}
 function coordinates(ray,q,t,z){t=R(t);let p=ray==='A'?[t,t.mul(q).frac(),R(z)]:[t.mul(q).frac(),t,R(z)],reflected=false;if(p[0].cmp('1/2')>0){p=[R(1).sub(p[0]),R(1).sub(p[1]),p[2]];reflected=true;}return{point:p,reflected,h:Number(orbit(ray,q,p).toString())};}
 function transfer(ray,q,parentIndex,h){const parent=parents[parentIndex],children=cells.filter(c=>c.parent_index===parentIndex),before=section(parent,p=>orbit(ray,q,p),h),after=children.map(c=>({id:c.id,points:section(c,p=>orbit(ray,q,p),h)}));const best=points=>points.length?points.reduce((a,b)=>a[2].cmp(b[2])>=0?a:b):null;return{parent:parent.id,children:children.map(c=>c.id),before,after,beforeBest:best(before),afterBest:best(after.flatMap(c=>c.points))};}
 function facets(shape){if(shape.faces)return shape.faces;return(shape.constraints||[]).map(([,n,b])=>shape.vertices.map((p,i)=>dot(n,p).cmp(b)===0?i:null).filter(i=>i!==null)).filter(ids=>ids.length>=3);}
 const serialize=value=>value instanceof CC.Rational?String(value):Array.isArray(value)?value.map(serialize):value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([k,v])=>[k,serialize(v)])):typeof value==='bigint'?String(value):value;
 return{R,min,max,ceil,range,rows,floor,parents,cells,caps,segments,shapes,speeds,orbit,time,physical,section,slice,horizontal,integerValues,contacts,safeSet,selector,analyze,inspect,contains,coordinates,transfer,facets,serialize};
}
if(typeof module!=='undefined')module.exports=createExplorerModel;
