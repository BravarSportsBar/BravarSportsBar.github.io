import re,os,sys,json
from collections import Counter
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from data import PAGES,ES_D,Q,PCS
from tr1 import EN,FR,DE
from tr2 import JA,KO,ZH
LANGS={'en':EN,'fr':FR,'de':DE,'ja':JA,'ko':KO,'zh':ZH}
BASE=os.path.dirname(os.path.abspath(__file__))
OUTDIR=os.path.abspath(BASE+'/../../assets/menu')
U='/mnt/user-data/uploads/'
os.makedirs(BASE+'/img',exist_ok=True)
# ---------- imágenes auxiliares
def prep():
    Image.open(U+'Hoja1-785x1024.jpg').convert('L').crop((0,615,785,815)).save(BASE+'/img/friends.jpg',quality=85)
    Image.open(U+'Hoja-5-785x1024.jpg').convert('L').crop((280,0,600,205)).save(BASE+'/img/pour.jpg',quality=88)
    Image.open(U+'Hoja-6-785x1024.jpg').convert('L').crop((280,0,570,205)).save(BASE+'/img/bar.jpg',quality=88)
    lg=Image.open(U+'logo.jpg').convert('L').crop((396,798,1652,1250)).resize((780,281))
    for name,col in (('logo_w',255),('logo_k',0)):
        im=Image.new('RGBA',lg.size,(col,col,col,0));im.putalpha(lg);im.save(BASE+f'/img/{name}.png')
if os.path.exists(U+'logo.jpg'):prep()
# ---------- formato de cantidades
def fmt_q(L,id):
    q=Q.get(id)
    if not q:return {}
    u=L['ui']
    out={}
    for k,n in zip('ab',q):
        out[k]=(u['pcs'] if id in PCS else u['g']).format(n=n)
    return out
ES_FMT=dict(g='{n}gr',pcs='{n} pzas')
def es_q(id):
    q=Q.get(id)
    if not q:return {}
    return {k:(ES_FMT['pcs'] if id in PCS else ES_FMT['g']).format(n=('%02d'%n if id in PCS and n<10 else n)) for k,n in zip('ab',q)}
# ---------- verificación
def nums(s):return Counter(int(x) for x in re.findall(r'\d+',s))
def verify():
    bad=0
    all_items=[i for p in PAGES.values() for side in p.values() for _,items in side for i in items]
    for lang,L in LANGS.items():
        for i in all_items:
            id=i['id']
            if i['d']:
                if id not in L['d']:print(lang,'FALTA desc',id);bad+=1;continue
                es=ES_D[id].format(**es_q(id));tr=L['d'][id].format(**fmt_q(L,id))
                if nums(es)!=nums(tr):print(lang,'NÚMEROS',id,dict(nums(es)),dict(nums(tr)));bad+=1
            if id in L['n']:
                a,b=nums(i['n']),nums(L['n'][id])
                if a and a!=b:print(lang,'NOMBRE nums',id,i['n'],'|',L['n'][id]);bad+=1
        # claves desconocidas
        ids={i['id'] for i in all_items}
        for k in list(L['d'])+list(L['n']):
            if k not in ids and k not in('camaron',):print(lang,'clave sobrante',k);bad+=1
    print('problemas:',bad)
    return bad
# ---------- HTML
ICON={
'a':'<svg viewBox="0 0 16 16"><path d="M4.500 9V3.500a1 1 0 012 0V7m0-3.800a1 1 0 012 0V7m0-3a1 1 0 012 0V8m0-2a1 1 0 012 0v5c0 2.700-1.800 4.500-4.500 4.500S3 14 2 12L1.200 9.500a1 1 0 011.800-.8L4.500 11" fill="none" stroke="#111" stroke-width="1.100" stroke-linecap="round" stroke-linejoin="round"/></svg>',
'v':'<svg viewBox="0 0 16 16"><path d="M3 13C3 6.500 7 3 13 3c0 6.500-3.500 10-10 10zM3 13l6-6" fill="none" stroke="#111" stroke-width="1.100" stroke-linecap="round" stroke-linejoin="round"/></svg>',
'g':'<svg viewBox="0 0 16 16"><path d="M2 11c0-4.500 2.500-7 7-7 0 4.500-2.500 7-7 7zM7 14c0-4.500 2.500-7 7-7 0 4.500-2.500 7-7 7z" fill="none" stroke="#111" stroke-width="1.100" stroke-linejoin="round"/></svg>',
'r':'<svg viewBox="0 0 16 16"><path d="M1 11.500c3 1.200 11 1.200 14 0M4.500 10.500C4.500 5 5.500 3.500 8 3.500s3.500 1.500 3.500 7" fill="none" stroke="#111" stroke-width="1.100" stroke-linecap="round"/></svg>'}
UNIT=re.compile(r'(\d)\s*(ML|G|OZ|L)\b')
def up(s):
    s=s.upper()
    return UNIT.sub(lambda m:m.group(1)+m.group(2).lower(),s)
def item_html(i,L):
    id=i['id'];u=L['ui']
    name=L['n'].get(id,i['n']);nm=up(name)
    ic=''.join(ICON[c] for c in i['ic'])
    h='<div class="it">'+(f'<span class="ic">{ic}</span>' if ic else '')
    if i.get('two'):
        lab=dict(mug=u['mug'],liter=u['liter'],c355=u['c355'])
        h+=f'<div class="nm"><span class="t">{nm}</span><span class="dt"></span><span class="pr2">'+'<br>'.join(f'<small>{lab[k]}</small> {p}' for k,p in i['two'])+'</span></div>'
    elif i.get('wine'):
        h+=f'<div class="nm"><span class="t">{nm}</span></div><div class="wn"><span><small>{u["glass"]}</small> {i["wine"][0]}</span><span><small>{u["bottle"]}</small> {i["wine"][1]}</span></div>'
    else:
        h+=f'<div class="nm"><span class="t">{nm}</span><span class="dt"></span><span class="pr">{i["p"]}</span></div>'
    if i['d'] and id in L['d']:
        h+='<p class="ds">'+L['d'][id].format(**fmt_q(L,id))+'</p>'
    if i.get('prot'):
        h+=f'<p class="pt">{u["prot"]}</p>'
        for k,pr in i['prot']:
            key='camaron' if k=='camaron' else k
            h+=f'<div class="pl"><span>· {u["protn"][key]} ({u["g"].format(n=100)})</span><span class="dt"></span><span>{pr}</span></div>'
    if i.get('extra'):
        h+=f'<div class="pl"><span>· {u["o700"]}</span><span class="dt"></span><span>{i["extra"][1]}</span></div>'
    return h+'</div>'
CFG={2:dict(top=215,L=(78,285),R=(428,305),hd=200,limL=868,limR=868),
     3:dict(top=52,L=(78,285),R=(428,305),hd=0,limL=925,limR=858),
     4:dict(top=52,L=(75,290),R=(424,300),hd=0,limL=860,limR=860),
     5:dict(top=245,L=(70,305),R=(418,300),hd=205,limL=960,limR=960),
     6:dict(top=245,L=(66,310),R=(416,305),hd=205,limL=960,limR=960)}
CSS=open(BASE+'/page.css').read()
def page_html(lang,n):
    L=LANGS[lang];u=L['ui'];c=CFG[n];P=PAGES[n]
    cols=''
    for side in('L','R'):
        x,w=c[side];secs=''
        for key,items in P.get(side,[]):
            secs+=f'<h3>{u["sect"][key]}</h3>'+''.join(item_html(i,L) for i in items)
        if n in(4,) and side=='L':secs+=f'<p class="note">{u["note"]}</p>'
        if n in(5,6) and side=='R':secs+=f'<p class="note" style="margin-top:34px">{u["note"]}</p>'
        cols+=f'<div class="col" data-lim="{c["lim"+side]}" style="left:{x}px;top:{c["top"]}px;width:{w}px">{secs}</div>'
    hd='';ttl={2:u['t2'],5:u['t5'],6:u['t6']}.get(n)
    if n==2:
        hd=f'<div class="hd" style="background-image:linear-gradient(90deg,#000 0%,#000a 40%,#0005 100%),url(img/friends.jpg)"><img class="logo" src="img/logo_w.png"><div class="ttl" style="left:355px">{ttl}</div><div class="tag">{u["tag"]}</div></div>'
    elif n in(5,6):
        im='pour' if n==5 else 'bar'
        hd=f'<div class="hd" style="background-image:linear-gradient(90deg,#000 0%,#000 30%,#0000 75%),url(img/{im}.jpg);background-position:right center;background-size:cover"><img class="logo" src="img/logo_w.png"><div class="ttl" style="right:46px">{ttl}</div></div>'
    else:
        hd='<div class="bar" style="top:0"></div>'
    extra=''
    if n in(2,3,4):
        leg=''.join(f'<div>{ICON[k]}<span>{t}</span></div>' for k,t in zip('avgr',u['leg']))
        extra+=f'<div class="legend">{leg}</div>'
    if n==2:extra+=f'<p class="note abs" style="left:80px;top:888px">{u["note"]}</p>'
    if n==3:extra+=f'<p class="note abs" style="left:428px;top:862px;width:300px">{u["note"]}</p>'
    if n in(3,4):extra+='<img class="blogo" src="img/logo_k.png">'
    extra+='<div class="bar" style="bottom:0"></div>'
    return f'<!doctype html><html lang="{ {"zh":"zh-CN","ja":"ja","ko":"ko"}.get(lang,lang)}"><meta charset="utf-8"><style>{CSS}</style><body><div class="pg">{hd}{cols}{extra}</div></body></html>'
FIT='''()=>{let k=1;const cols=[...document.querySelectorAll('.col')];
const over=()=>cols.some(c=>c.getBoundingClientRect().bottom>+c.dataset.lim);
while(over()&&k>0.5){k-=0.02;document.documentElement.style.setProperty('--k',k)}return k}'''
def render(langs):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUTDIR,exist_ok=True)
    rep={}
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':785,'height':1024},device_scale_factor=1.5)
        for lang in langs:
            os.makedirs(f'{OUTDIR}/{lang}',exist_ok=True)
            for n in (2,3,4,5,6):
                f=f'{BASE}/p_{lang}_{n}.html';open(f,'w').write(page_html(lang,n))
                pg.goto('file://'+f);pg.evaluate('document.fonts.ready');pg.wait_for_timeout(150)
                k=pg.evaluate(FIT);rep[(lang,n)]=round(k,2)
                pg.screenshot(path=f'{BASE}/tmp.png',clip={'x':0,'y':0,'width':785,'height':1024})
                Image.open(f'{BASE}/tmp.png').convert('RGB').save(f'{OUTDIR}/{lang}/page-{n}.jpg',quality=76,optimize=True)
        b.close()
    print(rep)
if __name__=='__main__':
    if verify():print('revisar antes de renderizar')
    render(sys.argv[1:] or list(LANGS))
