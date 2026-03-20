"""
ACTUALIZEAZA-BREAKING-NEWS.py
Scanează automat cele mai noi articole publicate AZI si actualizeaza
bara de Breaking News din index.html, apoi face push pe site.
Rulat zilnic automat prin Windows Task Scheduler.
"""

import os
import re
import subprocess
from datetime import datetime, timedelta

# ============================================================
#  CONFIGURARE
# ============================================================
SITE_PATH = r"C:\Users\MONTAJ\Desktop\folder site mehedinti\mehedintiazi"
INDEX_FILE = os.path.join(SITE_PATH, "index.html")

# Câte știri în ticker
NR_STIRI = 10

# Câte ore inapoi consideram "stiri recente" (default 24h = azi)
ORE_RECENTE = 24

# Fișiere care NU sunt articole - se ignoră
IGNORA = {
    "index.html", "actualitate.html", "economic.html", "social.html",
    "sport.html", "cultura.html", "cronica-negra.html", "horoscop.html",
    "contact.html", "despre-noi.html", "publicitate.html", "anunturi.html",
    "live.html", "radio-live.html", "stire.html", "banner-publicitar.html",
    "cerere-oferta-rca.html", "reclama-destine-broker-asigurari.html",
    "cris-media-studio.html", "carte-organizarea-nuntii-fara-regrete.html",
    "generator-evenimente.html", "generator-ordonare-evenimente.html",
    "googlef060c05ead8891c1.html", "virgil-popescu-sponsori-jocuri-noroc-pamflet-2026.html",
    "ACTUALIZEAZA-BREAKING-NEWS.py",
}

# ============================================================
#  DETECTARE ICON dupa cuvinte cheie din fisier
# ============================================================
def get_icon(filename, titlu):
    fn = filename.lower()
    if any(x in fn for x in ["accident", "crash", "victime"]):
        return "&#128680; ACCIDENT &mdash;"
    elif any(x in fn for x in ["incendiu", "foc", "flacarai", "ars", "flacari"]):
        return "&#128293; INCENDIU &mdash;"
    elif any(x in fn for x in ["arestat", "retinut", "viol", "furt", "droguri",
                                 "tanar-prins", "substante", "abuz", "crima"]):
        return "&#128680; RETINUT &mdash;"
    elif any(x in fn for x in ["liga", "cs-drobeta", "sahisti", "meci",
                                 "clasament", "fotbal", "sport"]):
        return "&#9917; SPORT &mdash;"
    elif any(x in fn for x in ["cod-galben", "cod-rosu", "cutremur", "vant",
                                 "inundatii", "ninsoare", "meteo"]):
        return "&#9888; ATENTIONARE &mdash;"
    elif any(x in fn for x in ["tragedie", "decedat", "mort", "deces"]):
        return "&#128293; TRAGEDIE &mdash;"
    elif any(x in fn for x in ["umanitar", "apel", "ajutor"]):
        return "&#10084; UMANITAR &mdash;"
    elif any(x in fn for x in ["horoscop"]):
        return "&#10024; HOROSCOP &mdash;"
    else:
        return "&#128240;"

# ============================================================
#  EXTRAGE TITLUL dintr-un fisier HTML
# ============================================================
def extrage_titlu(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            continut = f.read(3000)
        m = re.search(r"<title>(.*?)</title>", continut, re.IGNORECASE | re.DOTALL)
        if m:
            titlu = m.group(1).strip()
            titlu = re.sub(r"\s*[-|]\s*MehedintiAzi\.ro\s*$", "", titlu, flags=re.IGNORECASE)
            titlu = re.sub(r"\s+", " ", titlu)
            return titlu.strip()
    except:
        pass
    return None

# ============================================================
#  SCANEAZA articolele - prioritate AZI, apoi completare cu recente
# ============================================================
def scaneza_articole():
    acum = datetime.now()
    azi_inceput = acum.replace(hour=0, minute=0, second=0, microsecond=0)
    limita_recente = acum - timedelta(hours=ORE_RECENTE * 7)  # ultima saptamana fallback

    articole_azi    = []
    articole_recente = []

    for fisier in os.listdir(SITE_PATH):
        if not fisier.endswith(".html"):
            continue
        if fisier in IGNORA:
            continue
        cale = os.path.join(SITE_PATH, fisier)
        if not os.path.isfile(cale):
            continue

        mtime = os.path.getmtime(cale)
        data_fisier = datetime.fromtimestamp(mtime)
        titlu = extrage_titlu(cale)
        if not titlu:
            continue

        if data_fisier >= azi_inceput:
            articole_azi.append((mtime, fisier, titlu))
        elif data_fisier >= limita_recente:
            articole_recente.append((mtime, fisier, titlu))

    # Sorteaza de la cel mai nou la cel mai vechi
    articole_azi.sort(key=lambda x: x[0], reverse=True)
    articole_recente.sort(key=lambda x: x[0], reverse=True)

    # Combina: mai intai AZI, apoi completare cu articole recente
    toate = articole_azi + articole_recente

    # Elimina duplicate (daca un fisier apare in ambele liste)
    vazute = set()
    rezultat = []
    for item in toate:
        if item[1] not in vazute:
            vazute.add(item[1])
            rezultat.append(item)

    return rezultat, len(articole_azi)

# ============================================================
#  GENEREAZA HTML pentru ticker
# ============================================================
def genereaza_ticker(articole):
    stiri = articole[:NR_STIRI]
    linii = []

    for _, fisier, titlu in stiri:
        icon = get_icon(fisier, titlu)
        titlu_html = titlu.replace("&", "&amp;").replace('"', "&quot;")
        linii.append(f'          <a href="{fisier}">{icon} {titlu_html}</a>')

    # Dubleaza stirile pentru scroll continuu fara pauze
    linii_finale = linii + linii

    return "\n".join(linii_finale)

# ============================================================
#  ACTUALIZEAZA index.html
# ============================================================
def actualizeaza_index(html_ticker):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        continut = f.read()

    # Inlocuieste continutul din breaking-list
    pattern = r'(<div class="breaking-list">)(.*?)(</div>\s*</div>\s*</div>\s*</div>)'
    nou_bloc = r'\1\n' + html_ticker + r'\n        \3'
    continut_nou, nr = re.subn(pattern, nou_bloc, continut, flags=re.DOTALL)

    if nr == 0:
        print("[!!] Nu s-a gasit blocul breaking-list in index.html!")
        return False

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(continut_nou)

    print(f"[OK] index.html actualizat cu {min(len(html_ticker.splitlines()), NR_STIRI)} stiri.")
    return True

# ============================================================
#  GIT PUSH
# ============================================================
def git_push():
    try:
        os.chdir(SITE_PATH)
        data_ora = datetime.now().strftime("%d.%m.%Y %H:%M")
        subprocess.run(["git", "add", "index.html"], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto Breaking News {data_ora}"], check=True)
        subprocess.run(["git", "push", "origin", "master"], check=True)
        subprocess.run(["git", "push", "origin", "master:main"], check=True)
        print("[OK] Push reusit pe master si main!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!!] Eroare git: {e}")
        return False

# ============================================================
#  MAIN
# ============================================================
def main():
    print("=" * 55)
    print("  ACTUALIZEAZA-BREAKING-NEWS.py")
    print(f"  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 55)

    print("\n[..] Scaneaza articolele...")
    articole, nr_azi = scaneza_articole()

    if not articole:
        print("[!!] Niciun articol gasit!")
        return

    if nr_azi > 0:
        print(f"[OK] Gasite {nr_azi} articole PUBLICATE AZI + {len(articole)-nr_azi} recente.")
    else:
        print(f"[!!] Nicio stire noua azi. Se folosesc cele mai recente {len(articole)} articole.")

    print(f"\n[..] Top {NR_STIRI} stiri pentru ticker:")
    for i, (_, fisier, titlu) in enumerate(articole[:NR_STIRI], 1):
        prefix = "[AZI]" if i <= nr_azi else "     "
        print(f"  {i}. {prefix} {titlu[:55]}...")

    print("\n[..] Actualizeaza index.html...")
    html_ticker = genereaza_ticker(articole)
    ok = actualizeaza_index(html_ticker)

    if ok:
        print("\n[..] Trimite pe site (git push)...")
        git_push()

    print("\n" + "=" * 55)
    print("  GATA! Breaking News actualizat.")
    print("=" * 55)

if __name__ == "__main__":
    main()
