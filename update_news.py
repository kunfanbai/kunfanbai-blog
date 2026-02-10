import feedparser
import datetime

# 定义新闻源
FEEDS = {
    'NYT': 'https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml',
    'BBC': 'https://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
    'Reuters': 'https://www.reutersagency.com/feed/?best-topics=americas&post_type=best'
}

def get_news_html():
    html_snippets = ""
    for name, url in FEEDS.items():
        feed = feedparser.parse(url)
        html_snippets += f'<section class="media-section"><span class="media-label">{name}</span>'
        # 抓取每个源最新的3条新闻
        for entry in feed.entries[:3]:
            html_snippets += f'''
            <div class="news-card">
                <h3><a href="{entry.link}" target="_blank">{entry.title}</a></h3>
                <p style="font-size:0.85rem; color:#666;">{datetime.datetime.now().strftime("%Y-%m-%d")} · 实时抓取</p>
            </div>'''
        html_snippets += '</section>'
    return html_snippets

# 读取原有的 HTML 文件并替换占位符
with open('americas-focus.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 寻找你页面中媒体分栏的标志位进行替换（这里需要确保你HTML里有对应的标记）
# 简单起见，我们直接重新生成媒体分栏部分
start_mark = ""
end_mark = ""

if start_mark in content and end_mark in content:
    new_content = content.split(start_mark)[0] + start_mark + get_news_html() + end_mark + content.split(end_mark)[1]
    with open('americas-focus.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
