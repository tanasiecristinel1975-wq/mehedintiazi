# -*- coding: utf-8 -*-
"""
Generator automat de stiri pentru MehedintiAzi.ro
Citeste STIRE-NOUA.txt si genereaza fisierul HTML complet.
"""

import os
import re
import sys
from datetime import datetime

SITE_URL = "https://www.mehedintiazi.ro"
SITE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(SITE_DIR, "STIRE-NOUA.txt")

CATEGORII_EMOJI = {
    "Actualitate": "📰",
    "Ordine Publică": "🔔",
    "Sănătate": "🏥",
    "Cultură": "🎭",
    "Sport": "⚽",
    "Politică": "🏛️",
    "Economie": "💼",
    "Educație": "🎓",
    "Meteo": "🌦️",
}

def citeste_camp(continut, camp):
    pattern = rf"{camp}:\s*\n(.*?)(?=\n[A-Z]+:|$)"
    match = re.search(pattern, continut, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def titlu_la_slug(titlu):
    replacements = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
        'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't',
        'ş': 's', 'ţ': 't', 'Ş': 's', 'Ţ': 't',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'ä': 'a',
        'ó': 'o', 'ö': 'o', 'ô': 'o',
        'ú': 'u', 'ü': 'u', 'û': 'u',
        '"': '', '"': '', '„': '', '"': '',
        '«': '', '»': '', ''': '', ''': '',
    }
    slug = titlu.lower()
    for char, rep in replacements.items():
        slug = slug.replace(char, rep)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    slug = slug[:80]
    return slug

def proceseaza_text(text_raw):
    """Converteste textul simplu in paragrafe si subtitluri HTML."""
    linii = text_raw.split('\n')
    html_parts = []
    paragraf_curent = []

    for linie in linii:
        linie = linie.strip()
        if linie.startswith('== ') and linie.endswith(' =='):
            if paragraf_curent:
                text_p = ' '.join(paragraf_curent).strip()
                if text_p:
                    html_parts.append(f'<p>{proceseaza_bold(text_p)}</p>')
                paragraf_curent = []
            subtitlu = linie[3:-3].strip()
            html_parts.append(f'<h2>{subtitlu}</h2>')
        elif linie == '':
            if paragraf_curent:
                text_p = ' '.join(paragraf_curent).strip()
                if text_p:
                    html_parts.append(f'<p>{proceseaza_bold(text_p)}</p>')
                paragraf_curent = []
        else:
            paragraf_curent.append(linie)

    if paragraf_curent:
        text_p = ' '.join(paragraf_curent).strip()
        if text_p:
            html_parts.append(f'<p>{proceseaza_bold(text_p)}</p>')

    return '\n\n        '.join(html_parts)

def proceseaza_bold(text):
    """Converteste *cuvant* in <strong>cuvant</strong>."""
    return re.sub(r'\*(.+?)\*', r'<strong>\1</strong>', text)

def genereaza_html(titlu, data, ora, categorie, poza, text_html, taguri_lista, slug):
    emoji = CATEGORII_EMOJI.get(categorie, "📰")
    taguri_html = '\n          '.join([f'<span class="tag-item">{t.strip()}</span>' for t in taguri_lista])
    url_articol = f"{SITE_URL}/{slug}"
    img_url = f"{SITE_URL}/img/{poza}"

    # Prima propozitie ca subtitlu
    prima_propozitie = re.search(r'<p>(.*?)</p>', text_html)
    subtitlu = prima_propozitie.group(1)[:200] if prima_propozitie else titlu
    subtitlu = re.sub(r'<.*?>', '', subtitlu)

    html = f"""<!DOCTYPE html>
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
  <meta name="description" content="{subtitlu[:160]}" />
  <meta name="author" content="Redactia MehedintiAzi.ro" />
  <link rel="canonical" href="{url_articol}" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{titlu}" />
  <meta property="og:description" content="{subtitlu[:160]}" />
  <meta property="og:url" content="{url_articol}" />
  <meta property="og:site_name" content="MehedintiAzi.ro" />
  <meta property="og:image" content="{img_url}" />
  <meta property="article:published_time" content="2026-{datetime.now().strftime('%m-%d')}T{ora}:00+03:00" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{titlu}",
    "datePublished": "2026-{datetime.now().strftime('%m-%d')}T{ora}:00+03:00",
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
    .article-content strong {{ color: #111; }}
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
    const parser=new DOMParser();
    const doc=parser.parseFromString(html,'text/html');
    const header=doc.querySelector('header');
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

      <p class="article-subtitle">{subtitlu}</p>

      <div class="article-meta">
        <span>📅 {data}</span>
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
        <img src="img/{poza}" alt="{titlu}" />
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
        <div class="sidebar-stire">
          <img src="img/spital-judetean-urgenta-drobeta-modernizat-fonduri-europene-2026.jpg" alt="">
          <a href="spital-judetean-urgenta-drobeta-modernizat-fonduri-europene-2026.html">Spitalul Județean Drobeta, modernizat cu 26 milioane euro</a>
        </div>
        <div class="sidebar-stire">
          <img src="img/lucrarile-cinematograful-portile-de-fier-drobeta-2026.jpg" alt="">
          <a href="lucrarile-cinematograful-portile-de-fier-drobeta-2026.html">Lucrările avansează la Cinematograful Porțile de Fier</a>
        </div>
      </div>
    </aside>

  </div>

</main>

<div id="footer-placeholder"></div>
<script>
  fetch('index.html').then(r=>r.text()).then(html=>{{
    const parser=new DOMParser();
    const doc=parser.parseFromString(html,'text/html');
    const footer=doc.querySelector('footer');
    if(footer) document.getElementById('footer-placeholder').replaceWith(footer.cloneNode(true));
  }});
</script>

</body>
</html>"""
    return html, slug

def main():
    print("=" * 50)
    print("  GENERATOR STIRE - MehedintiAzi.ro")
    print("=" * 50)

    if not os.path.exists(TEMPLATE_FILE):
        print(f"\nERROR: Nu gasesc fisierul STIRE-NOUA.txt!")
        input("\nApasa Enter pentru a inchide...")
        sys.exit(1)

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        continut = f.read()

    titlu = citeste_camp(continut, "TITLU")
    data = citeste_camp(continut, "DATA")
    ora = citeste_camp(continut, "ORA")
    categorie = citeste_camp(continut, "CATEGORIE")
    poza = citeste_camp(continut, "POZA")
    text_raw = citeste_camp(continut, "TEXT")
    taguri_str = citeste_camp(continut, "TAGURI")

    # Validari
    erori = []
    if not titlu or titlu == "Scrie titlul complet al stirii aici":
        erori.append("- TITLU nu a fost completat!")
    if not poza or poza == "nume-poza.jpg":
        erori.append("- POZA nu a fost completata!")
    if not text_raw or len(text_raw) < 100:
        erori.append("- TEXT prea scurt (minim 100 caractere)!")

    if erori:
        print("\n⚠️  ERORI in STIRE-NOUA.txt:")
        for e in erori:
            print(e)
        print("\nCorecteaza fisierul STIRE-NOUA.txt si ruleaza din nou.")
        input("\nApasa Enter pentru a inchide...")
        sys.exit(1)

    # Verifica poza
    poza_path = os.path.join(SITE_DIR, "img", poza)
    if not os.path.exists(poza_path):
        print(f"\n⚠️  ATENTIE: Poza 'img/{poza}' nu exista!")
        print("   Copiaza poza in folderul img/ inainte de publicare.")
        raspuns = input("\nContinui oricum? (da/nu): ").strip().lower()
        if raspuns != "da":
            sys.exit(1)

    slug = titlu_la_slug(titlu) + "-2026"
    text_html = proceseaza_text(text_raw)
    taguri_lista = [t.strip() for t in taguri_str.split(',') if t.strip()]

    html, slug = genereaza_html(titlu, data, ora, categorie, poza, text_html, taguri_lista, slug)

    fisier_output = os.path.join(SITE_DIR, f"{slug}.html")
    with open(fisier_output, 'w', encoding='utf-8') as f:
        f.write(html)

    # Salveaza titlul pentru commit automat
    commit_file = os.path.join(SITE_DIR, ".commit_msg.txt")
    with open(commit_file, 'w', encoding='utf-8') as f:
        f.write(titlu[:100])

    print(f"\n OK Fisier generat: {slug}.html")
    print(f"   URL:         {SITE_URL}/{slug}")
    print(f"   Poza:        img/{poza}")
    print(f"   Categorie:   {categorie}")

if __name__ == "__main__":
    main()
