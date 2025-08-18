@echo off
chcp 65001 > nul
echo 🚀 システム設計図のPDF生成を開始します...
echo.

echo 📊 ステップ1: 画像ファイルの生成
python generate_images.py
if %errorlevel% neq 0 (
    echo ❌ 画像生成に失敗しました。
    pause
    exit /b 1
)

echo.
echo 📄 ステップ2: PDFファイルの作成
python create_pdf.py
if %errorlevel% neq 0 (
    echo ❌ PDF作成に失敗しました。
    pause
    exit /b 1
)

echo.
echo 🎉 完了！システム設計図のPDFが生成されました。
echo 📖 'システム設計図.pdf' を開いてご確認ください。
pause 