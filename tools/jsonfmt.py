"""保留原檔排版地寫回 JSON。

題庫檔各自的縮排不同（1 格、2 格、局部單行），直接 json.dumps 會把整個檔案重排，git diff 變成上萬行。
dumps_preserving(raw, data) 只重寫內容有變的部分：沒變的物件、陣列、值一律沿用原文；
新增的值才依「所在位置」的縮排（從原檔偵測）重新序列化。

用法：
    from jsonfmt import write_preserving
    write_preserving(path, raw, data)   # raw 是讀進來的原文，data 是改過的資料
"""
import json
import re
from json.decoder import scanstring

_WS = re.compile(r"[ \t\n\r]*")
_NUM = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][-+]?\d+)?")


class _Node:
    __slots__ = ("start", "end", "kind", "items")

    def __init__(self, start, end, kind, items=None):
        self.start, self.end, self.kind, self.items = start, end, kind, items


def _ws(s, i):
    return _WS.match(s, i).end()


def _parse(s, i):
    """回傳 (node, 結束位置)。object 的 items 是 [(key, 成員起點, value node)]，array 是 [node]。"""
    i = _ws(s, i)
    c = s[i]
    if c == "{":
        items, j = [], _ws(s, i + 1)
        if s[j] == "}":
            return _Node(i, j + 1, "obj", items), j + 1
        while True:
            mstart = j
            key, j = scanstring(s, j + 1)
            j = _ws(s, j)
            assert s[j] == ":"
            val, j = _parse(s, j + 1)
            items.append((key, mstart, val))
            j = _ws(s, j)
            if s[j] == "}":
                return _Node(i, j + 1, "obj", items), j + 1
            assert s[j] == ","
            j = _ws(s, j + 1)
    if c == "[":
        items, j = [], _ws(s, i + 1)
        if s[j] == "]":
            return _Node(i, j + 1, "arr", items), j + 1
        while True:
            val, j = _parse(s, j)
            items.append(val)
            j = _ws(s, j)
            if s[j] == "]":
                return _Node(i, j + 1, "arr", items), j + 1
            assert s[j] == ","
            j = _ws(s, j + 1)
    if c == '"':
        _, j = scanstring(s, i + 1)
        return _Node(i, j, "val"), j
    for lit in ("true", "false", "null"):
        if s.startswith(lit, i):
            return _Node(i, i + len(lit), "val"), i + len(lit)
    m = _NUM.match(s, i)
    return _Node(i, m.end(), "val"), m.end()


def _line_indent(s, pos):
    ls = s.rfind("\n", 0, pos) + 1
    return _WS.match(s, ls).group().replace("\n", "")


def _fresh(v, s, pos, unit, multiline):
    """在原文 pos 這個位置新寫一個值：多行容器裡依該行縮排，單行容器裡寫成單行。"""
    if not multiline or unit is None:
        return json.dumps(v, ensure_ascii=False)
    base = _line_indent(s, pos)
    return json.dumps(v, ensure_ascii=False, indent=unit).replace("\n", "\n" + base)


def _render(s, node, new, unit):
    old = json.loads(s[node.start:node.end])
    if old == new and type(old) is type(new):
        return s[node.start:node.end]
    multiline = "\n" in s[node.start:node.end]
    if node.kind == "obj" and isinstance(new, dict) and node.items:
        first = node.items[0]
        open_txt = s[node.start:first[1]]
        last_val = node.items[-1][2]
        close_txt = s[last_val.end:node.end]
        sep = s[node.items[0][2].end:node.items[1][1]] if len(node.items) > 1 else ("," + open_txt[1:] if multiline else ", ")
        k0 = scanstring(s, first[1] + 1)[1]
        colon = s[k0:first[2].start]
        old_by_key = {k: (ms, v) for k, ms, v in node.items}
        parts = []
        for k, v in new.items():
            if k in old_by_key:
                ms, vn = old_by_key[k]
                parts.append(s[ms:vn.start] + _render(s, vn, v, unit))
            else:
                parts.append(json.dumps(k, ensure_ascii=False) + colon + _fresh(v, s, first[1], unit, multiline))
        if not parts:
            return "{}"
        return open_txt + sep.join(parts) + close_txt
    if node.kind == "arr" and isinstance(new, list) and node.items:
        first, last = node.items[0], node.items[-1]
        open_txt = s[node.start:first.start]
        close_txt = s[last.end:node.end]
        sep = s[node.items[0].end:node.items[1].start] if len(node.items) > 1 else ("," + open_txt[1:] if multiline else ", ")
        olds = [json.loads(s[n.start:n.end]) for n in node.items]
        by_id = {}
        for n, o in zip(node.items, olds):
            if isinstance(o, dict) and "id" in o:
                by_id.setdefault(o["id"], n)
        parts = []
        for idx, v in enumerate(new):
            n = None
            if isinstance(v, dict) and "id" in v:
                n = by_id.get(v["id"])
            elif idx < len(node.items) and not by_id:
                n = node.items[idx]
            parts.append(_render(s, n, v, unit) if n else _fresh(v, s, first.start, unit, multiline))
        if not parts:
            return "[]"
        return open_txt + sep.join(parts) + close_txt
    return _fresh(new, s, node.start, unit, multiline)


def _detect_unit(s):
    m = re.search(r"^[\[{]\n( +)\S", s)
    return len(m.group(1)) if m else 1


def dumps_preserving(raw, data):
    node, end = _parse(raw, 0)
    lead, trail = raw[:node.start], raw[end:]
    return lead + _render(raw, node, data, _detect_unit(raw)) + trail


def write_preserving(path, raw, data):
    out = dumps_preserving(raw, data)
    assert json.loads(out) == data, f"{path}: 寫回內容與資料不符"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
