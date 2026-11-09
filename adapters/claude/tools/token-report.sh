#!/bin/bash
# Token use per Claude session and per agent, read from the local transcripts. Run when you want a number, not in the background.
# Usage: bash .claude/tools/token-report.sh [--since YYYY-MM-DD] [--csv] [--dir <projects dir>]
# Reads ~/.claude/projects/<this project>/*.jsonl and <session>/subagents/agent-*.jsonl on THIS machine only
# (a cloud session's transcripts disappear with its container; run this on the Mac for Mac sessions).
# Counts only numbers: no message text is read into the output. Each API message is counted once (the transcript repeats
# its usage on every content block).
# Columns: input = new input tokens, cache_write = tokens written to the prompt cache, cache_read = tokens read from it,
# output = tokens produced. Cache reads are far cheaper than input; do not add the four columns into one number.
exec python3 -I - "$@" <<'PY'
import sys, os, json, glob, collections, datetime

args = sys.argv[1:]
since = None; csv = False; base = None
i = 0
while i < len(args):
    a = args[i]
    if a == '--since': since = args[i+1]; i += 2
    elif a == '--csv': csv = True; i += 1
    elif a == '--dir': base = args[i+1]; i += 2
    else: print('unknown option', a); sys.exit(2)
if base is None:
    root = os.environ.get('CLAUDE_PROJECTS_DIR', os.path.expanduser('~/.claude/projects'))
    key = os.getcwd().replace('/', '-').replace('.', '-')
    base = os.path.join(root, key)
if not os.path.isdir(base):
    print('no transcripts at', base); sys.exit(1)

KEYS = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')

def read(path):
    """Return (first timestamp, message count, totals) with each message id counted once (max per field)."""
    per = {}; first = None; models = set()
    for line in open(path, errors='replace'):
        try: d = json.loads(line)
        except ValueError: continue
        m = d.get('message')
        if not isinstance(m, dict) or not m.get('usage'): continue
        first = first or d.get('timestamp')
        mid = m.get('id') or d.get('uuid')
        u = m['usage']; cur = per.setdefault(mid, dict.fromkeys(KEYS, 0))
        for k in KEYS: cur[k] = max(cur[k], u.get(k) or 0)
        if m.get('model'): models.add(m['model'])
    tot = dict.fromkeys(KEYS, 0)
    for u in per.values():
        for k in KEYS: tot[k] += u[k]
    return first, len(per), tot, ','.join(sorted(models))

rows = []
for f in sorted(glob.glob(os.path.join(base, '*.jsonl'))):
    sid = os.path.basename(f)[:-6]
    first, n, tot, models = read(f)
    if n == 0: continue
    day = (first or '')[:10]
    if since and day < since: continue
    rows.append(('session', sid[:8], day, 'main', models, n, tot))
    for sf in sorted(glob.glob(os.path.join(base, sid, 'subagents', 'agent-*.jsonl'))):
        meta = {}
        try: meta = json.load(open(sf[:-6] + '.meta.json'))
        except (OSError, ValueError): pass
        a_first, a_n, a_tot, a_models = read(sf)
        if a_n == 0: continue
        label = '%s: %s' % (meta.get('agentType', 'agent'), meta.get('description', os.path.basename(sf)[6:14]))
        rows.append(('agent', sid[:8], (a_first or day)[:10], label, a_models, a_n, a_tot))

def fmt(r):
    kind, sid, day, label, models, n, t = r
    return [kind, sid, day, label, models, str(n), str(t['input_tokens']), str(t['output_tokens']),
            str(t['cache_creation_input_tokens']), str(t['cache_read_input_tokens'])]

head = ['kind', 'session', 'date', 'label', 'model', 'msgs', 'input', 'output', 'cache_write', 'cache_read']
out = [fmt(r) for r in rows]
if csv:
    print(','.join(head))
    for r in out: print(','.join('"%s"' % c.replace('"', "'") if j == 3 else c for j, c in enumerate(r)))
    sys.exit(0)
if not out: print('no sessions found in', base); sys.exit(0)
tot = collections.Counter()
for r in rows:
    for k in KEYS: tot[k] += r[6][k]
w = [max(len(h), max(len(r[j]) for r in out)) for j, h in enumerate(head)]
w[3] = min(w[3], 48)
def line(cells): return '  '.join((c[:w[j]]).ljust(w[j]) if j < 5 else c.rjust(w[j]) for j, c in enumerate(cells))
print(line(head)); print(line(['-' * x for x in w]))
for r in out: print(line(r))
print(line(['-' * x for x in w]))
print(line(['total', '', '', '', '', str(sum(r[5] for r in rows)), str(tot['input_tokens']), str(tot['output_tokens']),
            str(tot['cache_creation_input_tokens']), str(tot['cache_read_input_tokens'])]))
print('\nAgent rows come from separate transcripts, so the total adds them to their session.')
PY
