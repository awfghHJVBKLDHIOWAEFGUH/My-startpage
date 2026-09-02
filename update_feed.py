import urllib.request
import xml.etree.ElementTree as ET
import json
import re

def fetch_youtube():
    try:
        url = "https://www.youtube.com/feeds/videos.xml?chart=most_popular"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        ns = {'yt': 'http://www.youtube.com/xml/schemas/2015', 'atom': 'http://www.w3.org/2005/Atom'}
        
        feed = []
        for entry in root.findall('atom:entry', ns)[:10]:
            video_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            author = entry.find('atom:author/atom:name', ns).text
            
            feed.append({
                "h": title,
                "p": f"{author} • Live Feed",
                "link": f"https://www.youtube.com/watch?v={video_id}",
                "thumb": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            })
        return feed
    except Exception as e:
        print(f"Error fetching YouTube: {e}")
        return []

def fetch_github():
    try:
        # Scrapes GitHub Trending HTML directly
        url = "https://github.com/trending"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')

        # Regex parsing for trending repo names & descriptions
        repos = re.findall(r'href="(/[^/]+/[^/]+)" class="Link', html)
        feed = []
        
        # Deduplicate and format top 10
        seen = set()
        for repo in repos:
            repo_clean = repo.strip('/')
            if repo_clean not in seen and 'features' not in repo_clean and 'sponsors' not in repo_clean:
                seen.add(repo_clean)
                feed.append({
                    "h": repo_clean,
                    "p": "Trending Open Source Repository",
                    "link": f"https://github.com/{repo_clean}",
                    "thumb": f"https://opengraph.githubassets.com/1/{repo_clean}"
                })
            if len(feed) >= 10:
                break
        return feed
    except Exception as e:
        print(f"Error fetching GitHub: {e}")
        return []

def fetch_reddit_tech(subreddit="technology"):
    try:
        # Public JSON feed for trending tech news (substitute for X/Twitter scrapers)
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        feed = []
        for post in data['data']['children']:
            p_data = post['data']
            feed.append({
                "h": p_data['title'],
                "p": f"r/{subreddit} • {p_data['score']} points",
                "link": f"https://reddit.com{p_data['permalink']}",
                "thumb": p_data.get('thumbnail') if p_data.get('thumbnail', '').startswith('http') else ""
            })
        return feed
    except Exception as e:
        print(f"Error fetching Reddit: {e}")
        return []

if __name__ == "__main__":
    all_data = {
        "youtube": fetch_youtube(),
        "github": fetch_github(),
        "twitch": fetch_reddit_tech("Twitch"), # Fetches live Twitch news/streams via Reddit Twitch feed
        "x": fetch_reddit_tech("technology")  # Fetches trending Tech news without needing X API key
    }
    
    with open('feed-data.json', 'w') as f:
        json.dump(all_data, f, indent=2)
        
    print("Updated all 4 feeds in feed-data.json!")
