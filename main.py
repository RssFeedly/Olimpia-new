import feedparser
import xml.etree.ElementTree as ET
import os

CHANNEL_ID = "UCDnZ8zbVWLaVfuDmNuWq7rw"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
XML_FILE = "olimpia.xml"

def generate_filtered_rss():
    print(f"Leyendo feed RSS de: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    
    # Cargar elementos anteriores si ya existían para no perderlos
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

    # Nuevo árbol XML
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Tigo Sports PY - Videos de Olimpia"
    ET.SubElement(channel, "link").text = f"https://www.youtube.com/channel/{CHANNEL_ID}"
    ET.SubElement(channel, "description").text = "Feed RSS automatizado que filtra videos de Olimpia de Tigo Sports PY"
    ET.SubElement(channel, "language").text = "es"

    new_added_count = 0
    
    # 1. Procesar los del feed actual de YouTube
    for entry in feed.entries:
        title = entry.title
        summary = getattr(entry, 'summary', '')
        
        # Filtro flexible: busca "olimpia" en título o descripción
        if "olimpia" in title.lower() or "olimpia" in summary.lower():
            guid_val = entry.id
            
            # Crear el item XML
            item = ET.Element("item")
            ET.SubElement(item, "title").text = title
            ET.SubElement(item, "link").text = entry.link
            ET.SubElement(item, "guid").text = guid_val
            if hasattr(entry, "published"):
                ET.SubElement(item, "pubDate").text = entry.published
                
            existing_items[guid_val] = item
            new_added_count += 1
            print(f"Encontrado y agregado: {title}")

    # 2. Agregar todos los acumulados al canal (ordenados o tal cual)
    for guid_val, item_elem in existing_items.items():
        channel.append(item_elem)

    print(f"Total de videos de Olimpia en el archivo acumulado: {len(existing_items)}")
    
    # Guardar archivo XML
    tree = ET.ElementTree(rss)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_filtered_rss()
