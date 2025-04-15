import jieba
import sqlite3
import datetime
import requests
#import ollama
import re


API_KEY = "37a5a585754851462945de4df7ba98c6"
API_URL_LIST = 'http://v.juhe.cn/toutiao/index'
API_URL_CONTENT = 'http://v.juhe.cn/toutiao/content'

MODEL_NAME = "deepseek-r1:1.5b"

CATEGORY_KEYWORDS = {
    "guonei": ["国内", "中国"],
    "guoji": ["国际", "国外", "世界"],
    "yule": ["娱乐", "电影", "明星", "综艺", "电视剧"],
    "tiyu": ["体育", "足球", "篮球", "运动", "赛事"],
    "junshi": ["军事", "战争", "兵器", "军队"],
    "keji": ["科技", "技术", "创新", "人工智能", "机器人"],
    "caijing": ["财经", "经济", "股票", "金融"],
    "youxi": ["游戏", "电竞", "游戏行业"],
    "qiche": ["汽车", "车", "车辆", "新能源"],
    "jiankang": ["健康", "医疗", "疾病", "健康养生"]
}

def get_tokens(user_query):
    for keyword_list in CATEGORY_KEYWORDS.values():
        for kw in keyword_list:
            jieba.add_word(kw, freq=999999)
    keywords = list(jieba.cut(user_query))

    stopwords = set(["我", "你", "他", "有", "的", "是", "看", "看看", "一下", "帮", "请", "什么"])
    filtered_keywords = [k for k in keywords if k not in stopwords and len(k.strip()) > 1]

    return filtered_keywords

def get_type(tokens):
    news_type = "top"
    for each in tokens:
        for key, value in CATEGORY_KEYWORDS.items():
            if each in value:
                news_type = key
    return news_type

def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def update_news_list(news_type):
    conn = sqlite3.connect('news_list.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            uniquekey TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            category TEXT
        )
        ''')
    conn.commit()

    cursor.execute('''
            SELECT MAX(date) FROM news WHERE category = ?
            ''', (news_type,))
    latest_date = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if latest_date:
        last_time = datetime.datetime.strptime(latest_date, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        if now - last_time < datetime.timedelta(hours=6):
            return
    #是否需要更新


    params = {"key": API_KEY, "type": news_type, "page": 1, "is_filter": 1}
    r = requests.get(API_URL_LIST, params=params)
    if r.status_code != 200:
        print('请求异常')
        return

    data = r.json()["result"]["data"]

    conn = sqlite3.connect('news_list.db')
    cursor = conn.cursor()

    for news_item in data:
        uniquekey = news_item["uniquekey"]
        title = news_item["title"]
        date = news_item["date"]
        category = get_type([news_item["category"]])

        cursor.execute('''
            INSERT OR IGNORE INTO news (uniquekey, title, date, category)
            VALUES (?, ?, ?, ?)
            ''', (uniquekey, title, date, category))

    conn.commit()
    cursor.close()
    conn.close()

def filter_news(news_date, news_type, tokens):
    conn = sqlite3.connect('news_list.db')
    cursor = conn.cursor()

    keyword_conditions = ""
    for keyword in tokens:
        keyword_conditions += f"SUM(CASE WHEN title LIKE '%{keyword}%' THEN 1 ELSE 0 END) + "
    keyword_conditions = keyword_conditions.rstrip(' +')

    sql_query = f"""
            SELECT uniquekey, title, date, category,
                   {keyword_conditions} AS keyword_match_count
            FROM news
            WHERE date LIKE ? 
            AND category LIKE ? 
            GROUP BY uniquekey, title, date, category
            ORDER BY keyword_match_count DESC
            LIMIT 1
            """

    cursor.execute(sql_query, (news_date + '%', news_type,))
    unique_key = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return unique_key

def get_content(unique_key):
    params = {"key": API_KEY, "uniquekey": unique_key}
    r = requests.get(API_URL_CONTENT, params=params)
    if r.status_code != 200:
        print('请求异常')
        return

    content = r.json()["result"]["content"]
    return content


def LLM_summary(news_content):
    pre_prompt = "用50个字总结一下："
    generated_text = ollama.generate(model=MODEL_NAME, prompt=pre_prompt + news_content)
    content = re.sub(r'<think>.*?</think>', '', generated_text["response"], flags=re.DOTALL)
    return content

def get_news(user_query):
    tokens = get_tokens(user_query)
    news_type = get_type(tokens)
    news_date = get_date()
    update_news_list(news_type)
    unique_key = filter_news(news_date, news_type, tokens)
    news_content = get_content(unique_key)
    #response = LLM_summary(news_content)
    return news_content

'''
sample_input = "今天有没有什么国际新闻"
print(get_news(sample_input))
'''