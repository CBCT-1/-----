// Build a formatted .docx from the Chinese translation markdown.
const fs = require('fs');
const path = require('path');
const D = require('docx');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType, HeadingLevel, LevelFormat,
  convertMillimetersToTwip,
} = D;

const SRC = 'translation.md';
const OUT = '中文译本.docx';

// ---- typography -----------------------------------------------------------
const SERIF = { ascii: 'Times New Roman', hAnsi: 'Times New Roman', eastAsia: '宋体' };
const SANS  = { ascii: 'Arial', hAnsi: 'Arial', eastAsia: '黑体' };
const INK = '1A1A1A', NAVY = '12233D', BLUE = '1F4D8F', GREY = '4A525C', GOLD = '7A5C10';
const TEXT_W = 9639;               // A4 minus 2cm margins, in DXA

// ---- tiny markdown block splitter -----------------------------------------
const lines = fs.readFileSync(SRC, 'utf8').replace(/\r\n/g, '\n').split('\n');
const blocks = [];
for (let i = 0; i < lines.length; i++) {
  const ln = lines[i];
  if (!ln.trim()) continue;
  if (/^#{1,4}\s/.test(ln)) {
    blocks.push({ t: 'h', level: ln.match(/^#+/)[0].length, text: ln.replace(/^#+\s*/, '') });
  } else if (/^---+$/.test(ln.trim())) {
    blocks.push({ t: 'hr' });
  } else if (ln.startsWith('>')) {
    const buf = [];
    while (i < lines.length && (lines[i].startsWith('>') || (buf.length && !lines[i].trim()))) {
      if (!lines[i].startsWith('>')) break;
      buf.push(lines[i].replace(/^>\s?/, ''));
      i++;
    }
    i--;
    const paras = buf.join('\n').split(/\n\s*\n/).map(s => s.replace(/\n/g, ' ').trim()).filter(Boolean);
    blocks.push({ t: 'quote', paras });
  } else if (ln.trim().startsWith('|')) {
    const buf = [];
    while (i < lines.length && lines[i].trim().startsWith('|')) { buf.push(lines[i].trim()); i++; }
    i--;
    blocks.push({ t: 'table', rows: buf });
  } else if (/^!\[/.test(ln.trim())) {
    blocks.push({ t: 'img', src: ln.match(/\(([^)]+)\)/)[1] });
  } else if (/^[-*]\s/.test(ln.trim())) {
    const buf = [];
    while (i < lines.length && /^[-*]\s/.test(lines[i].trim())) { buf.push(lines[i].trim().replace(/^[-*]\s*/, '')); i++; }
    i--;
    blocks.push({ t: 'ul', items: buf });
  } else if (/^\d+\.\s/.test(ln.trim())) {
    const buf = [];
    while (i < lines.length && /^\d+\.\s/.test(lines[i].trim())) { buf.push(lines[i].trim().replace(/^\d+\.\s*/, '')); i++; }
    i--;
    blocks.push({ t: 'ol', items: buf });
  } else {
    blocks.push({ t: 'p', text: ln.trim() });
  }
}

// ---- inline **bold** ------------------------------------------------------
function runs(text, opts = {}) {
  const base = { font: opts.font || SERIF, size: opts.size || 21, color: opts.color || INK };
  const ESC = '\u0000';                                   // park escaped asterisks
  const src = text.replace(/\\\*/g, ESC).replace(/\\_/g, '_');
  const out = [];
  for (const piece of src.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g)) {
    if (!piece) continue;
    const b = /^\*\*[^*]+\*\*$/.test(piece);
    const it = !b && /^\*[^*]+\*$/.test(piece);
    const t = (b ? piece.slice(2, -2) : it ? piece.slice(1, -1) : piece)
                .split(ESC).join('*');
    out.push(new TextRun({ ...base, text: t, bold: b || opts.bold, italics: it,
      color: b ? (opts.boldColor || NAVY) : base.color }));
  }
  return out.length ? out : [new TextRun({ ...base, text: '' })];
}

const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

// ---- element builders -----------------------------------------------------
function heading(b) {
  if (b.level === 1) {
    return new Paragraph({
      spacing: { after: 160 },
      children: runs(b.text, { font: SANS, size: 34, color: NAVY, bold: true, boldColor: NAVY }),
    });
  }
  if (b.level === 2) {
    return new Paragraph({
      heading: HeadingLevel.HEADING_1, spacing: { before: 380, after: 160 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLUE, space: 4 } },
      children: runs(b.text, { font: SANS, size: 26, color: NAVY, bold: true, boldColor: NAVY }),
    });
  }
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 110 },
    children: runs(b.text, { font: SANS, size: 22, color: BLUE, bold: true, boldColor: BLUE }),
  });
}

function para(b) {
  // figure captions read as a smaller, grey block
  if (/^\*\*图\s*\d+/.test(b.text)) {
    return new Paragraph({
      spacing: { before: 60, after: 260 }, alignment: AlignmentType.LEFT,
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'E2E7EE', space: 6 } },
      children: runs(b.text, { font: SANS, size: 17, color: GREY, boldColor: NAVY }),
    });
  }
  if (/^\*\*表\s*\d+/.test(b.text)) {
    return new Paragraph({
      spacing: { before: 260, after: 90 },
      children: runs(b.text, { font: SANS, size: 19, color: NAVY, boldColor: NAVY }),
    });
  }
  if (/^注[:：]/.test(b.text)) {
    return new Paragraph({
      spacing: { before: 60, after: 200 },
      children: runs(b.text, { font: SANS, size: 16, color: GREY }),
    });
  }
  return new Paragraph({
    spacing: { after: 130, line: 340 }, alignment: AlignmentType.BOTH,
    children: runs(b.text),
  });
}

function quote(b, first) {
  return b.paras.map((p, idx) => new Paragraph({
    spacing: { before: idx === 0 ? 60 : 0, after: idx === b.paras.length - 1 ? 260 : 90, line: 300 },
    indent: { left: 260, right: 160 },
    shading: { type: ShadingType.CLEAR, fill: first ? 'F5F7FA' : 'FDF9F0' },
    border: {
      top: idx === 0 ? { style: BorderStyle.SINGLE, size: 2, color: first ? 'F5F7FA' : 'FDF9F0', space: 4 } : NO_BORDER,
      left: { style: BorderStyle.SINGLE, size: 18, color: first ? BLUE : 'C8992A', space: 8 },
      bottom: idx === b.paras.length - 1 ? { style: BorderStyle.SINGLE, size: 2, color: first ? 'F5F7FA' : 'FDF9F0', space: 4 } : NO_BORDER,
    },
    children: runs(p, { font: SANS, size: 17, color: first ? '40474F' : '4A412C', boldColor: first ? NAVY : GOLD }),
  }));
}

function hrule() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D8DDE4', space: 1 } },
    children: [new TextRun({ text: '', size: 2 })],
  });
}

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}

function image(b) {
  const { w, h, data } = pngSize(b.src);
  const width = 560, height = Math.round(width * h / w);
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 220, after: 60 },
    children: [new ImageRun({ data, type: 'png', transformation: { width, height } })],
  });
}

function list(b, ordered) {
  return b.items.map(it => new Paragraph({
    numbering: { reference: ordered ? 'num-ol' : 'num-ul', level: 0 },
    spacing: { after: 90, line: 330 }, alignment: AlignmentType.BOTH,
    children: runs(it),
  }));
}

function table(b) {
  const cellsOf = r => r.replace(/^\||\|$/g, '').split('|').map(s => s.trim());
  const rows = b.rows.filter(r => !/^\|[\s:|-]+\|$/.test(r)).map(cellsOf);
  const head = rows[0], body = rows.slice(1);
  const n = head.length;
  const firstW = Math.round(TEXT_W * (n > 6 ? 0.20 : 0.28));
  const restW = Math.round((TEXT_W - firstW) / (n - 1));
  const widths = [firstW, ...Array(n - 1).fill(restW)];

  const mkCell = (txt, i, isHead, last) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 70, right: 70 },
    shading: isHead ? { type: ShadingType.CLEAR, fill: 'EEF2F7' } : undefined,
    borders: {
      top: isHead ? { style: BorderStyle.SINGLE, size: 10, color: NAVY } : NO_BORDER,
      left: NO_BORDER,
      bottom: isHead ? { style: BorderStyle.SINGLE, size: 6, color: NAVY }
                     : (last ? { style: BorderStyle.SINGLE, size: 10, color: NAVY }
                             : { style: BorderStyle.SINGLE, size: 2, color: 'E2E7EE' }),
      right: NO_BORDER,
    },
    children: [new Paragraph({
      alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
      spacing: { after: 0, line: 260 },
      children: runs(txt || '', { font: SANS, size: 16, color: isHead ? NAVY : INK,
                                  bold: isHead, boldColor: NAVY }),
    })],
  });

  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: head.map((c, i) => mkCell(c, i, true, false)) }),
      ...body.map((r, ri) => new TableRow({
        children: Array.from({ length: n }, (_, i) => mkCell(r[i], i, false, ri === body.length - 1)),
      })),
    ],
  });
}

// ---- assemble -------------------------------------------------------------
const children = [];
let quoteSeen = 0;
for (const b of blocks) {
  if (b.t === 'h') children.push(heading(b));
  else if (b.t === 'p') children.push(para(b));
  else if (b.t === 'quote') children.push(...quote(b, quoteSeen++ === 0));
  else if (b.t === 'hr') children.push(hrule());
  else if (b.t === 'img') children.push(image(b));
  else if (b.t === 'ul') children.push(...list(b, false));
  else if (b.t === 'ol') children.push(...list(b, true));
  else if (b.t === 'table') { children.push(table(b)); children.push(new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: '', size: 2 })] })); }
}

const doc = new Document({
  creator: 'Claude Code',
  title: '大学生隐私风险感知与隐私披露行为（中文译本）',
  description: 'Huang et al. (2026), Front. Psychol. 17:1891374, CC BY 4.0 — 中文译本',
  styles: { default: { document: { run: { font: SERIF, size: 21, color: INK } } } },
  numbering: {
    config: [
      { reference: 'num-ul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 420, hanging: 220 } } } }] },
      { reference: 'num-ol', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 420, hanging: 220 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        margin: {
          top: convertMillimetersToTwip(22), bottom: convertMillimetersToTwip(20),
          left: convertMillimetersToTwip(20), right: convertMillimetersToTwip(20),
        },
      },
    },
    footers: {
      default: new D.Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: 'Huang et al. (2026), Front. Psychol. 17:1891374 · CC BY 4.0 · 中文译本    ',
              font: SANS, size: 14, color: '8B929C' }),
            new TextRun({ children: [D.PageNumber.CURRENT], font: SANS, size: 14, color: '8B929C' }),
            new TextRun({ text: ' / ', font: SANS, size: 14, color: '8B929C' }),
            new TextRun({ children: [D.PageNumber.TOTAL_PAGES], font: SANS, size: 14, color: '8B929C' }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log('wrote', OUT, buf.length, 'bytes |', blocks.length, 'blocks');
});
