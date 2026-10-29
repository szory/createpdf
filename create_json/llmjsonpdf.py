"""
 w claude wpisz te fraze żeby wygenerować JSON i sprawdzić czy zgadza sie wynik z
 wejściowym promptem.

 check generated json structure with **query** variable in llmjsonpdf.py


    - producent: "ETON", nr: 1, miejsce instalacji: "kotłownia", volt: 230, typ: "HNB B16/2/003", amper_wywolania_pomiar: 24, czas_pomiar: 6,
    - producent: "ETON", nr: 2, miejsce instalacji: "kotłownia", volt: 230, typ: "HNC 40/4/003", amper_wywolania_pomiar: 24, czas_pomiar: 9,

"""

from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.prompts import (ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser

# Configuration
BASE_URL = "http://localhost:11434"
MODEL_NAME = "gpt-oss:120b-cloud"
# llama 3.2
# qwen3:30b
# gpt-oss:120b-cloud
# glm-4.7-flash:latest
# SpeakLeash/bielik-11b-v2.3-instruct:Q6_K
# gemma3, deepseek-r1 -< they don't have tools support yet

#(każdy następny numer będzie większy o jeden, zaczynając od 1),

def json_details_of_offer(query):

    llm = ChatOllama(model=MODEL_NAME, base_url=BASE_URL)

    system_template = '''
        Jesteś asystentem do spraw analizowania tekstów oraz generowania schematów JSON. 
    '''
    user_template = '''
        ## Analizując poniższy opis pomiarów elektrycznych:
        [OPIS-POMIARÓW-ELEKTRYCZNYCH]
        {query}
        [/OPIS-POMIARÓW-ELEKTRYCZNYCH]

        ## Stwórz kod JSON, który będzie wynikiem analizy powyższego opisu pomiarów-elektrycznych.
        ### Kod JSON powinien być stworzony według poniższego schematu danych:
        {{
            "data": "RRRR-MM-DD", typ string,
            "adres": adres pomiarów elektrycznych, typ string,
            "miejsce_badan": miejsce pomiarów elektrycznych, typ string,
            "ileFaz": ilość faz (domyślna wartość "3", dostępne wartości["1","3"]), typ string,

            "przewody": {{
                "YKY_5x10_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YAKXS_5x25_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDY_5x4_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_3x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_3x1_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_2x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_5x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string
            }},

            "petla_zwarcia":[
                {{
                    "lokalizacja": miejsce instalacji (np. gniazda wtykowego), typ string,
                    "nr": numer porządkowy (każdy następny numer będzie większy o jeden, zaczynając od 1), typ string,
                    "pomiar": odczyt liczbowy (np. 0.56), typ float, a jeśli w opisie jest "NU" to wartość "NU", typ string (każde gniazdo z opisu musi mieć swój wpis, także z "NU"),
                    "typ": typ bezpiecznika (domyślna-wartość="B", dostępne typy["B","C","gF","L"]), typ string,
                    "amper": ilość amper bezpiecznika (domyślna-wartość=16), typ int,
                    "volt": ilość volt (domyślna-wartość=230, dostępne wartości[230,400]), typ int
                }}
            ],
            "rcd":[
                {{
                    "producent": producent wyłącznika RCD/różnicówki, typ string,
                    "nr": numer porządkowy (każdy następny numer będzie większy o jeden, zaczynając od 1), typ string,
                    "miejsce_instalacji": miejsce instalacji wyłącznika RCD/różnicówki, typ string,
                    "volt": ilość volt (domyślna-wartość=230, dostępne wartości[230]), typ int,
                    "typ": model/typ wyłącznika RCD/różnicówki, typ string,
                    "amper_rcd": ilość amper (wartość powinna być wzięta jako znaki z przed znaku "/" w polu: "typ" np. 16/2/003), typ int,
                    "amper_wywolania": ilość mili-amperów wywołania (domyślna-wartość=30), typ int,
                    "amper_wywolania_pomiar": wartość mili-amperów zmierzona, typ int,
                    "czas_pomiar": czas w mili-sekundach zmierzony, typ int,
                    "usterki": opis usterek (domyślna-wartość="brak"), typ string
                }}
            ],
            "rezystancjaIzolacji": [], zawsze pusta lista,
            "rezystancjaIzolacjiMieszkania": [
                {{
                    "nr": numer porządkowy (każdy następny numer będzie większy o jeden, zaczynając od 1), typ string,
                    "miejsce_instalacji": miejsce instalacji obwodu, typ string,
                    "ileFaz": ilość faz (domyślna wartość "3", dostępne wartości["1","3"]), typ string,
                    "przewody": {{
                        "YKY_5x10_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YAKXS_5x25_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDY_3x4_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDY_5x4_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDYp_3x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDYp_3x1_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDYp_2x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDYp_5x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string
                    }}
                }}
            ],
            "uklad_zasilania": (domyślna wartość "TN-S", dostępne wartości["TN-S","TN-C-S","TN-C"]), typ string,
            "napiecie_sieci_zasilajacej": ilość volt (domyślna-wartość="400V", dostępne wartości["230V","400V"]), typ string
        }}

        ## wygeneruj tylko kod JSON, bez opisu, bez wyjaśnień.
    '''

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", user_template)]
    )

    llm_chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    result = llm_chain.invoke(
        {
            "query": query
        }
    )

    return result.replace("```json", "").replace("```", "")

if __name__ == "__main__":
    query_path = Path(__file__).parent / "query_json.txt"
    query = query_path.read_text(encoding="utf-8")
    print(json_details_of_offer(query))
