/* Produce exact browser-model records for the independently structured Python check. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
vm.runInThisContext(read('js/cc-core.js'));
const model=require('../model.js')(CC,JSON.parse(read('data/cc_geometry.json')),JSON.parse(read('data/cc_examples.json')));
const records=[];
for(const ray of ['A','B'])for(const count of [6,7])for(let q=2;q<=60;q++){
 const a=model.analyze(ray,q,count),safe={};for(const z of ['1/8','1/7','1/6'])safe[z]=model.safeSet(ray,q,count,z).intervals;
 const caps=model.caps.flatMap(c=>model.contacts(c,ray,q));
 records.push(model.serialize({ray,q,count,speeds:a.speeds,maximum:a.maximum,times:a.times,witness:a.witness,safe,capMaximum:caps.length?caps.map(c=>c.height).reduce(model.max):null}));
}
process.stdout.write(JSON.stringify(records));
