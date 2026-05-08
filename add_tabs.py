import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── Category rules (first match wins) ───────────────────────────────────────
def get_cat(href):
    h = href.lower()
    # Sport
    if any(k in h for k in ['liga-4', 'sanatatea-breznita', 'pandurii', 'cs-drobeta',
                              'fotbal', 'karting', 'sahist', 'olimpiada-satelor']):
        return 'sport'
    # Cronica Neagra
    cronica_keys = ['accident', 'retinut', 'arestat', 'talharie', 'tragedie',
                    'bebelus', 'motociclist', 'furt', 'captura', 'droguri',
                    'viol', 'minora', 'barbat-71', 'violenta', 'cocaina',
                    'frauda', 'descinderi', 'descarcerare', 'incendiu',
                    'retinuti', 'razie', 'tanara-disparuta',
                    'bratara', 'flagrant', 'barbat-retinut', 'retinuti-furt']
    cronica_exclude = ['marsul-pentru-viata', 'porti-deschise-politie',
                       'politisti-drobeta-donare', 'ziua-politiei',
                       'intalnire-scoala', 'exercitiu-interventie',
                       'masuri-siguranta-paste', 'jandarmeria-romana-176',
                       'exercitiu']
    if any(k in h for k in cronica_keys) and not any(x in h for x in cronica_exclude):
        return 'cronica'
    # Social
    if any(k in h for k in ['autism', 'inscrieri', 'apel-umanitar',
                              'centru-comunitar', 'donare-sange', 'protest-mineri',
                              'scoala-familie', 'masa-sanatoasa',
                              'marsul-pentru-viata', 'politisti-drobeta-donare',
                              'simpozion', 'mars-solidaritate']):
        return 'social'
    # Economic
    if any(k in h for k in ['drum-bahna', 'bloc-locuinte', 'reabilitare', 'camin-stud',
                              'investitie', 'drum-expres', 'spatii-verzi',
                              'promenada-crisan', 'fara-deseuri', 'apa-canalizare',
                              'centura', 'contract-finantare', 'pnrr', 'buget',
                              'altex', 'impozite', 'obiective-turistice',
                              'jocuri-noroc']):
        return 'economic'
    # Cultura
    if any(k in h for k in ['pastorala', 'florii', 'grup-catehetic', 'targ-paste',
                              'targ-florii', 'targ-miei',
                              'buna-vestire', 'pomenirea', 'doina-gorjului',
                              'refrenul', 'drumul-crucii', 'ziua-olteniei',
                              'la-multi-ani', 'conferinta-muzeu', 'zilele-parcului',
                              'targul-ofertei', 'porti-deschise-politie',
                              'ziua-politiei', 'jandarmeria-romana-176',
                              'descoperiri-arheologice', 'patrimoniu', 'muzeu',
                              'marsul-pentru-viata']):
        return 'cultura'
    return 'actualitate'

# Category display config
CAT_CONFIG = {
    'actualitate': {'label': 'Actualitate', 'color': '#1a3a5c', 'border': '#1a3a5c'},
    'cronica':     {'label': 'Cronica Neagra', 'color': '#c62828', 'border': '#c62828'},
    'sport':       {'label': 'Sport',          'color': '#1565c0', 'border': '#1565c0'},
    'social':      {'label': 'Social',         'color': '#2e7d32', 'border': '#2e7d32'},
    'economic':    {'label': 'Economic',       'color': '#e65100', 'border': '#e65100'},
    'cultura':     {'label': 'Cultura',        'color': '#6a1b9a', 'border': '#6a1b9a'},
}

# ─── Process each article-card: add data-cat + fix border-top + fix span ──────
def replace_card(m):
    card_html = m.group(0)
    # Extract href
    href_m = re.search(r'class="card-title"><a href="([^"]+)"', card_html)
    if not href_m:
        return card_html
    href = href_m.group(1)
    cat = get_cat(href)
    cfg = CAT_CONFIG[cat]

    # Fix border-top color
    card_html = re.sub(
        r'(class="article-card"[^>]*style="border-top:3px solid )[^"]+(")',
        lambda mm: mm.group(1) + cfg['border'] + mm.group(2),
        card_html
    )
    # Fix card-category span (color + text)
    card_html = re.sub(
        r'(<span class="card-category" style="background:)[^"]+("[^>]*>)[^<]*(</span>)',
        lambda mm: mm.group(1) + cfg['color'] + mm.group(2) + cfg['label'] + mm.group(3),
        card_html
    )
    # Add data-cat attribute to article-card div
    card_html = re.sub(
        r'<div class="article-card"',
        '<div class="article-card" data-cat="' + cat + '"',
        card_html,
        count=1
    )
    return card_html

# Match each full article-card div
card_pattern = re.compile(
    r'<div class="article-card"[^>]*>.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)
content = card_pattern.sub(replace_card, content)

# ─── Tab CSS ──────────────────────────────────────────────────────────────────
tab_css = """
<style>
/* ========== TAB FILTRU STIRI ========== */
.tabs-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0 0 18px 0;
  padding: 0;
  list-style: none;
}
.tabs-nav li { margin: 0; }
.tabs-nav button {
  background: #f0f4f8;
  border: 2px solid #d0d8e0;
  border-radius: 20px;
  color: #1a3a5c;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 5px 14px;
  transition: background .18s, color .18s, border-color .18s;
  white-space: nowrap;
}
.tabs-nav button:hover { background: #e0eaf4; border-color: #1a3a5c; }
.tabs-nav button.active { background: #1a3a5c; border-color: #1a3a5c; color: #fff; }
.tabs-nav button[data-tab="cronica"].active  { background:#c62828; border-color:#c62828; }
.tabs-nav button[data-tab="sport"].active    { background:#1565c0; border-color:#1565c0; }
.tabs-nav button[data-tab="social"].active   { background:#2e7d32; border-color:#2e7d32; }
.tabs-nav button[data-tab="economic"].active { background:#e65100; border-color:#e65100; }
.tabs-nav button[data-tab="cultura"].active  { background:#6a1b9a; border-color:#6a1b9a; }
.article-card.hidden-tab { display: none !important; }
</style>
"""

# ─── Tab nav HTML ──────────────────────────────────────────────────────────────
tab_nav = """
        <ul class="tabs-nav" id="stiriTabsNav">
          <li><button class="active" data-tab="toate">Toate</button></li>
          <li><button data-tab="actualitate">Actualitate</button></li>
          <li><button data-tab="cronica">Cronica Neagra</button></li>
          <li><button data-tab="sport">Sport</button></li>
          <li><button data-tab="social">Social</button></li>
          <li><button data-tab="economic">Economic</button></li>
          <li><button data-tab="cultura">Cultura</button></li>
        </ul>
"""

# ─── Tab JS ───────────────────────────────────────────────────────────────────
tab_js = """<script>
(function(){
  var nav = document.getElementById('stiriTabsNav');
  if(!nav) return;
  nav.addEventListener('click', function(e){
    var btn = e.target.closest('button[data-tab]');
    if(!btn) return;
    nav.querySelectorAll('button').forEach(function(b){ b.classList.remove('active'); });
    btn.classList.add('active');
    var tab = btn.getAttribute('data-tab');
    document.querySelectorAll('.articles-grid .article-card').forEach(function(card){
      if(tab === 'toate' || card.getAttribute('data-cat') === tab){
        card.classList.remove('hidden-tab');
      } else {
        card.classList.add('hidden-tab');
      }
    });
  });
})();
</script>"""

# ─── Insert CSS before </head> ────────────────────────────────────────────────
content = content.replace('</head>', tab_css + '</head>', 1)

# ─── Insert tab nav after section-header (before GRID comment) ────────────────
content = re.sub(
    r'(<!-- GRID 4 ARTICOLE.*?-->\s*\n)',
    tab_nav + r'\1',
    content,
    count=1,
    flags=re.DOTALL
)

# ─── Insert JS before </body> ────────────────────────────────────────────────
content = content.replace('</body>', tab_js + '\n</body>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Tab system added to index.html")
cats = {}
for m in re.finditer(r'data-cat="([^"]+)"', content):
    c = m.group(1)
    cats[c] = cats.get(c, 0) + 1
print("Category distribution:", cats)
