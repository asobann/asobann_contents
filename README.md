# asobann_contents

[asobann](https://github.com/yattom/asobann_app)（オンラインアナログゲームプラットフォーム）で遊べるコンテンツ（ゲーム）のリポジトリ。

## 構成

```
kit/       … キット定義JSON。1ゲーム=1キット
  100narabe.json, turtle_soup.json, ...   … 単純なキットは単一JSON
  the_kanban_game/                        … 画像を伴うキットはサブディレクトリ（JSON + images/）
  win_by_team/                            … CSV⇔JSON変換ツール(csv.py)を持つ例
artwork/   … 元画像・作業ファイル（xcf, svg, png等）。kitが参照する完成画像の原本
```

## キット定義JSONの構造（概要）

```json
{
  "kit": {
    "name": "Game Name",
    "label": "Game Name",
    "label_ja": "ゲーム名",
    "width": "400px", "height": "300px",
    "boxAndComponents": { "box name": ["component name", ...] },
    "usedComponentNames": ["...すべてのコンポーネント名..."]
  },
  "components": [
    { "name": "Card 01", "text": "...", "flippable": true, "draggable": true, ... }
  ]
}
```

- コンポーネントのプロパティ（`draggable`, `flippable`, `traylike`, `handArea`, `glued`, `counter` など）はasobann_app側のfeatシステムに対応する。詳細: asobann_app/docs/architecture.md の「featシステム」
- 表示名は `label` / `label_ja` のように `_ja` サフィックスで日本語版を併記できる（テキスト系プロパティ共通の規約）

## キットのアップロード

サーバの `/kits/create` エンドポイントへ multipart/form-data（フィールド名 `data`）でJSONをPOSTする:

```shell
curl -F "data=@kit/turtle_soup.json" http://localhost:8000/kits/create
```

- 同名キットは**上書き**される（バージョン番号が上がる）
- サーバの初期投入データはasobann_app側の `initial_deploy_data.json`（`python -m asobann.deploy`）で管理されており、本リポジトリのキットとは別系統である点に注意

## ツール

- `kit/win_by_team/csv.py` … カードのテキストをCSV⇔JSONで相互変換し、スプレッドシートで一括編集するためのツール（win_by_team専用。汎用化は未着手）

## 注意

- キットにアップロード検証はほぼない（サイズ・スキーマともに）。壊れたJSONを上げるとテーブルでのkit追加時にエラーになる
- 画像はキットJSONから相対パス or アップロード済みURLで参照する。運用中のサーバに対する画像の置き場所はasobann_app側の `UPLOADED_IMAGE_STORE` 設定に依存する
