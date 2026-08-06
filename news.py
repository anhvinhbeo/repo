import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re

# Danh sách nguồn RSS đã chuẩn hóa
SOURCES = [
    # ("Chủ đề", "Tên nguồn", "Link RSS XML")
    ("Indonesia & Chính phủ", "The Jakarta Post", "https://www.thejakartapost.com/rss/latest"),
    ("Indonesia & Chính phủ", "Antara News - Politik", "https://www.antaranews.com/rss/politik.xml"),
    ("Indonesia & Chính phủ", "Setkab Indonesia", "https://setkab.go.id/category/berita/feed/"),
    
    ("Quan hệ Việt Nam - Indonesia & ASEAN", "VOV News", "https://vov.vn/rss/su-kien/indonesia.rss"),
    ("Quan hệ Việt Nam - Indonesia & ASEAN", "The ASEAN Post", "https://theaseanpost.com/feed"),
    ("Quan hệ Việt Nam - Indonesia & ASEAN", "Mekong ASEAN", "https://mekongasean.vn/rss/kinh-te-khu-vuc-3.rss"),
    ("Quan hệ Việt Nam - Indonesia & ASEAN", "VietnamPlus", "https://www.vietnamplus.vn/rss/region/239.rss"),

    ("Nghiên cứu & Địa chính trị", "Nghiên cứu Quốc tế", "https://nghiencuuquocte.org/feed/"),
    ("Nghiên cứu & Địa chính trị", "Eurasia Review", "https://www.eurasiareview.com/category/east-asia-pacific/feed/"),
    ("Nghiên cứu & Địa chính trị", "The Diplomat", "https://thediplomat.com/category/southeast-asia/feed/"),
    ("Nghiên cứu & Địa chính trị", "ISEAS Blog", "https://iseas.edu.sg/library/blog/feed/"),

    ("Khu vực & Thế giới", "Báo Quốc Tế", "https://baoquocte.vn/rss/the-gioi.rss"),
    ("Khu vực & Thế giới", "Asia News Network", "https://asianews.network/feed/")
]

def clean_html_to_text(raw_html):
    """Bóc tách thẻ HTML để lấy văn bản tóm tắt thuần túy"""
    if not raw_html:
        return "Nội dung tóm tắt đang được cập nhật từ nguồn gốc."
    
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    # Loại bỏ khoảng trắng thừa hoặc xuống dòng liên tục
    text = re.sub(r'\s+', ' ', text)
    
    if len(text) < 30:
        return "Nội dung tóm tắt ngắn, vui lòng xem chi tiết tại link gốc bên dưới."
    return text[:350] + "..." if len(text) > 350 else text

def fetch_all_news():
    news_data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for category, source_name, url in SOURCES:
        if category not in news_data:
            news_data[category] = []
            
        try:
            # Tải dữ liệu RSS giả lập trình duyệt
            response = requests.get(url, headers=headers, timeout=12)
            feed = feedparser.parse(response.content)
            
            # Lấy tối đa 7 bài viết mới nhất mỗi nguồn
            for entry in feed.entries[:7]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '').strip()
                
                # Trích xuất phần nội dung/tóm tắt từ nhiều trường dữ liệu khác nhau
                raw_summary = entry.get('summary', entry.get('description', ''))
                if not raw_summary and 'content' in entry:
                    raw_summary = entry.content[0].value
                
                summary = clean_html_to_text(raw_summary)
                
                if title and link:
                    news_data[category].append({
                        'source': source_name,
                        'title': title,
                        'link': link,
                        'summary': summary
                    })
        except Exception as e:
            print(f"Lỗi khi đọc nguồn {source_name}: {e}")
            continue

    return news_data

# Lấy giờ Việt Nam / Indonesia (UTC+7)
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.now(tz)
time_string = now.strftime('%H:%M - %d/%m/%Y')

all_news = fetch_all_news()

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bản tin Tổng hợp Tin tức - UTC+7</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 950px; margin: 0 auto; padding: 20px; color: #2c3e50; background-color: #f4f6f9; }}
        .header {{ text-align: center; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px; }}
        h1 {{ color: #1a365d; margin: 0 0 10px 0; font-size: 24px; }}
        .timestamp {{ color: #718096; font-size: 14px; font-style: italic; }}
        h2 {{ color: #2b6cb0; margin-top: 35px; border-bottom: 2px solid #3182ce; padding-bottom: 8px; font-size: 20px; text-transform: uppercase; }}
        .article {{ background: #ffffff; margin-bottom: 18px; padding: 18px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #3182ce; }}
        .source-tag {{ display: inline-block; background: #e2e8f0; color: #4a5568; font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 4px; margin-bottom: 8px; }}
        .title {{ font-size: 17px; font-weight: bold; color: #1a202c; margin-bottom: 8px; line-height: 1.4; }}
        .summary {{ margin: 10px 0; color: #4a5568; font-size: 14px; text-align: justify; }}
        .link-box {{ background: #ebf8ff; padding: 10px; border-radius: 4px; border: 1px solid #bee3f8; word-break: break-all; margin-top: 10px; font-size: 13px; }}
        a {{ color: #2b6cb0; text-decoration: none; font-weight: 500; }}
        a:hover {{ text-decoration: underline; color: #2c5282; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BẢN TIN TỔNG HỢP TIN TỨC</h1>
        <div class="timestamp">Cập nhật lúc: {time_string} (Giờ UTC+7)</div>
    </div>
"""

for category, articles in all_news.items():
    if articles:
        html_content += f"<h2>{category} ({len(articles)} bài)</h2>"
        for item in articles:
            html_content += f"""
            <div class="article">
                <span class="source-tag">{item['source']}</span>
                <div class="title">{item['title']}</div>
                <div class="summary">{item['summary']}</div>
                <div class="link-box">
                    <strong>Link gốc:</strong> <a href="{item['link']}" target="_blank">{item['link']}</a>
                </div>
            </div>
            """

html_content += """
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Đã tạo lại index.html với tóm tắt nội dung đầy đủ!")
