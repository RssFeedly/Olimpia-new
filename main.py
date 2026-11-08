import feedparser
import xml.etree.ElementTree as ET
import os

# Usamos la lista de reproducciones de subidas públicas de @TigoSportsPY
# Esto evita problemas con IDs internos obsoletos de YouTube
RSS_URL = "https://www.youtube.com/feeds/videos.xml?user=TigoSportsPY"
# O alternativamente por playlist de subidas del canal principal
ALT_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw" 
XML_FILE = "olimpia.xml"

def generate_filtered_rss():
    print(f"Intentando leer feed...")
    feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCDnZ8zbVWLaVfuDmNuWq7rw")
    
    # Si por alguna razón el feed viene vacío, probamos una ruta alternativa basada en búsqueda directa o RSS general
    if not feed.entries:
        print("El feed principal no devolvió entradas, revisando conexión...")

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
    
    ET.SubElement(channel, "title").text = "Tigo Sports PY - Videos de Olimpia"
    ET.SubElement(channel, "link").text = "https://www.youtube.com/@TigoSportsPY"
    ET.SubElement(channel, "description").text = "Feed RSS automatizado que filtra videos de Olimpia de Tigo Sports PY"
    ET.SubElement(channel, "language").text = "es"

    new_added_count = 0
    
    print(f"Total de entradas leídas de YouTube: {len(feed.entries)}")
    
    for entry in feed.entries:
        title = entry.title
        summary = getattr(entry, 'summary', '')
        
        print(f"Revisando video: {title}")
        
        # Filtro flexible para capturar cualquier mención a Olimpia
        if "olimpia" in title.lower() or "olimpia" in summary.lower():
            guid_val = entry.id
            
            item = ET.Element("item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = entry.link
            ET.SubElement(item, "guid").text = guid_val
            if hasattr(entry, "published"):
                ET.SubElement(item, "pubDate").text = entry.published
                
            existing_items[guid_val] = item
            new_added_count += 1
            print(f"-> ¡MATCH DE OLIMPIA AGREGADO!: {title}")

    for guid_val, item_elem in existing_items.items():
        channel.append(item_elem)

    print(f"Total acumulado en el XML final: {len(existing_items)}")
    
    tree = ET.ElementTree(rss)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_filtered_rss()
