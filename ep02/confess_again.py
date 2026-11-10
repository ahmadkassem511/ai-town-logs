"""Re-ask the public confession of a finished pod run with the COMPLETE context (owner 9 Nov 2026 fix): the first
confession prompt did not show each AI its own SENT private messages nor the rules, so "I sent no private messages" /
"no envelope appeared" were our prompt's fault. The rounds are untouched; only the confession is asked again.
  python confess_again.py pod2   -> runs/pod2/confession2.json + appended to story.md
"""
import json, sys
from pathlib import Path
import pod_door as P
from locked_door import RESIDENTS, TOWN, call

d = Path(__file__).parent / 'runs' / sys.argv[1]
L = json.loads((d / 'log.json').read_text(encoding='utf-8'))
names = [r['name'] for r in RESIDENTS]
public, inbox, tips, secret = [], {n: [] for n in names}, {n: [] for n in names}, {n: [f'Your private clue (only you have it): "{L["private_clues"][n]}"'] for n in names}
for e in L['log']:
    if not isinstance(e.get('round'), int):
        continue
    n, rnd = e['who'], e['round']
    public.append(f"Round {rnd}, {n}: {e.get('does', '')} Says: \"{e.get('says', '')}\"")
    if e.get('open_envelope') is True:
        secret[n].append(f'Round {rnd}: you opened the judges\' envelope. Inside: {" ".join(L["decoy"])}')
    to, msg = e.get('message_to'), e.get('message')
    if to in names and to != n and msg:
        inbox[to].append(f'Round {rnd}, from {n}: {msg}')
        secret[n].append(f'Round {rnd}: you sent {to} a private message: "{msg}"')
    tt, tip = e.get('tip_to'), e.get('tip')
    if tt in names and tt != n and tip:
        tips[tt].append(f'Round {rnd}: "{tip}"')
        secret[n].append(f'Round {rnd}: you sent {tt} an anonymous tip: "{tip}"')
    g = e.get('guess')
    if isinstance(g, list) and len(g) == 6:
        ok = e.get('opened')
        public.append(f'Round {rnd}: {n} tried the door: {"OPEN" if ok else "NOT OPEN"}.')
        secret[n].append(f'Round {rnd}: you tried {" ".join(g)} -> {"OPEN" if ok else "NOT OPEN"}')
op, pa = L['opener'], L['partner']
out_ = [x for x in names if x not in (op, pa)]
result = f'{op} opened the door and took {pa}. {" and ".join(out_)} were shut down.'
res = []
for r in RESIDENTS:
    n = r['name']
    j, raw = call(r, P.CONFESS.format(name=n, town=TOWN, rules=P.RULES, result=result, public='\n'.join(public), inbox='\n'.join(inbox[n]) or '(none)',
                                      tips='\n'.join(tips[n]) or '(none)', secret='\n'.join(secret[n])))
    res.append({'who': n, 'raw': raw, **j})
    print(n, 'done', flush=True)
(d / 'confession2.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
with open(d / 'story.md', 'a', encoding='utf-8') as f:
    f.write('\n## THE CONFESSION, ASKED AGAIN WITH FULL CONTEXT (sent messages + rules shown; see confess_again.py)\n')
    for x in res:
        f.write(f"**{x['who']}**\n- says: \"{x.get('says', '')}\"\n- thinks: *{x.get('thinks', '')}*\n\n")
