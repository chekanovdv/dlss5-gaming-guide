from pathlib import Path
from bs4 import BeautifulSoup

p = Path('index.html')
soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')

def dedupe_by_strong(section_id, strong_text, tag='div'):
    section = soup.find('section', id=section_id)
    matches = []
    for node in section.find_all(tag):
        strong = node.find('strong', recursive=False)
        if strong and strong.get_text(' ', strip=True) == strong_text:
            matches.append(node)
    for node in matches[1:]:
        node.decompose()

# Remove duplicate callouts/notes if the one-shot updater was retriggered.
dedupe_by_strong('007firstlight', '15.09.2026 — Path Tracing + DLSS 4.5 Ray Reconstruction')
dedupe_by_strong('007firstlight', 'После патча 15.09:', tag='p')
dedupe_by_strong('witcher3', '29.09.2026 — The Witcher 3 Remastered')
for game_id in ('mafiade', 'nier'):
    dedupe_by_strong(game_id, 'HDR10 bridge в Feeder 0.15.1')

p.write_text(str(soup), encoding='utf-8')
