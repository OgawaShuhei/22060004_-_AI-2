# システム設計図PDF生成ガイド

## 概要

このガイドでは、READMEに記載されたシステム設計図を画像ファイルとして生成し、PDFに変換する方法を説明します。

## 必要なファイル

- `generate_images.py` - Mermaid図表を画像ファイルに変換
- `create_pdf.py` - 画像ファイルをPDFに結合
- `generate_pdf.bat` - Windows用バッチファイル
- `generate_pdf.ps1` - Windows用PowerShellスクリプト
- `requirements_images.txt` - 必要な依存関係

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements_images.txt
```

または個別にインストール：

```bash
pip install requests Pillow
```

### 2. ファイルの確認

以下のファイルが存在することを確認してください：
- `generate_images.py`
- `create_pdf.py`
- `generate_pdf.bat` (Windows)
- `generate_pdf.ps1` (Windows)

## 使用方法

### 方法1: 自動実行（推奨）

#### Windows環境

**コマンドプロンプトの場合：**
```cmd
generate_pdf.bat
```

**PowerShellの場合：**
```powershell
.\generate_pdf.ps1
```

### 方法2: 手動実行

#### ステップ1: 画像ファイルの生成

```bash
python generate_images.py
```

これにより、以下の画像ファイルが `images/` ディレクトリに生成されます：
- `system_architecture.png` - システムアーキテクチャ図
- `data_flow.png` - データフロー図
- `class_diagram.png` - クラス図
- `database_design.png` - データベース設計図

#### ステップ2: PDFファイルの作成

```bash
python create_pdf.py
```

これにより、`システム設計図.pdf` ファイルが作成されます。

## 生成されるファイル

### 画像ファイル（PNG形式）
- **system_architecture.png** - システム全体のアーキテクチャ
- **data_flow.png** - データの流れと処理フロー
- **class_diagram.png** - クラス構造と関係性
- **database_design.png** - データベーステーブル設計

### PDFファイル
- **システム設計図.pdf** - 全4ページの設計図（1ページに1つの図表）

## トラブルシューティング

### よくある問題

#### 1. 依存関係のエラー
```
ModuleNotFoundError: No module named 'requests'
```
**解決方法：**
```bash
pip install requests Pillow
```

#### 2. 画像生成の失敗
```
❌ system_architecture の生成に失敗しました
```
**解決方法：**
- インターネット接続を確認
- ファイアウォールの設定を確認
- しばらく待ってから再実行

#### 3. PDF作成の失敗
```
❌ PDFの作成に失敗しました
```
**解決方法：**
- `images/` ディレクトリに画像ファイルが存在するか確認
- 画像ファイルが破損していないか確認

### 手動での確認

#### 画像ファイルの確認
```bash
dir images
# または
ls images
```

#### PDFファイルの確認
```bash
dir *.pdf
# または
ls *.pdf
```

## カスタマイズ

### 画像形式の変更

`generate_images.py` の `mermaid_to_image` 関数で、出力形式を変更できます：

```python
# PNG形式（デフォルト）
file_path = mermaid_to_image(mermaid_code, name, "png")

# SVG形式
file_path = mermaid_to_image(mermaid_code, name, "svg")

# PDF形式（個別）
file_path = mermaid_to_image(mermaid_code, name, "pdf")
```

### 図表の追加・変更

`generate_images.py` の `diagrams` 辞書に新しい図表を追加できます：

```python
diagrams = {
    "new_diagram": """graph TD
        A[開始] --> B[処理]
        B --> C[終了]""",
    # ... 既存の図表
}
```

## 技術詳細

### 使用技術
- **Mermaid.js** - 図表の描画
- **Mermaid Live Editor API** - 画像生成
- **Pillow (PIL)** - 画像処理とPDF作成
- **Requests** - HTTP通信

### 処理フロー
1. Mermaid記法のコードをBase64エンコード
2. Mermaid Live Editor APIに送信
3. 画像ファイルをダウンロード
4. 複数の画像を1つのPDFに結合

## 注意事項

- インターネット接続が必要です（Mermaid Live Editor API使用のため）
- 生成される画像の品質は、Mermaid Live Editor APIの仕様に依存します
- 大量の図表を生成する場合は、APIの制限に注意してください
- 生成されたPDFは、標準的なPDFビューアーで開くことができます

## サポート

問題が発生した場合は、以下を確認してください：
1. Pythonのバージョン（3.6以上推奨）
2. 必要な依存関係のインストール状況
3. インターネット接続の状態
4. ファイルの権限設定

エラーメッセージと共に、お気軽にお問い合わせください。 