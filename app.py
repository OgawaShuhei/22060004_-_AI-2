import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.text_analyzer import TextAnalyzer
from src.database_manager import DatabaseManager
from src.url_analyzer import URLAnalyzer
import os
import base64
import time

# ページ設定
st.set_page_config(
    page_title="テキスト分析アプリ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        color: white;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #5a6fd8, #6a4190);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# アプリケーションの初期化
@st.cache_resource
def init_analyzer():
    return TextAnalyzer()

def init_database():
    """データベースを初期化（キャッシュなし）"""
    return DatabaseManager()

@st.cache_resource
def init_url_analyzer():
    return URLAnalyzer()

analyzer = init_analyzer()
db_manager = init_database()
url_analyzer = init_url_analyzer()

# ファイルダウンロード機能
def get_download_link(data, filename, file_type):
    """ファイルダウンロードリンクを生成"""
    if file_type == "csv":
        csv = data.to_csv(index=False, encoding='utf-8-sig')
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 {filename}をダウンロード</a>'
    elif file_type == "txt":
        b64 = base64.b64encode(data.encode('utf-8')).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 {filename}をダウンロード</a>'
    return href

# メインアプリケーション
def main():
    global db_manager
    
    # データベースの初期化確認
    try:
        # データベースの状態を確認
        db_manager.debug_database_state()
    except Exception as e:
        st.error(f"データベースの初期化に失敗しました: {str(e)}")
        st.info("データベースを再初期化しています...")
        try:
            # データベースを再初期化
            db_manager = DatabaseManager()
            st.success("データベースの初期化が完了しました")
        except Exception as e2:
            st.error(f"データベースの再初期化に失敗しました: {str(e2)}")
            st.stop()
    
    # セッション状態でページ管理
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 ホーム"
    
    # サイドバーでページ選択
    st.sidebar.title("📊 テキスト分析アプリ")
    page = st.sidebar.selectbox(
        "ページを選択",
        ["🏠 ホーム", "📝 テキスト分析", "📚 分析履歴", "📊 統計情報", "💾 データ管理"],
        index=["🏠 ホーム", "📝 テキスト分析", "📚 分析履歴", "📊 統計情報", "💾 データ管理"].index(st.session_state.current_page)
    )
    
    # ページが変更された場合、セッション状態を更新
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()
    
    if st.session_state.current_page == "🏠 ホーム":
        show_home_page()
    elif st.session_state.current_page == "📝 テキスト分析":
        show_analysis_page()
    elif st.session_state.current_page == "📚 分析履歴":
        show_history_page()
    elif st.session_state.current_page == "📊 統計情報":
        show_statistics_page()
    elif st.session_state.current_page == "💾 データ管理":
        show_data_management_page()

def show_home_page():
    """ホームページ"""
    st.markdown("""
    <div class="main-header">
        <h1>📊 テキスト分析アプリ</h1>
        <p>テキストを入力またはファイルをアップロードして、詳細な分析結果を取得しましょう</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 統計情報の表示
    stats = db_manager.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("総分析数", f"{stats['total_analyses']:,}")
    with col2:
        st.metric("平均テキスト長", f"{stats['avg_text_length']:,} 文字")
    with col3:
        st.metric("最も一般的な言語", stats['most_common_language'])
    with col4:
        st.metric("平均感情スコア", f"{stats['avg_sentiment_score']:.1f}%")
    
    st.markdown("---")
    
    # クイック分析セクション
    st.subheader("🚀 クイック分析")
    st.write("ホームページから直接テキスト分析を実行できます。")
    
    # 入力方法選択
    input_method = st.radio(
        "入力方法を選択してください",
        ["テキスト入力", "ファイルアップロード", "URL分析"],
        horizontal=True
    )
    
    # テキスト入力
    if input_method == "テキスト入力":
        text_input = st.text_area(
            "分析したいテキストを入力してください",
            height=150,
            placeholder="ここにテキストを入力してください..."
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 クイック分析", type="primary"):
                if text_input.strip():
                    with st.spinner("テキストを分析中..."):
                        results = analyzer.analyze_text(text_input)
                        # データベースに保存
                        analysis_id = db_manager.save_analysis_result(
                            text_input, results
                        )
                        st.session_state['home_results'] = results
                        st.session_state['home_analysis_id'] = analysis_id
                        st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                else:
                    st.error("テキストを入力してください")
        
        with col2:
            if st.button("📝 詳細分析ページへ"):
                st.session_state.current_page = "📝 テキスト分析"
                st.rerun()
    
    # ファイルアップロード
    elif input_method == "ファイルアップロード":
        uploaded_file = st.file_uploader(
            "テキストファイルをアップロード",
            type=['txt'],
            help="テキストファイル（.txt）のみ対応しています"
        )
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📁 クイック分析", type="primary"):
                    with st.spinner("ファイルを分析中..."):
                        text_content = uploaded_file.read().decode('utf-8')
                        if text_content.strip():
                            results = analyzer.analyze_text(text_content)
                            # データベースに保存
                            analysis_id = db_manager.save_analysis_result(
                                text_content, results, 
                                uploaded_file.name, len(text_content)
                            )
                            st.session_state['home_results'] = results
                            st.session_state['home_analysis_id'] = analysis_id
                            st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                        else:
                            st.error("ファイルが空です")
            
            with col2:
                if st.button("📝 詳細分析ページへ"):
                    st.session_state.current_page = "📝 テキスト分析"
                    st.rerun()
    
    # URL分析
    else:
        url_input = st.text_input(
            "分析したいWebページのURLを入力してください",
            placeholder="https://example.com または example.com"
        )
        
        if url_input:
            # URLの基本情報を表示
            page_info = url_analyzer.get_page_info(url_input)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ページタイトル:** {page_info['title']}")
                st.write(f"**文字数:** {page_info['char_count']:,}")
            
            with col2:
                if page_info['description']:
                    st.write(f"**説明:** {page_info['description'][:100]}...")
                else:
                    st.write("**説明:** なし")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🌐 URL分析", type="primary"):
                    success, result = url_analyzer.extract_text_from_url(url_input)
                    if success:
                        with st.spinner("テキストを分析中..."):
                            results = analyzer.analyze_text(result)
                            # データベースに保存
                            analysis_id = db_manager.save_analysis_result(
                                result, results, 
                                f"URL: {url_input}", len(result)
                            )
                            st.session_state['home_results'] = results
                            st.session_state['home_analysis_id'] = analysis_id
                            st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                    else:
                        st.error(f"URL分析に失敗しました: {result}")
            
            with col2:
                if st.button("📝 詳細分析ページへ"):
                    st.session_state.current_page = "📝 テキスト分析"
                    st.rerun()
    
    # ホームページでの結果表示（簡易版）
    if 'home_results' in st.session_state:
        st.markdown("---")
        st.subheader("📊 分析結果（簡易版）")
        
        results = st.session_state['home_results']
        
        # 基本統計の表示
        basic_stats = results['basic_stats']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("文字数", f"{basic_stats['character_count']:,}")
            st.metric("単語数", f"{basic_stats['word_count']:,}")
        
        with col2:
            st.metric("文の数", f"{basic_stats['sentence_count']:,}")
            st.metric("段落数", f"{basic_stats['paragraph_count']:,}")
        
        with col3:
            st.metric("平均単語数/文", f"{basic_stats['average_words_per_sentence']:.1f}")
            st.metric("平均文字数/単語", f"{basic_stats['average_characters_per_word']:.1f}")
        
        # 言語と感情の表示
        lang = results['language_detection']
        sentiment = results['sentiment_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            # 古いデータとの互換性のため、安全に言語コードを取得
            language_code = lang.get('language_code', lang.get('detected_language', 'unknown'))
            st.info(f"🌍 **検出された言語:** {lang['language_name']} ({language_code})")
        
        with col2:
            sentiment_color = "green" if sentiment['sentiment'] == 'ポジティブ' else "red" if sentiment['sentiment'] == 'ネガティブ' else "orange"
            st.metric("感情", sentiment['sentiment'], delta=f"{sentiment['polarity_percentage']}%")
        
        # 詳細結果へのリンク
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 詳細結果を表示", type="secondary"):
                st.session_state.current_page = "📝 テキスト分析"
                st.rerun()
        
        with col2:
            if st.button("📚 分析履歴を確認", type="secondary"):
                st.session_state.current_page = "📚 分析履歴"
                st.rerun()
    
    st.markdown("---")
    
    # 機能紹介
    st.subheader("🎯 主な機能")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📝 テキスト分析**
        - 基本統計（文字数、単語数、文の数）
        - 言語検出
        - 感情分析
        - 可読性分析
        - 単語頻度分析
        - 文の分析
        - 文字分析
        """)
    
    with col2:
        st.markdown("""
        **💾 データ管理**
        - 分析結果の自動保存
        - 分析履歴の閲覧
        - CSV/TXT形式でのエクスポート
        - 統計情報の表示
        - データの削除機能
        """)
    
    # 最近の分析履歴（簡易版）
    st.markdown("---")
    st.subheader("📚 最近の分析履歴")
    
    df = db_manager.get_all_analyses()
    if not df.empty:
        # 最新5件を表示
        recent_df = df.head(5)[['id', 'timestamp', 'file_name', 'text_length']].copy()
        recent_df['file_name'] = recent_df['file_name'].fillna('テキスト入力')
        recent_df.columns = ['ID', 'タイムスタンプ', 'ファイル名', '文字数']
        
        st.dataframe(
            recent_df,
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("📚 全履歴を表示"):
            st.session_state.current_page = "📚 分析履歴"
            st.rerun()
    else:
        st.info("まだ分析履歴がありません。テキスト分析を行ってください。")

def show_analysis_page():
    """テキスト分析ページ"""
    st.header("📝 テキスト分析")
    
    # 入力方法選択
    input_method = st.radio(
        "入力方法を選択してください",
        ["テキスト入力", "ファイルアップロード", "URL分析"],
        horizontal=True
    )
    
    # テキスト入力
    if input_method == "テキスト入力":
        text_input = st.text_area(
            "分析したいテキストを入力してください",
            height=200,
            placeholder="ここにテキストを入力してください..."
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 分析開始", type="primary"):
                if text_input.strip():
                    with st.spinner("テキストを分析中..."):
                        results = analyzer.analyze_text(text_input)
                        # データベースに保存
                        analysis_id = db_manager.save_analysis_result(
                            text_input, results
                        )
                        st.session_state['current_results'] = results
                        st.session_state['current_analysis_id'] = analysis_id
                        st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                else:
                    st.error("テキストを入力してください")
        
        with col2:
            if st.button("💾 分析結果を保存"):
                if 'current_results' in st.session_state:
                    st.success("分析結果がデータベースに保存されました")
                else:
                    st.warning("先にテキストを分析してください")
    
    # ファイルアップロード
    elif input_method == "ファイルアップロード":
        uploaded_file = st.file_uploader(
            "テキストファイルをアップロード",
            type=['txt'],
            help="テキストファイル（.txt）のみ対応しています"
        )
        
        if uploaded_file is not None:
            if st.button("📁 ファイル分析", type="primary"):
                with st.spinner("ファイルを分析中..."):
                    text_content = uploaded_file.read().decode('utf-8')
                    if text_content.strip():
                        results = analyzer.analyze_text(text_content)
                        # データベースに保存
                        analysis_id = db_manager.save_analysis_result(
                            text_content, results, 
                            uploaded_file.name, len(text_content)
                        )
                        st.session_state['current_results'] = results
                        st.session_state['current_analysis_id'] = analysis_id
                        st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                    else:
                        st.error("ファイルが空です")
    
    # URL分析
    else:
        url_input = st.text_input(
            "分析したいWebページのURLを入力してください",
            placeholder="https://example.com または example.com"
        )
        
        if url_input:
            # URLの基本情報を表示
            page_info = url_analyzer.get_page_info(url_input)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ページタイトル:** {page_info['title']}")
                st.write(f"**文字数:** {page_info['char_count']:,}")
            
            with col2:
                if page_info['description']:
                    st.write(f"**説明:** {page_info['description'][:100]}...")
                else:
                    st.write("**説明:** なし")
            
            if st.button("🌐 URL分析", type="primary"):
                success, result = url_analyzer.extract_text_from_url(url_input)
                if success:
                    with st.spinner("テキストを分析中..."):
                        results = analyzer.analyze_text(result)
                        # データベースに保存
                        analysis_id = db_manager.save_analysis_result(
                            result, results, 
                            f"URL: {url_input}", len(result)
                        )
                        st.session_state['current_results'] = results
                        st.session_state['current_analysis_id'] = analysis_id
                        st.success(f"✅ 分析完了！分析ID: {analysis_id}")
                else:
                    st.error(f"URL分析に失敗しました: {result}")
    
    # 結果表示
    if 'current_results' in st.session_state:
        display_results(st.session_state['current_results'])

def show_history_page():
    """分析履歴ページ"""
    st.header("📚 分析履歴")
    
    # 履歴データの取得
    df = db_manager.get_all_analyses()
    
    # デバッグ情報を表示
    st.write(f"データベースから取得した行数: {len(df)}")
    if not df.empty:
        st.write(f"データフレームの列: {list(df.columns)}")
        st.write(f"最初の行のID: {df.iloc[0]['id'] if 'id' in df.columns else 'ID列なし'}")
    
    # データベースの状態を確認
    if st.button("🔍 データベース状態を確認"):
        debug_info = db_manager.debug_database_state()
        if debug_info:
            st.write("**データベース状態:**")
            st.write(f"- 総件数: {debug_info['total_count']}")
            st.write(f"- 最小ID: {debug_info['min_id']}")
            st.write(f"- 最大ID: {debug_info['max_id']}")
            st.write("**テーブル構造:**")
            for col in debug_info['table_info']:
                st.write(f"- {col[1]} ({col[2]})")
        else:
            st.error("データベース状態の取得に失敗しました")
    
    if df.empty:
        st.info("まだ分析履歴がありません。テキスト分析を行ってください。")
        return
    
    # 検索・フィルタリング
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("検索（ファイル名またはテキスト内容）")
    with col2:
        language_filter = st.selectbox(
            "言語でフィルタ",
            ["すべて"] + list(df['language_detection'].apply(
                lambda x: x.get('language_name', '不明') if x else '不明'
            ).unique())
        )
    
    # フィルタリング
    if search_term:
        df = df[df['text_content'].str.contains(search_term, case=False, na=False) |
                df['file_name'].str.contains(search_term, case=False, na=False)]
    
    if language_filter != "すべて":
        df = df[df['language_detection'].apply(
            lambda x: x.get('language_name', '不明') if x else '不明'
        ) == language_filter]
    
    # 削除完了メッセージの表示
    if st.session_state.get('deletion_success', False):
        st.success("✅ データの削除が完了しました")
        # フラグをクリア
        st.session_state.deletion_success = False
    
    # 履歴テーブル
    st.subheader(f"分析履歴 ({len(df)}件)")
    
    # 表示用データフレーム（インデックスを保持）
    display_df = df[['id', 'timestamp', 'file_name', 'text_length']].copy()
    display_df['file_name'] = display_df['file_name'].fillna('テキスト入力')
    display_df.columns = ['ID', 'タイムスタンプ', 'ファイル名', '文字数']
    
    # データ表示と選択
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )
    
    # 行選択用のセレクトボックス
    if len(display_df) > 0:
        # デバッグ情報を表示
        st.write(f"データフレームの行数: {len(display_df)}")
        st.write(f"データフレームの列: {list(display_df.columns)}")
        
        row_options = [f"ID: {row['ID']} - {row['ファイル名']} ({row['タイムスタンプ']})" for _, row in display_df.iterrows()]
        selected_row_index = st.selectbox(
            "詳細を表示する行を選択してください",
            options=range(len(display_df)),
            format_func=lambda x: row_options[x] if x < len(row_options) else "選択してください"
        )
        
        # デバッグ情報を表示
        st.write(f"選択された行のインデックス: {selected_row_index}")
        
        # 詳細表示
        if selected_row_index is not None and selected_row_index < len(display_df):
            try:
                # 選択された行のIDを取得
                original_index = display_df.index[selected_row_index]
                selected_id = df.loc[original_index, 'id']
                
                st.write(f"元のインデックス: {original_index}")
                st.write(f"選択されたID: {selected_id}")
                
                analysis = db_manager.get_analysis_by_id(selected_id)
                
                if analysis:
                    st.subheader(f"分析詳細 (ID: {selected_id})")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**タイムスタンプ:** {analysis['timestamp']}")
                        st.write(f"**ファイル名:** {analysis['file_name'] or 'テキスト入力'}")
                        st.write(f"**文字数:** {analysis['text_length']:,}")
                    
                    with col2:
                        if st.button("🗑️ この分析を削除", type="secondary"):
                            # 削除確認
                            if st.checkbox("本当にこの分析を削除しますか？", key=f"confirm_delete_{selected_id}"):
                                st.write(f"削除を試行中... ID: {selected_id}")
                                
                                # 削除前のデータ件数を確認
                                before_count = len(db_manager.get_all_analyses())
                                st.write(f"削除前のデータ件数: {before_count}")
                                
                                try:
                                    # 削除実行
                                    delete_result = db_manager.delete_analysis(selected_id)
                                    st.write(f"削除結果: {delete_result}")
                                    
                                    if delete_result:
                                        # 削除後のデータ件数を確認
                                        after_count = len(db_manager.get_all_analyses())
                                        st.write(f"削除後のデータ件数: {after_count}")
                                        
                                        st.success("分析結果を削除しました")
                                        # 削除完了フラグを設定
                                        st.session_state.deletion_success = True
                                        # セッション状態をクリア
                                        if 'selected_row_index' in st.session_state:
                                            del st.session_state.selected_row_index
                                        # データを再取得して表示を更新
                                        st.rerun()
                                    else:
                                        st.error("削除に失敗しました")
                                except Exception as e:
                                    st.error(f"削除中にエラーが発生: {str(e)}")
                                    st.write(f"エラーの詳細: {type(e).__name__}: {str(e)}")
                            else:
                                st.info("削除をキャンセルしました")
                    
                    # テキスト内容の表示
                    with st.expander("テキスト内容を表示"):
                        st.text_area("テキスト内容", analysis['text_content'], height=200, disabled=True)
                    
                    # 分析結果の表示
                    display_results(analysis)
                else:
                    st.error(f"ID {selected_id} の分析結果が見つかりません")
            except (IndexError, KeyError) as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.warning("選択された行の処理中にエラーが発生しました。再度選択してください。")
        else:
            st.info("行を選択してください")

def show_statistics_page():
    """統計情報ページ"""
    st.header("📊 統計情報")
    
    stats = db_manager.get_statistics()
    df = db_manager.get_all_analyses()
    
    if df.empty:
        st.info("まだ分析データがありません。")
        return
    
    # 基本統計
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("総分析数", f"{stats['total_analyses']:,}")
    with col2:
        st.metric("平均テキスト長", f"{stats['avg_text_length']:,} 文字")
    with col3:
        st.metric("最も一般的な言語", stats['most_common_language'])
    with col4:
        st.metric("平均感情スコア", f"{stats['avg_sentiment_score']:.1f}%")
    
    st.markdown("---")
    
    # 言語分布
    st.subheader("🌍 言語分布")
    language_counts = df['language_detection'].apply(
        lambda x: x.get('language_name', '不明') if x else '不明'
    ).value_counts()
    
    fig = px.pie(
        values=language_counts.values,
        names=language_counts.index,
        title="分析されたテキストの言語分布"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 感情分布
    st.subheader("💝 感情分布")
    sentiment_counts = df['sentiment_analysis'].apply(
        lambda x: x.get('sentiment', '不明') if x else '不明'
    ).value_counts()
    
    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        title="感情分析の結果分布"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # テキスト長の分布
    st.subheader("📏 テキスト長の分布")
    fig = px.histogram(
        df, x='text_length',
        title="テキスト長の分布",
        labels={'text_length': '文字数', 'count': '件数'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_data_management_page():
    """データ管理ページ"""
    st.header("💾 データ管理")
    
    df = db_manager.get_all_analyses()
    
    # デバッグ情報を表示
    st.write(f"データベースから取得した行数: {len(df)}")
    if not df.empty:
        st.write(f"データフレームの列: {list(df.columns)}")
        st.write(f"最初の行のID: {df.iloc[0]['id'] if 'id' in df.columns else 'ID列なし'}")
    
    if df.empty:
        st.info("まだ分析データがありません。")
        return
    
    # エクスポート機能
    st.subheader("📤 データエクスポート")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 全データをCSVエクスポート"):
            csv_data = db_manager.export_to_csv()
            csv_filename = f"text_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            st.markdown(get_download_link(csv_data, csv_filename, "csv"), unsafe_allow_html=True)
    
    with col2:
        if st.button("📄 全データをTXTエクスポート"):
            txt_data = db_manager.export_to_txt()
            txt_filename = f"text_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
            st.markdown(get_download_link(txt_data, txt_filename, "txt"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 削除完了メッセージの表示
    if st.session_state.get('deletion_success', False):
        st.success("✅ データの削除が完了しました")
        # フラグをクリア
        st.session_state.deletion_success = False
    
    # データ削除機能
    st.subheader("🗑️ データ削除")
    
    # 選択可能なテーブル
    display_df = df[['id', 'timestamp', 'file_name', 'text_length']].copy()
    display_df['file_name'] = display_df['file_name'].fillna('テキスト入力')
    display_df.columns = ['ID', 'タイムスタンプ', 'ファイル名', '文字数']
    
    # データ表示と選択
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )
    
    # 行選択用のセレクトボックス
    if len(display_df) > 0:
        # デバッグ情報を表示
        st.write(f"データフレームの行数: {len(display_df)}")
        st.write(f"データフレームの列: {list(display_df.columns)}")
        
        row_options = [f"ID: {row['ID']} - {row['ファイル名']} ({row['タイムスタンプ']})" for _, row in display_df.iterrows()]
        selected_row_index = st.selectbox(
            "削除する行を選択してください",
            options=range(len(display_df)),
            format_func=lambda x: row_options[x] if x < len(row_options) else "選択してください"
        )
        
        # デバッグ情報を表示
        st.write(f"選択された行のインデックス: {selected_row_index}")
        
        # 選択された行の処理
        if selected_row_index is not None and selected_row_index < len(display_df):
            try:
                # 選択された行のIDを取得
                original_index = display_df.index[selected_row_index]
                selected_id = df.loc[original_index, 'id']
                
                st.write(f"元のインデックス: {original_index}")
                st.write(f"選択された分析ID: {selected_id}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ 選択した分析を削除", type="secondary"):
                        # 削除確認
                        if st.checkbox("本当にこの分析を削除しますか？", key=f"confirm_delete_management_{selected_id}"):
                            st.write(f"削除を試行中... ID: {selected_id}")
                            
                            # 削除前のデータ件数を確認
                            before_count = len(db_manager.get_all_analyses())
                            st.write(f"削除前のデータ件数: {before_count}")
                            
                            try:
                                # 削除実行
                                delete_result = db_manager.delete_analysis(selected_id)
                                st.write(f"削除結果: {delete_result}")
                                
                                if delete_result:
                                    # 削除後のデータ件数を確認
                                    after_count = len(db_manager.get_all_analyses())
                                    st.write(f"削除後のデータ件数: {after_count}")
                                    
                                    st.success("分析結果を削除しました")
                                    # 削除完了フラグを設定
                                    st.session_state.deletion_success = True
                                    # セッション状態をクリア
                                    if 'selected_row_index' in st.session_state:
                                        del st.session_state.selected_row_index
                                    # データを再取得して表示を更新
                                    st.rerun()
                                else:
                                    st.error("削除に失敗しました")
                            except Exception as e:
                                st.error(f"削除中にエラーが発生: {str(e)}")
                                st.write(f"エラーの詳細: {type(e).__name__}: {str(e)}")
                        else:
                            st.info("削除をキャンセルしました")
                
                with col2:
                    if st.button("🗑️ 全データを削除", type="secondary"):
                        if st.checkbox("本当に全データを削除しますか？"):
                            # 全データ削除の実装
                            st.warning("この機能は実装中です")
            except (IndexError, KeyError) as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.warning("選択された行の処理中にエラーが発生しました。再度選択してください。")
        else:
            st.info("行を選択してください")

def display_results(results):
    """分析結果を表示"""
    st.success("✅ 分析完了！")
    
    # タブで結果を表示
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 基本統計", "🌍 言語検出", "💝 感情分析", 
        "📖 可読性", "📈 単語頻度", "📝 文の分析", "🔤 文字分析"
    ])
    
    # 基本統計
    with tab1:
        basic_stats = results['basic_stats']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("文字数", f"{basic_stats['character_count']:,}")
            st.metric("単語数", f"{basic_stats['word_count']:,}")
        
        with col2:
            st.metric("文の数", f"{basic_stats['sentence_count']:,}")
            st.metric("段落数", f"{basic_stats['paragraph_count']:,}")
        
        with col3:
            st.metric("平均単語数/文", f"{basic_stats['average_words_per_sentence']:.1f}")
            st.metric("平均文字数/単語", f"{basic_stats['average_characters_per_word']:.1f}")
    
    # 言語検出
    with tab2:
        lang = results['language_detection']
        # 古いデータとの互換性のため、安全に言語コードを取得
        language_code = lang.get('language_code', lang.get('detected_language', 'unknown'))
        st.info(f"🌍 検出された言語: **{lang['language_name']}** ({language_code})")
    
    # 感情分析
    with tab3:
        sentiment = results['sentiment_analysis']
        
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_color = "green" if sentiment['sentiment'] == 'ポジティブ' else "red" if sentiment['sentiment'] == 'ネガティブ' else "orange"
            st.metric("感情", sentiment['sentiment'], delta=f"{sentiment['polarity_percentage']}%")
            
            # 感情スコアのプログレスバー
            st.progress(sentiment['polarity_percentage'] / 100)
            st.caption(f"ポジティブ度: {sentiment['polarity_percentage']}%")
        
        with col2:
            st.metric("主観性", f"{(sentiment['subjectivity'] * 100):.1f}%")
            
            # 感情の円グラフ
            fig = go.Figure(data=[go.Pie(
                labels=['ポジティブ', 'ネガティブ', '中性'],
                values=[sentiment['polarity_percentage'], 100-sentiment['polarity_percentage'], 0],
                hole=0.3
            )])
            fig.update_layout(title="感情分布")
            st.plotly_chart(fig, use_container_width=True)
    
    # 可読性分析
    with tab4:
        readability = results['readability_score']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Flesch可読性スコア", f"{readability['flesch_score']:.1f}")
            st.metric("音節数", f"{readability['syllable_count']:,}")
        
        with col2:
            st.info(f"📖 可読性レベル: **{readability['readability_level']}**")
            
            # 可読性スコアのゲージ
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = readability['flesch_score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "可読性スコア"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 70], 'color': "gray"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
    
    # 単語頻度
    with tab5:
        word_freq = results['word_frequency']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("ユニーク単語数", f"{word_freq['unique_words']:,}")
            st.metric("分析対象単語数", f"{word_freq['total_words_analyzed']:,}")
        
        with col2:
            if word_freq['most_common_words']:
                # 上位10単語の棒グラフ
                top_words = word_freq['most_common_words'][:10]
                words, counts = zip(*top_words)
                
                fig = px.bar(
                    x=words, 
                    y=counts,
                    title="最も頻繁に使用される単語（上位10）",
                    labels={'x': '単語', 'y': '出現回数'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
    
    # 文の分析
    with tab6:
        sentence_analysis = results['sentence_analysis']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("平均文の長さ", f"{sentence_analysis['average_sentence_length']:.1f} 単語")
        
        with col2:
            st.metric("最短文", f"{sentence_analysis['shortest_sentence']} 単語")
        
        with col3:
            st.metric("最長文", f"{sentence_analysis['longest_sentence']} 単語")
        
        # 文の長さ分布のヒストグラム
        if 'sentence_lengths' in sentence_analysis:
            fig = px.histogram(
                x=sentence_analysis['sentence_lengths'],
                title="文の長さ分布",
                labels={'x': '文の長さ（単語数）', 'y': '頻度'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 文字分析
    with tab7:
        char_analysis = results['character_analysis']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("総文字数", f"{char_analysis['total_letters']:,}")
            st.metric("ユニーク文字数", f"{char_analysis['unique_letters']:,}")
        
        with col2:
            if char_analysis['most_common_letters']:
                # 上位10文字の棒グラフ
                top_letters = char_analysis['most_common_letters'][:10]
                letters, counts = zip(*top_letters)
                
                fig = px.bar(
                    x=letters, 
                    y=counts,
                    title="最も頻繁に使用される文字（上位10）",
                    labels={'x': '文字', 'y': '出現回数'}
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
