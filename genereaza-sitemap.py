import os
from datetime import date

BASE_URL = "https://mehedintiazi.ro"
FOLDER = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().strftime("%Y-%m-%d")

# Pagini de exclus (nu sunt articole)
EXCLUDE = {
    "banner-publicitar.html",
    "generator-evenimente.html",
    "generator-ordonare-evenimente.html",
    "googlef060c05ead8891c1.html",
    "cerere-oferta-rca.html",
    "reclama-destine-broker-asigurari.html",
    "cris-media-studio.html",
    "carte-organizarea-nuntii-fara-regrete.html",
    "stire.html",
    "burtiera-carburanti.html",
}

# Pagini de categorie (sectiuni site)
CATEGORII = {
    "actualitate.html", "social.html", "economic.html", "sport.html",
    "cultura.html", "cronica-negra.html", "anunturi.html", "horoscop.html",
    "live.html", "radio-live.html", "despre-noi.html", "contact.html",
    "publicitate.html",
}

urls = []

# Homepage
urls.append(f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

# Categorii
for f in sorted(CATEGORII):
    if os.path.exists(os.path.join(FOLDER, f)):
        urls.append(f"""  <url>
    <loc>{BASE_URL}/{f}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""")

# Articole
articole = []
for f in os.listdir(FOLDER):
    if f.endswith(".html") and f not in EXCLUDE and f not in CATEGORII and f != "index.html":
        articole.append(f)

for f in sorted(articole):
    urls.append(f"""  <url>
    <loc>{BASE_URL}/{f}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "\n".join(urls) + "\n</urlset>"

output_path = os.path.join(FOLDER, "sitemap.xml")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Sitemap generat cu {len(urls)} URL-uri -> sitemap.xml")
