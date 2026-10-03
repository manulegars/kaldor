// SVG commun : aucune dépendance distante, même rendu pour l'écran et l'export.
export const fmt=(value,digits=2)=>value===null?'Non calculé':new Intl.NumberFormat('fr-FR',{maximumFractionDigits:digits}).format(value);
const NS='http://www.w3.org/2000/svg';
const colors=['#2758c5','#aa4611','#286b61'];
export function node(tag,attrs={},text='') {const e=document.createElementNS(NS,tag);for(const [key,value] of Object.entries(attrs))e.setAttribute(key,value);if(text)e.textContent=text;return e;}
function start(svg,width,height,title){svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.setAttribute('xmlns',NS);svg.append(node('title',{},title));}
function text(svg,x,y,value,attrs={}){svg.append(node('text',{x,y,'font-family':'system-ui, sans-serif','font-size':15,fill:'#142e3b',...attrs},value));}
function line(svg,x1,y1,x2,y2,attrs={}){svg.append(node('line',{x1,y1,x2,y2,stroke:'#bdc9cc',...attrs}));}
export function drawChart(svg,current,reference,extent,caption=''){
 const width=svg.clientWidth<600?600:900,height=520,L=80,R=width-38,T=50,B=425;
 start(svg,width,height,caption||current.y_label+' selon '+current.x_label);
 const [xmin,xmax]=current.domain_x,[ymin,ymax]=extent;
 const x=v=>L+(v-xmin)/(xmax-xmin)*(R-L),y=v=>B-(v-ymin)/(ymax-ymin)*(B-T);
 text(svg,L,23,current.y_label,{'font-size':16,'font-weight':600});
 for(let i=0;i<=5;i++) {const yy=ymin+(ymax-ymin)*i/5;line(svg,L,y(yy),R,y(yy),{stroke:'#e0e7e8'});text(svg,L-10,y(yy)+5,fmt(yy,1),{'text-anchor':'end','font-size':14});const xx=xmin+(xmax-xmin)*i/5;line(svg,x(xx),T,x(xx),B,{stroke:'#eef1f2'});text(svg,x(xx),B+25,fmt(xx,1),{'text-anchor':'middle','font-size':14});}
 line(svg,L,T,L,B,{stroke:'#677d83'});line(svg,L,B,R,B,{stroke:'#677d83'});
 if(ymin<0&&ymax>0)line(svg,L,y(0),R,y(0),{stroke:'#809395','stroke-dasharray':'2 4'});
 text(svg,(L+R)/2,height-46,current.x_label,{'text-anchor':'middle','font-size':15});
 for(const [isRef,data] of [[true,reference],[false,current]]) {
  data.curves.forEach((c,i)=>{const color=colors[c.style||0];svg.append(node('polyline',{points:c.points.map(([a,b])=>`${x(a)},${y(b)}`).join(' '),fill:'none',stroke:color,'stroke-width':isRef?2:3,'stroke-dasharray':isRef?'7 6':'none',opacity:isRef?.5:1}));if(!isRef){const point=c.points[Math.floor((c.points.length-1)*(i===0?.27:.72))];text(svg,Math.min(R-110,Math.max(L+5,x(point[0])+7)),Math.max(T+17,y(point[1])-12),c.name,{fill:color,'font-weight':700,'font-size':16});}});
  data.points.forEach((p,i)=>{if(p.x<xmin||p.x>xmax||p.y<ymin||p.y>ymax)return;const px=x(p.x),py=y(p.y);
   if(!isRef&&i===0){line(svg,px,py,px,B,{stroke:'#52646e','stroke-dasharray':'3 5'});line(svg,L,py,px,py,{stroke:'#52646e','stroke-dasharray':'3 5'});}
   svg.append(node(isRef||i>0?'rect':'circle',isRef||i>0?{x:px-4,y:py-4,width:8,height:8,fill:'white',stroke:isRef?'#64757c':'#aa4611','stroke-width':2}:{cx:px,cy:py,r:6,fill:'#142e3b',stroke:'white','stroke-width':2}));
   if(!isRef)text(svg,Math.min(R-90,Math.max(L+10,px+10)),py+(i===0?24:-22),p.name,{'font-size':14,'font-weight':700});
  });
 }
 if(current.observed){const o=current.observed;line(svg,x(o.x),T,x(o.x),B,{stroke:'#727b82','stroke-dasharray':'2 5'});line(svg,x(o.x),y(o.y1),x(o.x),y(o.y2),{stroke:'#727b82','stroke-width':4});}
 if(caption)text(svg,L,height-12,caption,{'font-size':12,fill:'#536875'});
}
const order=['growth','external','unemployment','inflation'];
const names={growth:'Croissance',external:'Extérieur',unemployment:'Chômage',inflation:'Inflation'};
const vectors={growth:[0,-1],external:[1,0],unemployment:[0,1],inflation:[-1,0]};
export function drawRadar(svg,result,reference){
 start(svg,600,420,'Radar des valeurs disponibles : référence en carrés, situation en cercles.');
 const cx=300,cy=200,radius=145;
 for(const proportion of [.25,.5,.75,1])svg.append(node('polygon',{points:order.map(k=>`${cx+vectors[k][0]*radius*proportion},${cy+vectors[k][1]*radius*proportion}`).join(' '),fill:'none',stroke:'#d9e2e1','stroke-dasharray':proportion===1?'none':'3 4'}));
 for(const key of order){const [vx,vy]=vectors[key];line(svg,cx,cy,cx+vx*radius,cy+vy*radius,{stroke:'#c0cdcb'});text(svg,cx+vx*(radius+48),cy+vy*(radius+22)+5,names[key],{'text-anchor':'middle','font-size':16,'font-weight':650});
  if(result.radar[key].score===null){text(svg,cx+vx*radius*.65,cy+vy*radius*.65+5,'NC',{'text-anchor':'middle','font-size':13,fill:'#748188'});continue;}
  for(const [ref,data]of [[true,reference],[false,result]]){const {score,outside}=data.radar[key];if(score===null)continue;const position=Math.max(0,Math.min(1,score));const px=cx+vx*radius*position,py=cy+vy*radius*position;line(svg,cx,cy,px,py,{stroke:ref?'#9aabb0':'#215e5e','stroke-width':ref?2:3,'stroke-dasharray':ref?'6 5':'none'});svg.append(node(ref?'rect':'circle',ref?{x:px-5,y:py-5,width:10,height:10,fill:'white',stroke:'#6b8187','stroke-width':2}:{cx:px,cy:py,r:6,fill:'#174e4f',stroke:'white','stroke-width':1.5}));if(outside)text(svg,px+10,py-8,'!',{fill:'#9e3e12','font-weight':800});}
 }
 text(svg,300,393,'□ Avant · ● Situation · NC : non calculé · ! hors échelle',{'text-anchor':'middle','font-size':13});
}
export function drawMini(svg,dimensions){start(svg,230,180,'Dimensions concernées par l’atelier');svg.append(node('path',{d:'M115 30 L200 85 L115 140 L30 85 Z',stroke:'#cbd9d5',fill:'none'}));for(const k of order){const[vx,vy]=vectors[k],x=115+vx*80,y=85+vy*55,active=dimensions.includes(k);svg.append(node(active?'circle':'rect',active?{cx:x,cy:y,r:6,fill:'#174e4f'}:{x:x-3,y:y-3,width:6,height:6,fill:'white',stroke:'#8c9b9d'}));text(svg,x,y+(vy<0?-12:vy>0?22:-12),names[k],{'text-anchor':'middle','font-size':12,'font-weight':active?800:400,fill:active?'#174e4f':'#6c7c81'});}text(svg,115,88,'Dimensions',{'text-anchor':'middle','font-size':11});}
export function drawTrajectory(svg,result,reference,period,stableExtent){
 const build=r=>({curves:[{name:'Inflation π',style:0,points:r.trajectory.map(p=>[p.t,p.inflation])},{name:'Anticipation πᵉ',style:1,points:r.trajectory.map(p=>[p.t,p.expected])}],points:[{name:`t${period}`,x:period,y:r.trajectory[period].inflation}],domain_x:[0,12],x_label:'Périodes du modèle · t0 à t12',y_label:'Inflation et anticipation · % par période'});
 const values=[0,...result.trajectory.flatMap(p=>[p.inflation,p.expected]),...reference.trajectory.flatMap(p=>[p.inflation,p.expected])];const lo=Math.min(...values),hi=Math.max(...values),pad=Math.max(1,(hi-lo)*.15);drawChart(svg,build(result),build(reference),stableExtent||[lo-pad,hi+pad],'Trajectoire calculée : la règle adaptative est appliquée entre les périodes.');
}
export function download(name,type,contents){const url=URL.createObjectURL(new Blob([contents],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
export function exportSVG(svg,name,metadata){const copy=svg.cloneNode(true);copy.setAttribute('xmlns',NS);const meta=node('metadata',{},JSON.stringify(metadata));copy.prepend(meta);download(name,'image/svg+xml',new XMLSerializer().serializeToString(copy));}
