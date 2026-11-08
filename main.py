import feedparser
import xml.etree.ElementTree as ET
import os

RSS_URL = "https://www.youtube.com/feeds/videos.xml?user=TigoSportsPY"
XML_FILE = "olimpia.xml"

def generate_filtered_rss():
    print(f"Leyendo feed de YouTube...")
    feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw")
    
    existing_items = {}
    if os.path.exists(XML_FILE):
        try:
            tree_old = ET.parse(XML_FILE)
            root_old = tree_old.getroot()
            channel_old = root_old.find("channel")
            if channel_old is not None:
                for item in channel_old.findall("item"):
                    guid = item.find("guid")
                    if guid is not None and guid.text:
                        existing_items[guid.text] = item
        except Exception as e:
            print(f"Aviso leyendo XML anterior: {e}")

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Tigo Sports PY - Videos de Olimpia (Estricto)"
    ET.SubElement(channel, "link").text = "https://www.youtube.com/@TigoSportsPY"
    ET.SubElement(channel, "description").text = "Feed RSS automatizado con videos cuyo título dice Olimpia"
    ET.SubElement(channel, "language").text = "es"

    new_added_count = 0
    
    for entry in feed.entries:
        title = entry.title
        
        # --- FILTRO ESTRICTO ---
        # Exigimos que la palabra "Olimpia" (o "olimpia") esté estrictamente dentro del TÍTULO del video.
        # Si prefieres que coincida exactamente con mayúscula inicial, usa "Olimpia" en lugar de title.lower()
        if "olimpia" in title.lower():
            guid_val = entry.id
            
            item = ET.Element("item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = entry.link
            ET.SubElement(item, "guid").text = guid_val
            if hasattr(entry, "published"):
                ET.SubElement(item, "pubDate").text = entry.published
                
            existing_items[guid_val] = item
            new_added_count += 1
            print(f"-> [ESTRICTO] Agregado por título: {title}")
        else:
            print(f"x Ignorado (no dice Olimpia en el título): {title}")

    for guid_val, item_elem in existing_items.items():
        channel.append(item_elem)

    print(f"Total acumulado en el XML final: {len(existing_items)}")
    
    tree = ET.ElementTree(rss)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_filtered_rss()
