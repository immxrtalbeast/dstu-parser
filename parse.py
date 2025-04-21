import requests
from bs4 import BeautifulSoup
import chardet
import httpx
import re

import httpx
from bs4 import BeautifulSoup
import chardet
import re

async def get_disciplines_module(url: str, direction_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        detected_encoding = chardet.detect(response.content)['encoding']
        html_doc = response.content.decode(detected_encoding)
        clean_html = re.sub(r'[^\x00-\x7F]+', '', html_doc)
        soup = BeautifulSoup(html_doc, 'html.parser')

        aLinks = soup.find_all('a', class_='aLink')

        disciplines = {f'{direction_name}': []}

        for a_tag in aLinks:
            if "РПД" in a_tag.get_text():
                filename = a_tag.find_parent().find_parent().find(class_="dxgv dx-al")
                file_url = a_tag['href'].split("=")[1].split('&')[0]
                print(filename.get_text(), file_url)
                parent_element = filename.find_parent()
                ac_elements = parent_element.find_all(class_="dxgv dx-ac")
                kyrs = ac_elements[2]
                semestr = ac_elements[3]

                disciplines[f'{direction_name}'].append(
                    {
                        "name": filename.get_text(),
                        "course": kyrs.get_text(),
                        "semester": semestr.get_text(),
                        "link": file_url
                    }
                )

        return disciplines

async def get_pdf(id_url, name):
        url = f"https://lk.donstu.ru/RPDPrint/printrp?id={id_url}&isPDF=true"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()

            with open(f"{name}.pdf", "wb") as file:
                file.write(response.content)

            print(f"Файл успешно сохранен как '{name}'")

        except httpx.RequestError as e:
            print(f"Ошибка при загрузке файла: {e}")


def get_url_direction(direction: str) -> str:

    dic = {
        # ИиВТ
        "ВКБ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=50117",
        "ВИАС" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48732",
        "ВПР" : "https://edu.donstu.ru/Plans/Plan.aspx?id=50104",
        "ВМО" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48571",
        "ЭИБТ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48832",
        "ВПМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48563",
        "БДиМО": "https://edu.donstu.ru/Plans/Plan.aspx?id=50288",
        "ВИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48724",
        "ВЗИС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48731",
        "ВИИМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48733",
        "ВИС" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48734",
        "ВЗПИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48749",
        "ВОЗПИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48754",
        "ВПИЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48757",
        "ВИБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48766",
        "ВЗИCS": "https://edu.donstu.ru/Plans/Plan.aspx?id=48744",



        #АгроПром
        "ЭИБ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48767",
        "АТК" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48601",
        "АЗТК" : "https://edu.donstu.ru/Plans/Plan.aspx?id=51236",
        "АБ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49735",


        #Авиа
        "АВЗТ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49811",
        "АВЭ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49812",
        "АВТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50951",
        "АВЗН" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49796",

        #АМиУ
        "УМТ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48803",
        "УЗМТ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48800",
        "УНЭ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=48792",
        "ПФМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48574",
        "УЭМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50263",
        "УЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48807",
        "УА": "https://edu.donstu.ru/Plans/Plan.aspx?id=49736",
        "УМР": "https://edu.donstu.ru/Plans/Plan.aspx?id=50958",
        "УТС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48965",
        "УЗИ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=50899",
        "УИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50900",
        "УЗНЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50990",
        "УЗА": "https://edu.donstu.ru/Plans/Plan.aspx?id=49752",
        "УЗМР": "https://edu.donstu.ru/Plans/Plan.aspx?id=50957",


        #АП
        "АЗТК":"https://edu.donstu.ru/Plans/Plan.aspx?id=50762",
        "АТК": "https://edu.donstu.ru/Plans/Plan.aspx?id=50692",
        "АМО": "https://edu.donstu.ru/Plans/Plan.aspx?id=50415",
        "АПМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49729",
        "АБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49733",
        "АЗП": "https://edu.donstu.ru/Plans/Plan.aspx?id=48926",
        "АОЗП": "https://edu.donstu.ru/Plans/Plan.aspx?id=50979",
        "АП": "https://edu.donstu.ru/Plans/Plan.aspx?id=48935",
        "АА": "https://edu.donstu.ru/Plans/Plan.aspx?id=49853",
        "АВБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49853",
        "АВЗБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50256",
        "АЗЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50251",
        "АЗМО": "https://edu.donstu.ru/Plans/Plan.aspx?id=48874",
        
        #АТК
        "ИСП11-kh12" : "https://edu.donstu.ru/Plans/Plan.aspx?id=51228",
        "ИСП9-kh11-13": "https://edu.donstu.ru/Plans/Plan.aspx?id=51231",
        "ИСП9-kh14-16": "https://edu.donstu.ru/Plans/Plan.aspx?id=51229",
        "МЭП9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51168",
        "ИСП9-K4": "https://edu.donstu.ru/Plans/Plan.aspx?id=51171",
        "ИСП9-K3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51172",
        "ИСП9-K2": "https://edu.donstu.ru/Plans/Plan.aspx?id=51173",
        "ИСП9-K1": "https://edu.donstu.ru/Plans/Plan.aspx?id=51174",
        "ТЭС9-K4": "https://edu.donstu.ru/Plans/Plan.aspx?id=51175",
        "ТЭС9-K3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51176",
        "ТЭС9-K2": "https://edu.donstu.ru/Plans/Plan.aspx?id=51177",
        "ЭЭМО9-К1": "https://edu.donstu.ru/Plans/Plan.aspx?id=51178",
        "ТМ11-Кz4": "https://edu.donstu.ru/Plans/Plan.aspx?id=51180",
        "ТМ9-К4": "https://edu.donstu.ru/Plans/Plan.aspx?id=51179",
        "ТМ11-К3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51182",
        "ТМ11-Кz3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51183",
        "ТМ9-К3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51181",
        "ТМП9-К4": "https://edu.donstu.ru/Plans/Plan.aspx?id=51184",
        "ТМП9-К3": "https://edu.donstu.ru/Plans/Plan.aspx?id=51185",
        "ТМ11-К2": "https://edu.donstu.ru/Plans/Plan.aspx?id=51187",
        "ТМ11-Кz2": "https://edu.donstu.ru/Plans/Plan.aspx?id=51188",
        "ТМ9-К2": "https://edu.donstu.ru/Plans/Plan.aspx?id=51186",
        "СП9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51193",
        "ЭТЭ9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51196",
        "ПЛА9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51200",
        "Ф9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51204",
        "В9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51208",
        "ПКК11": "https://edu.donstu.ru/Plans/Plan.aspx?id=51214",
        "ФК9": "https://edu.donstu.ru/Plans/Plan.aspx?id=51215",
        

        #БЖиИЭ
        "БЗПБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48589",
        "БПБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50039",
        "БЗТБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50239",
        "БЗТБд": "https://edu.donstu.ru/Plans/Plan.aspx?id=51451",
        "БЗТТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48949",
        "БОЗТБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48974",
        "БТБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48967",
        "БТТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49856",

        #БиоВетМед
        "ЕБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48825",
        "EF": "https://edu.donstu.ru/Plans/Plan.aspx?id=50247",
        "ЕФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48849",
        "ЕВ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48851",
        "ЕОЗВ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48855",
        "ЕИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48973",
        "ЕК": "https://edu.donstu.ru/Plans/Plan.aspx?id=49044",
        "ЕОЗК": "https://edu.donstu.ru/Plans/Plan.aspx?id=49048",

        #ДТ
        "ДТГК": "https://edu.donstu.ru/Plans/Plan.aspx?id=49764",
        "ДТЗГК": "https://edu.donstu.ru/Plans/Plan.aspx?id=48993",
        "ДТТЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50764",
        "ДТИТС": "https://edu.donstu.ru/Plans/Plan.aspx?id=50764",
        "ДТОП": "https://edu.donstu.ru/Plans/Plan.aspx?id=53404",
        "ДТЗОП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49787",
        "ДТЗТЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50771",
        "ДТС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48829",
        "ДТЗПГ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48837",
        "ДТПГ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48839",
        "ДТД":"https://edu.donstu.ru/Plans/Plan.aspx?id=48612",
        "ДТМТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50270",

        #ИБиМ
        "ИЗЭБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48861",
        "ИОЗЭБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50374",
        "ИЭБ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48863",
        "ИЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50201",
        "ИЭ2": "https://edu.donstu.ru/Plans/Plan.aspx?id=49032",
        "ИЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49067",
        "ИОЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49075",
        "ИМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49097",
        "ИЗМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49108",
        "ИМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49109",
        "ИГ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49137",
        "ИЗМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49122",
        "ИОЗБУS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49087",


        #ИОТ
        "ХС": "https://edu.donstu.ru/Plans/Plan.aspx?id=49699",
        "ХИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48737",
        "ХР": "https://edu.donstu.ru/Plans/Plan.aspx?id=49709",

        #ИПМ
        "ИПМП": "https://edu.donstu.ru/Plans/Plan.aspx?id=50430",
        "ИПММ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49305",
        "ИПМЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50040",
        "ИПБП": "https://edu.donstu.ru/Plans/Plan.aspx?id=50972",
        "ИПБТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=51227",
        "ИПБК": "https://edu.donstu.ru/Plans/Plan.aspx?id=50971",

        #ИС
        "ИСВВ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48623",
        "ИСПСМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48631",
        "ИСТСЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48635",
        "ИСТК": "https://edu.donstu.ru/Plans/Plan.aspx?id=50284",
        "ИССК": "https://edu.donstu.ru/Plans/Plan.aspx?id=50282",
        "ИСТВ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48646",
        "ИСМК": "https://edu.donstu.ru/Plans/Plan.aspx?id=49820",
        "ИСОЗМК": "https://edu.donstu.ru/Plans/Plan.aspx?id=49823",
        "ИСТЭМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49830",
        "ИСОЗПСМS": "https://edu.donstu.ru/Plans/Plan.aspx?id=50070",
        "ИСОЗМКS" : "https://edu.donstu.ru/Plans/Plan.aspx?id=51241",

        #ИФКиС
        "ДПО" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49221",
        "ФП" : "https://edu.donstu.ru/Plans/Plan.aspx?id=49221",
        "ФЗФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49530",
        "ФФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49544",
        "ФЗФS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49552",

        #КиМТ
        "КСС": "https://edu.donstu.ru/Plans/Plan.aspx?id=50412",
        "ИСМК" :"https://edu.donstu.ru/Plans/Plan.aspx?id=48953",
        "КЗСМ" : "https://edu.donstu.ru/Plans/Plan.aspx?id=50895",
        "КУК": "https://edu.donstu.ru/Plans/Plan.aspx?id=50896",
        "КЗИЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=53456",

        #КЭУП
        "СИС": "https://edu.donstu.ru/Plans/Plan.aspx?id=51120",
        "РВМП": "https://edu.donstu.ru/Plans/Plan.aspx?id=51116",
        "ЗСЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=51133",
        "ССД": "https://edu.donstu.ru/Plans/Plan.aspx?id=51124",
        "СПС": "https://edu.donstu.ru/Plans/Plan.aspx?id=51140",
        "УЮР": "https://edu.donstu.ru/Plans/Plan.aspx?id=51145",
        "ПНК": "https://edu.donstu.ru/Plans/Plan.aspx?id=51149",
        "УПДО": "https://edu.donstu.ru/Plans/Plan.aspx?id=51147",

        #МКиМТ
        "МКР": "https://edu.donstu.ru/Plans/Plan.aspx?id=49146",
        "МКЗР": "https://edu.donstu.ru/Plans/Plan.aspx?id=50437",
        "МКС": "https://edu.donstu.ru/Plans/Plan.aspx?id=49163",
        "МКМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49166",
        "МКЗНФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49557",
        "МКЗНХ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49569",
        "МКНФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49577",
        "МКЗИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49602",
        "МКИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49612",
        "МКЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50931",
        "МКОЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49639",
        "МКЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49641",
        "МКНХ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49587",
        "МКНХТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49595",

        #ПГС
        "ПГСУ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48827",
        "ПГПУ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48652",
        "ПГИП": "https://edu.donstu.ru/Plans/Plan.aspx?id=48666",
        "ПГС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48673",
        "ПГОЗС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48681",
        "ПГУ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48688",

        #ПЛ
        "ЛПП": "https://edu.donstu.ru/Plans/Plan.aspx?id=48865",
        "ЛЗИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49376",
        "ЛИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49370",
        "ЛЗЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49378",
        "ЛЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49398",
        "ЛОЗЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49425",

        #ППД
        "ДПК": "https://edu.donstu.ru/Plans/Plan.aspx?id=48857",
        "ДОЗПС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48867",
        "ДПС": "https://edu.donstu.ru/Plans/Plan.aspx?id=48859",
        "ДЗПО": "https://edu.donstu.ru/Plans/Plan.aspx?id=49271",
        "ДЗП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49742",
        "ДОЗП": "https://edu.donstu.ru/Plans/Plan.aspx?id=50355",
        "ДП":"https://edu.donstu.ru/Plans/Plan.aspx?id=50357",
        "ДПО": "https://edu.donstu.ru/Plans/Plan.aspx?id=49213",
        "ФП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49213",
        "ДЗПП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49289",
        "ДПП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49304",
        "ДЗСО": "https://edu.donstu.ru/Plans/Plan.aspx?id=49316",
        "ДСО": "https://edu.donstu.ru/Plans/Plan.aspx?id=49338",
        "ДПИ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50211",

        #СГ
        "ГЗПО": "https://edu.donstu.ru/Plans/Plan.aspx?id=49246",
        "ГПО":"https://edu.donstu.ru/Plans/Plan.aspx?id=49250",
        "ГЗП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49353",
        "ГОЗП" :"https://edu.donstu.ru/Plans/Plan.aspx?id=50988",
        "ГП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49363",
        "ГД": "https://edu.donstu.ru/Plans/Plan.aspx?id=49465",
        "ГЗД": "https://edu.donstu.ru/Plans/Plan.aspx?id=49479",
        "ГЗТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49501",
        "ГТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49518",

        #СТ
        "ИТДВ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50221",
        "ИОЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49054",
        "ИЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49070",
        "ПСЗСР": "https://edu.donstu.ru/Plans/Plan.aspx?id=50227",
        "ПССР": "https://edu.donstu.ru/Plans/Plan.aspx?id=49057",
        "ПСЗС": "https://edu.donstu.ru/Plans/Plan.aspx?id=49172",
        "ПСС": "https://edu.donstu.ru/Plans/Plan.aspx?id=49175",
        "ПОЗСТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49193",
        "ПСТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49186",
        "ПСГ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49196",
        "ПСЗСS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49177",
        "ПСЗТS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49190",
        "ПСЗГS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49202",
        "ПСЗС": "https://edu.donstu.ru/Plans/Plan.aspx?id=50368",

        #ТМ
        "ТМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50385",
        "ТКТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50339",
        "ТМТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50779",
        "ТТХ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50429",
        "ТЗКШ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48995",
        "ТКШ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49015",
        "ТД": "https://edu.donstu.ru/Plans/Plan.aspx?id=49684",
        "ТОЗД": "https://edu.donstu.ru/Plans/Plan.aspx?id=49690",
        "ТЗКТS": "https://edu.donstu.ru/Plans/Plan.aspx?id=50353",
        "ТОЗД": "https://edu.donstu.ru/Plans/Plan.aspx?id=49695",
        "ТЗМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49713",
        "ТЗКТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50345",
        "ТЗМТ": 'https://edu.donstu.ru/Plans/Plan.aspx?id=50858',
        
        #ТСиЭ
        "СПТувц": "https://edu.donstu.ru/Plans/Plan.aspx?id=48847",
        "СЗР": "https://edu.donstu.ru/Plans/Plan.aspx?id=48770",
        "СР": "https://edu.donstu.ru/Plans/Plan.aspx?id=48775",
        "СЗИТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48781",
        "СИТ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48786",
        "СЗТП": "https://edu.donstu.ru/Plans/Plan.aspx?id=49790",
        "СЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50884",
        "СОЗР": "https://edu.donstu.ru/Plans/Plan.aspx?id=50267",
        "СЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50886",
        "СЗЭ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49807",

        #ШАДИ
        "ШДМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50291",
        "ША": "https://edu.donstu.ru/Plans/Plan.aspx?id=48585",
        "ША": "https://edu.donstu.ru/Plans/Plan.aspx?id=48587",
        "ШОЗАд": "https://edu.donstu.ru/Plans/Plan.aspx?id=48594",
        "ШРА": "https://edu.donstu.ru/Plans/Plan.aspx?id=48597",
        "ШГР": "https://edu.donstu.ru/Plans/Plan.aspx?id=48603",
        "ШОЗГРд": "https://edu.donstu.ru/Plans/Plan.aspx?id=48609",
        "ШП": "https://edu.donstu.ru/Plans/Plan.aspx?id=48699",

        #ЭиНГП
        "ЭМФ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48580",
        "УЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48806",
        "ЭЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48806",
        "ЭЗЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48810",
        "ЭТМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49714",
        "ЭА": "https://edu.donstu.ru/Plans/Plan.aspx?id=50410",
        "ЭЗХ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50337",
        "ЭХ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50324",
        "ЭЗТМ": "https://edu.donstu.ru/Plans/Plan.aspx?id=50890",
        "ЭЗА": "https://edu.donstu.ru/Plans/Plan.aspx?id=50411",
        "ЭОЗЛ": "https://edu.donstu.ru/Plans/Plan.aspx?id=48816",

        #Ю
        "ЮЗЮS": "https://edu.donstu.ru/Plans/Plan.aspx?id=49081",
        "ЮОЗЮ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49094",
        "ЮЮ": "https://edu.donstu.ru/Plans/Plan.aspx?id=49117",





    }
    return dic[direction]

