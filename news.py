import feedparser
from datetime import datetime
import pytz

# Danh sách các nguồn RSS từ yêu cầu của bạn
RSS_FEEDS = {
    "Tin tức Indonesia & Chính phủ": [
        "https://www.thejakartapost.com/rss/latest",
        "https://www.antaranews.com/rss/politik.xml",
        "https://setkab.go.id/category/berita/feed/"
    ],
    "Quan hệ Việt Nam - Indonesia & ASEAN": [
        "https://www.vietnamplus.vn/rss/region/239.rss",
        "https://vov.vn/rss/su-kien/indonesia.rss",
        "https://theaseanpost.com/feed",
        "https://mekongasean.vn/rss/kinh-te-khu-vuc-3.rss"
    ],
    "Nghiên cứu & Địa chính trị": [
        "https://nghiencuuquocte.org/feed/",
        "https://www.eurasiareview.com/category/east-asia-pacific/feed/",
        "https://thediplomat.com/feed/"
    ],
    "Khu vực & Thế giới": [
        "https://baoquocte.vn/rss/the-gioi.rss",
        "https://asianews.network/tag/indonesia/feed/",
        "https://asianews.network/tag/vietnam/feed/"
    ]
}

# Lấy giờ UTC+7 (Việt Nam / Indonesia)
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.now(tz)
time_string = now.strftime('%H:%M - %d/%m/%Y')

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bản tin Tổng hợp Tin tức</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #e74c3c; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
        .article {{ margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 5px; }}
        .title {{ font-size: 17px; font-weight: bold; color: #111; margin-bottom: 8px; }}
        .summary {{ margin: 8px 0; color: #444; font-size: 14px; }}
        .link-box {{ background: #e8f4f8; padding: 8px 12px; border-left: 4px solid #3498db; word-break: break-all; margin-top: 8px; font-size: 13px; }}
        a {{ color: #2980b9; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>BẢN TIN TỔNG HỢP ({time_string})</h1>
    <p><em>Cập nhật tự động từ các nguồn được chỉ định.</em></p>
"""

for category, urls in RSS_FEEDS.items():
    html_content += f"<h2>{category.upper()}</h2>"
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]: # Lấy 3 tin mới nhất từ mỗi nguồn
                title = entry.get('title', 'Không có tiêu đề')
                link = entry.get('link', '#')
                summary = entry.get('summary', entry.get('description', 'Không có tóm tắt.'))
                
                # Cắt bớt độ dài tóm tắt nếu quá dài
                if len(summary) > 300:
                    summary = summary[:300] + "..."
                    
                html_content += f"""
                <div class="article">
                    <div class="title">{title}</div>
                    <div class="summary">{summary}</div>
                    <div class="link-box">
                        <strong>Link gốc:</strong> <a href="{link}" target="_blank">{link}</a>
                    </div>
                </div>
                """
        except Exception as e:
            continue

html_content += """
</body>
</html>
"""

# Ghi ra file index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Đã tạo file index.html thành công!")
