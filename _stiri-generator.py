# -*- coding: utf-8 -*-
"""
Generator automat de stiri din fisierele Markdown create prin Decap CMS.
Citeste _stiri/*.md si genereaza fisierele HTML + actualizeaza index.html.
Rulat de GitHub Actions la fiecare push pe main care modifica _stiri/.
"""

import os
import re
import glob
import yaml
import markdown

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
STIRI_DIR = os.path.join(SITE_DIR, '_stiri')
INDEX_PATH = os.path.join(SITE_DIR, 'index.html')
SITE_URL = "https://www.mehedintiazi.ro"

CATEGORII_EMOJI = {
    "Actualitate": "📰",
    "Ordine Publică": "🔔",
    "Sănătate": "🏥",
    "Cultură": "🎭",
    "Sport": "⚽",
    "Politică": "🏛️",
    "Economie": "💼",
    "Economic": "💼",
    "Educație": "🎓",
    "Meteo": "🌦️",
    "Social": "👥",
}

CATEGORII_CULORI = {
    "Actualitate": "#1a3a5c",
    "Ordine Publică": "#c0392b",
    "Social": "#27ae60",
    "Economic": "#2980b9",
    "Sport": "#f39c12",
    "Cultură": "#8e44ad",
    "Educație": "#1a73e8",
    "Meteo": "#16a085",
}

LUNI_RO = {
    '01': 'Ianuarie', '02': 'Februarie', '03': 'Martie',
    '04': 'Aprilie', '05': 'Mai', '06': 'Iunie',
    '07': 'Iulie', '08': 'August', '09': 'Septembrie',
    '10': 'Octombrie', '11': 'Noiembrie', '12': 'Decembrie'
}


def parse_frontmatter(content):
    """Extrage YAML front matter si corpul markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
            except Exception:
                metadata = {}
            return metadata, parts[2].strip()
    return {}, content


def format_date_ro(date_val):
    """Converteste data ISO in format romanesc: 26 Mai 2026."""
    try:
        date_str = str(date_val)[:10]
        year, month, day = date_str.split('-')
        return f"{int(day)} {LUNI_RO.get(month, month)} {year}"
    except Exception:
        return str(date_val)


def titlu_la_slug(titlu):
    """Transforma titlul in slug URL-friendly."""
    replacements = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
        'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't',
        'ş': 's', 'ţ': 't', 'Ş': 's', 'Ţ': 't',
        '"': '', '"': '', '„': '', '"': '',
        '«': '', '»': '', '\u2018': '', '\u2019': '',
    }
    slug = titlu.lower()
    for char, rep in replacements.items():
        slug = slug.replace(char, rep)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:80]


def get_poza_rel(poza_val):
    """Extrage doar numele fisierului din calea imaginii."""
    if not poza_val:
        return ''
    poza = str(poza_val)
    if poza.startswith('/img/'):
        return poza[5:]
    if poza.startswith('img/'):
        return poza[4:]
    if '/' in poza:
        return poza.split('/')[-1]
    return poza


def genereaza_articol_html(metadata, body_md, slug):
    """Genereaza HTML complet pentru un articol."""
    titlu = metadata.get('title', '')
    date_val = metadata.get('date', '')
    date_str = str(date_val)
    data_ro = format_date_ro(date_str)
    ora = date_str[11:16] if len(date_str) > 10 else '10:00'
    categorie = metadata.get('categorie', 'Actualitate')
    poza_rel = get_poza_rel(metadata.get('poza', ''))
    taguri_lista = metadata.get('taguri') or []
    if isinstance(taguri_lista, str):
        taguri_lista = [t.strip() for t in taguri_lista.split(',')]

    emoji = CATEGORII_EMOJI.get(categorie, '📰')
    url_articol = f"{SITE_URL}/{slug}"
    img_url = f"{SITE_URL}/img/{poza_rel}"

    # Converteste markdown in HTML
    text_html = markdown.markdown(body_md, extensions=['extra', 'nl2br'])

    # Prima propozitie ca subtitlu
    subtitlu_match = re.search(r'<p>(.*?)</p>', text_html, re.DOTALL)
    subtitlu_html = subtitlu_match.group(1) if subtitlu_match else titlu[:200]
    subtitlu_plain = re.sub(r'<.*?>', '', subtitlu_html)[:200]

    taguri_html = '\n          '.join(
        [f'<span class="tag-item">{t.strip()}</span>' for t in taguri_lista if t.strip()]
    )

    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-67X58CLV15"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-67X58CLV15');
</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{titlu} - MehedintiAzi.ro</title>
  <meta name="description" content="{subtitlu_plain[:160]}" />
  <meta name="author" content="Redactia MehedintiAzi.ro" />
  <link rel="canonical" href="{url_articol}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{titlu}" />
  <meta property="og:description" content="{subtitlu_plain[:160]}" />
  <meta property="og:url" content="{url_articol}" />
  <meta property="og:site_name" content="MehedintiAzi.ro" />
  <meta property="og:image" content="{img_url}" />
  <meta property="article:published_time" content="{date_str[:19]}+03:00" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{titlu}",
    "datePublished": "{date_str[:19]}+03:00",
    "image": "{img_url}",
    "author": {{ "@type": "Organization", "name": "Redactia MehedintiAzi.ro" }},
    "publisher": {{ "@type": "Organization", "name": "MehedintiAzi.ro" }}
  }}
  </script>

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="stylesheet" href="css/style.css" />
  <style>
    .article-page {{ padding: 25px 0; }}
    .article-layout {{ display: grid; grid-template-columns: 1fr 300px; gap: 25px; }}
    .breadcrumb {{ font-size: 12px; color: #999; margin-bottom: 15px; }}
    .breadcrumb a {{ color: #1a3a5c; }}
    .breadcrumb span {{ margin: 0 6px; }}
    .article-main {{ background: #fff; padding: 25px; border: 1px solid #ddd; }}
    .article-category {{ display: inline-block; background: #1a3a5c; color: #fff; font-size: 11px; font-weight: 700; padding: 4px 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
    .article-title {{ font-size: 28px; font-family: Georgia, serif; line-height: 1.3; color: #111; margin-bottom: 12px; }}
    .article-subtitle {{ font-size: 17px; color: #555; line-height: 1.5; margin-bottom: 15px; font-style: italic; border-left: 4px solid #1a3a5c; padding-left: 12px; }}
    .article-meta {{ display: flex; align-items: center; gap: 20px; padding: 10px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; margin-bottom: 20px; font-size: 13px; color: #888; flex-wrap: wrap; }}
    .article-meta .autor {{ color: #1a3a5c; font-weight: 700; }}
    .share-bar {{ display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }}
    .share-btn {{ display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; font-size: 13px; font-weight: 700; color: #fff; border: none; cursor: pointer; border-radius: 3px; text-decoration: none; }}
    .share-fb {{ background: #1877f2; }}
    .share-wa {{ background: #25d366; }}
    .share-copy {{ background: #555; }}
    .share-btn:hover {{ opacity: 0.9; color: #fff; }}
    .article-img-main {{ width: 100%; margin-bottom: 20px; }}
    .article-img-main img {{ width: 100%; max-height: 500px; object-fit: cover; }}
    .img-caption {{ font-size: 12px; color: #999; text-align: center; margin-top: 6px; font-style: italic; }}
    .article-content {{ font-size: 16px; line-height: 1.8; color: #222; }}
    .article-content p {{ margin-bottom: 16px; }}
    .article-content h2 {{ font-size: 22px; font-family: Georgia, serif; color: #1a3a5c; margin: 28px 0 12px; padding-bottom: 6px; border-bottom: 2px solid #eee; }}
    .article-content h3 {{ font-size: 19px; font-family: Georgia, serif; color: #333; margin: 22px 0 10px; }}
    .article-content strong {{ color: #111; }}
    .article-content ul {{ margin: 10px 0 16px 22px; }}
    .article-content ul li {{ margin-bottom: 6px; }}
    .article-content blockquote {{ border-left: 4px solid #1a3a5c; padding: 12px 20px; margin: 20px 0; background: #f0f4f8; font-style: italic; font-size: 17px; color: #444; }}
    .article-tags {{ margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee; }}
    .article-tags span {{ font-size: 13px; font-weight: 700; color: #555; margin-right: 8px; }}
    .tag-item {{ display: inline-block; background: #f0f4f8; color: #1a3a5c; font-size: 12px; padding: 3px 9px; margin: 3px 2px; border-radius: 2px; border: 1px solid #dde; }}
    .share-bottom {{ background: #f9f9f9; padding: 15px; margin-top: 20px; border: 1px solid #eee; text-align: center; }}
    .share-bottom p {{ font-size: 14px; font-weight: 700; color: #333; margin-bottom: 10px; }}
    .sidebar {{ display: flex; flex-direction: column; gap: 20px; }}
    .sidebar-box {{ background: #fff; border: 1px solid #ddd; padding: 15px; }}
    .sidebar-box h3 {{ font-size: 14px; text-transform: uppercase; font-weight: 700; color: #1a3a5c; border-bottom: 2px solid #1a3a5c; padding-bottom: 8px; margin-bottom: 12px; }}
    .sidebar-stire {{ display: flex; gap: 10px; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0; }}
    .sidebar-stire:last-child {{ border-bottom: none; margin-bottom: 0; }}
    .sidebar-stire img {{ width: 70px; height: 55px; object-fit: cover; flex-shrink: 0; }}
    .sidebar-stire a {{ font-size: 13px; color: #222; text-decoration: none; font-weight: 600; line-height: 1.4; }}
    .sidebar-stire a:hover {{ color: #1a3a5c; }}
    @media(max-width:768px) {{
      .article-layout {{ grid-template-columns: 1fr; }}
      .article-title {{ font-size: 22px; }}
    }}
  </style>
  <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
  <script>
    window.OneSignalDeferred = window.OneSignalDeferred || [];
    OneSignalDeferred.push(async function(OneSignal) {{
      await OneSignal.init({{ appId: "2e6f20be-5714-4e65-abbe-dd218bd3b3b2" }});
    }});
  </script>
  <link rel="alternate" type="application/rss+xml" title="MehedintiAzi.ro RSS" href="/feed.xml" />
</head>
<body>

<div id="header-placeholder"></div>
<script>
  fetch('index.html').then(r=>r.text()).then(html=>{{
    var parser=new DOMParser();
    var doc=parser.parseFromString(html,'text/html');
    var header=doc.querySelector('header');
    if(header) document.getElementById('header-placeholder').replaceWith(header.cloneNode(true));
  }});
</script>

<main class="container article-page">

  <div class="breadcrumb">
    <a href="index.html">Acasă</a><span>›</span>
    <a href="#">{categorie}</a><span>›</span>
    {titlu[:60]}
  </div>

  <div class="article-layout">
    <article class="article-main">

      <span class="article-category">{emoji} {categorie}</span>

      <h1 class="article-title">{titlu}</h1>

      <p class="article-subtitle">{subtitlu_plain}</p>

      <div class="article-meta">
        <span>📅 {data_ro}</span>
        <span>🕐 {ora}</span>
        <span class="autor">✏️ Redacția MehedintiAzi.ro</span>
        <span>👁 {categorie} · Mehedinți</span>
      </div>

      <div class="share-bar">
        <a class="share-btn share-fb" href="https://www.facebook.com/sharer/sharer.php?u={url_articol}" target="_blank">📌 Facebook</a>
        <a class="share-btn share-wa" href="https://wa.me/?text={url_articol}" target="_blank">📲 WhatsApp</a>
        <button class="share-btn share-copy" onclick="navigator.clipboard.writeText(window.location.href)">📋 Copiază link</button>
      </div>

      <div class="article-img-main">
        <img src="img/{poza_rel}" alt="{titlu}" />
        <p class="img-caption">Foto: MehedintiAzi.ro</p>
      </div>

      <div class="article-content">

        {text_html}

        <div class="article-tags">
          <span>Etichete:</span>
          {taguri_html}
        </div>

      </div><!-- /article-content -->

      <div class="share-bottom">
        <p>📎 Distribuie această știre</p>
        <div class="share-bar" style="justify-content:center;">
          <a class="share-btn share-fb" href="https://www.facebook.com/sharer/sharer.php?u={url_articol}" target="_blank">📌 Facebook</a>
          <a class="share-btn share-wa" href="https://wa.me/?text={url_articol}" target="_blank">📲 WhatsApp</a>
        </div>
      </div>

    </article>

    <aside class="sidebar">
      <div class="sidebar-box">
        <h3>Știri recente</h3>
        <div id="sidebar-stiri-recente">Se incarca...</div>
      </div>
    </aside>

  </div>

</main>

<div id="footer-placeholder"></div>
<script>
  fetch('index.html').then(r=>r.text()).then(html=>{{
    var parser=new DOMParser();
    var doc=parser.parseFromString(html,'text/html');
    var footer=doc.querySelector('footer');
    if(footer) document.getElementById('footer-placeholder').replaceWith(footer.cloneNode(true));
    var cards=doc.querySelectorAll('.article-card');
    var sideDiv=document.getElementById('sidebar-stiri-recente');
    if(sideDiv){{
      var html2='';var count=0;
      cards.forEach(function(card){{
        if(count>=4) return;
        var img=card.querySelector('img');
        var link=card.querySelector('.card-title a');
        if(img&&link){{
          html2+='<div class="sidebar-stire"><img src="'+img.getAttribute('src')+'" alt=""><a href="'+link.getAttribute('href')+'">'+link.textContent+'</a></div>';
          count++;
        }}
      }});
      sideDiv.innerHTML=html2||'<p>Nicio știre disponibilă.</p>';
    }}
  }});
</script>

</body>
</html>"""


def genereaza_card_index(titlu, data_ro, categorie, poza_rel, slug, excerpt):
    """Genereaza blocul HTML pentru cardul articolului din index.html."""
    culoare = CATEGORII_CULORI.get(categorie, '#1a3a5c')
    slug_comment = re.sub(r'[^A-Z0-9 ]', '', slug.upper().replace('-', ' '))[:60]
    excerpt_safe = excerpt[:150].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    titlu_safe = titlu.replace('"', '&quot;')
    return f"""
          <!-- ARTICOL - {slug_comment} -->
          <div class="article-card" style="border-top:3px solid {culoare};">
            <div class="card-img">
              <img src="img/{poza_rel}" alt="{titlu_safe}" style="width:100%;height:100%;object-fit:cover;" />
            </div>
            <div class="card-body">
              <span class="card-category" style="background:{culoare};">{categorie}</span>
              <h3 class="card-title"><a href="{slug}.html">{titlu}</a></h3>
              <p class="card-excerpt">{excerpt_safe}...</p>
              <div class="card-meta"><span>&#128336; {data_ro}</span><a href="{slug}.html" class="card-read">Citeste &rsaquo;</a></div>
            </div>
          </div>
"""


def main():
    print("=" * 55)
    print("  GENERATOR STIRI DIN DECAP CMS – MehedintiAzi.ro")
    print("=" * 55)

    md_files = glob.glob(os.path.join(STIRI_DIR, '*.md'))
    if not md_files:
        print("\nNu exista fisiere .md in _stiri/. Nimic de facut.")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()

    generated = 0
    cards_to_add = []

    for md_path in sorted(md_files, reverse=True):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata, body_md = parse_frontmatter(content)
        titlu = metadata.get('title', '').strip()

        if not titlu:
            print(f"  SKIP (fara titlu): {os.path.basename(md_path)}")
            continue

        # Construieste slug din numele fisierului (fara .md)
        md_basename = os.path.splitext(os.path.basename(md_path))[0]
        slug = md_basename

        # Genereaza fisierul HTML al articolului
        html_path = os.path.join(SITE_DIR, f"{slug}.html")
        articol_html = genereaza_articol_html(metadata, body_md, slug)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(articol_html)
        print(f"  OK  Articol generat: {slug}.html")
        generated += 1

        # Verifica daca articolul e deja in index.html
        if f'"{slug}.html"' in index_html or f"'{slug}.html'" in index_html:
            print(f"  --  Cardul exista deja in index.html, sarit.")
            continue

        # Pregateste cardul pentru index.html
        date_val = metadata.get('date', '')
        data_ro = format_date_ro(str(date_val))
        categorie = metadata.get('categorie', 'Actualitate')
        poza_rel = get_poza_rel(metadata.get('poza', ''))

        # Extrage excerpt din prima propozitie a body-ului
        text_html = markdown.markdown(body_md, extensions=['extra'])
        subtitlu_match = re.search(r'<p>(.*?)</p>', text_html, re.DOTALL)
        excerpt = re.sub(r'<.*?>', '', subtitlu_match.group(1) if subtitlu_match else titlu)[:160]

        card_html = genereaza_card_index(titlu, data_ro, categorie, poza_rel, slug, excerpt)
        cards_to_add.append(card_html)

    # Insereza cardurile noi la inceputul grilei din index.html
    if cards_to_add:
        insert_marker = '<div class="articles-grid mb-20">'
        if insert_marker in index_html:
            insert_pos = index_html.index(insert_marker) + len(insert_marker)
            all_cards = '\n'.join(cards_to_add)
            index_html = index_html[:insert_pos] + all_cards + index_html[insert_pos:]
            with open(INDEX_PATH, 'w', encoding='utf-8') as f:
                f.write(index_html)
            print(f"\n  OK  {len(cards_to_add)} card(uri) noi adaugate in index.html")
        else:
            print("\n  EROARE: Marcatorul articles-grid nu a fost gasit in index.html!")

    print(f"\n  Total articole generate: {generated}")
    print("=" * 55)


if __name__ == "__main__":
    main()
