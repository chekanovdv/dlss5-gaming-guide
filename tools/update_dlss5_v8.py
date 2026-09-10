from pathlib import Path
from bs4 import BeautifulSoup
import re

src=Path('index.html')
out=Path('index.html')
html=src.read_text(encoding='utf-8')
soup=BeautifulSoup(html,'html.parser')

def frag(markup):
    return BeautifulSoup(markup,'html.parser')

def set_table(sec_id, label, value):
    sec=soup.find(id=sec_id)
    if not sec:
        raise RuntimeError(f'Missing section {sec_id}')
    for tr in sec.find_all('tr'):
        tds=tr.find_all('td')
        if len(tds)>=2 and tds[0].get_text(' ',strip=True)==label:
            tds[1].clear(); tds[1].append(BeautifulSoup(value,'html.parser'))
            return True
    return False

def add_source(game_id, label, url):
    card=soup.find(id=f'{game_id}-sources')
    if not card: raise RuntimeError(f'Missing sources {game_id}')
    ul=card.find('ul')
    if not ul: raise RuntimeError(f'Missing ul {game_id}')
    for a in ul.find_all('a'):
        if a.get('href')==url: return
    li=soup.new_tag('li'); a=soup.new_tag('a', href=url, target='_blank'); a.string=label; li.append(a); ul.append(li)

def find_step(game_id, title_contains):
    sec=soup.find('section',id=game_id)
    for div in sec.find_all('div',class_='section',recursive=False):
        h=div.find('h3')
        if h and title_contains.lower() in h.get_text(' ',strip=True).lower():
            return div
    raise RuntimeError(f'No step {title_contains} in {game_id}')

def replace_body(step, markup):
    body=step.find('div',class_='section-body')
    body.clear(); body.append(BeautifulSoup(markup,'html.parser'))

for badge in soup.select('.badge'):
    if badge.get_text(' ',strip=True).startswith('Обновлено:'):
        badge.clear(); strong=soup.new_tag('strong'); strong.string='Обновлено:'; badge.append(strong); badge.append(' 10.09.2026')
for pill in soup.select('.status-pill.ok'):
    if pill.get_text(' ',strip=True).startswith('Проверено:'):
        pill.string='Проверено: 10.09.2026'

ap=soup.find(id='autopilot-note')
body=ap.find('div',class_='autopilot-details-body')
body.clear()
body.append(frag('''
<p><strong>Актуально: DLSS5 Autopilot v1.8.0 (10.09.2026).</strong> Это установщик и диагностический маршрутизатор для новых/проблемных игр; для уже настроенных игр сохраняйте game-specific профиль из этого справочника.</p>
<ul>
<li><strong>Aim for FPS:</strong> для OptiScaler-route и Feeder 64-bit D3D11 Autopilot теперь использует измеренные логи и предлагает рабочую область/Model Resolution под целевой FPS. Два замера на разных масштабах позволяют оценить модель <code>frame_ms = base + k × r²</code>.</li>
<li><strong>Crash diagnostics:</strong> если игра закрывается до появления ReShade/OptiScaler log, Autopilot читает Windows Application Error и учитывает faulting module; запись Windows имеет приоритет над «здоровым» последним логом.</li>
<li><strong>Driver preflight:</strong> минимальная версия для Neural Rendering — <code>616.56</code>. В отчётах Autopilot драйвер <code>616.64</code> встречается как частая причина проблем, поэтому при необъяснимом crash стоит сравнить поведение на другом актуальном драйвере/официальном hotfix, а не сразу менять маршрут мода.</li>
<li><strong>Runtimes:</strong> DLSS Super Resolution и Frame Generation Autopilot теперь получает из официального NVIDIA-репозитория SDK по release tag. Ray Reconstruction можно подменять только если игра уже поставляет RR и выбранный route поддерживает замену; launcher verification/anti-cheat могут вернуть или заблокировать изменённый DLL.</li>
<li><strong>32-bit DXVK/Vulkan:</strong> v1.8.0 исправляет конфликт регистрации 32/64-bit ReShade Vulkan layer, важный для старых 32-bit DX9→DXVK игр.</li>
</ul>
<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v1.8.0" target="_blank">DLSS5 Autopilot v1.8.0 — changelog</a></p>
'''))

set_table('onimusha-settings','Frame Generation','В игре OFF на первом запуске; после проверки NR — один FG-механизм за раз')
set_table('onimusha-settings','Ключевой параметр','Inputs/Motion = Native; Intensity ≈0.70; Local Structure ≈1.20; <code>nrSelfLayers=1.00</code>, <code>nrTrueLayers=1</code> как базовая точка')
step=find_step('onimusha','Установить RE_DLSS5_Load_Mod')
replace_body(step,'''
<p>Используйте текущую сборку <strong>RE_DLSS5_Load_Mod v0.63</strong> от 09.09.2026:</p>
<p><a href="https://github.com/LCPD15/RE_DLSS5_Load_Mod/releases/tag/v0.63" target="_blank">RE_DLSS5_Load_Mod v0.63 — GitHub Release</a></p>
<p>Распакуйте содержимое архива рядом с <code>OnimushaWotS.exe</code>. В v0.63 добавлены альтернативные proxy-DLL для случаев конфликта имён с другими модами: <code>winmm.dll</code>, <code>winhttp.dll</code>, <code>dinput8.dll</code>, <code>dxgi.dll</code>, <code>d3d11.dll</code>, <code>dsound.dll</code>, <code>xinput1_3.dll</code>, <code>xinput1_4.dll</code>, <code>xinput9_1_0.dll</code>. Не меняйте proxy без необходимости: выбирайте альтернативу только если стандартное имя конфликтует с REFramework/ReShade/другим loader.</p>
<div class="callout warn"><strong>Важно</strong>Не переносите в эту конфигурацию D18-patched <code>nvngx_dlssnr.dll</code>. Используйте runtime, совместимый с RE_DLSS5_Load_Mod/RTX 50, либо комплект текущей сборки.</div>
<div class="callout ok"><strong>Новые NR Layers из v0.62+</strong><code>nrSelfLayers</code> усиливает разницу NR без дополнительных вызовов модели (1.00–3.00), а <code>nrTrueLayers</code> выполняет последовательные NR-проходы (1–5) и заметно увеличивает GPU/VRAM. Для RTX 5080 начните с <code>1.00 / 1</code>; повышайте только после стабильного A/B-теста.</div>
''')
step=find_step('onimusha','Базовый профиль RTX 5080 / 4K')
pre=step.find('div',class_='section-body').find('pre')
if pre and 'NR Self Layers' not in pre.get_text():
    pre.string=pre.get_text().rstrip()+"\nNR Self Layers        1.00\nNR True Layers        1"
step=soup.find(id='onimusha-fg')
replace_body(step,'''
<p>Первый запуск выполняйте с <strong>Frame Generation OFF</strong>, чтобы отдельно проверить Neural Rendering. В актуальной ветке RE_DLSS5_Load_Mod предыдущие ограничения совместимости с FG были переработаны, но game-specific сочетание всё равно нужно тестировать после каждого обновления игры/loader.</p>
<pre>Frame Generation в Onimusha    OFF на базовом тесте
Smooth Motion / driver FG      OFF
NR Self Layers                 1.00
NR True Layers                 1</pre>
<p>После стабильного F8 ON/OFF и <code>Debug View → Diff</code> включите <strong>только один</strong> FG-механизм. Если при штатной интерполяции снова пропадает Diff/эффект NR, вернитесь к FG через DLSS5 Loader либо оставьте FG выключенным.</p>
<div class="callout"><strong>Проверка</strong>После включения FG снова сравните F8 ON/OFF и <code>Debug View → Diff</code>. Изменение должно сохраняться, а frametime — оставаться стабильным.</div>
''')
add_source('onimusha','RE_DLSS5_Load_Mod v0.63 — GitHub','https://github.com/LCPD15/RE_DLSS5_Load_Mod/releases/tag/v0.63')

for gid in ['batman','mafiade','nier']:
    sec=soup.find('section',id=gid)
    for node in sec.find_all(string=re.compile(r'DLSS5-Feeder')):
        if '0.15.1' not in str(node) and node.parent.name != 'a':
            node.replace_with(str(node).replace('DLSS5-Feeder','DLSS5-Feeder v0.15.1'))
    inst=find_step(gid,'Установ') if gid!='batman' else find_step(gid,'Установить DLSS5-Feeder')
    ibody=inst.find('div',class_='section-body')
    if gid in ['mafiade','nier']:
        replace_body(inst,'''
<p><strong>Рекомендуемый способ — one-command installer из DLSS5-Feeder v0.15.1:</strong></p>
<pre>tools\\Install-DLSS5Feeder.ps1</pre>
<p>Он ставит/обновляет ReShade, Feeder, motion-vector provider и необходимые runtimes с резервным копированием существующих файлов. При ручной установке для 64-bit D3D11:</p>
<pre>dlss5-feed.addon64 → рядом с EXE
DLSS5_Feed.fx → reshade-shaders\\Shaders\\
MartysMods_LAUNCHPAD.fx → motion-vector provider
renodx-dlss5.addon64
nvngx_dlssnr.dll
nvngx_dlss.dll</pre>
<p><a href="https://github.com/jlrouzies-fr/DLSS5-Feeder/releases/tag/v0.15.1" target="_blank">DLSS5-Feeder v0.15.1</a></p>
''')
    elif ibody and 'v0.15.1' not in ibody.get_text():
        ibody.insert(0, frag('<p><strong>Используйте DLSS5-Feeder v0.15.1.</strong> Рекомендуемый upstream способ — <code>tools\\Install-DLSS5Feeder.ps1</code>.</p>'))
    diag=soup.find('div',id=f'{gid}-diag')
    if not diag and gid=='batman': diag=soup.find('div',id='batman-fg')
    dbody=diag.find('div',class_='section-body')
    dbody.append(frag('''<div class="callout ok"><strong>HDR10 bridge в Feeder 0.15.1</strong>Если конкретная конфигурация реально выводит <strong>HDR10 PQ BT.2020</strong> в 10-bit swapchain, оставьте <code>hdr_bridge=-1</code> (auto). Feeder преобразует PQ → linear FP16 → PQ, чтобы DLSS-NR видел корректный HDR. Базовый <code>hdr_paper_white=203</code> нит. В <code>dlss5-feed.log</code> ищите <code>HDR10 bridge ON</code>. Для SDR этот путь не включается; функция относится к 64-bit D3D11.</div>'''))
    add_source(gid,'DLSS5-Feeder v0.15.1','https://github.com/jlrouzies-fr/DLSS5-Feeder/releases/tag/v0.15.1')

bat=soup.find(id='batman-fg')
replace_body(bat,'''
<p>Если NR перестаёт работать спустя несколько минут, сначала убедитесь, что установлен <strong>Feeder v0.15.1</strong>, затем проверьте <code>dlss5-feed.log</code> и Windows Application Error.</p>
<pre>D3D12 device removed 0x887A0006</pre>
<ul><li>оставьте Smooth Motion и OptiScaler выключенными;</li><li>уберите сторонние overlays/injectors, кроме ReShade/Feeder;</li><li>если crash происходит до записи лога, используйте диагностику DLSS5 Autopilot v1.8.0 по Windows Application Error.</li></ul>
<div class="callout ok"><strong>HDR10 bridge в Feeder 0.15.1</strong>Если конкретная конфигурация реально выводит <strong>HDR10 PQ BT.2020</strong> в 10-bit swapchain, оставьте <code>hdr_bridge=-1</code> (auto). Базовый <code>hdr_paper_white=203</code> нит; в <code>dlss5-feed.log</code> ищите <code>HDR10 bridge ON</code>. Для SDR bridge не активируется; путь относится к 64-bit D3D11.</div>
''')

sec=soup.find('section',id='007firstlight')
head=sec.find('div',class_='game-head').find('div',class_='card')
status=head.find('div',class_='status-strip')
status.insert_before(frag('''<div class="callout ok"><strong>15.09.2026 — Path Tracing + DLSS 4.5 Ray Reconstruction</strong>NVIDIA подтверждает обновление на 15 сентября. Текущий профиль (10.09) относится к версии до PT/RR. После патча заново проверьте цепочку в порядке: NR без FG → Ray Reconstruction → Dynamic MFG; не переносите старые выводы о совместимости на новый renderer без A/B.</div>''').find('div'))
set_table('007firstlight-settings','Frame Generation','Dynamic MFG / native DLSSG после стабильного NR; после 15.09 тестировать уже после RR')
settings=soup.find(id='007firstlight-settings')
if not any(td.get_text(' ',strip=True)=='Ray Tracing / RR' for td in settings.find_all('td')):
    for tr in settings.find('table').find_all('tr'):
        tds=tr.find_all('td')
        if tds and tds[0].get_text(' ',strip=True)=='Frame Generation':
            tr.insert_before(frag('<tr><td>Ray Tracing / RR</td><td>Path Tracing + DLSS 4.5 Ray Reconstruction — с обновления 15.09.2026; до этой даты не применяется</td></tr>').tr); break
body=soup.find(id='007firstlight-diag').find('div',class_='section-body')
body.append(frag('<p><strong>После патча 15.09:</strong> сначала FG OFF и RR OFF → проверить NR; затем RR ON → A/B; только последним включить Dynamic MFG.</p>'))
add_source('007firstlight','NVIDIA — Path Tracing update 15.09.2026','https://www.nvidia.com/en-sg/geforce/news/wardogs-aniimo-007-first-light-path-tracing-geforce-game-ready-driver/')

sec=soup.find('section',id='witcher3')
head=sec.find('div',class_='game-head').find('div',class_='card')
status=head.find('div',class_='status-strip')
status.insert_before(frag('''<div class="callout danger"><strong>29.09.2026 — The Witcher 3 Remastered</strong>CD PROJEKT RED выпускает бесплатный Remastered с изменениями графики, производительности и gameplay. Этот профиль проверен для текущей pre-Remastered версии. После обновления 29 сентября заново проверьте <code>bin\\x64_dx12</code>, DLL-hook, DLSS/XeSS input, NR и FG до применения старых workaround.</div>''').find('div'))
set_table('witcher3-settings','Ключевой параметр','До 29.09: установка в <code>bin\\x64_dx12</code>; при OptiFG HUDfix ON, Limit 1. После Remastered — revalidate route')
add_source('witcher3','CD PROJEKT RED — The Witcher 3 Remastered (29.09.2026)','https://www.thewitcher.com/gb/en/news/52017/announcing-the-witcher-3-wild-hunt-remastered')

footer=soup.find('footer',class_='footer')
footer.clear(); footer.append(frag('<strong>Интерфейс v8:</strong> 27 игровых профилей; актуализированы DLSS5 Autopilot 1.8.0, DLSS5-Feeder 0.15.1 и RE_DLSS5_Load_Mod 0.63; добавлены предупреждения о 007 Path Tracing/RR (15.09) и The Witcher 3 Remastered (29.09). Проверено: 10.09.2026.'))

out.write_text(str(soup),encoding='utf-8')
