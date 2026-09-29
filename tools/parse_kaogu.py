#!/usr/bin/env python3
"""Parse the 113 微免考古 text dump into structured JSON.

Output: list of question dicts written to ../subjects/micro-immuno/data/kaogu-raw.json
Manual fixes are applied afterwards in fix_kaogu.py.
"""
import json, re, sys
from pathlib import Path

SRC = Path(__file__).with_name('kaogu113.txt')
lines = SRC.read_text(encoding='utf-8').replace('\r','').split('\n')

# (section id, title, q_start, a_start, end)  -- 1-indexed inclusive line numbers
SECTIONS = [
    ('bact',   'Bacterial Structure, Classification, Genetics and Metabolism', 1, 282, 497),
    ('innate', 'Innate Immunity', 498, 813, 1042),
    ('agab',   'Antigen and Antibody & Antibody Diversity', 1043, 1215, 1316),
    ('tdev',   'The Development of T Cell & Antigen Recognition', 1317, 1405, 1473),
    ('tact',   'T cell Activation and Cell Cooperation', 1474, 1668, 1810),
    ('staph1', 'Staphylococcus, Streptococcus & Enterococcus Part I', 1811, 1873, 1919),
    ('staph2', 'Staphylococcus, Streptococcus & Enterococcus Part II', 1920, 2057, 2183),
    ('entero', 'Enterobacteriaceae', 2184, 2320, 2427),
    ('bacillus','Bacillus, Corynebacteria, Listeria', 2428, 2549, 2703),
    ('neis',   'Neisseria, Campylobacter, Helicobacter, Pseudomonas', 2704, 2884, 3193),
    ('fungi',  'Fungal Structure and Mycosis', 3194, 3528, 3858),
    ('mid111', '111 微免期中考古', 3859, 4248, 4349),
]

HEADER_RE = re.compile(r'(微免考古小隊|組長：|組長:|^選擇題$|^簡答$|^詳解$|恭喜你)')
QSTART_RE = re.compile(r'^\s*(\d{1,2})\s*[.．]\s*(.*)$')
NUMROW_RE = re.compile(r'^\s*\d{1,2}(\s+\d{1,2})*\s*$')


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def parse_questions(sec_lines, title):
    qs = []
    cur = None
    expected = 1
    for ln in sec_lines:
        if HEADER_RE.search(ln) or clean(ln) == clean(title) or clean(ln).startswith(title[:25]):
            continue
        m = QSTART_RE.match(ln)
        if m and int(m.group(1)) in (expected, expected + 1) and not re.match(r'^\s*\d+\.\s*\d', ln):
            n = int(m.group(1))
            cur = {'num': n, 'raw': m.group(2)}
            qs.append(cur)
            expected = n + 1
            continue
        if cur is not None:
            cur['raw'] += '\n' + ln
    out = []
    for q in qs:
        raw = q['raw']
        # split into stem / options on (A)...(E) markers (half-width parens only)
        parts = re.split(r'\(([A-E])\)', raw)
        stem = parts[0]
        opts = []
        seen = set()
        for i in range(1, len(parts) - 1, 2):
            k, t = parts[i], parts[i + 1]
            if k in seen:
                # duplicated letter (garbled layout) -> append to previous
                opts[-1]['t'] += f' ({k}) ' + t
                continue
            seen.add(k)
            opts.append({'k': k, 't': clean(t)})
        out.append({'num': q['num'], 'stem': clean(stem), 'stem_raw': stem.strip(),
                    'options': opts})
    return out


def parse_key(sec_lines):
    key = {}
    i = 0
    while i < len(sec_lines) - 1:
        ln = sec_lines[i]
        if NUMROW_RE.match(ln):
            nums = [int(x) for x in ln.split()]
            toks = sec_lines[i + 1].split()
            # merge "A or B"
            merged = []
            j = 0
            while j < len(toks):
                if j + 2 < len(toks) and toks[j + 1] == 'or':
                    merged.append(toks[j] + '/' + toks[j + 2]); j += 3
                else:
                    merged.append(toks[j]); j += 1
            if len(merged) == len(nums) and all(re.fullmatch(r'[A-EX]+|[A-E](/[A-E])+|見詳解', t) for t in merged):
                for n, t in zip(nums, merged):
                    key[n] = t
                i += 2
                continue
        i += 1
    return key


EXPL_RE = re.compile(r'^\s*(\d{1,2})\s*[.．]\s*(.*)$')


def parse_expl(sec_lines, title, maxn):
    ex = {}
    cur = None
    expected = 1
    skip_next = False
    for idx, ln in enumerate(sec_lines):
        if skip_next:
            skip_next = False
            continue
        if NUMROW_RE.match(ln) and idx + 1 < len(sec_lines) and re.fullmatch(r'(\s*([A-EX]+|[A-E]/[A-E]|or|見詳解))+\s*', sec_lines[idx + 1]):
            skip_next = True  # skip the answer row after a number row
            continue
        if HEADER_RE.search(ln) or clean(ln).startswith(title[:25]):
            continue
        m = EXPL_RE.match(ln)
        if m:
            n = int(m.group(1))
            rest = m.group(2)
            looks_like_ans = re.match(r'^\s*\(?[A-E]\)|^X\b|^\(?[A-E]\)?\s*(or|\()', rest) or rest.strip() == '' or n == expected
            if n >= expected and n <= maxn and n - expected <= 2 and looks_like_ans:
                cur = n
                ex[n] = rest
                expected = n + 1
                continue
        if cur is not None:
            ex[cur] += '\n' + ln
    return {k: v.strip() for k, v in ex.items()}


def main():
    allq = []
    for sid, title, qs_, as_, end in SECTIONS:
        qlines = lines[qs_ - 1:as_ - 1]
        alines = lines[as_ - 1:end]
        qs = parse_questions(qlines, title)
        key = parse_key(alines)
        ex = parse_expl(alines, title, max([q['num'] for q in qs] + [0]))
        for q in qs:
            n = q['num']
            q['id'] = f'k113-{sid}-{n:02d}'
            q['section'] = sid
            q['sectionTitle'] = title
            q['key'] = key.get(n)
            q['explain'] = ex.get(n, '')
            allq.append(q)
        print(f'{sid:8s} questions={len(qs):3d} keys={len(key):3d} expl={len(ex):3d}', file=sys.stderr)
    out = Path(__file__).parent / 'kaogu-raw.json'
    out.write_text(json.dumps(allq, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'total {len(allq)} -> {out}', file=sys.stderr)


if __name__ == '__main__':
    main()
