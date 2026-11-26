import urllib.request,urllib.parse,json,time,math,sys
R=[("那須千本松牧場","栃木県那須塩原市千本松799"),("那須高原南ヶ丘牧場","栃木県那須郡那須町湯本579"),("日光霧降高原大笹牧場","栃木県日光市瀬尾大笹原3405"),("森林ノ牧場","栃木県那須郡那須町豊原乙627-114"),("那須りんどう湖ファミリー牧場","栃木県那須郡那須町高久丙414-2"),
("伊香保グリーン牧場","群馬県渋川市金井2844-1"),("神津牧場","群馬県甘楽郡下仁田町南野牧250"),("ぐりーんふらわー牧場・大胡","群馬県前橋市滝窪町1081"),("赤城高原牧場クローネンベルク","群馬県前橋市苗ケ島町2331"),
("ダチョウ王国 石岡ファーム","茨城県石岡市半ノ木14052"),
("秩父高原牧場","埼玉県秩父郡皆野町大字下田野1867"),
("マザー牧場","千葉県富津市田倉940-3"),("成田ゆめ牧場","千葉県成田市名木730-3"),("千葉県酪農のさと","千葉県南房総市大井686"),
("磯沼ミルクファーム","東京都八王子市小比企町1011"),("夕やけ小やけふれあいの里","東京都八王子市上恩方町2030"),
("服部牧場","神奈川県愛甲郡愛川町半原6087"),("雪印こどもの国牧場","神奈川県横浜市青葉区奈良町700"),
("清泉寮ジャージー牧場","山梨県北杜市高根町清里3545"),("ふじさん牧場","山梨県富士吉田市新屋1936"),("山梨県立まきば公園","山梨県北杜市高根町東井出5577"),
("まかいの牧場","静岡県富士宮市内野1327"),("COW RESORT IDEBOK","静岡県富士宮市人穴728"),("富士ミルクランド","静岡県富士宮市上井出3690"),("酪農王国オラッチェ","静岡県田方郡函南町丹那349-1")]
def get(u,ua=True):
  return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'touring-stamp-builder/1.0 (personal)'}),timeout=30))
def d(a,b,c,e): return math.hypot((a-c)*111,(b-e)*91)
out=[]
for n,a in R:
  g=get('https://msearch.gsi.go.jp/address-search/AddressSearch?q='+urllib.parse.quote(a))
  glon,glat=g[0]['geometry']['coordinates'] if g else (None,None)
  try: nm=get('https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':n,'format':'json','limit':3,'countrycodes':'jp'}))
  except Exception as ex: nm=[]
  time.sleep(1.1)
  best=None
  for x in nm:
    if glat and d(float(x['lat']),float(x['lon']),glat,glon)<6: best=x;break
  if best: lat,lon,src=float(best['lat']),float(best['lon']),'osm'
  else: lat,lon,src=glat,glon,'gsi'
  print(n,src,lat,lon,g[0]['properties']['title'] if g else None)
  out.append({'n':n,'a':a,'lat':round(lat,5),'lon':round(lon,5)})
import pathlib
json.dump(out,open(pathlib.Path(__file__).resolve().parent.parent/'data/ranches.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
