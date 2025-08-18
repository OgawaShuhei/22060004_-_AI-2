import re
import requests
from textblob import TextBlob
from langdetect import detect, DetectorFactory
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import json

# NLTKのデータをダウンロード
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextAnalyzer:
    """テキスト分析を行うクラス"""
    
    def __init__(self):
        """初期化"""
        DetectorFactory.seed = 0
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_text(self, text):
        """テキストの包括的な分析を実行"""
        try:
            if not text or not text.strip():
                raise ValueError("テキストが空です")
            
            results = {
                'basic_stats': self._get_basic_stats(text),
                'language_detection': self._detect_language(text),
                'sentiment_analysis': self._analyze_sentiment(text),
                'readability_score': self._calculate_readability(text),
                'word_frequency': self._get_word_frequency(text),
                'sentence_analysis': self._analyze_sentences(text),
                'character_analysis': self._analyze_characters(text)
            }
            
            return results
        except Exception as e:
            print(f"テキスト分析中にエラーが発生: {str(e)}")
            # エラーが発生した場合のデフォルト結果を返す
            return {
                'basic_stats': {
                    'character_count': len(text) if text else 0,
                    'character_count_no_spaces': len(text.replace(' ', '')) if text else 0,
                    'word_count': 0,
                    'sentence_count': 0,
                    'paragraph_count': 0,
                    'average_words_per_sentence': 0,
                    'average_characters_per_word': 0
                },
                'language_detection': {
                    'detected_language': 'unknown',
                    'language_code': 'unknown',
                    'language_name': '分析できませんでした'
                },
                'sentiment_analysis': {
                    'polarity': 0,
                    'subjectivity': 0,
                    'sentiment': '分析できませんでした',
                    'polarity_percentage': 50
                },
                'readability_score': {
                    'flesch_score': 0,
                    'readability_level': '計算できませんでした',
                    'syllable_count': 0
                },
                'word_frequency': {
                    'unique_words': 0,
                    'most_common_words': [],
                    'total_words_analyzed': 0
                },
                'sentence_analysis': {
                    'average_sentence_length': 0,
                    'shortest_sentence': 0,
                    'longest_sentence': 0,
                    'sentence_lengths': []
                },
                'character_analysis': {
                    'total_letters': 0,
                    'unique_letters': 0,
                    'most_common_letters': [],
                    'letter_distribution': {}
                }
            }
    
    def _get_basic_stats(self, text):
        """基本的な統計情報を取得"""
        try:
            if not text or not text.strip():
                return {
                    'character_count': 0,
                    'character_count_no_spaces': 0,
                    'word_count': 0,
                    'sentence_count': 0,
                    'paragraph_count': 0,
                    'average_words_per_sentence': 0,
                    'average_characters_per_word': 0
                }
            
            words = word_tokenize(text.lower())
            sentences = sent_tokenize(text)
            
            return {
                'character_count': len(text),
                'character_count_no_spaces': len(text.replace(' ', '')),
                'word_count': len(words),
                'sentence_count': len(sentences),
                'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
                'average_words_per_sentence': len(words) / len(sentences) if sentences else 0,
                'average_characters_per_word': sum(len(word) for word in words) / len(words) if words else 0
            }
        except Exception as e:
            print(f"基本統計の取得中にエラー: {str(e)}")
            return {
                'character_count': len(text) if text else 0,
                'character_count_no_spaces': len(text.replace(' ', '')) if text else 0,
                'word_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'average_words_per_sentence': 0,
                'average_characters_per_word': 0
            }
    
    def _detect_language(self, text):
        """言語を検出"""
        try:
            if not text or not text.strip():
                return {
                    'detected_language': 'unknown',
                    'language_code': 'unknown',
                    'language_name': 'テキストが空です'
                }
            
            lang = detect(text)
            lang_names = {
                'en': '英語',
                'ja': '日本語',
                'es': 'スペイン語',
                'fr': 'フランス語',
                'de': 'ドイツ語',
                'it': 'イタリア語',
                'pt': 'ポルトガル語',
                'ru': 'ロシア語',
                'zh': '中国語',
                'ko': '韓国語'
            }
            return {
                'detected_language': lang,
                'language_code': lang,
                'language_name': lang_names.get(lang, f'言語コード: {lang}')
            }
        except Exception as e:
            print(f"言語検出中にエラー: {str(e)}")
            return {
                'detected_language': 'unknown',
                'language_code': 'unknown',
                'language_name': '検出できませんでした'
            }
    
    def _analyze_sentiment(self, text):
        """感情分析を実行"""
        try:
            if not text or not text.strip():
                return {
                    'polarity': 0,
                    'subjectivity': 0,
                    'sentiment': 'テキストが空です',
                    'polarity_percentage': 50
                }
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # 感情の強度を判定
            if polarity > 0.1:
                sentiment = 'ポジティブ'
            elif polarity < -0.1:
                sentiment = 'ネガティブ'
            else:
                sentiment = 'ニュートラル'
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment,
                'polarity_percentage': round((polarity + 1) * 50, 1)
            }
        except Exception as e:
            print(f"感情分析中にエラー: {str(e)}")
            return {
                'polarity': 0,
                'subjectivity': 0,
                'sentiment': '分析できませんでした',
                'polarity_percentage': 50
            }
    
    def _calculate_readability(self, text):
        """可読性スコアを計算"""
        try:
            if not text or not text.strip():
                return {
                    'flesch_score': 0,
                    'readability_level': 'テキストが空です',
                    'syllable_count': 0
                }
            
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())
            
            # 音節数を概算（英語の場合）
            syllables = sum(self._count_syllables(word) for word in words)
            
            # Flesch Reading Ease Score
            if sentences and words:
                flesch_score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
                flesch_score = max(0, min(100, flesch_score))
            else:
                flesch_score = 0
            
            # 可読性レベルを判定
            if flesch_score >= 90:
                level = '非常に簡単'
            elif flesch_score >= 80:
                level = '簡単'
            elif flesch_score >= 70:
                level = 'やや簡単'
            elif flesch_score >= 60:
                level = '普通'
            elif flesch_score >= 50:
                level = 'やや難しい'
            elif flesch_score >= 30:
                level = '難しい'
            else:
                level = '非常に難しい'
            
            return {
                'flesch_score': round(flesch_score, 1),
                'readability_level': level,
                'syllable_count': syllables
            }
        except Exception as e:
            print(f"可読性計算中にエラー: {str(e)}")
            return {
                'flesch_score': 0,
                'readability_level': '計算できませんでした',
                'syllable_count': 0
            }
    
    def _count_syllables(self, word):
        """単語の音節数を概算"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    def _get_word_frequency(self, text):
        """単語頻度を分析"""
        try:
            if not text or not text.strip():
                return {
                    'unique_words': 0,
                    'most_common_words': [],
                    'total_words_analyzed': 0
                }
            
            words = word_tokenize(text.lower())
            # ストップワードを除外
            words = [word for word in words if word.isalpha() and word not in self.stop_words]
            
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # 頻度順にソート
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'unique_words': len(word_freq),
                'most_common_words': sorted_words[:10],
                'total_words_analyzed': len(words)
            }
        except Exception as e:
            print(f"単語頻度分析中にエラー: {str(e)}")
            return {
                'unique_words': 0,
                'most_common_words': [],
                'total_words_analyzed': 0
            }
    
    def _analyze_sentences(self, text):
        """文の分析を実行"""
        try:
            if not text or not text.strip():
                return {
                    'average_sentence_length': 0,
                    'shortest_sentence': 0,
                    'longest_sentence': 0,
                    'sentence_lengths': []
                }
            
            sentences = sent_tokenize(text)
            sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
            
            if not sentence_lengths:
                return {
                    'average_sentence_length': 0,
                    'shortest_sentence': 0,
                    'longest_sentence': 0,
                    'sentence_lengths': []
                }
            
            return {
                'average_sentence_length': sum(sentence_lengths) / len(sentence_lengths),
                'shortest_sentence': min(sentence_lengths),
                'longest_sentence': max(sentence_lengths),
                'sentence_lengths': sentence_lengths
            }
        except Exception as e:
            print(f"文の分析中にエラー: {str(e)}")
            return {
                'average_sentence_length': 0,
                'shortest_sentence': 0,
                'longest_sentence': 0,
                'sentence_lengths': []
            }
    
    def _analyze_characters(self, text):
        """文字の分析"""
        try:
            if not text or not text.strip():
                return {
                    'total_letters': 0,
                    'unique_letters': 0,
                    'most_common_letters': [],
                    'letter_distribution': {}
                }
            
            char_count = {}
            for char in text:
                if char.isalpha():
                    char_count[char.lower()] = char_count.get(char.lower(), 0) + 1
            
            # 最も頻繁に使用される文字
            sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'total_letters': sum(char_count.values()),
                'unique_letters': len(char_count),
                'most_common_letters': sorted_chars[:10],
                'letter_distribution': char_count
            }
        except Exception as e:
            print(f"文字分析中にエラー: {str(e)}")
            return {
                'total_letters': 0,
                'unique_letters': 0,
                'most_common_letters': [],
                'letter_distribution': {}
            }
