"""tools/template.html の __DATA__ に data/spots.json を埋め込み、ルートの index.html を作る
data/yomi.json（名前→ひらがなの読み。道の駅は「道の駅」を除いた名前がキー。複数の読みは | 区切り）があれば y として付ける"""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parent.parent
spots=json.loads((root/'data/spots.json').read_text(encoding='utf-8'))
yomi=json.loads((root/'data/yomi.json').read_text(encoding='utf-8'))
used=set()
for s in spots:
  k=re.sub(r'^道の駅\s*','',s['n'])
  if k in yomi: s['y']=yomi[k]; used.add(k)
for k in set(yomi)-used: print('yomi.json の未使用キー:',k)
data=json.dumps(spots,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=(root/'tools/template.html').read_text(encoding='utf-8').replace('__DATA__',data)
(root/'index.html').write_text(html,encoding='utf-8')
print('index.html written')
