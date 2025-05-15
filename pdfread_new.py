import PyPDF2
import re
import os
import asyncio
from functools import partial
from parse import get_pdf

async def get_practice_pdf(link, file_name):
    return await extract_text(link, file_name, )



async def extract_text(link, file_name):
    if not os.path.exists(f"{file_name}.pdf"):
        await get_pdf(link, file_name)

    loop = asyncio.get_running_loop()
    text = await loop.run_in_executor(None, partial(extract_text_sync, f"{file_name}.pdf"))

    return await get_topics_and_sections(text)

def extract_text_sync(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file.close()
    os.remove(file_path)
    return text
async def get_topics_and_sections(text):
    CATEGORY_PATTERNS = {
        "practice": "/Пр/",
        "lectures": "/Лек/",
        "independent_works": "/Ср/"
    }

    def parse_content(text):
        section_pattern = re.compile(r'Раздел \d+\. .*?(?=\n\n|\n\d+\.|\Z)', re.MULTILINE | re.DOTALL)
        sections = [re.sub(r"стр\. \d+.*\.plx", "", s) for s in section_pattern.findall(text)]
        
        topic_pattern = re.compile(r'^(\d+\.\d+)\s+(.*?)/(\w+)/', re.MULTILINE | re.DOTALL)
        return sections, [
            f" {m[0]} {re.sub(r'ОПК-?\d+\.\d+\.\d+', '', m[1]).strip()} /{m[2]}/".strip()
            for m in topic_pattern.findall(text)
        ]

    sections, extracted_data = parse_content(text)
    
    categorized_topics = {cat: [] for cat in CATEGORY_PATTERNS}
    for data in extracted_data:
        for cat, pattern in CATEGORY_PATTERNS.items():
            if pattern in data:
                categorized_topics[cat].append(data)
                break

    return await asyncio.gather(
        *[combine_data(sections, topics) 
         for topics in categorized_topics.values()]
    )


async def combine_data(sections, topics):
    if not sections or not topics:
        return []
    
    result = []
    current_section_idx = 0
    
    get_section_number = lambda s: s.split()[1].split('.', 1)[0]
    get_topic_number = lambda t: t.split('.', 1)[0].strip()
    
    if sections:
        result.append(sections[0])
    
    for topic in topics:
        topic_num = get_topic_number(topic)
        
        while current_section_idx < len(sections):
            section_num = get_section_number(sections[current_section_idx])
            
            if topic_num == section_num:
                result.append(topic)
                break
                
            current_section_idx += 1
            if current_section_idx < len(sections):
                result.append(sections[current_section_idx])
        else:
            break
            
    return result