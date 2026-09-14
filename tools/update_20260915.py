from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Review stamp after checking the production-derived list of all 27 profiles.
s = s.replace('<strong>Обновлено:</strong> 12.09.2026', '<strong>Обновлено:</strong> 15.09.2026')
s = s.replace('Проверено: 12.09.2026', 'Проверено: 15.09.2026')

# DLSS5 Autopilot 1.8.2 + current route policy/runtime state.
autopilot = '''<details class="autopilot-details" id="autopilot-note"><summary>DLSS5 Autopilot — когда он нужен?</summary><div class="autopilot-details-body">
<p><strong>Актуально: DLSS5 Autopilot v1.8.2 (12.09.2026).</strong> Это установщик и диагностический маршрутизатор для новых/проблемных игр; для уже настроенных игр сохраняйте game-specific профиль из этого справочника.</p>
<ul>
<li><strong>NVIDIA driver:</strong> актуальный Game Ready по состоянию на 15.09.2026 — <strong>616.92 WHQL</strong>; минимум для текущего DLSS5 toolchain — <code>616.56</code>.</li>
<li><strong>Route policy 1.8.2:</strong> для игр <strong>без собственного DLSS</strong> на драйверах <code>616.64+</code> и 64-bit D3D11/D3D12 Autopilot теперь рекомендует <strong>standalone-dlssnr</strong>, если маршрут доступен. Причина: <code>native</code>, <code>bridge</code> и <code>feeder</code> используют <code>renodx-dlss5</code>, который на 616.64+ в заметном числе игр падает внутри driver NGX runtime. Standalone имеет собственный feed и не загружает этот add-on. Откат на 616.56 остаётся резервным вариантом.</li>
<li><strong>Игры со штатным DLSS:</strong> автоматическая рекомендация не переводится на standalone. D3D12 обычно получает <code>optiscaler</code> первым выбором, <code>native</code> и <code>neural-upstream</code> доступны как альтернативы; D3D11 со штатным DLSS использует <code>bridge</code>. <code>neural-upstream</code> запускает NR до апскейла; при DLSS Frame Generation cadence следует ставить <strong>Quality</strong>.</li>
<li><strong>FPS / NR dial:</strong> у <code>optiscaler</code> основной регулятор — Model Resolution <strong>25–100%</strong> (стоимость приблизительно масштабируется с квадратом разрешения); у Feeder 64-bit D3D11 — work area <strong>50–100%</strong>; standalone снижает нагрузку через reduced-resolution fullscreen/borderless режим.</li>
<li><strong>DLSS runtimes:</strong> официальный публичный NVIDIA DLSS SDK обновлён до <strong>310.9.1</strong> (08.09.2026): добавлен DLSS Ray Reconstruction Transformer Mode / Preset F и исправления стабильности. Это SR/RR SDK; <strong>DLSS Neural Rendering runtime <code>nvngx_dlssnr.dll</code> для RTX 50 остаётся 310.8.0</strong> и не входит в публичный DLSS SDK.</li>
<li><strong>Multi-frame generation:</strong> Autopilot 1.8.2 больше не перезаписывает занятое другим ASI-loader имя вроде Cyber Engine Tweaks <code>version.dll</code>; при подходящей структуре MFG unlock помещается в существующую папку plugins.</li>
<li><strong>Shared compatibility feed:</strong> актуальная база сгенерирована <strong>14.09.2026 20:18 UTC</strong> и содержит <strong>75 отчётов</strong>. Для профилей справочника: 007 First Light — <code>optiscaler</code> <strong>1 success / 0 fail</strong> на 616.92; Cyberpunk 2077 — <strong>1 / 2</strong> суммарно; Onimusha — <strong>0 / 1</strong> на 616.92; RDR2 — <strong>0 / 1</strong>. Это пользовательская статистика, а не универсальный verdict.</li>
</ul>
<p><a href="https://github.com/Kizzuwatnaa/DLSS5-Autopilot/releases/tag/v1.8.2" target="_blank">DLSS5 Autopilot v1.8.2 — changelog</a></p>
<p><a href="https://github.com/NVIDIA/DLSS/releases/tag/v310.9.1" target="_blank">NVIDIA DLSS SDK 310.9.1</a></p>
<p><a href="https://www.nvidia.com/en-sg/geforce/news/wardogs-aniimo-007-first-light-path-tracing-geforce-game-ready-driver/" target="_blank">NVIDIA Game Ready 616.92 WHQL — 09.09.2026</a></p>
</div></details>'''
s, n = re.subn(r'<details class="autopilot-details" id="autopilot-note">.*?</details>', autopilot, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Autopilot block not found')

# Global current-version references.
s = s.replace('DLSS5 Autopilot v1.8.1', 'DLSS5 Autopilot v1.8.2')
s = s.replace('Autopilot 1.8.1', 'Autopilot 1.8.2')
s = s.replace('releases/tag/v1.8.1', 'releases/tag/v1.8.2')
s = s.replace('1.16.0-beta.1', '1.16.0-beta.2')


def patch_section(html, sid, fn):
    pattern = rf'(<section class="tab-panel" id="{re.escape(sid)}">)(.*?)(</section>)'
    m = re.search(pattern, html, flags=re.S)
    if not m:
        raise SystemExit(f'Section {sid} not found')
    block = m.group(2)
    new_block = fn(block)
    return html[:m.start()] + m.group(1) + new_block + m.group(3) + html[m.end():]

# Current Autopilot feed has one successful 007/OptiScaler result on 616.92.
def patch_007(block):
    note = '<div class="callout ok"><strong>Autopilot: подтверждённый запуск</strong>В compatibility feed от 14.09 есть <strong>1 успешный запуск OptiScaler-route на драйвере 616.92</strong>. Это поддерживает текущий маршрут, но после установки Path Tracing/Ray Reconstruction update от 15.09 совместимость renderer нужно проверить повторно.</div>'
    if 'Autopilot: подтверждённый запуск' not in block:
        block = block.replace('<div class="status-strip">', note + '<div class="status-strip">', 1)
    block = block.replace('NVIDIA подтверждает обновление на 15 сентября. Текущий профиль (10.09) относится к версии до PT/RR. После патча заново проверьте цепочку в порядке: NR без FG → Ray Reconstruction → Dynamic MFG; не переносите старые выводы о совместимости на новый renderer без A/B.',
                          'NVIDIA и IO Interactive заявили Path Tracing + DLSS Ray Reconstruction update на 15 сентября. На момент этой проверки отдельный live changelog новой PC-сборки ещё не опубликован. После фактической установки обновления заново проверьте цепочку в порядке: NR без FG → Ray Reconstruction → Dynamic MFG; не переносите выводы старого renderer без A/B.')
    block = block.replace('Path Tracing + DLSS 4.5 Ray Reconstruction — с обновления 15.09.2026; до этой даты не применяется',
                          'Path Tracing + DLSS 4.5 Ray Reconstruction — после фактической установки обновления 15.09.2026')
    return block
s = patch_section(s, '007firstlight', patch_007)

# Compatibility feed changed Cyberpunk aggregate from 1/1 to 1/2.
def patch_cyberpunk(block):
    block = re.sub(r'<div class="callout warn"><strong>Autopilot shared results</strong>.*?</div>',
                   '<div class="callout warn"><strong>Autopilot shared results</strong>К 14.09 compatibility feed содержит для Cyberpunk 2077 <code>optiscaler</code>-route <strong>1 successful / 2 failed</strong> суммарно: на 616.56 — 1/1, плюс один fail на 610.88. Это не отменяет рабочий ручной профиль, но делает обязательными A/B и <code>OptiScaler.log</code> на конкретной системе.</div>',
                   block, count=1, flags=re.S)
    return block
s = patch_section(s, 'cyberpunk', patch_cyberpunk)

# Games without native DLSS: Autopilot 1.8.2 now recommends standalone-dlssnr on 616.64+.
feeder_beta_note = '<div class="callout ok"><strong>DLSS5-Feeder 1.16.0-beta.2 — 14.09.2026</strong>Новая prerelease-сборка исправляет D3D12 stale-output/Close() failure, 64-bit crash dumps, ложный off-thread Present stop на D3D12/Vulkan, version reporting renodx-dlss5 и verifier. Эти fixes ещё не были повторно протестированы авторами во всех затронутых играх. Для ручного стабильного fallback сохраняйте <strong>0.15.1</strong>; beta.2 используйте для ретеста конкретной проблемы с логами.</div>'


def patch_feeder_game(block, game_label):
    # Recommendation and driver note.
    block = block.replace('Рекомендуемый маршрут: <strong>DLSS5-Feeder v0.15.1 + ReShade</strong>.',
                          'Рекомендуемый маршрут на NVIDIA 616.64+: <strong>DLSS5 Autopilot 1.8.2 → standalone-dlssnr</strong>. Ручной fallback: <strong>DLSS5-Feeder v0.15.1 + ReShade</strong>.')
    block = block.replace('Рекомендуемый маршрут: <strong>DLSS5-Feeder + ReShade</strong>.',
                          'Рекомендуемый маршрут на NVIDIA 616.64+: <strong>DLSS5 Autopilot 1.8.2 → standalone-dlssnr</strong>. Ручной fallback: <strong>DLSS5-Feeder v0.15.1 + ReShade</strong>.')
    block = re.sub(r'<div class="callout warn"><strong>Драйвер 616\.64\+ / Autopilot 1\.8\.2</strong>.*?</div>',
                   '<div class="callout warn"><strong>Driver 616.64+ — route изменён в Autopilot 1.8.2</strong>Для 64-bit D3D11/D3D12 игры без собственного DLSS первым автоматическим маршрутом теперь является <strong>standalone-dlssnr</strong>. Feeder остаётся ручным fallback; откат на 616.56 — резерв, если standalone не подходит.</div>',
                   block, count=1, flags=re.S)
    if 'DLSS5-Feeder 1.16.0-beta.2 — 14.09.2026' not in block:
        block = block.replace('<div class="status-strip">', feeder_beta_note + '<div class="status-strip">', 1)

    # Summary/table text.
    block = block.replace('<div class="metric"><div class="label">Метод</div><div class="value">DLSS5-Feeder v0.15.1</div></div>',
                          '<div class="metric"><div class="label">Метод</div><div class="value">standalone-dlssnr / Feeder fallback</div></div>')
    block = block.replace('<tr><td>Маршрут</td><td>DLSS5-Feeder v0.15.1 + ReShade</td></tr>',
                          '<tr><td>Маршрут</td><td>Autopilot standalone-dlssnr на 616.64+; Feeder v0.15.1 + ReShade как manual fallback</td></tr>')
    block = block.replace('<tr><td>Маршрут</td><td>DLSS5-Feeder + ReShade</td></tr>',
                          '<tr><td>Маршрут</td><td>Autopilot standalone-dlssnr на 616.64+; Feeder v0.15.1 + ReShade как manual fallback</td></tr>')
    block = block.replace('<tr><td>Input</td><td>Synthetic DLAA contract</td></tr>',
                          '<tr><td>Input</td><td>Standalone own feed; Synthetic DLAA contract только для Feeder fallback</td></tr>')
    block = block.replace('<tr><td>DLSS5 Neural Rendering</td><td>ON через DLSS5-Feeder v0.15.1</td></tr>',
                          '<tr><td>DLSS5 Neural Rendering</td><td>ON через standalone-dlssnr; Feeder v0.15.1 как fallback</td></tr>')
    block = block.replace('<tr><td>DLSS5 Neural Rendering</td><td>ON</td></tr>',
                          '<tr><td>DLSS5 Neural Rendering</td><td>ON; standalone-dlssnr предпочтителен на 616.64+</td></tr>', 1)
    block = block.replace('ReShade Full Add-on + motion-vector provider; OptiScaler и Smooth Motion OFF',
                          'На 616.64+ сначала standalone-dlssnr; для Feeder fallback: ReShade Full Add-on + motion-vector provider; OptiScaler/Smooth Motion OFF')
    block = block.replace('LaunchPad MV → DLSS5 Feed → NR',
                          'На 616.64+ standalone-dlssnr; Feeder fallback: LaunchPad MV → DLSS5 Feed → NR')
    block = block.replace('MSAA/SSAA OFF; LaunchPad MV обязателен',
                          'На 616.64+ standalone-dlssnr; Feeder fallback: MSAA/SSAA OFF, LaunchPad MV обязателен')

    # Mark manual Feeder steps as fallback and update prerelease reference.
    block = block.replace('<h3>Установить DLSS5-Feeder v0.15.1</h3>', '<h3>Ручной fallback: установить DLSS5-Feeder v0.15.1</h3>')
    block = block.replace('<h3>Установка</h3></div><div class="section-body"><p><strong>Рекомендуемый способ — one-command installer из DLSS5-Feeder v0.15.1:</strong>',
                          '<h3>Установка</h3></div><div class="section-body"><p><strong>На 616.64+ сначала попробуйте Autopilot 1.8.2 → standalone-dlssnr. Ниже — ручной Feeder fallback.</strong></p><p><strong>Рекомендуемый способ для fallback — one-command installer из DLSS5-Feeder v0.15.1:</strong>')
    block = block.replace('<h3>Установка</h3></div><div class="section-body"><p>Установите ReShade Full Add-on Support, затем:',
                          '<h3>Установка</h3></div><div class="section-body"><p><strong>На 616.64+ сначала попробуйте Autopilot 1.8.2 → standalone-dlssnr. Ниже — ручной Feeder fallback.</strong></p><p>Установите ReShade Full Add-on Support, затем:')
    block = block.replace('используйте диагностику DLSS5 Autopilot v1.8.2 по Windows Application Error.',
                          'используйте диагностику DLSS5 Autopilot v1.8.2 по Windows Application Error и сравните standalone-dlssnr route.')
    return block

for sid, label in [('batman','Batman: Arkham Knight'), ('mafiade','Mafia: Definitive Edition'), ('nier','NieR:Automata')]:
    s = patch_section(s, sid, lambda b, label=label: patch_feeder_game(b, label))

# Footer: component/runtime snapshot after all profile checks.
footer = '<footer class="footer"><strong>Интерфейс v11:</strong> 27 игровых профилей; проверено 15.09.2026. Обновлён DLSS5 Autopilot до 1.8.2: для 64-bit D3D11/D3D12 игр без собственного DLSS на NVIDIA 616.64+ приоритетным стал standalone-dlssnr; уточнены native / neural-upstream / optiscaler / bridge / feeder routes и cadence. DLSS5-Feeder: stable 0.15.1, свежий troubleshooting build 1.16.0-beta.2 (14.09). NVIDIA public DLSS SDK — 310.9.1 (SR/RR, Preset F), DLSSNR runtime RTX 50 — 310.8.0. Без новых релизов: OptiScaler_DLSSNR 0.2.0, OptiScaler 0.9.4, RE_DLSS5_Load_Mod 0.63, ReShade 6.8.0. Autopilot compatibility feed: 75 отчётов, 14.09 20:18 UTC.</footer>'
s, n = re.subn(r'<footer class="footer">.*?</footer>', footer, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Footer not found')

# Sanity checks: UI/UX structure and dynamic production-derived list remain intact.
required = [
    'const allGames = [', 'game-finder', 'context-bar', 'step-section', 'copy-btn',
    'DLSS5 Autopilot v1.8.2', 'standalone-dlssnr', '1.16.0-beta.2',
    'NVIDIA DLSS SDK 310.9.1', 'Интерфейс v11', 'Проверено: 15.09.2026'
]
for needle in required:
    if needle not in s:
        raise SystemExit(f'Missing required marker: {needle}')

# Exactly the existing 27 game profiles must remain.
ids = re.findall(r"\{ value: '([^']+)', label: '[^']+' \}", s)
if len(ids) != 27 or len(set(ids)) != 27:
    raise SystemExit(f'Expected 27 unique allGames entries, got {len(ids)} / {len(set(ids))}')

p.write_text(s, encoding='utf-8')
print('Updated', p, p.stat().st_size, 'bytes; games:', len(ids))
