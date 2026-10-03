'use strict';
const $ = id => document.getElementById(id);
const INITIAL = Object.freeze({A:1,mu:.2,z:0,alpha:2.5,beta:1,observed:.1});
let params={...INITIAL}, reference={...INITIAL}, before={...INITIAL};
let lastData=null, sequence=0, controller=null, gesture=false;
let yDomain=null, animation=null, playing=false, animationToken=0;
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
const fmt=(n,d=1)=>new Intl.NumberFormat('fr-FR',{maximumFractionDigits:d,minimumFractionDigits:d}).format(n);
const controls=[
 ['z','Facteurs renforçant le salaire négocié',-1,1,.01,1,'z déplace WS à chômage donné ; il ne décrit pas à lui seul une politique publique.'],
 ['mu','Marge sur coût des entreprises',0,1.5,.01,100,'μ en %. Une marge plus élevée réduit le salaire réel compatible avec les prix.'],
 ['A','Productivité',.2,3,.01,1,'A est un indice : 1 correspond à la productivité initiale.'],
 ['alpha','Sensibilité des salaires au chômage',.1,6,.05,1,'α est strictement positif. Il détermine la pente de WS.'],
 ['beta','Transmission de la productivité aux salaires',0,1,.01,1,'β = 0 : aucune transmission ; β = 1 : transmission complète.'],
 ['observed','Chômage observé',0,1,.005,100,'En % des actifs. Ce repère ne change ni les courbes ni leur intersection.']
];
for(const [key,label,min,max,step,factor,help] of controls){
 const box=document.createElement('div');box.className='control';
 box.innerHTML=`<div class="control-head"><label for="${key}-range">${label}</label><input id="${key}-number" type="number" min="${min*factor}" max="${max*factor}" step="${step*factor}" aria-label="${label}, saisie numérique" aria-describedby="${key}-help"></div><input id="${key}-range" type="range" min="${min}" max="${max}" step="${step}" aria-describedby="${key}-help"><p id="${key}-help">${help}</p>`;
 $(['z','mu','A'].includes(key)?'simple-controls':'advanced-controls').append(box);
 for(const suffix of ['range','number']){
  const input=$(key+'-'+suffix);
  input.addEventListener('focus',()=>{gesture=false;});
  input.addEventListener('pointerdown',()=>{gesture=false;});
  input.addEventListener('change',()=>{gesture=false;});
  input.addEventListener('input',()=>{
   if(!input.validity.valid||input.value===''){return;}
   const value=Number(input.value)/(suffix==='number'?factor:1);
   if(!Number.isFinite(value)||value<min||value>max)return;
   if(!gesture){before={...params};gesture=true;}
   stopAnimation();animation=null;
   params={...params,[key]:value};syncControls(input);requestRender();
  });
 }
}
function syncControls(exclude=null){for(const [key,,min,max,step,factor] of controls){for(const suffix of ['range','number']){const input=$(key+'-'+suffix);if(input!==exclude)input.value=Number((params[key]*(suffix==='number'?factor:1)).toFixed(6));}}}
function stopAnimation(){playing=false;animationToken++;$('pause').disabled=true;$('animate').textContent='Animer';}
async function calculate(p,ref,prior,signal){const response=await fetch('/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({parameters:p,reference:ref,before:prior,axis:$('axis').value}),signal});const data=await response.json();if(!response.ok)throw Error(data.error||'Erreur de calcul');return data;}
async function requestRender(){
 const id=++sequence;if(controller)controller.abort();controller=new AbortController();
 document.body.classList.add('pending');$('request-state').textContent='Calcul…';$('error').hidden=true;
 try{const data=await calculate({...params},{...reference},{...before},controller.signal);if(id!==sequence)return false;lastData=data;expandDomain(data);render(data);document.body.classList.remove('pending');$('request-state').textContent='À jour';return true;}
 catch(e){if(id!==sequence||e.name==='AbortError')return false;$('error').textContent='Calcul indisponible : '+e.message;$('error').hidden=false;$('request-state').textContent='Résultats non actualisés';return false;}
}
function expandDomain(data){const values=[0,...data.result.ws,data.result.index,...data.reference.ws,data.reference.index];const lo=Math.floor((Math.min(...values)-15)/20)*20,hi=Math.ceil((Math.max(...values)+20)/20)*20;yDomain=yDomain?[Math.min(lo,yDomain[0]),Math.max(hi,yDomain[1])]:[lo,hi];}
const NS='http://www.w3.org/2000/svg';
function svg(tag,attrs={},text=''){const n=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text)n.textContent=text;return n;}
function draw(data){
 const chart=$('chart');chart.replaceChildren(svg('title',{id:'chart-title'},'Relations WS et PS'),svg('desc',{id:'chart-desc'},data.result.interior?`Équilibre : chômage ${fmt(data.result.u*100)} %, salaire réel indice ${fmt(data.result.index)}.`:'Aucun équilibre intérieur avec ces paramètres.'));
 const compact=chart.clientWidth<600;
 const W=compact?600:900,H=550,left=82,right=W-45,top=45,bottom=470;
 chart.setAttribute('viewBox',`0 0 ${W} ${H}`);
 const x=n=>left+n/100*(right-left),y=n=>bottom-(n-yDomain[0])/(yDomain[1]-yDomain[0])*(bottom-top);
 const employment=$('axis').value==='employment';
 const line=(x1,y1,x2,y2,attrs={})=>chart.append(svg('line',{x1,y1,x2,y2,...attrs}));
 for(let i=0;i<=5;i++){const value=yDomain[0]+i*(yDomain[1]-yDomain[0])/5;line(left,y(value),right,y(value),{stroke:'#e1e7eb'});chart.append(svg('text',{x:left-12,y:y(value)+5,'text-anchor':'end'},fmt(value,0)));}
 for(let i=0;i<=100;i+=10){line(x(i),top,x(i),bottom,{stroke:'#eef1f3'});chart.append(svg('text',{x:x(i),y:bottom+26,'text-anchor':'middle'},String(i)));}
 line(left,top,left,bottom,{stroke:'#536875'});line(left,bottom,right,bottom,{stroke:'#536875'});
 if(yDomain[0]<0)line(left,y(0),right,y(0),{stroke:'#a9b7bf','stroke-dasharray':'3 5'});
 chart.append(svg('text',{x:left,y:22},'Salaire réel · indice (base initiale = 100)'));
 chart.append(svg('text',{x:(left+right)/2,y:H-18,'text-anchor':'middle'},(employment?'Emploi':'Chômage')+' · % de la population active'));
 function curves(r,ref){const points=r.ws.map((v,i)=>`${x(employment?100-i:i)},${y(v)}`).join(' ');chart.append(svg('polyline',{points,fill:'none',stroke:'#2758c5','stroke-width':ref?2:3,'stroke-dasharray':ref?'8 7':'none',opacity:ref?.48:1}));line(left,y(r.index),right,y(r.index),{stroke:'#aa4611','stroke-width':ref?2:3,'stroke-dasharray':ref?'8 7':'none',opacity:ref?.48:1});if(ref&&r.in_domain)chart.append(svg('circle',{cx:x(r.x),cy:y(r.index),r:6,fill:'white',stroke:'#637681','stroke-dasharray':'2 2'}));}
 curves(data.reference,true);curves(data.result,false);
 const r=data.result;
 const uLabel=employment?95:5;
 chart.append(svg('text',{x:x(employment?100-uLabel:uLabel)+8,y:y(r.ws[uLabel])-12,class:'ws-label'},'WS'));
 chart.append(svg('text',{x:right-38,y:y(r.index)-12,class:'ps-label'},'PS'));
 const ox=x((employment?1-params.observed:params.observed)*100);
 line(ox,top,ox,bottom,{stroke:'#5d6570','stroke-dasharray':'3 6','stroke-width':1.5});
 line(ox,y(r.observed_ws),ox,y(r.index),{stroke:'#566472','stroke-width':5,opacity:.7});
 chart.append(svg('rect',{x:ox-4,y:y(r.observed_ws)-4,width:8,height:8,fill:'#2758c5'}));
 chart.append(svg('rect',{x:ox-4,y:y(r.index)-4,width:8,height:8,fill:'#aa4611'}));
 if(r.in_domain){const ex=x(r.x),ey=y(r.index);line(ex,ey,ex,bottom,{stroke:'#182e3c','stroke-dasharray':'4 5'});line(left,ey,ex,ey,{stroke:'#182e3c','stroke-dasharray':'4 5'});chart.append(svg('circle',{cx:ex,cy:ey,r:6,fill:'#182e3c',stroke:'white','stroke-width':2}));chart.append(svg('text',{x:ex+10,y:ey+23,'font-weight':800},'E'));}
}
function render(data){const r=data.result,ref=data.reference;
 $('unemployment').textContent=r.interior?fmt(r.u*100)+' %':'—';$('wage').textContent=r.interior?fmt(r.index):'—';$('employment').textContent=r.interior?fmt(r.employment*100)+' %':'—';
 const delta=(a,b,unit)=>{const d=a-b;return (d>1e-8?'+':'')+fmt(d)+' '+unit+' / référence';};
 $('du').textContent=r.interior&&ref.interior?delta(r.u*100,ref.u*100,'pt'):'Sans équilibre intérieur';$('dw').textContent=r.interior&&ref.interior?delta(r.index,ref.index,'pt d’indice'):'Base initiale = 100';$('de').textContent=r.interior&&ref.interior?delta(r.employment*100,ref.employment*100,'pt'):'Population active donnée';
 $('domain-warning').hidden=r.interior;$('domain-warning').textContent=`Aucun équilibre intérieur avec ces paramètres. Intersection algébrique : u* = ${fmt(r.u*100)} %, salaire indice ${fmt(r.index)}. ${r.in_domain?'Intersection à la frontière du domaine.':'Intersection hors de [0 ; 100 %], non affichée comme équilibre réalisable.'}`;
 $('explanation').textContent=data.explanation;
 $('axis-note').textContent=$('axis').value==='employment'?'Emploi = 100 × (1 − u) : part des actifs en emploi, et non taux d’emploi de la population en âge de travailler.':'Chômage = 100 × u : part de la population active au chômage. WS est décroissante selon cette convention.';
 $('gap').textContent=`Chômage observé : ${fmt(params.observed*100)} % · WS : ${fmt(r.observed_ws)} · PS : ${fmt(r.index)} · Écart WS − PS : ${fmt(r.gap)} points d’indice.`;
 $('phillips').textContent=!r.interior?'Sans équilibre intérieur, on ne présente pas ici de comparaison à un chômage d’équilibre réalisable.':Math.abs(params.observed-r.u)<1e-8?'Le chômage observé égale u* : pas de pression supplémentaire relativement aux anticipations dans ce modèle. Cela ne signifie pas une inflation nulle.':params.observed<r.u?'Le chômage observé est inférieur à u* : WS dépasse PS, ce qui suggère une pression inflationniste relativement aux anticipations.':'Le chômage observé est supérieur à u* : WS est inférieur à PS, ce qui suggère une pression désinflationniste relativement aux anticipations, sans impliquer nécessairement une baisse du niveau des prix.';
 draw(data);
}
$('axis').addEventListener('change',()=>{requestRender();});
$('remember').addEventListener('click',()=>{stopAnimation();animation=null;reference={...params};before={...params};requestRender();$('animation-status').textContent='Référence mémorisée. La base de l’indice salarial reste 100 à l’équilibre initial.';});
$('reset').addEventListener('click',()=>{stopAnimation();animation=null;params={...INITIAL};reference={...INITIAL};before={...INITIAL};gesture=false;yDomain=null;syncControls();$('progress').value=0;$('animation-status').textContent='Paramètres et référence réinitialisés.';requestRender();});
const targets={bargaining:{z:.15},moderation:{z:-.15},markup:{mu:.4},competition:{mu:.05},'productivity-full':{A:1.1,beta:1},'productivity-none':{A:1.1,beta:0}};
async function prepare(){stopAnimation();const token=animationToken;const key=$('scenario').value;
 // With no transmission, β is zero in BOTH configurations: only A changes.
 const start={...INITIAL,...(key==='productivity-none'?{beta:0}:{})};
 const end={...start,...targets[key]};params={...start};reference={...start};before={...start};syncControls();
 animation={start,end,t:0};yDomain=null;
 try{const endpoint=await calculate(end,start,start);if(token!==animationToken)return false;expandDomain(endpoint);await requestRender();return token===animationToken;}catch(e){$('error').textContent=e.message;$('error').hidden=false;return false;}
}
async function play(){
 if(playing)return;
 if(!animation||animation.t>=1){if(!await prepare())return;}
 playing=true;const token=++animationToken;$('pause').disabled=false;$('animate').textContent='En cours';
 if(reduced.matches){params={...animation.end};animation.t=1;syncControls();await requestRender();$('progress').value=1;stopAnimation();$('animation-status').textContent='Résultat affiché directement : préférence de réduction des animations.';return;}
 const started=performance.now(),initialT=animation.t;
 $('animation-status').textContent='Comparaison progressive des configurations…';
 async function tick(){if(!playing||token!==animationToken)return;const t=Math.min(1,initialT+(performance.now()-started)/4500);animation.t=t;params=Object.fromEntries(Object.keys(INITIAL).map(k=>[k,animation.start[k]+t*(animation.end[k]-animation.start[k])]));syncControls();$('progress').value=t;
 const ok=await requestRender();if(token!==animationToken||!playing)return;if(!ok){stopAnimation();return;}if(t<1){requestAnimationFrame(tick);}else{stopAnimation();$('animation-status').textContent='Comparaison terminée. Les courbes et E sont recalculés à chaque étape.';}}
 requestAnimationFrame(tick);
}
$('animate').addEventListener('click',play);
$('pause').addEventListener('click',()=>{stopAnimation();$('animate').textContent='Reprendre';$('animation-status').textContent='Comparaison en pause.';});
$('replay').addEventListener('click',async()=>{if(await prepare())play();});
$('scenario').addEventListener('change',()=>{stopAnimation();animation=null;$('progress').value=0;$('animation-status').textContent='Scénario sélectionné : cliquer sur Animer pour repartir des paramètres initiaux.';});
reduced.addEventListener('change',()=>{if(reduced.matches&&playing){stopAnimation();$('animation-status').textContent='Animation interrompue selon la préférence du navigateur.';}});
window.addEventListener('resize',()=>{if(lastData)draw(lastData);});
syncControls();requestRender();
