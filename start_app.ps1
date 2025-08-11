# テキスト分析アプリ - PowerShell起動スクリプト
# 実行ポリシーを変更する必要がある場合: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "テキスト分析アプリ - PowerShell起動スクリプト" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Pythonのバージョンを確認
Write-Host "Pythonのバージョンを確認中..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "エラー: Pythonが見つかりません" -ForegroundColor Red
    Write-Host "Pythonがインストールされているか、PATHに追加されているか確認してください" -ForegroundColor Red
    Read-Host "Enterキーを押して終了"
    exit 1
}

Write-Host ""

# pipのバージョンを確認
Write-Host "pipのバージョンを確認中..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "pip: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "エラー: pipが見つかりません" -ForegroundColor Red
    Write-Host "pipをインストールしてください: python -m ensurepip --upgrade" -ForegroundColor Red
    Read-Host "Enterキーを押して終了"
    exit 1
}

Write-Host ""

# 依存関係をインストール
Write-Host "依存関係をインストール中..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "依存関係のインストールが完了しました" -ForegroundColor Green
} catch {
    Write-Host "警告: 依存関係のインストールでエラーが発生しました" -ForegroundColor Yellow
    Write-Host "既にインストールされている場合は問題ありません" -ForegroundColor Yellow
}

Write-Host ""

# Streamlitアプリケーションを起動
Write-Host "Streamlitアプリケーションを起動中..." -ForegroundColor Yellow
Write-Host "ブラウザが自動で開きます" -ForegroundColor Green
Write-Host "アプリケーションを停止するには、このウィンドウで Ctrl+C を押してください" -ForegroundColor Green
Write-Host ""

try {
    streamlit run app.py
} catch {
    Write-Host "アプリケーションの起動でエラーが発生しました" -ForegroundColor Red
    Write-Host "エラー詳細: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "アプリケーションが終了しました" -ForegroundColor Cyan
Read-Host "Enterキーを押して終了"
