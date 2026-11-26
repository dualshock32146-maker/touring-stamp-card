#!/bin/sh
# 国土数値情報（道の駅 P35-18 / ダム W01-14）をダウンロードして raw/ に展開する
set -e
cd "$(dirname "$0")/.."
mkdir -p raw/p35 raw/w01
curl -sSL -o raw/P35-18_GML.zip https://nlftp.mlit.go.jp/ksj/gml/data/P35/P35-18/P35-18_GML.zip
curl -sSL -o raw/W01-14_GML.zip https://nlftp.mlit.go.jp/ksj/gml/data/W01/W01-14/W01-14_GML.zip
unzip -o -q raw/P35-18_GML.zip -d raw/p35
unzip -o -q raw/W01-14_GML.zip -d raw/w01
echo done
