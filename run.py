import feedparser
import csv
import datetime

# 定义 arXiv 的 API URL，这里以计算机科学领域为例
url = 'http://export.arxiv.org/rss/cs.ir'

# 使用 feedparser 解析 RSS 源
feed = feedparser.parse(url)

# 假设我们要筛选出 cs.IR 领域的论文
# target_category = 'cs.IR'

# 获取当前日期
today = datetime.date.today().strftime("%d-%b-%Y")
import os
os.makedirs(today,exist_ok=True)
os.chdir(today)
# 打开 Markdown 文件以写入报告
with open('README.md', 'w', encoding='utf-8') as mdfile:
    with open('../README.md', 'a', encoding='utf-8') as mdfile_total:
        # 打开 CSV 文件以写入数据
        with open('papers.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Desc','author']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 写入表头
            writer.writeheader()
            # 写入每篇论文的信息
            for entry in feed.entries:
                # categories = [tag['term'] for tag in entry.tags]
                # if target_category in categories:
                title = entry.title
                low_title=str.lower(title)
                if "multimodal" in low_title or 'multi-modal' in low_title or 'generative' in low_title or 'llm' in low_title:
                    #  and ("search" in low_title or "retrieval" in low_title):
                    link = entry.link
                    abstract = entry.summary.split("Abstract: ")[1]
                    writer.writerow({'Title': title, 'Link': link, 'Desc': abstract,'author':entry.author})
        mdfile.write(f"# arXiv Daily Report - {today}\n\n")
        mdfile.write("| Title | Link | abstract | author |\n")
        mdfile.write("| --- | --- | --- | --- |\n")

        # 读取 CSV 文件并写入 Markdown 表格
        with open('papers.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['Title']
                link = row['Link']
                desc = row['Desc']
                author = row['author']
                mdfile.write(f"| {title} | [{link}]({link}) | {desc} | {author} |\n")
                mdfile_total.write(f"| {title} | [{link}]({link}) | {desc} | {author} |\n")
