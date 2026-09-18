from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
assert 'Обновлено:</strong> 17.09.2026' in s and 'DLSS5 Autopilot v1.9.0' in s

s=s.replace('Обновлено:</strong> 17.09.2026','Обновлено:</strong> 19.09.2026',1)
s=s.replace('Проверено: 17.09.2026','Проверено: 19.09.2026')
s=s.replace('Источники: 16.09.2026','Источники: 19.09.2026')
s=s.replace('DLSS5 Autopilot 1.9.0 → standalone-dlssnr','DLSS5 Autopilot 2.0.1 → standalone-dlssnr')
s=s.replace('Autopilot 1.9.0 / Driver 616.64+ — route policy сохраняется','Autopilot 2.0.1 / Driver 616.64+ — первый route policy сохраняется')
s=s.replace('диагностику DLSS5 Autopilot v1.8.2','диагностику DLSS5 Autopilot v2.0.1')

new_details='''<details class="autopilot-details" id="autopilot-note"><summary>DLSS5 Autopilot — когда он нужен?</summary><div class="autopilot-details-body">
<p><strong>Актуально: DLSS5 Autopilot v2.0.1 (17.09.2026).</strong> Это установщик, диагностический маршрутизатор и инструмент измерения стоимости Neural Rendering; для уже настроенных игр сохраняйте game-specific профиль из этого справочника.</p>
<ul>
<li><strong>NVIDIA driver:</strong> актуальный Game Ready по состоянию на 19.09.2026 — <strong>616.92 WHQL</strong>; минимум для текущего DLSS5 toolchain — <code>616.56</code>.</li>
<li><strong>Первый маршрут:</strong> базовые правила не изменены. Для игр <strong>без собственного DLSS</strong> на <code>616.64+</code> и 64-bit D3D11/D3D12 первым выбором остаётся <strong>standalone-dlssnr</strong>, если он доступен; <code>feeder</code> — fallback. Для игр со штатным DLSS D3D12 обычно первым остаётся <code>optiscaler</code>; <code>native</code> и <code>neural-upstream</code> доступны как альтернативы, D3D11 со штатным DLSS — <code>bridge</code>.</li>
<li><strong>Что изменилось в 2.0/2.0.1:</strong> после rule-based первого маршрута AUTOPILOT ранжирует последующие варианты с учётом shared compatibility: маршрут, который в этой игре ни разу не сработал, уходит ниже ещё не опробованного; абсолютное число отчётов учитывается вместе с долей успехов. Это <strong>не</strong> заменяет game-specific диагностику.</li>
<li><strong>Автодиагностика:</strong> watcher теперь отслеживает реально загруженные DLL и логи, после закрытия игры сообщает результат и предлагает следующий маршрут, если текущая цепочка не могла сработать. Игры с anti-cheat и launcher EXE автоматически не запускаются.</li>
<li><strong>DXVK exception:</strong> игры, которым нужен DXVK, в 2.0.1 больше не переводятся автоматически на standalone только из-за драйвера 616.64+, поскольку standalone обходит DXVK; применяется обнаруженный API и соответствующий маршрут.</li>
<li><strong>Ложное распознавание DLSS:</strong> собственные остатки Autopilot и NGX-файлы от стороннего DLSS swapper/wrapper больше не считаются доказательством того, что игра штатно вызывает DLSS. Это особенно важно для Batman: Arkham Knight и других игр без native DLSS.</li>
<li><strong>Cadence / NR Scale:</strong> для <code>neural-upstream</code> при DLSS Frame Generation оставляйте cadence <strong>Quality</strong>. Для <code>optiscaler</code> Model Resolution остаётся главным регулятором; для Feeder 64-bit D3D11 — work area. Измеряемая настройка из 1.9.x сохранена; при наличии нескольких успешных измеренных результатов конкретной игры используйте их как стартовую точку, а не общий процент из таблицы.</li>
<li><strong>DLSS runtimes:</strong> официальный NVIDIA DLSS SDK — <strong>310.9.1</strong> (SR/RR, включая Ray Reconstruction Transformer Mode / Preset F). DLSS Neural Rendering runtime <code>nvngx_dlssnr.dll</code> для RTX 50 остаётся отдельным runtime поколения <strong>310.8.0</strong> и не является содержимым публичного DLSS SDK.</li>
<li><strong>DLSS5-Feeder:</strong> стабильная рекомендация остаётся <strong>0.15.1</strong>. Для troubleshooting доступен <strong>1.16.0-beta.4 (16.09.2026)</strong>: поверх beta.3 добавлен workaround для 32-bit игр в exclusive fullscreen — host запускается без окна, чтобы не замораживать swapchain; <code>host_window=2</code> принудительно включает этот режим. Для 64-bit профилей справочника это не причина менять stable-рекомендацию.</li>
<li><strong>Shared compatibility feed:</strong> актуальная база содержит <strong>136 отчётов</strong> (сгенерирована 18.09.2026 20:24 UTC). Для профилей справочника: 007 First Light — <code>optiscaler</code> <strong>1 success / 0 fail</strong>; Cyberpunk 2077 — <code>optiscaler</code> <strong>2 / 2</strong> и <code>neural-upstream</code> <strong>1 / 0</strong>; Starfield — <code>neural-upstream</code> <strong>0 / 1</strong>; Onimusha — <code>native</code> <strong>0 / 1</strong> и <code>optiscaler</code> <strong>0 / 1</strong>; RDR2 — <code>optiscaler</code> <strong>0 / 1</strong>. Малые выборки — ориентир для A/B, а не универсальный verdict.</li>
</ul>
<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v2.0.1" target="_blank">DLSS5 Autopilot v2.0.1 — changelog</a></p>
<p><a href="https://github.com/jlrouzies-fr/DLSS5-Feeder/releases/tag/v1.16.0-beta.4" target="_blank">DLSS5-Feeder 1.16.0-beta.4 — troubleshooting build</a></p>
<p><a href="https://github.com/NVIDIA/DLSS/releases/tag/v310.9.1" target="_blank">NVIDIA DLSS SDK 310.9.1</a></p>
<p><a href="https://www.nvidia.com/en-sg/geforce/news/wardogs-aniimo-007-first-light-path-tracing-geforce-game-ready-driver/" target="_blank">NVIDIA Game Ready 616.92 WHQL — 09.09.2026</a></p>
</div></details>'''
s,n=re.subn(r'<details class="autopilot-details" id="autopilot-note">.*?</details>',new_details,s,count=1,flags=re.S); assert n==1

def update_section(gid, fn):
    global s
    m=re.search(rf'(<section class="tab-panel" id="{re.escape(gid)}"[^>]*>)(.*?)(?=<section class="tab-panel"|<footer class="footer">)',s,re.S)
    assert m, gid
    body=fn(m.group(2))
    s=s[:m.start(2)]+body+s[m.end(2):]

def replace_callout(body, heading, html):
    pat=rf'<div class="callout [^"]+"><strong>{re.escape(heading)}</strong>.*?</div>'
    body,n=re.subn(pat,html,body,count=1,flags=re.S); assert n==1,(heading,n)
    return body

# Batman + Feeder prerelease notes in three x64 profiles.
def batman(body):
    old='DLSS5-Feeder 1.16.0-beta.3 — 16.09.2026'
    html='''<div class="callout ok"><strong>Autopilot 2.0.1 — исправлено ложное распознавание native DLSS</strong>Если рядом с Arkham Knight остался <code>nvngx_dlss.dll</code> от DLSS swapper/wrapper, актуальный Autopilot больше не должен принимать его за штатный DLSS игры и предлагать неверные DLSS/DX12 routes. Чистая папка всё равно предпочтительна.</div><div class="callout ok"><strong>DLSS5-Feeder 1.16.0-beta.4 — 16.09.2026</strong>Beta.4 добавляет workaround для <strong>32-bit exclusive fullscreen</strong> (windowless host, <code>host_window=2</code>). Batman: Arkham Knight — 64-bit D3D11, поэтому это <strong>не</strong> основание менять рабочий fallback: сохраняйте stable <strong>0.15.1</strong>, prerelease используйте только для диагностики.</div>'''
    return replace_callout(body,old,html)
update_section('batman',batman)
for gid,label in [('mafiade','Mafia: Definitive Edition'),('nier','NieR:Automata')]:
    def f(body,label=label):
        html=f'''<div class="callout ok"><strong>DLSS5-Feeder 1.16.0-beta.4 — 16.09.2026</strong>Beta.4 исправляет запуск 64-bit host для <strong>32-bit игр в exclusive fullscreen</strong> (windowless host, <code>host_window=2</code>) и включает предыдущие beta.1–beta.3 fixes. {label} в этом профиле не требует перехода на beta.4: для ручного стабильного fallback сохраняйте <strong>0.15.1</strong>, prerelease используйте только для диагностики конкретной проблемы.</div>'''
        return replace_callout(body,'DLSS5-Feeder 1.16.0-beta.3 — 16.09.2026',html)
    update_section(gid,f)

# Cyberpunk shared compatibility.
def cyber(body):
    html='''<div class="callout warn"><strong>Autopilot shared results — 18.09 / 136 reports</strong>Для Cyberpunk 2077 актуальный feed показывает <code>optiscaler</code> <strong>2 success / 2 fail</strong> и <code>neural-upstream</code> <strong>1 success / 0 fail</strong>. Выборка всё ещё мала: основной ручной профиль OptiScaler_DLSSNR не меняется, а upstream остаётся A/B-альтернативой. На драйвере 616.92 в feed уже два успешных результата; проверяйте конкретную систему по логам и держите FG OFF во время настройки NR.</div>'''
    return replace_callout(body,'Autopilot shared results — 16.09 / 99 reports',html)
update_section('cyberpunk',cyber)

# 007 PT hotfix and current feed.
def bond(body):
    html='''<div class="callout ok"><strong>17.09.2026 — Game Update 1.2.1, Path Tracing Hotfix #1</strong>После выхода Path Tracing + DLSS 4.5 Ray Reconstruction IOI выпустила hotfix 1.2.1: исправлены несколько GPU crash/hang и scene-specific crash с включённым Path Tracing. Разработчики отдельно признают оставшиеся проблемы производительности и обещают дальнейшие исправления. Поэтому сохраняйте поэтапную проверку: <strong>NR при PT/RR/FG OFF → PT + RR → Dynamic MFG последним</strong>; стартовый NR Scale не снижайте только из-за hotfix без собственного A/B-бенчмарка.</div>'''
    body=replace_callout(body,'15.09.2026 — Path Tracing + DLSS 4.5 Ray Reconstruction уже доступны',html)
    html2='''<div class="callout ok"><strong>Autopilot shared result</strong>В актуальном feed (18.09, 136 отчётов) для 007 First Light остаётся <strong>1 success / 0 fail</strong> на <code>optiscaler</code> и драйвере 616.92. Этот результат относится к маршруту в целом и <strong>не доказывает</strong> стабильность NR-fork одновременно с Path Tracing, RR и Dynamic MFG.</div>'''
    body=replace_callout(body,'Autopilot shared result',html2)
    anchor='<li><a href="https://www.nvidia.com/en-ph/geforce/news/007-first-light-path-tracing-dlss-4-5-ray-reconstruction-update-out-now/" target="_blank">NVIDIA — Path Tracing + DLSS 4.5 Ray Reconstruction update out now</a></li>'
    assert anchor in body
    return body.replace(anchor,anchor+'<li><a href="https://ioi.dk/007firstlightgame/patch-notes/2026/1-2-1-game-update" target="_blank">IO Interactive — Game Update 1.2.1 / Path Tracing Hotfix #1</a></li>',1)
update_section('007firstlight',bond)

# Crimson Desert 2.03 RR changes.
def crimson(body):
    old_heading='Patch 2.02.00 — исправлен запуск с DLSS Frame Generation'
    m=re.search(rf'<div class="callout ok"><strong>{re.escape(old_heading)}</strong>.*?</div>',body,re.S); assert m
    add='''<div class="callout ok"><strong>Patch 2.03.00 — NVIDIA Streamline SDK 2.14.1 и новый RR transformer</strong>Официальный патч от 18.09.2026 обновил NVIDIA Streamline до <strong>2.14.1</strong> и применил актуальную transformer-модель DLSS Ray Reconstruction. Сначала подтвердите clean native DLSS/RR на 2.03.00, затем отдельно включайте OptiScaler_DLSSNR. Не считайте совместимость штатного RR доказательством совместимости NR-fork + RR; <code>nvngx_dlssd.dll</code> игры на первом тесте не подменяйте.</div>'''
    body=body[:m.start()]+add+m.group(0).replace('Patch 2.02.00 — исправлен запуск с DLSS Frame Generation','Patch 2.02.00 — DLSS Frame Generation startup crash исправлен').replace('Официальные patch notes от 11.09.2026 указывают исправление crash при запуске игры с включённым DLSS Frame Generation. На актуальной версии native DLSSG можно ретестировать после стабильного NR, но диагностику по-прежнему начинайте с <strong>FG OFF</strong> и включайте FG только после подтверждения базового NR.','Исправление от 11.09 остаётся актуальным: native DLSSG можно ретестировать после стабильного NR, но первичную диагностику выполняйте с <strong>FG OFF</strong>.')+body[m.end():]
    body=body.replace('<tr><td>Ray Reconstruction</td><td>ON при RT, если изображение стабильно</td></tr>','<tr><td>Ray Reconstruction</td><td>Native RR из patch 2.03.00 / Streamline 2.14.1; включать после отдельной проверки NR</td></tr>',1)
    body=body.replace('<tr><td>Ключевой параметр</td><td>OptiPatcher не использовать; при OptiFG HUDFix ON, Limit 2</td></tr>','<tr><td>Ключевой параметр</td><td>OptiPatcher не использовать; сначала сохранить штатный RR runtime 2.03.00; при OptiFG HUDFix ON, Limit 2</td></tr>',1)
    anchor='<li><a href="https://crimsondesert.pearlabyss.com/ru-RU/News/Notice/Detail?_boardNo=130" target="_blank">Crimson Desert — patch 2.02.00 (DLSS Frame Generation startup crash fix)</a></li>'
    assert anchor in body
    return body.replace(anchor,anchor+'<li><a href="https://crimsondesert.pearlabyss.com/en-us/News/Notice/Detail?_boardNo=131" target="_blank">Crimson Desert — patch 2.03.00 (Streamline 2.14.1 / DLSS Ray Reconstruction transformer)</a></li>',1)
update_section('crimson',crimson)

# Beast v1.0.12 changes DLSS/FG settings and is newer than OptiPatcher rolling.
def beast(body):
    anchor='''<div class="callout ok"><strong>Game update v1.0.11 — upscaling menu reorganized</strong>В патче v1.0.11 разработчики реорганизовали параметры upscaling, чтобы дефолты применялись по обнаруженной GPU. После обновления <strong>не переносите старое состояние меню автоматически</strong>: перед NR/FG тестом вручную выберите DLSS и убедитесь, что игра действительно использует DLSS input. Это не является отдельным подтверждением NR-fork.</div>'''
    add='''<div class="callout warn"><strong>Game update v1.0.12 — 17.09.2026: изменены DLSS / Frame Generation settings</strong>Патч теперь подстраивает доступные Frame Generation options под GPU <strong>RTX 40 / RTX 50</strong>; при <strong>DLSS-Dynamic</strong> и мониторе 120 Гц+ добавлен выбор target frame rate. После обновления заново проверьте игровые DLSS/FG параметры, не переносите старое состояние меню автоматически и первичный NR-тест выполняйте с <strong>FG OFF</strong>. Патч вышел после OptiPatcher rolling 11.09: также проверьте, что patcher действительно находит актуальные patterns; при отсутствии сигнатуры не форсируйте старые offsets.</div>'''
    assert anchor in body; body=body.replace(anchor,anchor+add,1)
    body=body.replace('<tr><td>Frame Generation</td><td>Native DLSSG после проверки NR; coupled с DLSS начиная с update 1.0.9</td></tr><tr><td>Ключевой параметр</td><td>DLSS input; при проблемах с текущим патчем — OptiPatcher rolling 11.09.2026+</td></tr>','<tr><td>Frame Generation</td><td>Native DLSSG после проверки NR; после v1.0.12 заново выбрать доступный RTX 50 FG option</td></tr><tr><td>Ключевой параметр</td><td>DLSS input; DLSS-Dynamic target FPS доступен на 120 Гц+, но для первичной NR-настройки оставить обычный Quality/рекомендуемый режим; проверить OptiPatcher patterns на v1.0.12</td></tr>',1)
    old='<div class="section step-section" id="beast-fg"><div class="section-title"><div class="step-num">3</div><h3>Frame Generation</h3></div><div class="section-body"><p>После стабильной проверки NR используйте штатный <strong>DLSS Frame Generation</strong>. В актуальной поддержке OptiPatcher DLSSG связан с выбранным DLSS-upscaler, поэтому оставьте игровой upscaler на DLSS; Smooth Motion и альтернативный FG — OFF.</p></div></div>'
    new='<div class="section step-section" id="beast-fg"><div class="section-title"><div class="step-num">3</div><h3>Frame Generation</h3></div><div class="section-body"><p>После стабильной проверки NR используйте штатный <strong>DLSS Frame Generation</strong>. Начиная с v1.0.12 игра сама адаптирует набор FG-options под RTX 40/50; для RTX 5080 заново выберите нужный native option после патча. В поддержке OptiPatcher DLSSG связан с выбранным DLSS-upscaler, поэтому оставьте игровой upscaler на DLSS; Smooth Motion и альтернативный FG — OFF. Если используете DLSS-Dynamic на дисплее 120 Гц+, v1.0.12 добавляет target frame rate — это отдельная игровая настройка и не заменяет NR Scale.</p></div></div>'
    assert old in body; body=body.replace(old,new,1)
    src='<li><a href="https://steamdb.info/patchnotes/25130977/" target="_blank">Beast of Reincarnation v1.0.11 — patch notes mirror</a></li>'
    assert src in body
    return body.replace(src,src+'<li><a href="https://steamdb.info/patchnotes/25337386/" target="_blank">Beast of Reincarnation v1.0.12 — 17.09.2026</a></li>',1)
update_section('beast',beast)

# STALKER 2 Patch 2.0.6 vs older OptiPatcher rolling patterns.
def stalker(body):
    anchor='''<div class="callout ok"><strong>OptiPatcher rolling 11.09.2026+</strong>Rolling Release содержит обновлённые паттерны для S.T.A.L.K.E.R. 2. Если stable <code>v0.41</code> на текущем патче игры не открывает DLSS/DLSSG inputs либо patcher перестал находить сигнатуру, используйте rolling build от 11 сентября или новее.</div>'''
    add='''<div class="callout warn"><strong>Patch 2.0.6 — 18.09.2026</strong>GSC выпустила небольшой crash-fix patch и отдельно предупреждает, что после обновления модификации могут перестать работать. Последний OptiPatcher rolling в момент проверки датирован 11.09, то есть старше game build 2.0.6. После обновления <strong>обязательно проверьте лог patcher/signature match</strong>; при отсутствии сигнатуры не форсируйте старый patch. Рекомендуемый DLSS route не меняется.</div>'''
    assert anchor in body; body=body.replace(anchor,anchor+add,1)
    body=body.replace('<tr><td>Ключевой параметр</td><td>Reflex ON; FSR3.1 input не рекомендуется; OptiPatcher rolling 11.09.2026+ для актуальных patterns</td></tr>','<tr><td>Ключевой параметр</td><td>Reflex ON; FSR3.1 input не рекомендуется; на game patch 2.0.6 перепроверить signature match — rolling 11.09 старше текущего build</td></tr>',1)
    marker='</ul></div></section>'
    assert marker in body
    return body.replace(marker,'<li><a href="https://steamdb.info/patchnotes/25382007/" target="_blank">S.T.A.L.K.E.R. 2 — Patch 2.0.6 / 18.09.2026</a></li>'+marker,1)
update_section('stalker2',stalker)

# KCD II community signal; keep clean route recommendation.
def kcd2(body):
    old='''<div class="callout warn"><strong>OptiScaler подтверждён; NR требует теста</strong>Wiki OptiScaler: тест 0.9.4 на Radeon 9070 XT, загрузчик dxgi.dll, рекомендован OptiFG → XeFG. Штатных Reflex и DLSS-FG нет. Инструкции для AMD/Intel со spoofing не переносите на RTX 5080. Совместимость NR + выбранного FG нужно проверить отдельно.</div>'''
    add='''<div class="callout warn"><strong>Community signal — 16.09.2026: DLSS5 + MFG в KCD II</strong>На Nexus обновлён отдельный community-пакет, автор которого сообщает рабочую комбинацию DLSS 5 + MFG и отдельно предупреждает о кратких визуальных сбоях/дублированных кадрах при резких переключениях камеры в диалогах. Это полезное подтверждение <strong>принципиальной реализуемости</strong> NR + FG в KCD II, но не подтверждение именно нашей чистой связки OptiScaler_DLSSNR + RTX 5080: пакет объединяет несколько компонентов, а Nexus помечает его файлы как <em>Some suspicious files</em>. Поэтому пакет не используется как базовый источник DLL; устанавливайте компоненты из репозиториев авторов и проверяйте NR → FG раздельно.</div>'''
    assert old in body; body=body.replace(old,old+add,1)
    needle='<p>В игре нет штатного DLSS-FG согласно compatibility-профилю.'
    assert needle in body; body=body.replace(needle,'<p>Community-профиль от 16.09 демонстрирует DLSS5 + MFG, но также описывает артефакты на резких dialogue/cutscene camera cuts. Поэтому даже при успешном MFG отдельно проверяйте диалоги и кат-сцены; это не повод переносить его bundled DLL в чистую установку.</p>'+needle,1)
    src='<li><a href="https://www.nexusmods.com/kingdomcomedeliverance2/mods/541" target="_blank" rel="noopener noreferrer">Авторская инструкция: путь к EXE в Steam, не подтверждение NR</a></li>'
    assert src in body
    return body.replace(src,src+'<li><a href="https://www.nexusmods.com/kingdomcomedeliverance2/mods/3630" target="_blank" rel="noopener noreferrer">Community compatibility signal: DLSS5 + MFG, updated 16.09.2026 (не использовать bundled files как baseline)</a></li>',1)
update_section('kcd2',kcd2)

footer='''<footer class="footer"><strong>Интерфейс v14:</strong> 29 игровых профилей, комплексная проверка 19.09.2026. DLSS5 Autopilot обновлён до <strong>2.0.1</strong>: первый route остаётся rule-based, а последующие варианты теперь ранжируются с учётом shared results; добавлены watcher реальных DLL/logs, DXVK exception и исправление ложного определения native DLSS по остаточным NGX-файлам. Shared compatibility feed — <strong>136 отчётов</strong> (18.09 20:24 UTC); Cyberpunk 2077 теперь имеет <strong>2/2</strong> для optiscaler и 1/0 для neural-upstream, Onimusha — 0/1 native и 0/1 optiscaler. DLSS5-Feeder: stable <strong>0.15.1</strong>, troubleshooting <strong>1.16.0-beta.4</strong> с windowless-host workaround для 32-bit exclusive fullscreen. Для 007: First Light учтён hotfix 1.2.1 с PT GPU crash/hang fixes; для Crimson Desert — patch 2.03.00 с NVIDIA Streamline 2.14.1 и новым transformer для DLSS Ray Reconstruction; для S.T.A.L.K.E.R. 2 — patch 2.0.6 с обязательной перепроверкой OptiPatcher signatures; для Beast of Reincarnation — v1.0.12 с GPU-aware FG options и DLSS-Dynamic target FPS на 120 Гц+; для Kingdom Come: Deliverance II добавлен community-сигнал DLSS5 + MFG с отдельным предупреждением о camera-cut artifacts и непроверенных bundled files. Без новых stable-релизов, требующих глобальной смены остальных маршрутов: OptiScaler_DLSSNR 0.2.0, OptiScaler 0.9.4, OptiPatcher Rolling 11.09, RE_DLSS5_Load_Mod 0.63, REFramework 1.5.9.1, ReShade 6.8.0, NVIDIA DLSS SDK 310.9.1; Game Ready остаётся 616.92 WHQL.</footer>'''
s,n=re.subn(r'<footer class="footer">.*?</footer>',footer,s,count=1,flags=re.S); assert n==1

m=re.search(r'const allGames\s*=\s*\[(.*?)\];',s,re.S); assert m
assert len(re.findall(r'\{\s*value:',m.group(1)))==29
assert s.count('Проверено: 19.09.2026')==27 and s.count('Источники: 19.09.2026')==2
for x in ['DLSS5 Autopilot v2.0.1','1.16.0-beta.4','Patch 2.03.00','Patch 2.0.6','Game update v1.0.12','kingdomcomedeliverance2/mods/3630','Интерфейс v14:']:
    assert x in s,x
assert '1.16.0-beta.3' not in s and 'Autopilot 1.9.0' not in s
p.write_text(s,encoding='utf-8')