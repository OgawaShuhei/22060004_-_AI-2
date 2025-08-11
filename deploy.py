#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Cloud デプロイ用起動スクリプト
"""

import streamlit as st
import os
import sys

# プロジェクトのルートディレクトリをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# メインアプリケーションをインポート
from app import main

if __name__ == "__main__":
    main()
