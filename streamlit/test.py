import streamlit as st   # streamlitのライブラリを読み込む
from PIL import Image # 画像を扱うためライブラリを読み込む
import pandas as pd # 表を扱うためpandasライブラリを読み込む

st.title('Streamlitを試しに使ってみる') # ページのタイトル 
st.write('これが私の作るWebサイトです') # テキストを追加


# Streamlitでコードブロックを書いてみる

st.write('■ Streamlitでコードブロックを書いてみる')
code = '''def hello():
     print("Hello, Streamlit!")'''
st.code(code, language='python')


# 表を追加してみる(データフレーム形式)

st.write('■ 表を表示')
df = pd.DataFrame({
    '1列目' : ['トマト', 'きゅうり', 'なすび'],
    '2列目' : ['100円', '200円', '300円'],
})

st.table(df)

# 画像を挿入してみる

st.write('■ 画像を表示')
img = Image.open('test.png') #ファイルtest.pyと同階層
st.image(img, use_column_width=True)
