from pathlib import Path
from html import escape
import hashlib
import re
import sys

EXPECTED_BLOB = '0458225f4924ad0796b9c2b3a21c5c93b4b56c9f'
GAMES = [
    {
        'id': 'kcd',
        'name': 'Kingdom Come: Deliverance',
        'aliases': ['Kingdom Come Deliverance 1', 'KCD1', 'Кингдом Кам'],
        'route': 'Autopilot: standalone-dlssnr; Feeder как резерв',
        'status': 'NR: экспериментальный профиль',
        'intro': 'Первая часть: 64-bit DirectX 11, без штатного DLSS. Обычная замена nvngx_dlss.dll не добавляет отсутствующую интеграцию. Профиль относится к Windows-версии оригинальной игры, а не к Kingdom Come: Deliverance II.',
        'warning': 'Маршрут выбран по общей политике Autopilot для игр без DLSS, а не по подтверждённому тесту KCD на RTX 5080. На NVIDIA 616.64+ первым проверяйте standalone-dlssnr; Feeder используйте только отдельной чистой установкой. Наличие ReShade overlay ещё не доказывает работу Neural Rendering.',
        'metrics': [('API', 'DirectX 11 / x64'), ('DLSS input', 'Штатного нет'), ('NR', 'Экспериментальный'), ('FG / RR', 'Не штатные функции')],
        'settings': [
            ('Разрешение экрана', '3840×2160; сначала сравните NR OFF / ON без генерации кадров'),
            ('Графика', 'Начните с High; тени и дальность прорисовки повышайте после проверки времени кадра'),
            ('Маршрут', 'Autopilot → standalone-dlssnr на 616.64+, если он предложен для обнаруженного EXE'),
            ('DLSS Super Resolution', 'В игре отсутствует; SR собственного standalone-маршрута не равен штатной интеграции'),
            ('NR Scale / work area', 'У standalone нет универсального OptiScaler NR Scale. Для отдельного Feeder D3D11: сначала work area 100%, затем проба 75% при нехватке производительности'),
            ('Cadence', 'Оставьте настройку выбранного маршрута по умолчанию; режим Quality от neural-upstream сюда не переносится'),
            ('Frame Generation', 'OFF при установке. Не добавлять OptiFG: он рассчитан на D3D12. FG собственного standalone — только отдельный эксперимент после NR'),
            ('Ray Reconstruction', 'Не применимо к штатному рендереру; копирование nvngx_dlssd.dll не добавляет RR'),
            ('HDR / Smooth Motion', 'SDR и Smooth Motion OFF для первого теста; дополнительные обработчики изображения подключать по одному'),
        ],
        'steps': [
            ('install', '1', 'Подготовка и установка', '''<p>Запустите чистую игру и сохраните копии установленных proxy-DLL и конфигураций. В Steam типичный путь к исполняемому файлу:</p><pre>...\\KingdomComeDeliverance\\Bin\\Win64\\KingdomCome.exe</pre><p>В других магазинах путь может отличаться: проверьте его через «Открыть расположение файла» у работающего процесса. Не устанавливайте моды в корень игры или папку Mods вместо каталога фактически запущенного EXE.</p><ol><li>Скачайте Autopilot из репозитория автора. Выберите игру и проверьте обнаруженные <strong>x64 / DirectX 11 / no native DLSS</strong>.</li><li>Откройте <strong>What will happen?</strong>, проверьте резервные копии и отсутствие перезаписи чужого загрузчика. На драйвере 616.64+ выберите <code>standalone-dlssnr</code>, если он доступен.</li><li>Установите маршрут. Не добавляйте поверх него ручной OptiScaler, второй ReShade или Feeder. Используйте NR-runtime, совместимый с RTX 50; SR/RR DLL не заменяют <code>nvngx_dlssnr.dll</code>.</li></ol>'''),
            ('nr', '2', 'Первый запуск и резервный маршрут', '''<pre>1. Запустить игру без FG и Smooth Motion
2. Открыть интерфейс, указанный установщиком
3. Сравнить одинаковую сцену: NR OFF → NR ON
4. Autopilot → did it work? → проверить логи
5. Проверить движение камеры, диалоги и загрузку сохранения</pre><p>У standalone результат выводится через собственное окно. При нехватке производительности проверьте рекомендованный автором reduced-resolution fullscreen/borderless режим; это не тот же регулятор, что NR Scale в OptiScaler.</p><p><strong>Резерв:</strong> сначала удалите текущий маршрут через Autopilot, затем установите <code>feeder</code>. Он использует ReShade с поддержкой add-on, буфер глубины и шейдерные motion vectors. Проверьте корректность глубины, векторов движения и факт выполнения модели. На 616.64+ возможны ошибки NGX, описанные автором Autopilot; стабильность именно KCD не подтверждена. Самостоятельно понижать драйвер только ради этого профиля не требуется.</p>'''),
            ('fg', '3', 'Генерация кадров и ограничения', '''<p>Штатные NVIDIA DLSS FG/MFG и Ray Reconstruction здесь не подтверждены и не включаются простой заменой DLL. Общий OptiFG поддерживает D3D12, поэтому его инструкцию нельзя переносить на эту D3D11-игру.</p><p>Оставьте FG выключенным до устойчивой работы NR. Возможности FG внутри standalone проверяйте отдельно по его текущей документации, не смешивая их со Smooth Motion или внешней интерполяцией. Возврат к чистому рендереру остаётся безопасным вариантом.</p>'''),
            ('diag', '4', 'Диагностика и откат', '''<p><strong>Вылет до меню:</strong> проверьте, не заняты ли <code>dxgi.dll</code>, <code>d3d11.dll</code> или <code>version.dll</code> ранее установленными ReShade/ENB/ASI-модами. Не заменяйте их вслепую и не удаляйте файлы Windows. Сначала вернитесь к чистому запуску.</p><p><strong>NR визуально не работает:</strong> проверьте выбранный EXE, вывод standalone и логи; у Feeder дополнительно проверьте глубину и motion vectors. <strong>Шлейфы на интерфейсе:</strong> отключите дополнительные эффекты и FG, сравните диалог и движение камеры с NR OFF.</p><p><strong>Откат:</strong> Autopilot → Uninstall восстанавливает его резервные копии. Для ручной установки удаляйте только добавленные вами компоненты и возвращайте сохранённые оригиналы. После патча игры повторно проверяйте EXE и совместимость.</p>'''),
        ],
        'sources': [
            ('https://github.com/Kizzuwatnaa/DLSS5-Autopilot#which-route-a-game-gets', 'Autopilot: политика маршрутов и ограничения драйверов'),
            ('https://github.com/jlrouzies-fr/DLSS5-Feeder', 'DLSS5-Feeder: документация автора'),
            ('https://github.com/optiscaler/OptiScaler#optifg--hudfix-experimental-hud-ghosting-fix', 'OptiScaler: OptiFG только для D3D12'),
            ('https://www.nexusmods.com/kingdomcomedeliverance/mods/1603', 'Авторская инструкция ReShade: расположение EXE, не подтверждение NR'),
            ('https://store.steampowered.com/app/379430/Kingdom_Come_Deliverance/', 'Страница Windows-версии игры'),
        ],
    },
    {
        'id': 'kcd2',
        'name': 'Kingdom Come: Deliverance II',
        'aliases': ['Kingdom Come: Deliverance 2', 'Kingdom Come Deliverance 2', 'KCD2', 'Кингдом Кам 2'],
        'route': 'OptiScaler_DLSSNR через штатный DLSS; Autopilot optiscaler',
        'status': 'OptiScaler подтверждён; NR требует теста',
        'intro': 'Вторая часть: DirectX 12 и штатный DLSS Super Resolution. У обычного OptiScaler есть отдельный compatibility-профиль для игры; это не равно подтверждению всех NR-форков и комбинаций FG на RTX 5080.',
        'warning': 'Wiki OptiScaler: тест 0.9.4 на Radeon 9070 XT, загрузчик dxgi.dll, рекомендован OptiFG → XeFG. Штатных Reflex и DLSS-FG нет. Инструкции для AMD/Intel со spoofing не переносите на RTX 5080. Совместимость NR + выбранного FG нужно проверить отдельно.',
        'metrics': [('API', 'DirectX 12 / x64'), ('Input', 'Штатный DLSS SR'), ('Injection', 'dxgi.dll'), ('FG', 'Опциональный OptiFG')],
        'settings': [
            ('Разрешение экрана', '3840×2160'),
            ('Графика', 'High / Ultra как отправная точка; Experimental не использовать для первого теста NR'),
            ('DLSS Super Resolution', 'Quality; Balanced пробовать только при нехватке GPU-производительности'),
            ('Маршрут NR', 'OptiScaler_DLSSNR / Autopilot optiscaler; сначала проверить обычный DLSS без NR'),
            ('NR Scale / Model Resolution', '75% как пробная стартовая точка; 100% для сравнения качества. Это не измеренный оптимум RTX 5080'),
            ('Cadence', 'В OptiScaler не переносить cadence от другого add-on. Для отдельного neural-upstream начать с Quality / каждый кадр, если такой режим доступен'),
            ('Frame Generation', 'OFF при проверке NR. Затем OptiFG → XeFG, только если выбранный NR-форк поддерживает эту связку; иначе отдельный тест FSR3.1 FG или оставить OFF'),
            ('DLSS FG / MFG / Reflex / RR', 'Не считать штатно доступными. NVIDIA App override сам по себе не добавляет отсутствующую интеграцию'),
            ('HDR', 'Сначала SDR. При отдельной проверке HDR + XeFG может потребоваться r_HDRPipeline=2 в user.cfg'),
            ('Smooth Motion', 'OFF, если используется другой механизм генерации кадров'),
        ],
        'steps': [
            ('install', '1', 'Установка в правильный каталог', '''<p>Сначала проверьте чистую игру со штатным DLSS Quality, без FG и визуальных модов. Сохраните оригинальные DLL и конфигурации. Типичный путь Steam:</p><pre>...\\KingdomComeDeliverance2\\Bin\\Win64MasterMasterSteamPGO\\KingdomCome.exe</pre><p>Имя EXE совпадает с первой частью, но каталог и игра другие. Для другого магазина найдите фактически запущенный EXE, не копируйте файлы сразу во все каталоги Bin.</p><ol><li><strong>Автоматически:</strong> Autopilot → выбрать KCD II → проверить x64 / D3D12 / native DLSS → <code>optiscaler</code>. До установки просмотрите список замен и сохранение оригинального DLSS.</li><li><strong>Вручную, вместо Autopilot:</strong> распакуйте выбранный релиз <code>OptiScaler_DLSSNR</code> рядом с EXE и используйте установщик этого релиза с <code>dxgi.dll</code> и NVIDIA. Не заменяйте его DLL обычным OptiScaler поверх установленного NR-форка.</li><li>Добавьте требуемый релизом <code>nvngx_dlssnr.dll</code> для RTX 50 по документации автора. Обычный <code>nvngx_dlss.dll</code> — отдельный SR-runtime. OptiPatcher, REFramework и RE_DLSS5_Load_Mod для этого профиля не требуются.</li></ol><p>В <code>optiscaler</code>-маршруте ReShade для NR не нужен. Если <code>dxgi.dll</code> уже занят ReShade, сначала уберите конфликт через резервную копию; совместную загрузку настраивайте отдельно, не перезаписывая один мод другим.</p>'''),
            ('nr', '2', 'Проверка Neural Rendering', '''<pre>Игра: DLSS Quality, FG OFF, Smooth Motion OFF
Insert → OptiScaler: сначала проверить DLSS без NR
Neural Rendering ON → Model Resolution 75%
Сравнить ту же сцену при NR OFF / ON
Кратко проверить 100% и время кадра
Autopilot → did it work? / журналы выбранного форка</pre><p>Сравните лицо в диалоге, волосы, растительность, движение камеры и интерфейс. Сам факт наличия DLSS или меню OptiScaler не подтверждает выполнение NR.</p><p><strong>Альтернативы Autopilot:</strong> <code>native</code> и <code>neural-upstream</code> допустимы по общей политике D3D12 + DLSS, но не помечены здесь как проверенные KCD II-маршруты. Перед сменой полностью удалите предыдущую установку. У neural-upstream NR выполняется до апскейла; его cadence не равен Model Resolution в OptiScaler.</p>'''),
            ('fg', '3', 'Frame Generation и HDR', '''<p>Подтверждённая запись обычного OptiScaler рекомендует <strong>OptiFG → XeFG</strong>. Включайте эту связку после стабильного NR и только при её наличии в выбранной версии NR-форка. При отсутствии XeFG не смешивайте библиотеки разных сборок: проверьте поддерживаемый ею FSR3.1 FG либо оставьте генерацию выключенной.</p><p>В игре нет штатного DLSS-FG согласно compatibility-профилю. Поэтому не обещается NVIDIA MFG 4×/6× через простую замену <code>nvngx_dlssg.dll</code> или override в NVIDIA App.</p><p>Только если при HDR + XeFG возникают проблемы, сохраните <code>user.cfg</code> и добавьте или измените в нём:</p><pre>r_HDRPipeline=2</pre><p>Это рекомендация wiki для совместимого HDR10-вывода, а не обязательная настройка SDR и не доказательство HDR-совместимости NR. При искажении цвета верните SDR и отключите FG для диагностики.</p>'''),
            ('diag', '4', 'Диагностика и откат', '''<p><strong>Нет Insert overlay:</strong> проверьте, что мод находится рядом с запущенным EXE, а <code>dxgi.dll</code> принадлежит выбранному OptiScaler. <strong>Не работает NR:</strong> проверьте именно NR-форк, архитектуру runtime, лог и активный DLSS input.</p><p><strong>Вылет или шлейф после FG:</strong> верните FG OFF и повторите тест. Старые советы о принудительных HUD Fix не применяйте без проверки своей версии. Совместимость обычного OptiScaler на Radeon не гарантирует ту же комбинацию NR + XeFG на RTX 5080.</p><p><strong>После обновления игры:</strong> сравните версии и оригинальные DLL, снова проверьте DLSS → NR → FG → HDR. Для отката используйте Uninstall выбранного установщика либо верните свои резервные копии; не удаляйте штатные файлы игры вслепую.</p>'''),
        ],
        'sources': [
            ('https://github.com/optiscaler/OptiScaler/wiki/Kingdom-Come-Deliverance-II', 'Game-specific wiki: OptiScaler 0.9.4, dxgi.dll, XeFG и HDR'),
            ('https://github.com/Dagherbou/OptiScaler_DLSSNR/releases', 'OptiScaler_DLSSNR: релизы автора'),
            ('https://github.com/Kizzuwatnaa/DLSS5-Autopilot#which-route-a-game-gets', 'Autopilot: optiscaler / native / neural-upstream'),
            ('https://www.nvidia.com/en-eu/geforce/news/dlss-kingdom-come-deliverance-ii-and-many-more-games/', 'NVIDIA: штатная поддержка DLSS Super Resolution'),
            ('https://www.nexusmods.com/kingdomcomedeliverance2/mods/541', 'Авторская инструкция: путь к EXE в Steam, не подтверждение NR'),
        ],
    },
]


def render(g):
    i = g['id']
    out = [f'\n<section class="tab-panel" id="{i}" data-profile-added="2026-09-16">']
    out += [f'<div class="game-head"><div class="card"><h2>{escape(g["name"])}</h2><p>{escape(g["intro"])}</p><p>Маршрут для проверки: <strong>{escape(g["route"])}</strong>.</p><div class="callout warn"><strong>{escape(g["status"])}</strong>{escape(g["warning"])}</div><div class="status-strip"><span class="status-pill exp">NR: требуется проверка в игре</span><span class="status-pill warn">Источники: 16.09.2026</span></div></div><div class="card"><div class="summary-grid">']
    for label, value in g['metrics']:
        out += [f'<div class="metric"><div class="label">{escape(label)}</div><div class="value">{escape(value)}</div></div>']
    out += ['</div></div></div>']
    out += [f'<div class="section recommended-profile" id="{i}-settings"><div class="section-title"><div class="step-num">★</div><h3>Рекомендуемые настройки RTX 5080 / 4K</h3></div><div class="section-body"><div class="callout"><strong>Стартовые настройки, не результаты бенчмарка</strong>Замеры на вашей RTX 5080 не выполнялись. Меняйте один параметр за раз и сравнивайте время кадра в одинаковой сцене без FG.</div><table class="matrix"><tr><th>Параметр</th><th>Рекомендация</th></tr>']
    for label, value in g['settings']:
        out += [f'<tr><td>{escape(label)}</td><td>{escape(value)}</td></tr>']
    out += ['</table></div></div>']
    for suffix, number, title, body in g['steps']:
        out += [f'<div class="section step-section" id="{i}-{suffix}"><div class="section-title"><div class="step-num">{number}</div><h3>{escape(title)}</h3></div><div class="section-body">{body}</div></div>']
    out += [f'<div class="card source-list" id="{i}-sources" style="margin-top:18px"><h3>Источники и компоненты</h3><ul>']
    for url, title in g['sources']:
        out += [f'<li><a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(title)}</a></li>']
    out += ['</ul><p class="small">Статус отражает доступные документы, а не личный запуск игры. Скачивайте компоненты из репозиториев авторов; обещания «DLSS 5 free upgrade / FPS ×4» не являются подтверждением совместимости.</p></div></section>\n']
    return '\n'.join(out)


def patch(path):
    raw = path.read_bytes()
    actual_blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
    if actual_blob != EXPECTED_BLOB:
        raise RuntimeError('Production changed: stop instead of overwriting concurrent edits: ' + actual_blob)
    text = raw.decode('utf-8')
    before_ids = re.findall(r'<section\b[^>]*class="tab-panel(?: active)?"[^>]*id="([^"]+)"', text)
    assert len(before_ids) == len(set(before_ids)) == 27
    for game in GAMES:
        assert f'id="{game["id"]}"' not in text
    assert text.count('<footer class="footer">') == 1
    text = text.replace('<footer class="footer">', ''.join(render(g) for g in GAMES) + '<footer class="footer">', 1)
    anchor = "  { value: 'yakuza3', label: 'Yakuza Kiwami 3 & Dark Ties' }"
    assert text.count(anchor) == 1
    import json
    items = []
    for g in GAMES:
        items.append('  { value: ' + json.dumps(g['id']) + ', label: ' + json.dumps(g['name'], ensure_ascii=False) + ', aliases: ' + json.dumps(g['aliases'], ensure_ascii=False) + ' }')
    text = text.replace(anchor, anchor + ',\n' + ',\n'.join(items), 1)
    old_search = "return allGames.filter(g => g.label.toLocaleLowerCase('ru-RU').includes(q));"
    new_search = "return allGames.filter(g => [g.label, ...(g.aliases || [])].some(name => name.toLocaleLowerCase('ru-RU').includes(q)));"
    assert text.count(old_search) == 1
    text = text.replace(old_search, new_search, 1)
    old_badge = '<strong>Игр:</strong> 27'
    assert text.count(old_badge) == 1
    text = text.replace(old_badge, '<strong>Игр:</strong> 29', 1)
    text = text.replace('<strong>Обновлено:</strong> 15.09.2026', '<strong>Обновлено:</strong> 16.09.2026', 1)
    old_footer = '<strong>Интерфейс v11:</strong> 27 игровых профилей; проверено 15.09.2026.'
    new_footer = '<strong>Интерфейс v12:</strong> 29 игровых профилей. 16.09.2026 добавлены Kingdom Come: Deliverance и Kingdom Come: Deliverance II: отдельные маршруты, таблицы RTX 5080 / 4K, установка, NR, FG/HDR, диагностика и источники. NR-совместимость обозначена отдельно от обычного OptiScaler; настройки стартовые, без заявленных бенчмарков. Поиск второй части работает по II, 2 и KCD2. Остальные 27 профилей сохранены без изменений; их предыдущая комплексная проверка — 15.09.2026.'
    assert text.count(old_footer) == 1
    text = text.replace(old_footer, new_footer, 1)
    after_ids = re.findall(r'<section\b[^>]*class="tab-panel(?: active)?"[^>]*id="([^"]+)"', text)
    assert len(after_ids) == len(set(after_ids)) == 29
    assert after_ids[:27] == before_ids
    assert re.findall(r'<style>.*?</style>', text, re.S) == re.findall(r'<style>.*?</style>', raw.decode(), re.S)
    for game in GAMES:
        for suffix in ['settings', 'install', 'nr', 'fg', 'diag', 'sources']:
            assert text.count(f'id="{game["id"]}-{suffix}"') == 1
    path.write_bytes(text.encode('utf-8'))
    print('Profiles:', len(before_ids), '->', len(after_ids))
    print('SHA256:', hashlib.sha256(path.read_bytes()).hexdigest())
    print('MD5:', hashlib.md5(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    patch(Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html'))
