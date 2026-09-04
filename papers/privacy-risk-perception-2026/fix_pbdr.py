# -*- coding: utf-8 -*-
"""docx-js 9.7.1 emits <w:pBdr> children as top,bottom,left,... but the OOXML
schema fixes the order at top,left,bottom,right,between,bar. Reorder them."""
import re, shutil, subprocess, sys, os, zipfile

DOCX = sys.argv[1] if len(sys.argv) > 1 else '中文译本.docx'
ORDER = ['top', 'left', 'bottom', 'right', 'between', 'bar']
WORK = '_fixdocx'

shutil.rmtree(WORK, ignore_errors=True)
with zipfile.ZipFile(DOCX) as z:
    names = z.namelist()
    z.extractall(WORK)

path = os.path.join(WORK, 'word/document.xml')
xml = open(path, encoding='utf-8').read()

fixed = [0]
def reorder(m):
    body = m.group(1)
    kids = re.findall(r'<w:(?:top|left|bottom|right|between|bar)\b[^>]*/>', body)
    if len(kids) != len(re.findall(r'<w:\w+', body)):
        return m.group(0)                      # unexpected content, leave alone
    key = lambda k: ORDER.index(re.match(r'<w:(\w+)', k).group(1))
    ordered = sorted(kids, key=key)
    if ordered != kids:
        fixed[0] += 1
    return '<w:pBdr>%s</w:pBdr>' % ''.join(ordered)

xml = re.sub(r'<w:pBdr>(.*?)</w:pBdr>', reorder, xml, flags=re.S)
open(path, 'w', encoding='utf-8').write(xml)

# rezip preserving the original entry order ([Content_Types].xml must be first)
out = DOCX
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names:
        z.write(os.path.join(WORK, n), n)
shutil.rmtree(WORK, ignore_errors=True)
print('reordered %d <w:pBdr> blocks in %s' % (fixed[0], out))
