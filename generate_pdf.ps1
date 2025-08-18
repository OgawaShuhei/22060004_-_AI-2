# システム設計図のPDF生成スクリプト
Write-Host "🚀 システム設計図のPDF生成を開始します..." -ForegroundColor Green
Write-Host ""

# ステップ1: 画像ファイルの生成
Write-Host "📊 ステップ1: 画像ファイルの生成" -ForegroundColor Yellow
try {
    python generate_images.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 画像生成に失敗しました。" -ForegroundColor Red
        Read-Host "Enterキーを押して終了"
        exit 1
    }
} catch {
    Write-Host "❌ 画像生成でエラーが発生しました: $_" -ForegroundColor Red
    Read-Host "Enterキーを押して終了"
    exit 1
}

Write-Host ""

# ステップ2: PDFファイルの作成
Write-Host "📄 ステップ2: PDFファイルの作成" -ForegroundColor Yellow
try {
    python create_pdf.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ PDF作成に失敗しました。" -ForegroundColor Red
        Read-Host "Enterキーを押して終了"
        exit 1
    }
} catch {
    Write-Host "❌ PDF作成でエラーが発生しました: $_" -ForegroundColor Red
    Read-Host "Enterキーを押して終了"
    exit 1
}

Write-Host ""
Write-Host "🎉 完了！システム設計図のPDFが生成されました。" -ForegroundColor Green
Write-Host "📖 'システム設計図.pdf' を開いてご確認ください。" -ForegroundColor Cyan
Read-Host "Enterキーを押して終了" 