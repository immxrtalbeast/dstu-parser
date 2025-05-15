import json
import os
import sys
import random as rnd
sys.path.append(os.path.dirname(__file__))
from pdfread_new import get_practice_pdf



async def create_hierarchy(discipline_name: str, link_id) -> list:
    data_practice, data_lecture, data_independent = await get_practice_pdf(link_id, discipline_name)
    
    root = {
        discipline_name: {
            "practice": {"categories": []},
            "lectures": {"categories": []},
            "independent_works": {"categories": []}
        }
    }

    def process_category(data: list, category_type: str, separator:str) -> None:
        current_category = None
        topics = []
        
        for item in data:
            if "Раздел" in item:
                if current_category is not None:
                    current_category["topics"] = topics
                    root[discipline_name][category_type]["categories"].append(current_category)
                    
                parts = item.replace("Раздел", "").split()
                current_category = {
                    "name": " ".join(parts[1:]).strip(),
                    "topics": []
                }
                topics = []
            else:
                parts = item.split()
                topic_name = " ".join(parts[1:])
                topic_name = topic_name.replace(separator, '')
                topics.append(topic_name.strip())
        
        if current_category is not None:
            current_category["topics"] = topics
            root[discipline_name][category_type]["categories"].append(current_category)

    type_mapping = [
        (data_practice, "practice", "/Пр/"),
        (data_lecture, "lectures", "/Лек/"),
        (data_independent, "independent_works", "/Ср/")
    ]
    
    for data, category_type, separator in type_mapping:
        process_category(data, category_type, separator)

    return root