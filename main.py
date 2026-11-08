import feedparser
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCDnZ8zbVWLaVfuDmNuWq7rw"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def generate_filtered_rss():
    print(f"Leyendo feed RSS de: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Tigo Sports PY - Videos de Olimpia"
    ET.SubElement(channel, "link").text = f"https://www.youtube.com/channel/{CHANNEL_ID}"
    ET.SubElement(channel, "description").text = "Feed RSS automatizado que filtra videos de Olimpia de Tigo Sports PY"
    ET.SubElement(channel, "language").text = "es"

    added_count = 0
    
    for entry in feed.entries:
        title = entry.title
        # También revisamos la summary/descripción por si acaso el título no dice Olimpia
        summary = getattr(entry, 'summary', '')
        
        # Buscamos la palabra "olimpia" tanto en el título como en la descripción (sin importar mayúsculas)
        if "olimpia" in title.lower() or "olimpia" in summary.lower():
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = entry.link
            ET.SubElement(item, "guid").text = entry.id
            
            if hasattr(entry, "published"):
                ET.SubElement(item, "pubDate").text = entry.published
                
            added_count += 1

    print(f"Se encontraron {added_count} videos relacionados con 'Olimpia'.")
    
    tree = ET.ElementTree(rss)
    tree.write("olimpia.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_filtered_rss()
