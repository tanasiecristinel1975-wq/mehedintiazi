# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

content = open('index.html', encoding='utf-8').read()

old_marker = 'href="poligon-examen-auto-permis-categoria-b-reintroducere-2026.html"'
idx = content.find(old_marker)
# Gasim inceputul liniei (a href)
start = content.rfind('<a href', 0, idx)
# Gasim dupa cele 3 linkuri (3 inchideri </a>)
end = content.find('</a>', content.find('</a>', content.find('</a>', start) + 1) + 1) + 4

old_block = content[start:end]
new_block = '''<a href="cupa-mehedinti-inot-bazinul-drobeta-2026.html">&#127946; Cupa Mehedin\u021bi la \u00cenot \u2014 Robert Glin\u021b\u0103, campion european \u015fi olimpic, prezent la Bazinul Drobeta</a>
          <a href="spital-judetean-urgenta-drobeta-modernizat-fonduri-europene-2026.html">&#127973; Spitalul Jude\u021bean Drobeta, complet modernizat cu peste 26 milioane euro din fonduri europene</a>
          <a href="lucrarile-cinematograful-portile-de-fier-drobeta-2026.html">&#127916; Cinematograful Por\u021bile de Fier: acoperi\u015f finalizat 100%, fa\u021bad\u0103 70-80% \u2014 finisajele interioare \u00encep \u00een maxim o s\u0103pt\u0103m\u00e2n\u0103</a>'''

content = content.replace(old_block, new_block, 1)
open('index.html', 'w', encoding='utf-8').write(content)
print('OK - Breaking news actualizat!')
