/* Run from the Site checkout. The original, checked-in static export lives at archive/. */
import {readFile,writeFile,mkdir,cp,access} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {parseArgs} from "node:util";

const here=path.dirname(fileURLToPath(import.meta.url));
const {values}=parseArgs({options:{archive:{type:"string",default:"archive"},output:{type:"string",default:"dist"},
  manifest:{type:"string",default:".openai/hosting.json"},migrations:{type:"string",default:"drizzle"}}});
const output=path.resolve(values.output);
const archive=path.resolve(values.archive);
if (archive===output || archive.startsWith(output+path.sep)) throw Error("Keep the archived static export outside the new build output.");
const manifest=JSON.parse(await readFile(values.manifest,"utf8"));
if (!manifest.project_id || manifest.static || manifest.d1!=="DB") throw Error("Preserve the Site ID, remove static, and set d1 to DB in .openai/hosting.json.");
const types={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8",".json":"application/json; charset=utf-8"};
const table={};
async function asset(source,urls) {
  const value=[types[path.extname(source)],await readFile(source,"utf8")];
  for (const url of urls) table[url]=value;
}
await asset(path.join(here,"live.html"),["/","/index.html"]);
await asset(path.join(here,"live.js"),["/live.js"]);
await asset(path.join(here,"live.css"),["/live.css"]);
for (const f of ["index.html","app.js","style.css","results.json","snapshot.json","demo/index.html","demo/cases.json"]) {
  const urls=["/archive/"+f];
  if (f==="index.html") urls.push("/archive/");
  if (f==="demo/index.html") urls.push("/archive/demo/","/demo/","/demo/index.html");
  if (f==="demo/cases.json" || ["results.json","snapshot.json","app.js","style.css"].includes(f)) urls.push("/"+f);
  await asset(path.join(archive,f),urls);
}
const source=await readFile(path.join(here,"worker.mjs"),"utf8");
// Store each asset's bytes once, even when legacy URLs alias the same file.
const assets=[...new Set(Object.values(table))];
const routes=Object.fromEntries(Object.entries(table).map(([k,v])=>[k,assets.indexOf(v)]));
const prefix="const _assets="+JSON.stringify(assets)+";\nconst ASSETS=Object.fromEntries(Object.entries("+JSON.stringify(routes)+").map(([k,i])=>[k,_assets[i]]));\n";
await mkdir(path.join(output,"server"),{recursive:true});
await mkdir(path.join(output,".openai"),{recursive:true});
await writeFile(path.join(output,"server/index.js"),prefix+source);
await writeFile(path.join(output,".openai/hosting.json"),JSON.stringify(manifest,null,2)+"\n");
const migrationRoot=path.join(here,"drizzle");
if (path.resolve(values.migrations)!==migrationRoot) {
  for (const f of ["0000_pilot_state.sql","meta/0000_snapshot.json","meta/_journal.json"]) {
    const from=path.join(migrationRoot,f), to=path.join(values.migrations,f);
    try {
      await access(to);
      if (!(await readFile(from)).equals(await readFile(to))) throw Error("Existing Site migration conflicts with "+f);
    } catch (e) { if (e.code!=="ENOENT") throw e; }
    await mkdir(path.dirname(to),{recursive:true});
    await cp(from,to);
  }
}
await cp(values.migrations,path.join(output,".openai/drizzle"),{recursive:true});
console.log("Built embedded Worker with "+assets.length+" assets, "+Object.keys(routes).length+" routes, and the D1 migration.");
