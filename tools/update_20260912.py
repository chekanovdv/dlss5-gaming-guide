from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = s.replace('<strong>Обновлено:</strong> 10.09.2026', '<strong>Обновлено:</strong> 12.09.2026')
s = s.replace('Проверено: 10.09.2026', 'Проверено: 12.09.2026')

autopilot = '''<details class="autopilot-details" id="autopilot-note"><summary>DLSS5 Autopilot — когда он нужен?</summary><div class="autopilot-details-body">
<p><strong>Актуально: DLSS5 Autopilot v1.8.1 (10.09.2026).</strong> Это установщик и диагностический маршрутизатор для новых/проблемных игр; для уже настроенных игр сохраняйте game-specific профиль из этого справочника.</p>
<ul>
<li><strong>Driver 616.64+:</strong> на новых драйверах NVIDIA neural rendering чаще проходит через driver runtime; RenoDX DLSS5 add-on в маршрутах <code>feeder</code>/<code>native</code>/<code>bridge</code> может падать на evaluate. Для <strong>64-bit D3D11/D3D12</strong> Autopilot 1.8.1 рекомендует сначала попробовать экспериментальный <strong>standalone route</strong>, и только затем рассматривать откат драйвера.</li>
<li><strong>Standalone route:</strong> имеет собственный feed и не загружает <code>renodx-dlss5</code>; пока считается экспериментальным и выводит результат через собственное окно. Для 32-bit, DX9/DX10, Vulkan и OpenGL этот маршрут не предлагается.</li>
<li><strong>OptiScaler route:</strong> исправлена ссылка «update available», которая ранее могла вести на mainline OptiScaler без Neural Rendering. Если выбран FSR/XeSS input, этот upscaler должен реально включаться в настройках самой игры.</li>
<li><strong>Vulkan detection:</strong> игры Vulkan с NVIDIA crash library больше не определяются ошибочно как D3D12.</li>
<li><strong>MFG/cache:</strong> ошибка загрузки Multi Frame Generation больше не срывает всю установку, а повреждённый cached download автоматически отбрасывается.</li>
<li><strong>Diagnostics:</strong> исправлены ложные диагнозы «старый драйвер», «OptiScaler не загрузился» и случаи, когда игра с собственным DLSS определялась как игра без DLSS.</li>
<li><strong>Bridge:</strong> для игр без собственного DLSS Autopilot теперь корректно сохраняет <code>synth_after</code> в <code>dlss5-bridge.cfg</code>; старую bridge-установку такого типа следует переустановить через 1.8.1.</li>
</ul>
<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v1.8.1" target="_blank">DLSS5 Autopilot v1.8.1 — changelog</a></p>
</div></details>'''

s, n = re.subn(r'<details class="autopilot-details" id="autopilot-note">.*?</details>', autopilot, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Autopilot block not found')

s = s.replace('DLSS5 Autopilot v1.8.0', 'DLSS5 Autopilot v1.8.1')
s = s.replace('releases/tag/v1.8.0', 'releases/tag/v1.8.1')

def patch_section(html, sid, fn):
    pattern = rf'(<section class="tab-panel" id="{re.escape(sid)}">)(.*?)(</section>)'
    m = re.search(pattern, html, flags=re.S)
    if not m:
        raise SystemExit(f'Section {sid} not found')
    block = m.group(2)
    return html[:m.start()] + m.group(1) + fn(block) + m.group(3) + html[m.end():]

def onimusha(block):
    note = '<div class="callout warn"><strong>Если v0.63 не запускается</strong>v0.63 остаётся текущим официальным релизом. При этом в пользовательских отчётах по Onimusha есть системы, где v0.62/v0.63 не загружаются, а <strong>v0.59 работает стабильно</strong>. Сначала исключите конфликт proxy-DLL и полностью удалите D18; если проблема сохраняется — используйте v0.59 как проверенный fallback для этой конкретной системы, не смешивая версии.</div>'
    if 'Если v0.63 не запускается' not in block:
        m = re.search(r'(<div class="section step-section">\s*<div class="section-title"><div class="step-num">5</div>)', block)
        if not m:
            raise SystemExit('Onimusha step 5 marker not found')
        block = block[:m.start()] + note + '\n' + block[m.start():]
    return block

s = patch_section(s, 'onimusha', onimusha)

feeder_warning = '<div class="callout warn"><strong>Драйвер 616.64+ / Autopilot 1.8.1</strong>Для RTX 5080 на новых драйверах RenoDX DLSS5 add-on в Feeder-route может падать на evaluate. Если это происходит в 64-bit D3D11/D3D12, сначала попробуйте <strong>Autopilot standalone route</strong> перед откатом драйвера. Стабильной версией Feeder остаётся <strong>0.15.1</strong>; <strong>1.16.0-beta.1</strong> используйте только для ретеста свежих багов с логами.</div>'
for sid in ('batman', 'mafiade', 'nier'):
    def add_feeder(block, warning=feeder_warning):
        if 'Драйвер 616.64+ / Autopilot 1.8.1' not in block:
            block = block.replace('<div class="status-strip">', warning + '<div class="status-strip">', 1)
        return block
    s = patch_section(s, sid, add_feeder)

def cyberpunk(block):
    warning = '<div class="callout warn"><strong>RTX 5080 + Frame Generation</strong>Есть воспроизводимые пользовательские отчёты о GPU page fault/device removal при многократном переключении Neural Rendering или изменении NR Scale после включения native/driver FG. Настройте NR при <strong>FG OFF</strong>, затем включите один FG-механизм и во время игровой сессии не переключайте F8/NR Scale без необходимости. При crash выключите FG и перезапустите игру.</div>'
    if 'RTX 5080 + Frame Generation' not in block:
        block = block.replace('<div class="status-strip">', warning + '<div class="status-strip">', 1)
    return block

s = patch_section(s, 'cyberpunk', cyberpunk)

footer = '<footer class="footer"><strong>Интерфейс v9:</strong> 27 игровых профилей; проверено 12.09.2026. Обновлён DLSS5 Autopilot до 1.8.1 и рекомендации для NVIDIA 616.64+; DLSS5-Feeder 0.15.1 остаётся стабильным, 1.16.0-beta.1 отмечен как troubleshooting build; для Onimusha добавлен fallback v0.59 при проблемах v0.63; для Cyberpunk добавлено предупреждение по NR toggle/FG на RTX 5080.</footer>'
s, n = re.subn(r'<footer class="footer">.*?</footer>', footer, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Footer not found')

p.write_text(s, encoding='utf-8')
print(f'Updated index.html: {p.stat().st_size} bytes')
