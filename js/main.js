/* Bravar Sports Bar - comportamiento del sitio (navegación, carruseles, libro del menú, PDF) */
var t=document.getElementById('t');t.innerHTML=t.textContent.split('').map(function(c,i){return '<span style="animation-delay:'+(i*.09+.2)+'s">'+c+'</span>'}).join('');
var m='';for(var i=0;i<12;i++)m+='FÚTBOL <b>★</b> NFL <b>★</b> BOX <b>★</b> BÉISBOL <b>★</b> CERVEZA FRÍA <b>★</b> ';document.getElementById('mq').innerHTML=m;
var bt=document.getElementById('bt'),nl=document.getElementById('nl');
bt.onclick=function(){nl.classList.toggle('on')};nl.onclick=function(){nl.classList.remove('on')};
var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('on');io.unobserve(x.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e)});
document.querySelectorAll('.carw').forEach(function(w){var c=w.querySelector('.car'),paused=false;
w.querySelectorAll('.ar').forEach(function(b){b.onclick=function(){c.scrollBy({left:b.dataset.d*340,behavior:'smooth'})}});
w.onmouseenter=function(){paused=true};w.onmouseleave=function(){paused=false};
setInterval(function(){if(paused)return;if(c.scrollLeft+c.clientWidth>=c.scrollWidth-10)c.scrollTo({left:0,behavior:'smooth'});else c.scrollBy({left:340,behavior:'smooth'})},4200)});
var tb=document.querySelectorAll('.tabs button'),pl=document.querySelectorAll('.pl');
tb.forEach(function(b){b.onclick=function(){tb.forEach(function(x){x.classList.remove('on')});pl.forEach(function(x){x.classList.remove('on')});b.classList.add('on');pl[b.dataset.p].classList.add('on')}});

(function(){var bk=document.getElementById('bk'),lv=[].slice.call(bk.querySelectorAll('.lf')),N=lv.length,s=0,mob=matchMedia('(max-width:820px)'),ch=document.querySelectorAll('.chips button');
function mx(){return mob.matches?N-1:N}
function zi(){lv.forEach(function(l,i){l.style.zIndex=i<s?i:N-i})}
function go(n,q){s=Math.max(0,Math.min(mx(),n));lv.forEach(function(l,i){l.classList.toggle('fl',i<s)});bk.className='bk '+(s==0?'s0':(s==mx()&&!mob.matches?'se':'sm'));setTimeout(zi,q?0:450);ch.forEach(function(c){c.classList.toggle('on',+c.dataset.s==s)})}
lv.forEach(function(l,i){l.onclick=function(){go(i<s?s-1:s+1)}});
document.getElementById('nx').onclick=function(){go(s+1)};document.getElementById('pv').onclick=function(){go(s-1)};
ch.forEach(function(c){c.onclick=function(){go(+c.dataset.s)}});
var x0;bk.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});bk.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)go(s+(dx<0?1:-1))});
document.addEventListener('keydown',function(e){if(e.key=='Escape')lb.classList.remove('on');var r=document.getElementById('libro').getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0){if(e.key=='ArrowRight')go(s+1);if(e.key=='ArrowLeft')go(s-1)}});
var lb=document.getElementById('lb'),li=document.getElementById('lbi');
document.getElementById('zm').onclick=function(){var a=[];if(!mob.matches&&s>0)a.push(lv[s-1].querySelector('.b'));if(s<N)a.push(lv[s].querySelector('.f'));li.innerHTML='';a.forEach(function(e){if(e&&e.classList.contains('mp')){var m=document.createElement('img');m.src=getComputedStyle(e).backgroundImage.slice(5,-2);li.appendChild(m)}});if(!li.children.length){var m=document.createElement('img');m.src=getComputedStyle(lv[1].querySelector('.f')).backgroundImage.slice(5,-2);li.appendChild(m)}lb.classList.add('on');lb.scrollTop=0};
document.getElementById('lbx').onclick=function(){lb.classList.remove('on')};lb.onclick=function(e){if(e.target==lb)lb.classList.remove('on')};
go(0,1);mob.addEventListener&&mob.addEventListener('change',function(){go(s,1)});
})();

(function(){
var hx=document.querySelector('.hx');for(var i=0;i<16;i++){var s=document.createElement('i');s.className='sp';s.style.setProperty('--x',(Math.random()*100)+'%');s.style.setProperty('--d',(Math.random()*7)+'s');hx.appendChild(s)}
document.querySelectorAll('.car').forEach(function(c){[].forEach.call(c.children,function(k,i){k.style.setProperty('--n',i)})});
var pg=document.getElementById('pg'),hv=document.querySelector('.hv img');
addEventListener('scroll',function(){var m=document.documentElement.scrollHeight-innerHeight;pg.style.width=(scrollY/m*100)+'%';if(hv&&scrollY<innerHeight)hv.style.translate='0 '+(scrollY*.12)+'px'},{passive:true});
var cur=document.getElementById('cur'),rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a||a.getAttribute('href')=='#'||rm)return;var t=document.querySelector(a.getAttribute('href'));if(!t)return;e.preventDefault();document.getElementById('nl').classList.remove('on');cur.className='cur in';setTimeout(function(){document.documentElement.style.scrollBehavior='auto';scrollTo(0,t.getBoundingClientRect().top+scrollY-(t.id=='inicio'?0:60));document.documentElement.style.scrollBehavior='';cur.className='cur out';setTimeout(function(){cur.className='cur'},560)},500)});
var lb=document.getElementById('lb'),li=document.getElementById('lbi');
function all(){li.innerHTML='';document.querySelectorAll('#bk .mp').forEach(function(e){var m=document.createElement('img');m.src=getComputedStyle(e).backgroundImage.slice(5,-2);li.appendChild(m)});lb.classList.add('on');lb.scrollTop=0}
document.getElementById('pdf').onclick=async function(){
var l=BravarMenu.lang,name='Menu-Bravar-Sports-Bar-'+l.toUpperCase()+'.pdf',u;
function save(blob){var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();a.remove()}
try{u=await BravarMenu.buildPdf()}catch(e){
 if(window.STATIC_PDF){var a=document.createElement('a');a.href='assets/pdf/menu-'+l+'.pdf';a.download=name;document.body.appendChild(a);a.click();a.remove()}else all();return}
var blob=new Blob([u],{type:'application/pdf'});
if(window.claude){try{var dl=await window.claude.use('downloads');if(dl){await dl.save({filename:name,data:blob});return}}catch(e){if(e&&e.code=='declined')return}return all()}
save(blob)};
})();

/* ---------- Menú en varios idiomas + PDF ---------- */
(function(){
var M=window.MENU_PAGES||{};
function pages(l){var p=M[l]||M.es;return [M.cover,p[2],p[3],p[4],p[5],p[6]]}
function bytes(u){
 if(u.indexOf('data:')==0){var b=atob(u.split(',')[1]),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return Promise.resolve(a)}
 return fetch(u).then(function(r){if(!r.ok)throw 0;return r.arrayBuffer()}).then(function(x){return new Uint8Array(x)})}
function info(a){var i=2;while(i<a.length){if(a[i]!=255){i++;continue}var m=a[i+1];if(m>=192&&m<=195)return{h:a[i+5]*256+a[i+6],w:a[i+7]*256+a[i+8]};i+=2+a[i+2]*256+a[i+3]}throw 0}
function build(arr){var enc=new TextEncoder(),parts=[],off=[],len=0,n=arr.length,kids=[],i;
 function add(x){if(typeof x=='string')x=enc.encode(x);parts.push(x);len+=x.length}
 function obj(k,s){off[k]=len;add(k+' 0 obj\n'+s+'\nendobj\n')}
 add('%PDF-1.4\n');obj(1,'<< /Type /Catalog /Pages 2 0 R >>');
 for(i=0;i<n;i++)kids.push((3+i*3)+' 0 R');
 obj(2,'<< /Type /Pages /Kids ['+kids.join(' ')+'] /Count '+n+' >>');
 arr.forEach(function(a,i){var f=info(a),pw=595,ph=Math.round(595*f.h/f.w),b=3+i*3,cs='q '+pw+' 0 0 '+ph+' 0 0 cm /Im'+i+' Do Q';
  obj(b,'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 '+pw+' '+ph+'] /Resources << /XObject << /Im'+i+' '+(b+2)+' 0 R >> >> /Contents '+(b+1)+' 0 R >>');
  obj(b+1,'<< /Length '+cs.length+' >>\nstream\n'+cs+'\nendstream');
  off[b+2]=len;add((b+2)+' 0 obj\n<< /Type /XObject /Subtype /Image /Width '+f.w+' /Height '+f.h+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+a.length+' >>\nstream\n');add(a);add('\nendstream\nendobj\n')});
 var total=3*n+3,x=len;add('xref\n0 '+total+'\n0000000000 65535 f \n');
 for(i=1;i<total;i++)add(('0000000000'+off[i]).slice(-10)+' 00000 n \n');
 add('trailer\n<< /Size '+total+' /Root 1 0 R >>\nstartxref\n'+x+'\n%%EOF');
 var out=new Uint8Array(len),p=0;parts.forEach(function(q){out.set(q,p);p+=q.length});return out}
window.BravarMenu={lang:'es',
 setLang:function(l){if(!M[l])l='es';this.lang=l;document.querySelectorAll('#bk [data-pg]').forEach(function(e){e.style.backgroundImage='url("'+M[l][e.dataset.pg]+'")'})},
 buildPdf:function(){return Promise.all(pages(this.lang).map(bytes)).then(build)}};
BravarMenu.setLang('es');
})();
