# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Define the keywords for each text
text0_keywords = ["政治正确", "美国", "以色列", "中东", "军事", "伊朗", "哈马斯", "俄罗斯", "战争"]
text1_keywords = ["纳粹", "以色列", "情绪", "支持", "犹太人", "谴责", "内塔尼亚胡", "发言"]
text2_keywords = ["美国政府", "压力", "国际社会", "民意", "拜登", "战争", "美国国内", "军事", "美国选情"]
text3_keywords = ["登子", "AI", "犹太财团", "民主党", "漂亮国", "抗议", "大漂亮", "震撼", "施压"]
text4_keywords = ["以色列", "枪", "犹太人大屠杀", "阿拉伯人", "巴勒斯坦", "哈马斯", "逻辑", "幌子"]
text5_keywords = ["各国", "弱小国家", "俄乌战争", "难民", "以色列", "欺负"]

# Combine all keywords into a single list
all_keywords = text0_keywords + text1_keywords + text2_keywords + text3_keywords + text4_keywords + text5_keywords

# Join the keywords into a single string
text = ' '.join(all_keywords)

# Specify a Chinese font that supports the characters you are using
font_path = 'C:/Windows/Fonts/simkai.ttf'  # Replace with the path to a Chinese font file

# Generate the word cloud with the specified font
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)

# Plot the WordCloud image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
