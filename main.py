diff --git a/main.py b/main.py
index 7f79d868ff8e83f07caec0aed82668e75d5dc064..7101667384ca7abd3bf46def2d5f40c96dcd5be5 100644
--- a/main.py
+++ b/main.py
@@ -1,75 +1,74 @@
 import random
 import streamlit as st
 import re
 import os
 import time
 import importlib
 from gtts import gTTS
-from pydub import AudioSegment
 from openai import OpenAI
 
 # 初始化 OpenAI client
 client = OpenAI(api_key=st.secrets["openai_api_key"])
 
 # 要載入的檔名清單
 book_names = [
     "jun_18_a",
 ]
 
 # 動態匯入並建立 book_options 字典
 book_options = {
     name: importlib.import_module(name).word_data for name in book_names
 }
 
 
 # UI
 st.title("📚 英文單字遊戲 / English Vocabulary Game")
 selected_book = st.selectbox("請選擇一本書 / Choose a book:", list(book_options.keys()))
 word_data = book_options[selected_book]
 st.write(f"📖 單字庫總數 / Total words: {len(word_data)}")
 
 num_questions = st.number_input("輸入測試題數 / Number of questions:", min_value=1, max_value=len(word_data), value=5, step=1)
 test_type = st.radio("請選擇測試類型 / Choose test type:", ["拼寫測試 / Spelling", "填空測試 / Fill-in-the-blank", "單字造句 / Sentence creation"])
 
 # 工具函式
 def get_unique_words(n):
     all_words = [(w, d[0], d[1]) for w, d in word_data.items()]
     random.shuffle(all_words)
     return all_words[:n]
 
 def mask_word(sentence, word):
     pattern = re.compile(re.escape(word), re.IGNORECASE)
     return pattern.sub(word[0] + "_" * (len(word)-2) + word[-1], sentence)
 
-def play_pronunciation(text, mp3="pronunciation.mp3", wav="pronunciation.wav"):
-    tts = gTTS(text=text, lang='fr')
+def play_pronunciation(text, mp3="pronunciation.mp3"):
+    """Generate and play pronunciation audio in MP3 format."""
+    tts = gTTS(text=text, lang="fr")
     tts.save(mp3)
-    AudioSegment.from_mp3(mp3).export(wav, format="wav")
-    if os.path.exists(wav):
-        with open(wav, "rb") as f:
-            st.audio(f, format="audio/wav")
+    if os.path.exists(mp3):
+        with open(mp3, "rb") as f:
+            st.audio(f.read(), format="audio/mp3")
 
 def clean_text(t):
     t = t.replace('’', "'").replace('‘', "'")
     return re.sub(r"[^a-zA-ZÀ-ÿ’'\- ]", '', t).lower().strip()
 
 # 初始化狀態
 if (
     "initialized" not in st.session_state
     or st.session_state.selected_book != selected_book
     or st.session_state.num_questions != num_questions
 ):
     st.session_state.words = get_unique_words(num_questions)
     st.session_state.current_index = 0
     st.session_state.score = 0
     st.session_state.mistakes = []
     st.session_state.submitted = False
     st.session_state.input_value = ""
     st.session_state.initialized = True
 
 st.session_state.selected_book = selected_book
 st.session_state.num_questions = num_questions
 st.session_state.test_type = test_type
 
 # 顯示題目
 if st.session_state.current_index < len(st.session_state.words):
