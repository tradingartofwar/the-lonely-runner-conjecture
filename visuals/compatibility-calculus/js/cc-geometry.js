const CCGeometry = (() => {
  const {R,add,clearSVG}=CC;
  function draw(node,cap,section,point,hit,state){
    const height=Math.round(node.getBoundingClientRect().height),width=clearSVG(node,height);
    add(node,'title',{},`Cap ${cap.id}; horizontal section; ${hit?'physical contact':'ambient points before contact'}`);
    const cv=cap.vertices.map(v=>v.map(x=>R(x).number()));
    const context=state.full?CC_DATA.geometry.full_cells:[];
    const all=[...cv,...context.flatMap(c=>c.vertices.map(v=>v.map(x=>R(x).number())))];
    const center=[0,1,2].map(i=>(Math.min(...all.map(v=>v[i]))+Math.max(...all.map(v=>v[i])))/2);
    const az=state.azimuth*Math.PI/180,ti=state.tilt*Math.PI/180;
    function raw(v){const x=v[0]-center[0],y=v[1]-center[1],z=4*(v[2]-center[2]);return [x*Math.cos(az)-y*Math.sin(az),(x*Math.sin(az)+y*Math.cos(az))*Math.sin(ti)-z*Math.cos(ti)];}
    const rv=all.map(raw),xs=rv.map(p=>p[0]),ys=rv.map(p=>p[1]);
    const scale=Math.min((width-84)/(Math.max(...xs)-Math.min(...xs)||1),(height-110)/(Math.max(...ys)-Math.min(...ys)||1));
    const mid=[(Math.min(...xs)+Math.max(...xs))/2,(Math.min(...ys)+Math.max(...ys))/2];
    const project=v=>{const p=raw(v);return [width/2+(p[0]-mid[0])*scale,height/2-5+(p[1]-mid[1])*scale];};
    const pts=v=>v.map(p=>project(p).join(',')).join(' ');
    for(const cell of context){const v=cell.vertices.map(p=>p.map(x=>R(x).number()));for(const [i,j]of cell.edges)add(node,'polyline',{points:pts([v[i],v[j]]),class:'context-edge'});if(cell.singleton){const p=project(v[0]);add(node,'circle',{cx:p[0],cy:p[1],r:5,class:'singleton'});}}
    for(const face of [[0,1,2],[0,2,3],[0,3,1],[1,2,3]])add(node,'polygon',{points:pts(face.map(i=>cv[i])),class:'cap-face'});
    for(const [i,j]of [[0,1],[0,2],[0,3],[1,2],[2,3],[3,1]])add(node,'polyline',{points:pts([cv[i],cv[j]]),class:'cap-edge'});
    const sectionFloats=section.map(v=>v.map(x=>R(x).number()));
    add(node,'polygon',{points:pts(sectionFloats),class:'section'});
    const peak=project(cv[0]);add(node,'circle',{cx:peak[0],cy:peak[1],r:3,fill:'var(--green)'});
    add(node,'text',{x:Math.max(10,Math.min(width-135,peak[0]+10)),y:Math.max(20,peak[1]-14)},`P${cap.id} · z = 1/6`);
    if(point){const p=project(point.map(x=>R(x).number()));add(node,'circle',{cx:p[0],cy:p[1],r:6,class:hit?'hit':'ambient'});if(hit){add(node,'text',{x:Math.max(10,Math.min(width-105,p[0]+10)),y:Math.min(height-58,p[1]+22),class:'point-label'},'Integer contact');}}
    add(node,'text',{x:10,y:height-12,class:'small'},state.full?'Full atlas · hollow points = singleton cells':'Cap base z = 1/7 · vertical scale ×4');
    const origin=[width-53,height-55];
    for(const [name,v]of [['x',[Math.cos(az),Math.sin(az)*Math.sin(ti)]],['y',[-Math.sin(az),Math.cos(az)*Math.sin(ti)]],['z',[0,-Math.cos(ti)]]]){
      const end=[origin[0]+v[0]*26,origin[1]+v[1]*26];add(node,'line',{x1:origin[0],y1:origin[1],x2:end[0],y2:end[1],stroke:'var(--muted)'});add(node,'text',{x:end[0]+3,y:end[1]-3,class:'small'},name);
    }
  }
  function interval(node,contact,lo,hi,hit){
    const height=120,width=clearSVG(node,height),h=Number(contact.orbit_integer);
    const vals=[R(contact.h0).number(),R(contact.interval[0]).number(),R(contact.interval[1]).number(),h];
    const a=Math.floor(Math.min(...vals))-.25,b=Math.ceil(Math.max(...vals))+.25;
    const x=v=>25+(v-a)/(b-a)*(width-50),base=77;
    add(node,'title',{},`Projected interval [${lo}, ${hi}]; ${hit?'integer reached':'no integer yet'}`);
    add(node,'line',{x1:25,y1:base,x2:width-25,y2:base,stroke:'var(--line)','stroke-width':1});
    for(let k=Math.ceil(a);k<=Math.floor(b);k++){
      add(node,'line',{x1:x(k),y1:25,x2:x(k),y2:base+6,stroke:'var(--muted)','stroke-dasharray':'3 4','stroke-width':1});add(node,'text',{x:x(k),y:base+25,'text-anchor':'middle'},String(k));
    }
    const y=43,l=x(lo.number()),r=x(hi.number());
    add(node,'line',{x1:l,y1:y,x2:r,y2:y,stroke:hit?'var(--green)':'var(--amber)','stroke-width':7,'stroke-linecap':'round'});
    add(node,'circle',{cx:l,cy:y,r:4,fill:hit?'var(--green)':'var(--amber)'});add(node,'circle',{cx:r,cy:y,r:4,fill:hit?'var(--green)':'var(--amber)'});
    if(hit)add(node,'circle',{cx:x(h),cy:y,r:7,class:'hit'});
    add(node,'text',{x:width-5,y:height-2,'text-anchor':'end',class:'small'},'H = x − qy');
    add(node,'text',{x:5,y:15,class:'small'},'Integer orbit slices');
  }
  function runners(node,rows,z,t){
    const height=285,width=clearSVG(node,height),cx=width/2,cy=138,r=Math.min(94,(width-95)/2);
    add(node,'title',{},`Seven runners at exact time ${t}; separation ${z}`);
    const xy=(p,rad=r)=>[cx+Math.sin(2*Math.PI*p)*rad,cy-Math.cos(2*Math.PI*p)*rad];
    add(node,'circle',{cx,cy,r,fill:'none',stroke:'var(--line)','stroke-width':2});
    const forbidden=[];for(let i=0;i<=50;i++)forbidden.push(xy(-z.number()+2*z.number()*i/50).join(','));
    add(node,'polyline',{points:forbidden.join(' '),fill:'none',stroke:'var(--red)','stroke-width':7,'stroke-opacity':.45,'stroke-dasharray':'3 4'});
    for(const f of [z.number(),1-z.number()]){const a=xy(f,r-11),b=xy(f,r+11);add(node,'line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'var(--red)','stroke-width':1});}
    const groups=new Map();for(const row of rows){const key=String(row.phase);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(row);}
    let index=0;
    for(const group of groups.values()){
      const row=group[0],p=xy(row.phase.number()),active=group.some(r=>r.distance.cmp(z)===0);
      add(node,'circle',{cx:p[0],cy:p[1],r:active?6:4.5,fill:active?'var(--green)':'var(--blue)',stroke:'var(--surface)','stroke-width':1.5});
      const label=xy(row.phase.number(),r+19+(index%2)*12);
      add(node,'line',{x1:p[0],y1:p[1],x2:label[0],y2:label[1],stroke:'var(--line)'});
      add(node,'text',{x:label[0],y:label[1]+4,'text-anchor':'middle',class:active?'point-label':''},group.map(r=>r.speed).join(','));index++;
    }
    const zero=xy(0);add(node,'rect',{x:zero[0]-5,y:zero[1]-5,width:10,height:10,fill:'var(--text)'});
    add(node,'text',{x:cx,y:cy-r-20,'text-anchor':'middle'},'0 · reference');
    add(node,'text',{x:cx,y:cy-3,'text-anchor':'middle',class:'small'},'PHYSICAL TIME');
    add(node,'text',{x:cx,y:cy+21,'text-anchor':'middle',style:'font-size:22px;font-family:Georgia,serif'},String(t));
    add(node,'text',{x:cx,y:height-6,'text-anchor':'middle',class:'small'},'Speed labels · green = limiting');
  }
  return {draw,interval,runners};
})();
