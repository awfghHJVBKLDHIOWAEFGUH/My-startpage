import urllib.request
import xml.etree.ElementTree as ET
import json

def fetch_youtube_trending():
    url = "https://www.youtube.com/feeds/videos.xml?chart=most_popular"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
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
            
        with open('feed-data.json', 'w') as f:
            json.dump(feed, f, indent=2)
            
        print("Successfully updated feed-data.json")
    except Exception as e:
        print(f"Error fetching feed: {e}")

if __name__ == "__main__":
    fetch_youtube_trending()
