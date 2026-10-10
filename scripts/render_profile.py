#!/usr/bin/env python3
"""Render GitHub-native SVG widgets from public data, using only the standard library."""
from datetime import datetime, timezone, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json, math, os, textwrap, urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'generated'
OUT.mkdir(parents=True,exist_ok=True)
CYAN,PURPLE,PINK='#5ce1e6','#a99bff','#f391c6'
BG,PANEL,LINE,WHITE,MUTED='#0b1020','#111a2e','#293656','#ecf2ff','#99a9ca'
TODAY=datetime.now(timezone.utc).date()

def fetch(url):
    headers={'User-Agent':'KobetsDev-profile-widgets'}
    if url.startswith('https://api.github.com/') and os.environ.get('GITHUB_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=40) as r:
        return r.read().decode()

def txt(x,y,s,size=20,color=WHITE,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(s))}</text>'

def rect(x,y,w,h,fill=PANEL,r=14,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'

def svg(name,w,h,content,title):
    style='''text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 22s linear infinite}.float{animation:float 5s ease-in-out infinite}.pulse{animation:pulse 3s ease-in-out infinite}.scan{stroke-dasharray:14 900;animation:scan 7s linear infinite}.cursor{animation:blink 1s steps(2,end) infinite}.type{animation:type 10s steps(32,end) infinite}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes float{50%{transform:translateY(-10px)}}@keyframes pulse{50%{opacity:.35}}@keyframes scan{to{stroke-dashoffset:-1828}}@keyframes blink{50%{opacity:0}}@keyframes type{0%,6%{width:0}42%,82%{width:610px}95%,100%{width:0}}@media(prefers-reduced-motion:reduce){*{animation:none!important}.type{width:610px}}'''
    doc=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><defs><linearGradient id="accent"><stop stop-color="{CYAN}"/><stop offset=".55" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient><radialGradient id="glow"><stop stop-color="#6d44bd" stop-opacity=".26"/><stop offset="1" stop-color="#6d44bd" stop-opacity="0"/></radialGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#8aa2db" stroke-opacity=".05"/></pattern><clipPath id="bounds"><rect width="{w}" height="{h}" rx="22"/></clipPath><clipPath id="typing"><rect class="type" width="610" height="44"/></clipPath></defs><style>{style}</style><g clip-path="url(#bounds)">{rect(0,0,w,h,BG,22)}<rect width="{w}" height="{h}" fill="url(#grid)"/>{content}</g><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="{LINE}"/></svg>'''
    (OUT/name).write_text(doc)

def hero():
    c='<ellipse cx="920" cy="160" rx="420" ry="370" fill="url(#glow)"/>'
    c+=txt(46,48,'K / DEV',18,CYAN,700,'class="mono" letter-spacing="3"')
    c+=txt(1154,48,'REACT · TYPESCRIPT · PYTHON',14,MUTED,400,'class="mono" text-anchor="end"')
    c+='<path d="M46 68H1154" stroke="#293656"/><path class="scan" d="M46 68H1154" stroke="url(#accent)" stroke-width="2"/>'
    c+=txt(45,153,'Alexander',82,WHITE,700,'letter-spacing="-4"')
    c+=txt(45,239,'Kobets',82,'url(#accent)',700,'letter-spacing="-4"')
    c+=txt(48,284,'FRONTEND DEVELOPER',21,CYAN,700,'class="mono" letter-spacing="3"')
    c+='<g transform="translate(48 310)"><g clip-path="url(#typing)">'+txt(0,28,'> turning ideas into interfaces_',22,WHITE,400,'class="mono"')+'</g></g>'
    c+=txt(48,378,'React interfaces. Python tools. Curious by default.',18,MUTED)
    c+='<g class="float">'+rect(714,109,435,284,'#0d1528',16,'stroke="#3c3b68"')
    for i,col in enumerate([PINK,'#f5cc8d',CYAN]): c+=f'<circle cx="{739+i*19}" cy="131" r="4.5" fill="{col}"/>'
    c+=txt(1124,136,'alex@dev:~',14,MUTED,400,'class="mono" text-anchor="end"')
    c+='<path d="M714 153H1149" stroke="#293656"/>'
    lines=[('$ whoami',CYAN),('frontend developer',WHITE),('$ cat interests.json',PURPLE),('{',MUTED),('  "web": "React + TypeScript",',WHITE),('  "tools": "Python + Telegram"',WHITE),('}',MUTED)]
    for i,(s,col) in enumerate(lines): c+=txt(738,182+i*25,s,16,col,400,'class="mono"')
    c+=txt(738,372,'$ ',16,CYAN,400,'class="mono"')+rect(759,358,9,17,CYAN,0,'class="cursor"')+'</g>'
    c+='<g transform="translate(646 209)"><g class="orbit" fill="none" stroke="#8581d8" stroke-width="1.2" opacity=".65"><ellipse rx="48" ry="16"/><ellipse rx="48" ry="16" transform="rotate(60)"/><ellipse rx="48" ry="16" transform="rotate(120)"/></g><circle r="5" fill="#5ce1e6" class="pulse"/></g>'
    c+='<path d="M46 416H1154" stroke="#293656"/>'
    for x,s,col in [(48,'01 / INTERFACES',CYAN),(433,'02 / AUTOMATION',PURPLE),(872,'03 / EXPERIMENTS',PINK)]: c+=txt(x,450,s,13,col,700,'class="mono" letter-spacing="2"')
    svg('hero.svg',1200,478,c,'Alexander Kobets — frontend developer. React, TypeScript and Python. Animated developer terminal.')

PROJECTS=[
 ('toggle-sdk','01','Runtime, under control.','Typed configuration with TTL caching, request deduplication and a React demo.','TypeScript / React',CYAN,'config'),
 ('ipa-restore','02','Bring your apps back.','Search, download, install over USB and verify offloaded iPhone apps.','Python / CLI / iOS',PURPLE,'phone'),
 ('text_to_paper_bot','03','Text. With a human touch.','A Telegram bot that renders typed text as handwritten-style pages.','Python / Pillow / Telegram',PINK,'paper'),
 ('aiogram_calendar_with_time','04','Pick a date. And a time.','An extension of aiogram_calendar with inline time selection for Telegram bots.','Python / aiogram','#f5cc8d','calendar')]

def project_cards(repos):
    lookup={r['name']:r for r in repos}
    for repo,num,title,desc,stack,color,kind in PROJECTS:
        r=lookup[repo]
        c=txt(26,35,f'PROJECT / {num}',12,color,700,'class="mono" letter-spacing="2"')+txt(554,38,'↗',25,color,400,'text-anchor="end"')
        c+=txt(26,75,repo if len(repo)<24 else 'calendar + time picker',28,WHITE,700)
        c+=txt(26,104,title,17,color,700)
        for i,line in enumerate(textwrap.wrap(desc,43)): c+=txt(26,140+i*25,line,21,MUTED)
        c+='<g transform="translate(0 20)">'
        c+=rect(26,192,528,77,'#101b30',10,'stroke="#263453"')
        if kind=='config':
            for i,label in enumerate(['REQUEST','CACHE','CONFIG']):
                x=43+i*170
                c+=rect(x,211,138,38,'#172840',7)+txt(x+69,235,label,12,color,700,'class="mono" text-anchor="middle"')
                if i<2: c+=f'<path d="M{x+140} 230h28" stroke="{color}" stroke-dasharray="3 5" class="pulse"/>'
        elif kind=='phone':
            c+=rect(45,204,30,54,'#0b1020',5,'stroke="#a99bff"')+txt(99,225,'APP STORE → USB → IPHONE',14,color,700,'class="mono"')
            c+=rect(99,241,405,4,'#263453',2)+rect(99,241,345,4,color,2,'class="pulse"')
        elif kind=='paper':
            c+=txt(46,234,'Aa',29,color,700)+txt(105,234,'→',24,MUTED)
            for i in range(3): c+=f'<path d="M155 {214+i*14}q20 -8 40 0t40 0t40 0t40 0" fill="none" stroke="{color}" opacity="{1-i*.2}" stroke-width="2"/>'
            c+=txt(426,235,'.png',17,color,400,'class="mono"')
        else:
            for i in range(7): c+=rect(44+i*31,212,22,28,color if i==4 else '#23314b',5,'class="pulse"' if i==4 else '')
            c+=txt(325,238,'14 : 30',29,color,700,'class="mono"')
        c+='</g>'
        c+=txt(26,325,stack,16,color,700,'class="mono"')
        c+=txt(554,357,'PUSHED '+r['pushed_at'][:10],11,MUTED,400,'class="mono" text-anchor="end"')
        c+=txt(26,357,f"★ {r['stargazers_count']}  /  FORKS {r['forks_count']}",11,MUTED,400,'class="mono"')
        svg(f'project-{repo}.svg',580,380,c,f'{repo}. {desc} {stack}. Public repository metadata updated {TODAY}.')

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days={}; self.active=None; self.labels={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and a.get('data-date'): self.days[a['id']]={'date':a['data-date'],'level':int(a['data-level'])}
        if tag=='tool-tip' and a.get('for','').startswith('contribution-day'):
            self.active=a['for']; self.labels[self.active]=''
    def handle_data(self,data):
        if self.active: self.labels[self.active]+=data
    def handle_endtag(self,tag):
        if tag=='tool-tip': self.active=None
    def result(self):
        result=[]
        for key,d in self.days.items():
            if d['date']>TODAY.isoformat(): continue
            label=self.labels.get(key,'').strip()
            if not label: raise ValueError('Contribution count label missing')
            count=0 if label.startswith('No ') else int(label.split()[0].replace(',',''))
            result.append(dict(d,count=count))
        if len(result)<300: raise ValueError('Incomplete public contribution calendar')
        return sorted(result,key=lambda d:d['date'])

def skyline(days,repos):
    c=txt(34,44,'ACTIVITY / CONTRIBUTION CITY',17,CYAN,700,'class="mono" letter-spacing="2"')
    c+=txt(1166,44,str(TODAY)+' · DAILY SYNC',12,MUTED,400,'class="mono" text-anchor="end"')
    cutoff=(TODAY-timedelta(days=364)).isoformat()
    total=sum(d['count'] for d in days if d['date']>=cutoff)
    active=sum(d['count']>0 for d in days if d['date']>=cutoff)
    own=[r for r in repos if not r['fork']]
    for x,value,label in [(38,total,'CONTRIBUTIONS / 365D'),(337,active,'ACTIVE DAYS / 365D'),(636,len(own),'PUBLIC ORIGINAL REPOS'),(935,len({r['language'] for r in own if r['language']}),'PRIMARY LANGUAGES')]:
        c+=txt(x,105,value,43,WHITE,700)+txt(x,133,label,11,MUTED,400,'class="mono" letter-spacing="1"')
    # Each tower encodes one actual public contribution day.
    for n,d in enumerate(days):
        col,row=divmod(n,7); x=139+col*17-row*12; y=192+col*1.12+row*9
        height=3 if not d['count'] else 10+math.log2(d['count']+1)*18
        color=['#202b45','#3a5882','#547db0','#8672cf','#b095f1'][d['level']]
        c+=f'<g><title>{d["date"]}: {d["count"]} contributions</title><path d="M{x} {y}l12 5v{-height}l-12 -5Z" fill="{color}" opacity=".55"/><path d="M{x+12} {y+5}l12 -5v{-height}l-12 5Z" fill="{color}" opacity=".8"/><path d="M{x} {y-height}l12 -5 12 5-12 5Z" fill="{color}"/></g>'
    c+=txt(34,353,'Each tower is a day. Height follows contribution count.',15,MUTED)
    c+=txt(1166,353,'PUBLIC GITHUB ACTIVITY',11,PURPLE,700,'class="mono" text-anchor="end"')
    svg('activity.svg',1200,380,c,f'Public contribution skyline. {total} contributions and {active} active days in the last 365 days. Updated {TODAY}.')

def footer():
    c='<ellipse cx="610" cy="230" rx="550" ry="310" fill="url(#glow)"/>'
    c+=txt(600,56,'HAVE SOMETHING INTERESTING IN MIND?',15,CYAN,700,'class="mono" text-anchor="middle" letter-spacing="3"')
    c+=txt(600,113,"Let's build it.",49,WHITE,700,'text-anchor="middle" letter-spacing="-2"')
    c+=txt(600,155,'@Ya_Kobets / kobets.dev@gmail.com',18,MUTED,400,'class="mono" text-anchor="middle"')
    c+='<path d="M210 191H990" stroke="url(#accent)" stroke-width="2" class="pulse"/>'
    svg('footer.svg',1200,214,c,'Let’s build it. Telegram @Ya_Kobets or kobets.dev@gmail.com.')

def main():
    repos=[]
    for page in range(1,100):
        batch=json.loads(fetch(f'https://api.github.com/users/KobetsDev/repos?per_page=100&type=owner&page={page}'))
        repos.extend(batch)
        if len(batch)<100: break
    parser=Calendar(); parser.feed(fetch('https://github.com/users/KobetsDev/contributions'))
    days=parser.result()
    hero(); project_cards(repos); skyline(days,repos); footer()
    print(f'Rendered 7 widgets from {len(repos)} public repositories and {len(days)} calendar days.')

if __name__=='__main__': main()
