# ツーリング御朱印帳（touring-stamp-card）

バイクツーリング用の個人Webアプリ。道の駅・ダム・牧場を「御朱印」のように集める。GitHub Pagesで公開し、スマホ（Brave）からホーム画面に追加して使っている。

- 公開URL: https://dualshock32146-maker.github.io/touring-stamp-card/
- 対象地域: 関東1都6県＋山梨・静岡（今後全国へ拡張予定）

## 構成

- `index.html` — 配信される本体。**直接編集しない**。`tools/template.html` から生成する
- `tools/template.html` — アプリ本体（HTML/CSS/JS、Leaflet 1.9.4）。`__DATA__` にスポットデータが埋め込まれる
- `data/spots.json` — 全スポット（id, c=カテゴリ m道の駅/d ダム/f 牧場, n名前, p都県, t市町村, la/lo座標, r判定半径m, x補足, u公式URL）
- `data/ranches.json` — 手動選定した観光牧場リスト（名前・住所・座標）
- `tools/fetch_sources.sh` — 国土数値情報（道の駅P35-18、ダムW01-14）をraw/へ取得
- `tools/build_data.py` — raw/ と ranches.json から data/spots.json を生成（対象都県はファイル内の `P`）
- `tools/geocode_ranches.py` — 牧場リストを住所から座標化（地理院API＋Nominatim）
- `tools/build_html.py` — template + spots.json → index.html

## 更新手順

```
sh tools/fetch_sources.sh        # データを入れ直すときだけ
python3 tools/build_data.py      # 要 pyshp
python3 tools/build_html.py
```
変更後は index.html も一緒にコミットする（Pagesはmainのルートを配信）。

## 仕様メモ

- 獲得判定: GPSで現在地とスポットの距離を計算し、判定半径（道の駅400m／ダム800m／牧場1500m）＋GPS誤差（最大300m）以内なら獲得。範囲外でも「手動で記録」可能、その印には「記」が付く
- 記録（日時・距離・メモ・写真Blob）は端末のIndexedDB（DB名 `goshuin`）のみに保存。サーバーには送らない。達成タブからJSONで書き出し/読み込み
- spotのidはデータの行番号ベース（m123, d530, f0）。データを作り直すとidがずれて既存の記録と対応しなくなるので、作り直すときはid対応に注意
- 地図: 標準はOpenStreetMapタイル、切替で地理院（標準/淡色/航空写真）。Googleマップのタイルは規約上使わない
- 利用者はスマホ中心。タップ領域は大きめに、文言は日本語
