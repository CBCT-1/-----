# -*- coding: utf-8 -*-
import os
from playwright.sync_api import sync_playwright

HERE = os.path.abspath('.')
FOOT = ('<div style="width:100%;font-family:sans-serif;font-size:8px;color:#8b929c;'
        'padding:0 18mm;display:flex;justify-content:space-between;">'
        '<span>Huang et al. (2026), Front. Psychol. 17:1891374 · CC BY 4.0 · 中文译本</span>'
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox', '--font-render-hinting=none'])
    pg = b.new_page()
    pg.goto('file://%s/translation.html' % HERE, wait_until='networkidle')
    pg.emulate_media(media='print')
    pg.pdf(path='中文译本.pdf', format='A4', print_background=True,
           display_header_footer=True,
           header_template='<div></div>', footer_template=FOOT,
           margin={'top': '19mm', 'bottom': '17mm', 'left': '18mm', 'right': '18mm'})
    b.close()
print('pdf ok', os.path.getsize('中文译本.pdf'), 'bytes')
