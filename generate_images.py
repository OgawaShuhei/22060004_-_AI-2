#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid図表を画像ファイルとして生成するスクリプト
"""

import os
import requests
import base64
from pathlib import Path

def mermaid_to_image(mermaid_code, filename, output_format="png"):
    """
    Mermaidコードを画像ファイルに変換
    
    Args:
        mermaid_code (str): Mermaid記法のコード
        filename (str): 出力ファイル名（拡張子なし）
        output_format (str): 出力形式（png, svg, pdf）
    """
    
    # Mermaid Live Editor APIを使用
    mermaid_url = "https://mermaid.ink/img/"
    
    # MermaidコードをBase64エンコード
    encoded_code = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    
    # 画像URLを構築
    image_url = f"{mermaid_url}{encoded_code}.{output_format}"
    
    try:
        # 画像をダウンロード
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 出力ディレクトリを作成
        output_dir = Path("images")
        output_dir.mkdir(exist_ok=True)
        
        # ファイルに保存
        output_path = output_dir / f"{filename}.{output_format}"
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ {filename}.{output_format} を生成しました: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"❌ {filename} の生成に失敗しました: {e}")
        return None

def main():
    """メイン処理"""
    
    # システム設計図のMermaidコード
    diagrams = {
        "system_architecture": """graph TB
    subgraph "フロントエンド"
        UI[Streamlit UI]
    end
    
    subgraph "バックエンド"
        MA[メインアプリ<br/>app.py]
        TA[テキスト分析<br/>text_analyzer.py]
        UA[URL分析<br/>url_analyzer.py]
        DM[データベース管理<br/>database_manager.py]
    end
    
    subgraph "データ層"
        DB[(SQLite DB)]
        FS[ファイルシステム]
    end
    
    subgraph "外部ライブラリ"
        NLTK[NLTK<br/>自然言語処理]
        TB[TextBlob<br/>感情分析]
        LD[langdetect<br/>言語検出]
        BS[BeautifulSoup4<br/>HTML解析]
        REQ[Requests<br/>HTTP通信]
    end
    
    subgraph "外部サービス"
        WEB[Webページ]
    end
    
    UI --> MA
    MA --> TA
    MA --> UA
    MA --> DM
    TA --> NLTK
    TA --> TB
    TA --> LD
    UA --> REQ
    UA --> BS
    UA --> WEB
    DM --> DB
    DM --> FS""",

        "data_flow": """flowchart TD
    A[ユーザー入力] --> B{入力タイプ}
    
    B -->|テキスト| C[テキスト分析]
    B -->|ファイル| D[ファイル読み込み]
    B -->|URL| E[URL分析]
    
    D --> C
    E --> F[Webスクレイピング]
    F --> G[テキスト抽出]
    G --> C
    
    C --> H[分析処理]
    H --> I[基本統計]
    H --> J[言語検出]
    H --> K[感情分析]
    H --> L[可読性分析]
    H --> M[単語頻度分析]
    
    I --> N[結果統合]
    J --> N
    K --> N
    L --> N
    M --> N
    
    N --> O[データベース保存]
    N --> P[結果表示]
    
    O --> Q[履歴管理]
    P --> R[ユーザー確認]""",

        "class_diagram": """classDiagram
    class TextAnalyzer {
        +analyze_text(text: str) dict
        +get_basic_stats(text: str) dict
        +detect_language(text: str) str
        +analyze_sentiment(text: str) dict
        +calculate_readability(text: str) dict
        +analyze_word_frequency(text: str) dict
        +analyze_sentences(text: str) dict
        +analyze_characters(text: str) dict
    }
    
    class URLAnalyzer {
        +extract_text_from_url(url: str) dict
        +validate_url(url: str) bool
        +scrape_webpage(url: str) str
        +clean_html_content(html: str) str
    }
    
    class DatabaseManager {
        +init_database()
        +save_analysis_result(data: dict) bool
        +get_all_results() list
        +search_results(query: str) list
        +delete_result(result_id: int) bool
        +export_to_csv() str
        +export_to_txt() str
        +get_statistics() dict
    }
    
    class StreamlitApp {
        +main()
        +home_page()
        +text_analysis_page()
        +url_analysis_page()
        +history_page()
        +statistics_page()
    }
    
    StreamlitApp --> TextAnalyzer
    StreamlitApp --> URLAnalyzer
    StreamlitApp --> DatabaseManager""",

        "database_design": """erDiagram
    ANALYSIS_RESULTS {
        int id PK
        text text_content
        text file_name
        text url
        text language
        float sentiment_score
        float subjectivity_score
        float readability_score
        int char_count
        int word_count
        int sentence_count
        int paragraph_count
        text word_frequency
        text sentence_lengths
        text char_frequency
        datetime timestamp
    }
    
    ANALYSIS_RESULTS ||--o{ EXPORT_HISTORY : "generates"
    
    EXPORT_HISTORY {
        int id PK
        int analysis_id FK
        text export_type
        text file_path
        datetime export_time
    }"""
    }
    
    print("🚀 システム設計図の画像生成を開始します...")
    
    # 各図表を画像として生成
    generated_files = []
    for name, mermaid_code in diagrams.items():
        print(f"\n📊 {name} を生成中...")
        file_path = mermaid_to_image(mermaid_code, name, "png")
        if file_path:
            generated_files.append(file_path)
    
    print(f"\n🎉 完了！ {len(generated_files)}個の画像ファイルを生成しました。")
    print("📁 画像ファイルは 'images/' ディレクトリに保存されています。")
    
    return generated_files

if __name__ == "__main__":
    main() 