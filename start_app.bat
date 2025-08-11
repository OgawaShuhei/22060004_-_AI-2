@echo off
chcp 65001 >nul
echo ========================================
echo テキスト分析アプリ - Windows起動スクリプト
echo ========================================
echo.

echo Pythonのバージョンを確認中...
python --version
if errorlevel 1 (
    echo エラー: Pythonが見つかりません
    echo Pythonがインストールされているか、PATHに追加されているか確認してください
    pause
    exit /b 1
)

echo.
echo pipのバージョンを確認中...
pip --version
if errorlevel 1 (
    echo エラー: pipが見つかりません
    echo pipをインストールしてください: python -m ensurepip --upgrade
    pause
    exit /b 1
)

echo.
echo 依存関係をインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告: 依存関係のインストールでエラーが発生しました
    echo 既にインストールされている場合は問題ありません
)

echo.
echo Streamlitアプリケーションを起動中...
echo ブラウザが自動で開きます
echo アプリケーションを停止するには、このウィンドウで Ctrl+C を押してください
echo.

streamlit run app.py

echo.
echo アプリケーションが終了しました
pause
