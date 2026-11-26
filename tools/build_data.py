import json,shapefile,sys
import pathlib
root=pathlib.Path(__file__).resolve().parent.parent
base=str(root/'raw')
P=['茨城県','栃木県','群馬県','埼玉県','千葉県','東京都','神奈川県','山梨県','静岡県']
out=[]
import re
def muni(a):
  m=re.match(r'^(?:.+?郡)?(.+?[市町村])',a)
  return m.group(1) if m else a[:6]
g=json.load(open(base+'/p35/P35-18_GML/P35-18_Roadside_Station.geojson'))
for i,f in enumerate(g['features']):
  p=f['properties']
  if p['P35_003'] not in P: continue
  lon,lat=f['geometry']['coordinates']
  out.append({'id':'m%d'%i,'c':'m','n':'道の駅 '+p['P35_006'],'p':p['P35_003'],'t':p['P35_004'],'la':round(lat,5),'lo':round(lon,5),'r':400,'u':p['P35_007'] or ''})
TY={'1':'アーチ式','2':'バットレス式','3':'アースフィル','4':'ロックフィル','5':'中空重力式','6':'重力式アーチ','7':'重力式コンクリート','8':'複合式','12':'その他'}
PU={'1':'洪水調節','2':'流水維持','3':'農業用水','4':'水道','5':'工業用水','6':'発電','7':'消流雪','8':'レクリエーション'}
r=shapefile.Reader(base+'/w01/W01-14-g_Dam.shp',encoding='cp932')
W={}
for i,(rec,sh) in enumerate(zip(r.records(),r.shapes())):
  addr=rec[12]; pref=next((p for p in P if addr.startswith(p)),None)
  if not pref: continue
  h=rec[6]; info=[]
  if h>0: info.append('堤高%gm'%h)
  if rec[4] in TY: info.append(TY[rec[4]])
  pu='・'.join(PU[x] for x in rec[5].split(',') if x in PU)
  if pu: info.append(pu)
  if rec[11] and rec[11]!='-': info.append(rec[11]+'年完成')
  lon,lat=sh.points[0]
  W['d%d'%i]={'t':muni(addr[len(pref):]),'la':round(lat,5),'lo':round(lon,5),'x':' / '.join(info)}
# ダムは国交省「ダムカード配布場所一覧」に載っている＝見学者を受け入れているものだけ（data/damcards.json）
for d in json.load(open(root/'data/damcards.json',encoding='utf-8')):
  if 'w01' in d:
    w=W[d['w01']]; sid=d['w01']; t,la,lo,x=w['t'],w['la'],w['lo'],w['x']
  else:
    sid='dk%d'%d['no']; t=''; la,lo=d['pos']; x=''
  k='ダムカード配布：'+'、'.join(d['card_places'])
  if d['card_notes']: k+='（'+'／'.join(d['card_notes'])+'）'
  out.append({'id':sid,'c':'d','n':d['name'],'p':d['pref'],'t':t,'la':la,'lo':lo,'r':800,'x':x,'k':k,'rv':d['river'] or ''})
# 牧場は手動選定・営業確認済みのリスト（idは固定）
for x in json.load(open(root/'data/ranches.json',encoding='utf-8')):
  pref=next(p for p in P if x['a'].startswith(p))
  out.append({'id':x['id'],'c':'f','n':x['n'],'p':pref,'t':muni(x['a'][len(pref):]),'la':x['lat'],'lo':x['lon'],'r':1500,'x':x.get('note','')})
import collections
print(collections.Counter(o['c'] for o in out))
json.dump(out,open(root/'data/spots.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
