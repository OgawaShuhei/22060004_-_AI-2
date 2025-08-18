#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像ファイルをPDFに変換するスクリプト
"""

from pathlib import Path
from PIL import Image
import os

def create_pdf_from_images(image_dir="images", output_pdf="システム設計図.pdf"):
    """
    画像ファイルをPDFに変換
    
    Args:
        image_dir (str): 画像ファイルが格納されているディレクトリ
        output_pdf (str): 出力PDFファイル名
    """
    
    # 画像ディレクトリのパス
    img_dir = Path(image_dir)
    
    if not img_dir.exists():
        print(f"❌ 画像ディレクトリ '{image_dir}' が見つかりません。")
        print("先に 'python generate_images.py' を実行してください。")
        return False
    
    # 画像ファイルを取得（PNG形式）
    image_files = list(img_dir.glob("*.png"))
    
    if not image_files:
        print(f"❌ '{image_dir}' ディレクトリに画像ファイルが見つかりません。")
        return False
    
    # 画像ファイルを名前順にソート
    image_files.sort()
    
    print(f"📁 画像ファイル {len(image_files)}個 を発見しました:")
    for img_file in image_files:
        print(f"  - {img_file.name}")
    
    try:
        # 最初の画像を開く
        first_image = Image.open(image_files[0])
        
        # 他の画像をリストに追加
        other_images = []
        for img_file in image_files[1:]:
            img = Image.open(img_file)
            # RGB形式に変換（PNGの透明度を処理）
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            other_images.append(img)
        
        # PDFとして保存
        pdf_path = Path(output_pdf)
        first_image.save(
            pdf_path,
            "PDF",
            save_all=True,
            append_images=other_images,
            resolution=100.0
        )
        
        print(f"\n✅ PDFファイルを作成しました: {pdf_path}")
        print(f"📊 ページ数: {len(image_files)}")
        print(f"💾 ファイルサイズ: {pdf_path.stat().st_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ PDFの作成に失敗しました: {e}")
        return False

def main():
    """メイン処理"""
    
    print("📄 システム設計図のPDF作成を開始します...")
    
    # PDFを作成
    success = create_pdf_from_images()
    
    if success:
        print("\n🎉 PDFファイルの作成が完了しました！")
        print("📖 'システム設計図.pdf' を開いてご確認ください。")
    else:
        print("\n❌ PDFファイルの作成に失敗しました。")
        print("画像ファイルが正しく生成されているか確認してください。")

if __name__ == "__main__":
    main() 