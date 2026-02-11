import feedparser
import datetime
import os

# 严格聚焦美洲地区的顶级新闻源
FEEDS = {
    'The New York Times | Americas': 'https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml',
    'BBC News | Latin America': 'https://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
    'Reuters | Americas News': 'https://www.reutersagency.com/feed/?best-topics=americas&post_type=best'
}

def get_news_html():
    html_snippets = ""
    for name, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            html_snippets += f'<section class="media-section"><span class="media-label">{name}</span>'
            for entry in feed.entries[:3]:
                clean_title = entry.title.replace('"', '&quot;').replace("'", "&apos;")
                html_snippets += f'''
                <div class="news-card">
                    <h3><a href="{entry.link}" target="_blank">{clean_title}</a></h3>
                    <p style="font-size:0.85rem; color:#666;">{datetime.datetime.now().strftime("%Y-%m-%d")} · 自动化监测</p>
                </div>'''
            html_snippets += '</section>'
        except Exception as e:
            print(f"Error parsing {name}: {e}")
    return html_snippets

def update_file():
    file_path = 'americas-focus.html'
    # 必须填入具体的标记内容
    start_mark = ""
    end_mark = ""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 核心检查：确保标记完全匹配
    if start_mark not in content:
        print(f"错误：在 HTML 中没找到开始标记 {start_mark}")
        exit(1)
    if end_mark not in content:
        print(f"错误：在 HTML 中没找到结束标记 {end_mark}")
        exit(1)

    # 精准替换
    pre_content = content.split(start_mark)[0]
    post_content = content.split(end_mark)[1]
    
    new_html = pre_content + start_mark + "\n" + get_news_html() + "\n" + end_mark + post_content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("成功：美洲聚焦页面已更新！")

if __name__ == "__main__":
    update_file()
