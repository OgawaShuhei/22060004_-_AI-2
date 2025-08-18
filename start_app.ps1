# テキスト分析アプリ起動スクリプト (PowerShell)
Write-Host "テキスト分析アプリを起動中..." -ForegroundColor Green
Write-Host ""

# Pythonがインストールされているかチェック
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Pythonバージョン: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "エラー: Pythonがインストールされていません。" -ForegroundColor Red
    Write-Host "Python 3.8以上をインストールしてください。" -ForegroundColor Yellow
    Read-Host "Enterキーを押して終了"
    exit 1
}

# 仮想環境が存在するかチェック
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "仮想環境を有効化中..." -ForegroundColor Cyan
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "仮想環境が見つかりません。新しく作成します..." -ForegroundColor Yellow
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    Write-Host "必要なパッケージをインストール中..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

# アプリケーションを起動
Write-Host "アプリケーションを起動中..." -ForegroundColor Green
streamlit run app.py

Read-Host "Enterキーを押して終了"
