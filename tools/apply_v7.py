from pathlib import Path
from bs4 import BeautifulSoup
import re

src=Path('index.html')
soup=BeautifulSoup(src.read_text(encoding='utf-8'),'html.parser')

G=[
 dict(id='007firstlight',name='007: First Light',status='Recommended',scls='ok',route='OptiScaler_DLSSNR',inj='dxgi.dll',inp='DLSS',fg='Native DLSSG',patch='Не требуется',warn='При crash/порче изображения включите RestoreComputeSignature=true. FSR3.1 input не использовать.',nr='85–100%',extra='Sharpness Override по вкусу; RestoreComputeSignature=true',src='https://github.com/optiscaler/OptiScaler/wiki/007-First-Light'),
 dict(id='beast',name='Beast of Reincarnation',status='Recommended',scls='ok',route='OptiScaler_DLSSNR + OptiPatcher',inj='dxgi.dll',inp='DLSS',fg='После проверки NR',patch='OptiPatcher ON',warn='FSR3 input может приводить к crash; для RTX 5080 используйте DLSS.',nr='85–100%',extra='FSR3 input OFF',src='https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List'),
 dict(id='indiana',name='Indiana Jones and the Great Circle',status='Recommended',scls='ok',route='OptiScaler_DLSSNR',inj='dxgi.dll / winmm.dll',inp='DLSS',fg='Native FG',patch='Не требуется',warn='При проблемах с FG/overlay временно закройте RTSS/MSI Afterburner.',nr='80–100%',extra='Full RT / Path Tracing по запасу FPS',src='https://github.com/optiscaler/OptiScaler/wiki/Indiana-Jones-and-the-Great-Circle'),
 dict(id='avatar',name='Avatar: Frontiers of Pandora',status='Recommended',scls='ok',route='OptiScaler_DLSSNR',inj='dxgi.dll',inp='DLSS',fg='Native DLSSG',patch='Spoofing OFF',warn='Обязательно Dxgi=false: spoofing может снижать FPS и ломать освещение/RT в интерьерах.',nr='85–100%',extra='[Spoofing] Dxgi=false',src='https://github.com/optiscaler/OptiScaler/wiki/Avatar-Frontiers-of-Pandora'),
 dict(id='mafiaold',name='Mafia: The Old Country',status='Recommended',scls='ok',route='OptiScaler_DLSSNR + OptiPatcher',inj='dxgi.dll',inp='DLSS',fg='Native DLSSG',patch='OptiPatcher ON',warn='При flicker попробуйте Non-Linear Color/sRGB Input.',nr='85–100%',extra='Non-Linear Color/sRGB при flicker',src='https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List'),
 dict(id='mafiade',name='Mafia: Definitive Edition',status='Experimental',scls='exp',route='DLSS5-Feeder + ReShade',inj='ReShade dxgi.dll',inp='Synthetic DLAA contract',fg='OFF',patch='Не использовать OptiScaler',warn='DX11-игра без штатного DLSS. Feeder и OptiScaler/Smooth Motion одновременно не использовать.',nr='100% на старте',extra='LaunchPad MV → DLSS5 Feed → NR',src='https://github.com/jlrouzies-fr/DLSS5-Feeder'),
 dict(id='bloodlines2',name='Vampire: The Masquerade - Bloodlines 2',status='Recommended',scls='ok',route='OptiScaler_DLSSNR + OptiPatcher',inj='dxgi.dll',inp='DLSS',fg='Native DLSSG если стабилен',patch='OptiPatcher ON',warn='Сначала добейтесь стабильного NR с FG OFF; затем включайте FG.',nr='85–100%',extra='FG тестировать после NR',src='https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List'),
 dict(id='ronin',name='Rise of the Ronin',status='Supported with workaround',scls='warn',route='OptiScaler_DLSSNR',inj='dxgi.dll',inp='DLSS',fg='После проверки NR',patch='FSR OFF',warn='FSR inputs не работают. Если overlay OptiScaler не появляется, compatibility guide отмечает workaround через Nukem-мод.',nr='85–100%',extra='DLSS only; FSR input OFF',src='https://github.com/optiscaler/OptiScaler/wiki/Rise-of-the-Ronin'),
 dict(id='nier',name='NieR:Automata',status='Experimental',scls='exp',route='DLSS5-Feeder + ReShade',inj='ReShade dxgi.dll',inp='Synthetic DLAA contract',fg='OFF',patch='OptiScaler OFF',warn='64-bit D3D11 без штатного DLSS. Feeder несовместим с OptiScaler и Smooth Motion.',nr='100% на старте',extra='MSAA/SSAA OFF; LaunchPad MV обязателен',src='https://github.com/jlrouzies-fr/DLSS5-Feeder'),
 dict(id='stalker2',name='S.T.A.L.K.E.R. 2: Heart of Chornobyl',status='Recommended',scls='ok',route='OptiScaler_DLSSNR + OptiPatcher',inj='dxgi.dll / winmm.dll',inp='DLSS',fg='Native DLSSG / XeFG',patch='OptiPatcher ON',warn='FSR3.1 upscaling input показывает худшее качество; для RTX 5080 используйте DLSS.',nr='80–100%',extra='Reflex ON; FSR3.1 input не рекомендуется',src='https://github.com/optiscaler/OptiScaler/wiki/S.T.A.L.K.E.R.-2-Heart-of-Chornobyl'),
 dict(id='splitfiction',name='Split Fiction',status='Supported route',scls='warn',route='OptiScaler_DLSSNR',inj='dxgi.dll',inp='FSR3',fg='FSR3 FG после NR',patch='Не требуется',warn='В compatibility list подтверждён FSR3 input; отдельный DLSS input не подтверждён.',nr='85–100%',extra='A/B-проверка обязательна; Smooth Motion OFF',src='https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List'),
 dict(id='resonance',name='Resonance: A Plague Tale Legacy',status='Recommended / recent support',scls='ok',route='OptiScaler_DLSSNR + optional OptiPatcher',inj='dxgi.dll',inp='DLSS 4/4.5',fg='Native DLSS FG/MFG',patch='Recent OptiPatcher support',warn='OptiPatcher support добавлен недавно; при проблемах сначала проверьте чистый OptiScaler route.',nr='80–100%',extra='DLSS Quality; Preset M при необходимости',src='https://github.com/optiscaler/OptiPatcher/releases'),
 dict(id='yakuza3',name='Yakuza Kiwami 3 & Dark Ties',status='Experimental',scls='exp',route='OptiScaler_DLSSNR trial / Autopilot',inj='dxgi.dll (trial)',inp='DLSS 4',fg='NVIDIA MFG после NR',patch='OptiPatcher пока не ставить',warn='PC-версия имеет DLSS 4/FSR3/XeSS2, но отдельной протестированной записи OptiScaler пока нет.',nr='85–100%',extra='При неудачном hook использовать DLSS5 Autopilot route detection',src='https://github.com/Kizzuwatnaa/DLSS5-Autopilot'),
]

def section(g):
    feeder='Feeder' in g['route']
    if feeder:
        install=f'''<p>Установите ReShade Full Add-on Support, затем:</p><pre>dlss5-feed.addon64 → рядом с EXE\nDLSS5_Feed.fx → reshade-shaders\\Shaders\\\nMartysMods_LAUNCHPAD.fx → motion-vector provider</pre><p>Добавьте <code>renodx-dlss5.addon64</code>, <code>nvngx_dlssnr.dll</code> и <code>nvngx_dlss.dll</code>.</p>'''
        enable='<pre>MSAA / SSAA OFF\nMotion Vector Provider ON\nDLSS5 Feed ON\nNeural Rendering ON</pre>'
        diag='<p>Проверяйте <code>dlss5-feed.log</code> на <code>feature ready</code> и <code>frame N delivered</code>. Порядок эффектов: motion vectors → DLSS5 Feed.</p>'
    else:
        install=f'''<p>Распакуйте OptiScaler_DLSSNR рядом с основным EXE и запустите:</p><pre>setup_windows.bat\n→ {g['inj']}\n→ Nvidia</pre><p>Добавьте оригинальный RTX 50 <code>nvngx_dlssnr.dll</code>. {('Установите OptiPatcher в OptiScaler\\plugins\\ и включите LoadAsiPlugins=true.' if 'OptiPatcher' in g['route'] else '')}</p>'''
        enable=f'''<pre>{g['inp']} Quality / рекомендуемый режим\nFrame Generation OFF\nInsert → OptiScaler\nNeural Rendering ON\nNR Scale 100%</pre>'''
        diag=f'''<p>{g['warn']}</p>'''
    rows=[('Разрешение','3840×2160'),('Маршрут',g['route']),('Input',g['inp']),('DLSS5 Neural Rendering','ON'),('NR Scale',g['nr']),('Frame Generation',g['fg']),('Ключевой параметр',g['extra'])]
    trs=''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in rows)
    return f'''<section id="{g['id']}" class="tab-panel">
<div class="game-head"><div class="card"><h2>{g['name']}</h2><p>Рекомендуемый маршрут: <strong>{g['route']}</strong>.</p><div class="callout {'danger' if g['scls']=='exp' else 'warn'}"><strong>{g['status']}</strong>{g['warn']}</div><div class="status-strip"><span class="status-pill {g['scls']}">{g['status']}</span><span class="status-pill ok">Проверено: 09.09.2026</span></div></div>
<div class="card"><div class="summary-grid"><div class="metric"><div class="label">Injection</div><div class="value good">{g['inj']}</div></div><div class="metric"><div class="label">Input</div><div class="value">{g['inp']}</div></div><div class="metric"><div class="label">NR</div><div class="value">{g['route']}</div></div><div class="metric"><div class="label">FG</div><div class="value">{g['fg']}</div></div></div></div></div>
<div class="section recommended-profile" id="{g['id']}-settings"><div class="section-title"><div class="step-num">★</div><h3>Рекомендуемые настройки RTX 5080 / 4K</h3></div><div class="section-body"><table class="matrix"><tr><th>Параметр</th><th>Рекомендация</th></tr>{trs}</table><p class="small">Сначала проверяйте Neural Rendering без Frame Generation; затем включайте только один FG-механизм.</p></div></div>
<div class="section step-section" id="{g['id']}-install"><div class="section-title"><div class="step-num">1</div><h3>Установка</h3></div><div class="section-body">{install}</div></div>
<div class="section step-section"><div class="section-title"><div class="step-num">2</div><h3>Первый запуск DLSS5</h3></div><div class="section-body">{enable}</div></div>
<div class="section step-section" id="{g['id']}-fg"><div class="section-title"><div class="step-num">3</div><h3>Frame Generation</h3></div><div class="section-body"><p>{g['fg']}. Включайте только после стабильной работы NR; Smooth Motion оставьте OFF, если используется другой FG.</p></div></div>
<div class="section step-section" id="{g['id']}-diag"><div class="section-title"><div class="step-num">4</div><h3>Диагностика</h3></div><div class="section-body">{diag}</div></div>
<div class="card source-list" id="{g['id']}-sources" style="margin-top:18px"><h3>Ссылки</h3><ul><li><a href="{g['src']}" target="_blank">Основной compatibility/source</a></li><li><a href="https://github.com/Dagherbou/OptiScaler_DLSSNR/releases" target="_blank">OptiScaler_DLSSNR</a></li></ul></div></section>'''

footer=soup.find('footer')
for g in G:
    if soup.find(id=g['id']) is None:
        footer.insert_before(BeautifulSoup(section(g),'html.parser').section)

meta=soup.select_one('.meta')
for b in list(meta.select('.badge')):
    t=b.get_text(' ',strip=True)
    if 'Игр:' in t: b.decompose()
    elif t.startswith('Обновлено:'):
        b.clear(); st=soup.new_tag('strong'); st.string='Обновлено:'; b.append(st); b.append(' 09.09.2026')
b=soup.new_tag('span',**{'class':'badge'}); st=soup.new_tag('strong'); st.string='Игр:'; b.append(st); b.append(' 27'); meta.insert(0,b)
for p in soup.select('.status-pill.ok'):
    if p.get_text(strip=True).startswith('Проверено:'): p.string='Проверено: 09.09.2026'

allgames=[]
for sec in soup.select('section.tab-panel'):
    h=sec.select_one('.game-head h2')
    if h: allgames.append((sec['id'],h.get_text(strip=True)))
script=soup.find('script'); txt=script.string or script.get_text()
arr=',\n'.join(f'  {{ value: {sid!r}, label: {label!r} }}' for sid,label in allgames)
txt=re.sub(r'const allGames = \[\n.*?\n\];','const allGames = [\n'+arr+'\n];',txt,flags=re.S); script.string=txt
footer.clear(); footer.append(BeautifulSoup('<strong>Интерфейс v7:</strong> production-справочник содержит 27 игровых профилей с маршрутами DLSS5, таблицами RTX 5080 / 4K, FG и диагностикой.','html.parser'))

out=Path('index.html'); out.write_text(str(soup),encoding='utf-8')
print('updated index.html'); print('games',len(allgames)); print('bytes',out.stat().st_size)
