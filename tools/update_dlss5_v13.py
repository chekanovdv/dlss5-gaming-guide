from pathlib import Path
import re, json
src=Path('index.html')
out=Path('index.html')
text=src.read_text(encoding='utf-8')
orig=text

text=text.replace('<span class="badge"><strong>Обновлено:</strong> 16.09.2026</span>', '<span class="badge"><strong>Обновлено:</strong> 17.09.2026</span>')
text=text.replace('Проверено: 15.09.2026', 'Проверено: 17.09.2026')

new_auto='''<details class="autopilot-details" id="autopilot-note"><summary>DLSS5 Autopilot — когда он нужен?</summary><div class="autopilot-details-body">
<p><strong>Актуально: DLSS5 Autopilot v1.9.0 (15.09.2026).</strong> Это установщик, диагностический маршрутизатор и инструмент измерения стоимости Neural Rendering; для уже настроенных игр сохраняйте game-specific профиль из этого справочника.</p>
<ul>
<li><strong>NVIDIA driver:</strong> актуальный Game Ready по состоянию на 17.09.2026 — <strong>616.92 WHQL</strong>; минимум для текущего DLSS5 toolchain — <code>616.56</code>.</li>
<li><strong>Route policy 1.9.0:</strong> базовая логика маршрутизации относительно 1.8.2 не изменилась. Для игр <strong>без собственного DLSS</strong> на драйверах <code>616.64+</code> и 64-bit D3D11/D3D12 Autopilot рекомендует <strong>standalone-dlssnr</strong>, если он доступен; <code>feeder</code> остаётся fallback. Причина — частые faults <code>renodx-dlss5</code> внутри driver NGX runtime на 616.64+. Откат на 616.56 остаётся резервным вариантом.</li>
<li><strong>Игры со штатным DLSS:</strong> D3D12 обычно получает <code>optiscaler</code> первым выбором, <code>native</code> и <code>neural-upstream</code> доступны как альтернативы; D3D11 со штатным DLSS использует <code>bridge</code>. <code>neural-upstream</code> запускает NR до апскейла; при DLSS Frame Generation cadence следует ставить <strong>Quality</strong>.</li>
<li><strong>AUTOPILOT в 1.9.0:</strong> режим теперь формально выполняет цикл «установить → запустить → проверить реально загруженные DLL → при неудаче перейти к следующему маршруту» максимум для трёх маршрутов. Игры с anti-cheat и launcher EXE автоматически не запускаются.</li>
<li><strong>NR Scale / work area:</strong> для <code>optiscaler</code> Model Resolution остаётся главным регулятором; для Feeder 64-bit D3D11 — work area. Начиная с 1.9.0 Autopilot читает измерения из логов: для OptiScaler достаточно одной измеренной сессии для оценки model cost, а для Feeder требуется две сессии с разницей work area не менее 5 пунктов. Если для конкретной игры накоплено ≥3 успешных измеренных результата на маршруте, используйте их как стартовую точку вместо общего процента из таблицы.</li>
<li><strong>DLSS runtimes:</strong> официальный NVIDIA DLSS SDK — <strong>310.9.1</strong> (SR/RR, включая Ray Reconstruction Transformer Mode / Preset F). <strong>DLSS Neural Rendering runtime <code>nvngx_dlssnr.dll</code> для RTX 50 остаётся отдельным runtime поколения 310.8.0</strong> и не является содержимым публичного DLSS SDK.</li>
<li><strong>DLSS5-Feeder:</strong> стабильная рекомендация остаётся <strong>0.15.1</strong>. Для troubleshooting доступен <strong>1.16.0-beta.3 (16.09.2026)</strong>: он включает beta.2 D3D12/Vulkan fixes, увеличивает ожидание 32-bit host pipe с 15 до 60 секунд и улучшает диагностику multi-GPU fence/import и 32-bit overlay input. Beta используйте только для ретеста конкретной проблемы с логами.</li>
<li><strong>Shared compatibility feed:</strong> база сгенерирована <strong>16.09.2026 17:58 UTC</strong> и содержит <strong>99 отчётов</strong>. Для профилей справочника: 007 First Light — <code>optiscaler</code> <strong>1 success / 0 fail</strong>; Cyberpunk 2077 — <code>optiscaler</code> <strong>1 / 2</strong> и <code>neural-upstream</code> <strong>1 / 0</strong>; Starfield — <code>neural-upstream</code> <strong>0 / 1</strong>; Onimusha — <code>optiscaler</code> <strong>0 / 1</strong>; RDR2 — <code>optiscaler</code> <strong>0 / 1</strong>. Единичные отчёты — ориентир для A/B, а не универсальный verdict.</li>
</ul>
<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v1.9.0" target="_blank">DLSS5 Autopilot v1.9.0 — changelog</a></p>
<p><a href="https://github.com/jlrouzies-fr/DLSS5-Feeder/releases/tag/v1.16.0-beta.3" target="_blank">DLSS5-Feeder 1.16.0-beta.3 — troubleshooting build</a></p>
<p><a href="https://github.com/NVIDIA/DLSS/releases/tag/v310.9.1" target="_blank">NVIDIA DLSS SDK 310.9.1</a></p>
<p><a href="https://www.nvidia.com/en-sg/geforce/news/wardogs-aniimo-007-first-light-path-tracing-geforce-game-ready-driver/" target="_blank">NVIDIA Game Ready 616.92 WHQL — 09.09.2026</a></p>
</div></details>'''
text,n=re.subn(r'<details class="autopilot-details" id="autopilot-note">.*?</details>', new_auto, text, count=1, flags=re.S)
assert n==1, f'autopilot replace {n}'

text=text.replace('DLSS5 Autopilot 1.8.2 → standalone-dlssnr', 'DLSS5 Autopilot 1.9.0 → standalone-dlssnr')
text=text.replace('Driver 616.64+ — route изменён в Autopilot 1.8.2', 'Autopilot 1.9.0 / Driver 616.64+ — route policy сохраняется')

old_beta='''<div class="callout ok"><strong>DLSS5-Feeder 1.16.0-beta.2 — 14.09.2026</strong>Новая prerelease-сборка исправляет D3D12 stale-output/Close() failure, 64-bit crash dumps, ложный off-thread Present stop на D3D12/Vulkan, version reporting renodx-dlss5 и verifier. Эти fixes ещё не были повторно протестированы авторами во всех затронутых играх. Для ручного стабильного fallback сохраняйте <strong>0.15.1</strong>; beta.2 используйте для ретеста конкретной проблемы с логами.</div>'''
new_beta='''<div class="callout ok"><strong>DLSS5-Feeder 1.16.0-beta.3 — 16.09.2026</strong>Новая prerelease-сборка включает beta.2 D3D12/Vulkan fixes, увеличивает ожидание 32-bit host pipe с <strong>15 до 60 секунд</strong>, улучшает диагностику multi-GPU cross-process fence и логирование ввода 32-bit overlay. Для ручного стабильного fallback сохраняйте <strong>0.15.1</strong>; beta.3 используйте только для ретеста конкретной проблемы и сохраняйте логи.</div>'''
count=text.count(old_beta)
assert count==3, f'beta callout count {count}'
text=text.replace(old_beta,new_beta)

def update_section(text, sid, fn):
    pat=rf'<section class="tab-panel" id="{re.escape(sid)}">.*?</section>'
    m=re.search(pat,text,re.S)
    assert m, sid
    sec=m.group(0)
    new=fn(sec)
    assert new!=sec, f'no change {sid}'
    return text[:m.start()]+new+text[m.end():]

def upd_007(sec):
    sec=re.sub(r'<div class="callout ok"><strong>15\.09\.2026 — Path Tracing \+ DLSS 4\.5 Ray Reconstruction</strong>.*?</div>',
'''<div class="callout ok"><strong>15.09.2026 — Path Tracing + DLSS 4.5 Ray Reconstruction уже доступны</strong>Обновление вышло: NVIDIA подтверждает live Path Tracing и DLSS Ray Reconstruction для 007: First Light. Для текущей сборки проверяйте цепочку поэтапно: <strong>NR при RR/FG OFF → RR ON → Dynamic MFG последним</strong>. Подтверждение обычного OptiScaler не считается подтверждением <strong>OptiScaler_DLSSNR + Path Tracing/RR/MFG</strong> — NR-fork нужно проверять отдельно по <code>OptiScaler.log</code> и A/B.</div>''', sec, count=1, flags=re.S)
    sec=re.sub(r'<div class="callout ok"><strong>Autopilot: подтверждённый запуск</strong>.*?</div>',
'''<div class="callout ok"><strong>Autopilot shared result</strong>В актуальном feed (16.09, 99 отчётов) для 007 First Light остаётся <strong>1 success / 0 fail</strong> на <code>optiscaler</code> и драйвере 616.92. Этот результат получен для маршрута в целом и <strong>не доказывает</strong> стабильность NR-fork одновременно с новым Path Tracing, RR и Dynamic MFG.</div>''', sec, count=1, flags=re.S)
    sec=sec.replace('<tr><td>Ray Tracing / RR</td><td>Path Tracing + DLSS 4.5 Ray Reconstruction — после фактической установки обновления 15.09.2026</td></tr>', '<tr><td>Ray Tracing / RR</td><td>Path Tracing + DLSS 4.5 Ray Reconstruction доступны; включать после отдельной проверки NR</td></tr>')
    sec=sec.replace('<tr><td>Frame Generation</td><td>Dynamic MFG / native DLSSG после стабильного NR; после 15.09 тестировать уже после RR</td></tr>', '<tr><td>Frame Generation</td><td>Dynamic MFG / native DLSSG — включать последним после стабильных NR и RR</td></tr>')
    sec=sec.replace('<p><strong>После патча 15.09:</strong> сначала FG OFF и RR OFF → проверить NR; затем RR ON → A/B; только последним включить Dynamic MFG.</p>', '<p><strong>Текущий PT/RR build:</strong> сначала FG OFF и RR OFF → проверить NR; затем RR ON → A/B; только последним включить Dynamic MFG. Если проблема появляется только после RR или MFG, не приписывайте её NR без повторного теста предыдущего шага.</p>')
    sec=re.sub(r'<li><a href="https://www\.nvidia\.com/[^"]*007-first-light[^"]*" target="_blank">NVIDIA — Path Tracing update 15\.09\.2026</a></li>', '<li><a href="https://www.nvidia.com/en-ph/geforce/news/007-first-light-path-tracing-dlss-4-5-ray-reconstruction-update-out-now/" target="_blank">NVIDIA — Path Tracing + DLSS 4.5 Ray Reconstruction update out now</a></li>', sec)
    return sec
text=update_section(text,'007firstlight',upd_007)

def upd_beast(sec):
    insert='''<div class="callout ok"><strong>Game update v1.0.11 — upscaling menu reorganized</strong>В патче v1.0.11 разработчики реорганизовали параметры upscaling, чтобы дефолты применялись по обнаруженной GPU. После обновления <strong>не переносите старое состояние меню автоматически</strong>: перед NR/FG тестом вручную выберите DLSS и убедитесь, что игра действительно использует DLSS input. Это не является отдельным подтверждением NR-fork.</div>'''
    idx=sec.find('<div class="status-strip">')
    assert idx!=-1
    sec=sec[:idx]+insert+sec[idx:]
    marker='<div class="card source-list" id="beast-sources"'
    mi=sec.find(marker); assert mi!=-1
    ul_end=sec.find('</ul>',mi); assert ul_end!=-1
    li='<li><a href="https://steamdb.info/patchnotes/25130977/" target="_blank">Beast of Reincarnation v1.0.11 — patch notes mirror</a></li>'
    sec=sec[:ul_end]+li+sec[ul_end:]
    return sec
text=update_section(text,'beast',upd_beast)

def upd_crimson(sec):
    insert='''<div class="callout ok"><strong>Patch 2.02.00 — исправлен запуск с DLSS Frame Generation</strong>Официальные patch notes от 11.09.2026 указывают исправление crash при запуске игры с включённым DLSS Frame Generation. На актуальной версии native DLSSG можно ретестировать после стабильного NR, но диагностику по-прежнему начинайте с <strong>FG OFF</strong> и включайте FG только после подтверждения базового NR.</div>'''
    idx=sec.find('<div class="status-strip">'); assert idx!=-1
    sec=sec[:idx]+insert+sec[idx:]
    marker='<div class="card source-list" id="crimson-sources"'
    mi=sec.find(marker); assert mi!=-1
    ul_end=sec.find('</ul>',mi); assert ul_end!=-1
    li='<li><a href="https://crimsondesert.pearlabyss.com/ru-RU/News/Notice/Detail?_boardNo=130" target="_blank">Crimson Desert — patch 2.02.00 (DLSS Frame Generation startup crash fix)</a></li>'
    sec=sec[:ul_end]+li+sec[ul_end:]
    return sec
text=update_section(text,'crimson',upd_crimson)

def upd_cyber(sec):
    old=re.search(r'<div class="callout warn"><strong>Autopilot shared results</strong>.*?</div>',sec,re.S)
    assert old
    new='''<div class="callout warn"><strong>Autopilot shared results — 16.09 / 99 reports</strong>Для Cyberpunk 2077 текущий feed показывает <code>optiscaler</code> <strong>1 success / 2 fail</strong> и <code>neural-upstream</code> <strong>1 success / 0 fail</strong>. Один успешный upstream-report полезен как A/B альтернатива, но его недостаточно, чтобы автоматически менять основной ручной профиль OptiScaler_DLSSNR. Проверяйте конкретную систему по логам и держите FG OFF во время настройки NR.</div>'''
    return sec[:old.start()]+new+sec[old.end():]
text=update_section(text,'cyberpunk',upd_cyber)

def upd_starfield(sec):
    anchor='<p>Рабочая схема: <strong>DLSS input → OptiScaler_DLSSNR → DLSS5 NR</strong>. FSR3 inputs для OptiScaler в Starfield использовать не следует — они отмечены как приводящие к crash.</p>'
    assert anchor in sec
    call='''<div class="callout warn"><strong>Autopilot shared result — neural-upstream</strong>В feed от 16.09 для Starfield есть <strong>0 success / 1 fail</strong> на <code>neural-upstream</code>. Единичный fail не доказывает общую несовместимость, но текущий основной маршрут <strong>DLSS input → OptiScaler_DLSSNR</strong> сохраняется; upstream используйте только как диагностический A/B.</div>'''
    return sec.replace(anchor, anchor+call,1)
text=update_section(text,'starfield',upd_starfield)

new_footer='''<footer class="footer"><strong>Интерфейс v13:</strong> 29 игровых профилей, комплексная проверка 17.09.2026. DLSS5 Autopilot обновлён до <strong>1.9.0</strong>: route policy 1.8.2 сохранена, но добавлен полноценный цикл AUTOPILOT до трёх маршрутов и измеряемая настройка Model Resolution/work area. Shared compatibility feed — <strong>99 отчётов</strong> (16.09 17:58 UTC); отдельно отражены новые route-specific данные Cyberpunk 2077 и Starfield. DLSS5-Feeder: stable <strong>0.15.1</strong>, troubleshooting <strong>1.16.0-beta.3</strong> (16.09) с 60-секундным 32-bit host timeout и расширенной диагностикой. Для 007: First Light учтён уже вышедший Path Tracing + DLSS 4.5 Ray Reconstruction update; обычная совместимость OptiScaler не приравнивается к подтверждению NR-fork + RR/MFG. Для Beast of Reincarnation учтён v1.0.11 с реорганизованными upscaling defaults, для Crimson Desert — patch 2.02.00 с исправлением startup crash при DLSS Frame Generation. Без новых stable-релизов, требующих смены маршрутов: OptiScaler_DLSSNR 0.2.0, OptiScaler 0.9.4, OptiPatcher Rolling 11.09, RE_DLSS5_Load_Mod 0.63, REFramework 1.5.9.1, ReShade 6.8.0, NVIDIA DLSS SDK 310.9.1.</footer>'''
text,n=re.subn(r'<footer class="footer">.*?</footer>',new_footer,text,count=1,flags=re.S)
assert n==1
text=text.replace('Интерфейс v12', 'Интерфейс v13')
out.write_text(text,encoding='utf-8')

m=re.search(r'const allGames\s*=\s*\[(.*?)\];', text, re.S)
assert m
items=re.findall(r'''\{\s*value:\s*['\"]([^'\"]+)['\"],\s*label:\s*['\"]([^'\"]+)['\"]''', m.group(1))
assert len(items)==29, len(items)
assert text.count('<section class="tab-panel" id=')==29
assert 'DLSS5 Autopilot v1.9.0' in text and '1.16.0-beta.3' in text and '99 отчётов' in text
print('updated index.html', len(text), 'chars; games=',len(items))
