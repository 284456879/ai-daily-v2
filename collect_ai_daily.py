"""
每天10点自动收集全网AI热点和火爆GitHub开源项目
推送到Notion
"""

import json
import requests
from datetime import datetime
import pytz
import os

# Notion API 配置
NOTION_KEY = os.environ.get("NOTION_KEY")
NOTION_VERSION = "2025-09-03"
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

# 时区配置
HONGKONG_TZ = pytz.timezone('Asia/Hong_Kong')

def create_notion_page(title, content_blocks):
    """在 Notion 中创建页面"""
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": title}}]
            }
        },
        "children": content_blocks
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def collect_ai_hotspots():
    """收集 AI 热点"""
    print("Collecting AI hotspots...")

    # 从多个来源收集 AI 热点
    hotspots = []

    # 1. Hacker News AI 相关帖子
    try:
        hn_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        hn_stories = requests.get(hn_url).json()[:20]  # 获取最新的20个故事

        for story_id in hn_stories:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url).json()

            # 过滤 AI 相关的帖子
            title = story.get('title', '')
            ai_keywords = ['AI', 'artificial intelligence', 'machine learning', 'deep learning',
                         'neural', 'LLM', 'GPT', 'Claude', 'openai', 'chatgpt']

            if any(keyword.lower() in title.lower() for keyword in ai_keywords):
                hotspots.append({
                    "title": title,
                    "description": f"Hacker News - {story.get('score', 0)} points",
                    "source": "Hacker News",
                    "url": story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                })
    except Exception as e:
        print(f"Error collecting Hacker News: {e}")

    # 2. Product Hunt AI 相关产品（简化版）
    try:
        # 注意：Product Hunt API 需要认证，这里简化处理
        hotspots.append({
            "title": "Product Hunt - Daily AI Products",
            "description": "Check Product Hunt for daily AI product launches",
            "source": "Product Hunt",
            "url": "https://www.producthunt.com"
        })
    except Exception as e:
        print(f"Error collecting Product Hunt: {e}")

    print(f"Collected {len(hotspots)} AI hotspots")
    return hotspots

def collect_github_trending():
    """收集 GitHub 热门开源项目"""
    print("Collecting GitHub trending repositories...")

    projects = []

    # GitHub Trending API（需要登录或使用第三方 API）
    # 这里使用 GitHub 搜索 API 作为替代
    try:
        # 搜索热门 AI 相关仓库
        search_queries = [
            "artificial intelligence stars:>100",
            "machine learning stars:>100",
            "deep learning stars:>100",
            "LLM stars:>100",
            "python stars:>1000 language:python"
        ]

        for query in search_queries:
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"

            # GitHub API 不需要认证，但有限制
            headers = {
                "Accept": "application/vnd.github.v3+json"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('items', [])[:3]:  # 每个查询取前3个
                    projects.append({
                        "name": item['name'],
                        "description": item['description'] or "No description",
                        "stars": item['stargazers_count'],
                        "language": item['language'] or "Unknown",
                        "url": item['html_url'],
                        "created_at": item['created_at']
                    })
            else:
                print(f"GitHub API error: {response.status_code}")

    except Exception as e:
        print(f"Error collecting GitHub trending: {e}")

    # 去重（按名称）
    seen = set()
    unique_projects = []
    for project in projects:
        if project['name'] not in seen:
            seen.add(project['name'])
            unique_projects.append(project)

    # 按星标数排序，取前 15 个
    unique_projects.sort(key=lambda x: x['stars'], reverse=True)
    final_projects = unique_projects[:15]

    print(f"Collected {len(final_projects)} GitHub trending projects")
    return final_projects

def main():
    """主函数"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collecting AI hotspots and GitHub projects...")

    # 收集数据
    ai_hotspots = collect_ai_hotspots()
    github_projects = collect_github_trending()

    print(f"Collected {len(ai_hotspots)} AI hotspots")
    print(f"Collected {len(github_projects)} GitHub trending projects")

    # 创建文本内容
    ai_hotspots_text = ""
    for item in ai_hotspots:
        ai_hotspots_text += f"{item['title']} - {item['description']}\nLink: {item['url']}\n\n"

    github_projects_text = ""
    for project in github_projects:
        github_projects_text += f"{project['name']} ({project['language']}) - {project['stars']} stars\n{project['description']}\nLink: {project['url']}\n\n"

    # 创建 Notion 内容块
    content_blocks = []

    # AI 热点部分
    content_blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "AI Hotspots"}}]
        }
    })

    for item in ai_hotspots:
        content_blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"text": {"content": item['title']}},
                    {"text": {"content": " - "}},
                    {"text": {"content": item['source']}},
                    {"text": {"content": ": "}},
                    {"type": "text", "text": {"content": item['description'], "link": {"url": item['url']}}}
                ]
            }
        })

    # GitHub 热门项目部分
    content_blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "GitHub Trending"}}]
        }
    })

    for project in github_projects:
        content_blocks.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"text": {"content": project['name']}},
                    {"text": {"content": " ("}},
                    {"text": {"content": str(project['stars'])}},
                    {"text": {"content": " stars) - "}},
                    {"text": {"content": project['language']}},
                    {"text": {"content": ": "}},
                    {"type": "text", "text": {"content": project['description'], "link": {"url": project['url']}}}
                ]
            }
        })

    # 创建 Notion 页面
    date_str = datetime.now(HONGKONG_TZ).strftime("%Y-%m-%d")
    result = create_notion_page(f"AI Daily {date_str}", content_blocks)

    if "id" in result:
        print(f"Successfully created Notion page: {result['id']}")
        print(f"View page: https://www.notion.so/{result['id'].replace('-', '')}")
    else:
        print(f"Failed to create page: {result}")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Done!")

if __name__ == "__main__":
    main()
