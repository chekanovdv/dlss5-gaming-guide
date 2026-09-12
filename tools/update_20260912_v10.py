from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# DLSS5 Autopilot: shared compatibility feed updated after v9 was published.
needle = '<li><strong>Bridge:</strong> для игр без собственного DLSS Autopilot теперь корректно сохраняет <code>synth_after</code> в <code>dlss5-bridge.cfg</code>; старую bridge-установку такого типа следует переустановить через 1.8.1.</li>'
insert = needle + '\n<li><strong>Shared compatibility feed (12.09.2026, 20:27 UTC):</strong> база Autopilot выросла до <strong>56 отчётов</strong>. Среди профилей этого справочника появились новые данные: Cyberpunk 2077 — OptiScaler <strong>1 success / 1 fail</strong> на 616.56; Onimusha: Way of the Sword — OptiScaler <strong>0 / 1</strong> на 616.92; Red Dead Redemption 2 — OptiScaler <strong>0 / 1</strong> (одиночный отчёт без зафиксированной версии драйвера). Это пользовательская статистика, а не запрет маршрута: при уже рабочей ручной конфигурации не меняйте route только из-за одного отчёта.</li>'
assert needle in s
s = s.replace(needle, insert, 1)

needle = '<li><strong>Driver 616.64+:</strong> на новых драйверах NVIDIA neural rendering чаще проходит через driver runtime; RenoDX DLSS5 add-on в маршрутах <code>feeder</code>/<code>native</code>/<code>bridge</code> может падать на evaluate. Для <strong>64-bit D3D11/D3D12</strong> Autopilot 1.8.1 рекомендует сначала попробовать экспериментальный <strong>standalone route</strong>, и только затем рассматривать откат драйвера.</li>'
replace = '<li><strong>NVIDIA driver:</strong> актуальный Game Ready по состоянию на 12.09.2026 — <strong>616.92 WHQL</strong>; минимум для текущего DLSS5 toolchain — <code>616.56</code>. Начиная с 616.64 neural rendering чаще проходит через driver runtime; RenoDX DLSS5 add-on в маршрутах <code>feeder</code>/<code>native</code>/<code>bridge</code> может падать на evaluate. Для <strong>64-bit D3D11/D3D12</strong> Autopilot 1.8.1 рекомендует сначала попробовать экспериментальный <strong>standalone route</strong>, и только затем рассматривать откат драйвера.</li>'
assert needle in s
s = s.replace(needle, replace, 1)

needle = '<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v1.8.1" target="_blank">DLSS5 Autopilot v1.8.1 — changelog</a></p>'
replace = needle + '\n<p><a href="https://www.nvidia.com/en-in/geforce/news/wardogs-aniimo-007-first-light-path-tracing-geforce-game-ready-driver/" target="_blank">NVIDIA Game Ready 616.92 WHQL — 09.09.2026</a></p>'
assert needle in s
s = s.replace(needle, replace, 1)

# RDR2: one new failed shared result. Keep the manual ASI route as the recommended profile.
needle = '''<div class="callout warn">
<strong>Важно</strong>
          Не используйте эту конфигурацию в Red Dead Online. Для тестирования модов запускайте Story Mode.
        </div>'''
replace = needle + '<div class="callout warn"><strong>Новый отчёт Autopilot</strong>В shared compatibility feed от 12.09 появился один неуспешный отчёт для <code>optiscaler</code> в RDR2. Это недостаточно для признания маршрута несовместимым; текущий ручной профиль <strong>ASI → Ultimate ASI Loader → OptiPatcher</strong> остаётся основным. При сбое сохраняйте <code>OptiScaler.log</code> и не переходите на другой route без диагностики.</div>'
assert needle in s
s = s.replace(needle, replace, 1)

# Onimusha: new 616.92 failed OptiScaler result; current RE-specific loader remains preferred.
needle = '''<div class="callout warn">
<strong>Не смешивать загрузчики</strong>
        Если ранее устанавливался D18 / мод №57, полностью удалите его файлы перед установкой RE_DLSS5_Load_Mod. Одновременно использовать D18 и RE_DLSS5_Load_Mod не следует.
      </div>'''
replace = needle + '<div class="callout warn"><strong>Autopilot / driver 616.92</strong>В shared compatibility feed от 12.09 зафиксирован один неуспешный запуск <code>optiscaler</code>-route для Onimusha на драйвере 616.92. Поэтому для этого профиля по-прежнему предпочтителен описанный ниже <strong>REFramework + RE_DLSS5_Load_Mod</strong>, а Autopilot/OptiScaler следует использовать только как отдельный диагностический эксперимент.</div>'
assert needle in s
s = s.replace(needle, replace, 1)

# Cyberpunk: shared data is now split success/fail on the same driver.
needle = '<div class="callout warn"><strong>RTX 5080 + Frame Generation</strong>Есть воспроизводимые пользовательские отчёты о GPU page fault/device removal при многократном переключении Neural Rendering или изменении NR Scale после включения native/driver FG. Настройте NR при <strong>FG OFF</strong>, затем включите один FG-механизм и во время игровой сессии не переключайте F8/NR Scale без необходимости. При crash выключите FG и перезапустите игру.</div>'
replace = needle + '<div class="callout warn"><strong>Autopilot shared results</strong>К 12.09 база Autopilot содержит для Cyberpunk 2077 на драйвере 616.56 один успешный и один неуспешный результат <code>optiscaler</code>-route. Это подтверждает необходимость A/B и логов на конкретной системе: не считайте один успешный/неуспешный запуск универсальной совместимостью.</div>'
assert needle in s
s = s.replace(needle, replace, 1)

# Beast of Reincarnation: stable 0.41 is supported, but current rolling has updated patterns.
needle = '<div class="callout warn"><strong>Recommended</strong>FSR3 input может приводить к crash; для RTX 5080 используйте DLSS.</div>'
replace = needle + '<div class="callout ok"><strong>OptiPatcher: актуальные patterns</strong>Stable <code>v0.41</code> уже поддерживает Beast of Reincarnation, но rolling build от <strong>11.09.2026</strong> содержит дополнительные обновления поддержки. Начиная с game update 1.0.9 DLSS и DLSS Frame Generation связаны; если текущий build не открывает DLSSG корректно, используйте свежий rolling OptiPatcher и выбирайте <strong>DLSS</strong> как игровой upscaler.</div>'
assert needle in s
s = s.replace(needle, replace, 1)
s = s.replace('<div class="metric"><div class="label">FG</div><div class="value">После проверки NR</div></div>', '<div class="metric"><div class="label">FG</div><div class="value">Native DLSSG после NR</div></div>', 1)
s = s.replace('<tr><td>Frame Generation</td><td>После проверки NR</td></tr><tr><td>Ключевой параметр</td><td>FSR3 input OFF</td></tr>', '<tr><td>Frame Generation</td><td>Native DLSSG после проверки NR; coupled с DLSS начиная с update 1.0.9</td></tr><tr><td>Ключевой параметр</td><td>DLSS input; при проблемах с текущим патчем — OptiPatcher rolling 11.09.2026+</td></tr>', 1)
s = s.replace('<div class="section step-section" id="beast-fg"><div class="section-title"><div class="step-num">3</div><h3>Frame Generation</h3></div><div class="section-body"><p>После проверки NR. Включайте только после стабильной работы NR; Smooth Motion оставьте OFF, если используется другой FG.</p></div></div>', '<div class="section step-section" id="beast-fg"><div class="section-title"><div class="step-num">3</div><h3>Frame Generation</h3></div><div class="section-body"><p>После стабильной проверки NR используйте штатный <strong>DLSS Frame Generation</strong>. В актуальной поддержке OptiPatcher DLSSG связан с выбранным DLSS-upscaler, поэтому оставьте игровой upscaler на DLSS; Smooth Motion и альтернативный FG — OFF.</p></div></div>', 1)
s = s.replace('</ul></div></section><section class="tab-panel" id="indiana">', '<li><a href="https://github.com/optiscaler/OptiPatcher/releases/tag/rolling" target="_blank">OptiPatcher Rolling Release</a></li></ul></div></section><section class="tab-panel" id="indiana">', 1)

# STALKER 2: rolling has refreshed patterns for current game builds.
needle = '<div class="callout warn"><strong>Recommended</strong>FSR3.1 upscaling input показывает худшее качество; для RTX 5080 используйте DLSS.</div>'
replace = needle + '<div class="callout ok"><strong>OptiPatcher rolling 11.09.2026+</strong>Rolling Release содержит обновлённые паттерны для S.T.A.L.K.E.R. 2. Если stable <code>v0.41</code> на текущем патче игры не открывает DLSS/DLSSG inputs либо patcher перестал находить сигнатуру, используйте rolling build от 11 сентября или новее.</div>'
assert needle in s
s = s.replace(needle, replace, 1)
s = s.replace('<tr><td>Ключевой параметр</td><td>Reflex ON; FSR3.1 input не рекомендуется</td></tr>', '<tr><td>Ключевой параметр</td><td>Reflex ON; FSR3.1 input не рекомендуется; OptiPatcher rolling 11.09.2026+ для актуальных patterns</td></tr>', 1)
s = s.replace('</ul></div></section><section class="tab-panel" id="splitfiction">', '<li><a href="https://github.com/optiscaler/OptiPatcher/releases/tag/rolling" target="_blank">OptiPatcher Rolling Release</a></li></ul></div></section><section class="tab-panel" id="splitfiction">', 1)

# Resonance: support was added after v0.41, so the optional patcher requires rolling or a future stable.
needle = '<div class="callout warn"><strong>Recommended / recent support</strong>OptiPatcher support добавлен недавно; при проблемах сначала проверьте чистый OptiScaler route.</div>'
replace = '<div class="callout warn"><strong>Recommended / recent support</strong>Поддержка Resonance добавлена <strong>после stable OptiPatcher v0.41</strong>. Если используете OptiPatcher, берите <strong>Rolling Release от 11.09.2026 или новее</strong>; иначе оставьте чистый OptiScaler route.</div>'
assert needle in s
s = s.replace(needle, replace, 1)
s = s.replace('<tr><td>Ключевой параметр</td><td>DLSS Quality; Preset M при необходимости</td></tr>', '<tr><td>Ключевой параметр</td><td>DLSS Quality; Preset M при необходимости; OptiPatcher только rolling 11.09.2026+ или будущий stable с Resonance support</td></tr>', 1)

pattern = r'(<section class="tab-panel" id="resonance">)(.*?)(</section>)'
m = re.search(pattern, s, re.S)
assert m
block = m.group(2)
needle = '<p>Добавьте оригинальный RTX 50 <code>nvngx_dlssnr.dll</code>. Установите OptiPatcher в OptiScaler\\plugins\\ и включите LoadAsiPlugins=true.</p>'
assert needle in block
block = block.replace(needle, '<p>Добавьте оригинальный RTX 50 <code>nvngx_dlssnr.dll</code>. Если нужен OptiPatcher, используйте <strong>Rolling Release 11.09.2026+</strong>, поместите <code>OptiPatcher.asi</code> в <code>OptiScaler\\plugins\\</code> и включите <code>LoadAsiPlugins=true</code>. Stable v0.41 выпущен до добавления поддержки Resonance.</p>', 1)
block = block.replace('<ul><li><a href="https://github.com/optiscaler/OptiPatcher/releases" target="_blank">Основной compatibility/source</a></li>', '<ul><li><a href="https://github.com/optiscaler/OptiPatcher/releases/tag/rolling" target="_blank">OptiPatcher Rolling Release — Resonance support</a></li>', 1)
s = s[:m.start()] + m.group(1) + block + m.group(3) + s[m.end():]

# Footer / component baseline.
footer = '<footer class="footer"><strong>Интерфейс v10:</strong> 27 игровых профилей; проверено 12.09.2026. Учтён Autopilot shared compatibility feed (56 отчётов, 12.09 20:27 UTC) с новыми результатами для RDR2, Onimusha и Cyberpunk; уточнены OptiPatcher rolling-паттерны для Beast of Reincarnation, S.T.A.L.K.E.R. 2 и Resonance: A Plague Tale Legacy. Базовые версии без новых релизов: OptiScaler_DLSSNR 0.2.0, OptiScaler 0.9.4, DLSS5 Autopilot 1.8.1, DLSS5-Feeder stable 0.15.1 / 1.16.0-beta.1 troubleshooting, RE_DLSS5_Load_Mod 0.63, ReShade 6.8.0.</footer>'
s, n = re.subn(r'<footer class="footer">.*?</footer>', footer, s, count=1, flags=re.S)
assert n == 1

assert s.count('<section class="tab-panel') == 27
for marker in ('game-finder', 'context-bar', 'step-section', 'copy-btn', '@media (max-width:760px)', 'Интерфейс v10'):
    assert marker in s

p.write_text(s, encoding='utf-8')
print('Updated index.html', p.stat().st_size)
