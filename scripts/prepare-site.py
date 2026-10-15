"""Move the reviewed reading demo into its own static website."""
from pathlib import Path
import json, re, shutil, sys

root=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]).resolve()
original=source/'artivid'
page=(root/'index.html').read_text()
if '/artivid/' not in page and 'Сайт создан на Syolana' in page:
    print('The independent reading entry is already prepared.')
    raise SystemExit(0)
for directory in ('books','covers','audio-library','assets'):
    shutil.copytree(original/directory,root/directory,dirs_exist_ok=True)
for name in ('flight.js','scene-audio.js','utils.js'):
    shutil.copy2(source/name,root/name)
shutil.copy2(source/'assets/logo.svg',root/'assets/syolana-logo.svg')
(root/'styles.css').write_text((original/'styles.css').read_text())
bootstrap="window.__syolanaAssetBase=new URL('./',document.baseURI).href;window.__syolanaAssetReady=Promise.resolve(window.__syolanaAssetBase);"
page,count=re.subn(r'<script>window\.__syolanaAssetReady=.*?</script>','<script>'+bootstrap+'</script>',page,count=1,flags=re.S)
assert count==1,'Unexpected original entry page'
page,count=re.subn(r'function oo\(t\)\{return typeof t=="string".*?:t\}', 'function oo(t){return t}',page,count=1)
assert count==1,'Unexpected asset resolver'
page=page.replace('https://syolana.com/artivid/','').replace('https://syolana.website.yandexcloud.net/artivid/','')
page=page.replace('import(window.__syolanaAssetBase+"themes.js")','import("https://syolana.com/themes.js")')
page=page.replace('https://syolana.com/assets/syolana-logo.svg','assets/syolana-logo.svg')
footer='''<footer id="footer" class="partner-footer">
  <div class="partner-footer-meta"><span>© Артивид</span><nav class="partner-footer-nav" aria-label="Информация о сайте"><a href="#/terms">Условия чтения</a><a href="#/privacy">Данные</a><a href="https://www.avito.ru/brands/i223140984" rel="noopener noreferrer">Авторам и читателям</a></nav></div>
  <p class="partner-footer-credit"><a class="syolana-credit" href="https://syolana.com/" target="_blank" rel="noopener noreferrer"><img src="assets/syolana-logo.svg" width="28" height="28" alt=""><span>Сайт создан на Syolana</span></a></p>
</footer>'''
page,count=re.subn(r'<footer id="footer">.*?</footer>',footer,page,count=1,flags=re.S)
assert count==1,'Unexpected original footer'
page=page.replace('</head>','<link rel="stylesheet" href="partner-attribution.css?v=20261015-credit-1"></head>')
assert '/artivid/' not in page,'The reading site still depends on its former location'
assert 'Сайт создан на Syolana' in page
(root/'index.html').write_text(page)
(root/'robots.txt').write_text('User-agent: *\nAllow: /\n')
(root/'.nojekyll').touch()
for path in (root/'books').glob('*.json'):json.loads(path.read_text())
assert (root/'assets/syolana-logo.svg').is_file()
print('Standalone reading site prepared; books and reading audio are local.')
