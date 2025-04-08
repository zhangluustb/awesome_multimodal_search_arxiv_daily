import urllib.parse
import urllib.request
import feedparser
import csv

# 定义查询参数
# base_url = 'http://export.arxiv.org/api/query?'
# search_query = 'cat:cs.ir AND submittedDate:[20240101 TO 20250408]'
url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=multimodal&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=exclude&date-filter_by=past_12&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start="
start = 0

i = 0
with open('./README.md', 'a', encoding='utf-8') as mdfile:
    # 打开 CSV 文件以写入数据
    with open('history.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Link', 'Desc','author']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
        # 写入表头
        writer.writeheader()
        while True:
            # 构建查询 URL
            c_url = url + str(start)
            print(c_url)

            # 发送请求并解析结果
            response = urllib.request.urlopen(c_url).read()
            feed = feedparser.parse(response)
            # 写入每篇论文的信息
            if len(feed.entries) == 0:
                break
            for entry in feed.entries:
                i=i+1
                print(i)
                title = entry.title
                low_title=str.lower(title)
                if "multimodal" in low_title or 'multi-modal' in low_title or 'generative' in low_title or 'llm' in low_title:
                    link = entry.link.replace('\n', ' ')
                    abstract = entry.summary.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ') #.split("Abstract: ")[1]
                    writer.writerow({'Title': title, 'Link': link, 'Desc': "",'author':entry.author.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')})
            start += 200

        # 读取 CSV 文件并写入 Markdown 表格
        with open('history.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['Title']
                link = row['Link']
                desc = row['Desc']
                author = row['author']
                mdfile.write(f"| {title} | [{link}]({link}) | {desc} | {author} |\n")