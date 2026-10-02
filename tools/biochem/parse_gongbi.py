"""把 113 生化共筆（pdftotext -layout 輸出）解析成題目 JSON 的初稿。
用法：python3 tools/biochem/parse_gongbi.py  → tools/biochem/gongbi-raw.json
"""
import json, re, os
HERE = os.path.dirname(__file__)
L = open(os.path.join(HERE, 'gongbi113.txt'), encoding='utf-8').read().replace('\r', '').split('\n')

# (起始行號, 章節 id, 來源標籤)
SECTIONS = [
    (1, 'ch17', '17-1'), (110, 'ch17', '17-2'), (511, 'ch21', '21'),
    (729, 'ch23', '23-1'), (1240, 'ch23', '23-2'), (1724, 'ch18', '18'), (2886, 'ch22', '22'),
]
bounds = [s[0] - 1 for s in SECTIONS] + [len(L)]

NUMROW = re.compile(r'^\s*(\d+)(\s+\d+)+\s*$')
LETROW = re.compile(r'^\s*([A-EX]{1,4})(\s+[A-EX]{1,4})*\s*$')

def parse_section(lines):
    # 找答案表
    t0 = None
    for i, l in enumerate(lines):
        if NUMROW.match(l) and l.split()[0] == '1':
            t0 = i; break
    assert t0 is not None
    answers = {}
    i = t0; last = t0
    while i < len(lines) and i < t0 + 40:
        if NUMROW.match(lines[i]):
            nums = [int(x) for x in lines[i].split()]
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines) and LETROW.match(lines[j]):
                lets = lines[j].split()
                if len(lets) == len(nums):
                    for n, a in zip(nums, lets): answers[n] = a
                    last = j
            i = j + 1
        else:
            i += 1
    qpart = lines[:t0]; epart = lines[last + 1:]
    # 題目
    qs = {}; cur = None; expect = 1; field = None
    for l in qpart:
        m = re.match(r'^\s*(\d+)\s*\.\s*(.*)$', l)
        if m and int(m.group(1)) == expect:
            cur = {'num': expect, 'stem': m.group(2).strip(), 'options': []}
            qs[expect] = cur; expect += 1; field = 'stem'; continue
        if cur is None: continue
        s = l.strip()
        if not s or s in ('選擇題', '簡答', '簡答選擇題'): continue
        mo = re.match(r'^\(([A-E])\)\s*(.*)$', s)
        if mo:
            cur['options'].append({'k': mo.group(1), 't': mo.group(2).strip()}); field = 'opt'; continue
        if field == 'opt' and cur['options']:
            cur['options'][-1]['t'] += ' ' + s
        else:
            cur['stem'] += ('\n' if re.match(r'^\(?\d\)?[.)]', s) else ' ') + s
    # 詳解
    ex = {}; cur = None; expect = 1
    for l in epart:
        m = re.match(r'^\s*(\d+)\s*\.\s*(\([A-EX]\)|X|\(X\)|[A-E]\b)?(.*)$', l)
        if m and int(m.group(1)) == expect and (m.group(2) or expect == 1 or True):
            # 只在「數字. (」或「數字.(」型態才換題，避免詳解內文的編號清單誤判
            if re.match(r'^\s*\d+\s*\.\s*(\(|X)', l):
                cur = expect; ex[cur] = [m.group(3).strip()]; expect += 1; continue
        if cur is not None:
            ex[cur].append(l.strip())
    return qs, answers, ex

out = []
for k, (start, ch, tag) in enumerate(SECTIONS):
    qs, ans, ex = parse_section(L[bounds[k]:bounds[k + 1]])
    for n, q in qs.items():
        e = '\n'.join(x for x in ex.get(n, []) if x).strip()
        out.append({'tag': tag, 'chapter': ch, 'num': n, 'stem': q['stem'], 'options': q['options'],
                    'answer': ans.get(n, ''), 'explain_raw': e})
    print(tag, 'questions', len(qs), 'answers', len(ans), 'explains', len(ex))
json.dump(out, open(os.path.join(HERE, 'gongbi-raw.json'), 'w'), ensure_ascii=False, indent=1)
