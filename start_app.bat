@echo off
echo テキスト分析アプリを起動中...
echo.

REM Pythonがインストールされているかチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません。
    echo Python 3.8以上をインストールしてください。
    pause
    exit /b 1
)

REM 仮想環境が存在するかチェック
if exist "venv\Scripts\activate.bat" (
    echo 仮想環境を有効化中...
    call venv\Scripts\activate.bat
) else (
    echo 仮想環境が見つかりません。新しく作成します...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 必要なパッケージをインストール中...
    pip install -r requirements.txt
)

REM アプリケーションを起動
echo アプリケーションを起動中...
streamlit run app.py

pause
