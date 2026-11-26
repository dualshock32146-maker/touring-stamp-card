"""tools/template.html の __DATA__ に data/spots.json を埋め込み、ルートの index.html を作る"""
import pathlib
root=pathlib.Path(__file__).resolve().parent.parent
data=(root/'data/spots.json').read_text(encoding='utf-8').replace('<','\\u003c')
html=(root/'tools/template.html').read_text(encoding='utf-8').replace('__DATA__',data)
(root/'index.html').write_text(html,encoding='utf-8')
print('index.html written')
