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
                "YDYp_3x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_3x1_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                "YDYp_5x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string
            }},

            "petla_zwarcia":[
                {{
                    "lokalizacja": miejsce instalacji (np. gniazda wtykowego), typ string,
                    "nr": numer porządkowy (każdy następny numer będzie większy o jeden, zaczynając od 1), typ string,
                    "pomiar": odczyt liczbowy (np. 0.56), typ float,
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
                        "YDYp_3x2_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
                        "YDYp_3x1_5_mm2": ilość obwodów (domyślna wartość "0"), typ string,
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

    print("----------PARAMS----------\n", result)

    return result.replace("```json", "").replace("```", "")

if __name__ == "__main__":
    query="""
        data pomiarów elektrycznych: 2026-10-09,
        adres pomiarów elektrycznych: "80-178 Gdańsk, Wrześniowa 17",
        miejsce badań: budynek jednorodzinny,
        pętle zwarcia gniazd:
        - gniazdo 0.48, miejsce instalacji: garaż,
        - gniazdo 0.47, miejsce instalacji: garaż,
        - gniazdo 0.45, miejsce instalacji: garaż,
        - gniazdo 0.51, miejsce instalacji: garaż,
        - gniazdo 0.39, miejsce instalacji: garaż,
        - gniazdo 0.46, miejsce instalacji: garaż,
        
        - gniazdo 0.58, miejsce instalacji: kuchnia,
        - gniazdo 0.69, miejsce instalacji: kuchnia,
        - gniazdo 0.72, miejsce instalacji: kuchnia,
        - gniazdo 0.50, miejsce instalacji: kuchnia,
        - gniazdo 0.91, miejsce instalacji: kuchnia,
        - gniazdo 0.92, miejsce instalacji: kuchnia,
        
        - gniazdo 0.42, miejsce instalacji: łazienka-parter,
        - gniazdo 0.48, miejsce instalacji: łazienka-parter,
        - gniazdo 0.42, miejsce instalacji: łazienka-parter,
        
        - gniazdo 0.83, miejsce instalacji: weranda
        
        - gniazdo 0.91, miejsce instalacji: pralnia,
        - gniazdo 0.91, miejsce instalacji: pralnia,
        - gniazdo 0.81, miejsce instalacji: pralnia,
        - gniazdo 0.82, miejsce instalacji: pralnia,

        - gniazdo 0.72, miejsce instalacji: łazienka-piętro,
        - gniazdo 0.72, miejsce instalacji: łazienka-piętro,
        - gniazdo 0.81, miejsce instalacji: łazienka-piętro,
        
        rcd:
        - producent: "MOELLER", nr: 1, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 24, czas_pomiar: 6,
        - producent: "MOELLER", nr: 2, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 21, czas_pomiar: 16,
        - producent: "MOELLER", nr: 3, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 21, czas_pomiar: 17,
        - producent: "MOELLER", nr: 4, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 21, czas_pomiar: 17
        - producent: "MOELLER", nr: 5, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 21, czas_pomiar: 17,
        - producent: "MOELLER", nr: 6, miejsce instalacji: "garaż", volt: 230, typ: "CKN6 B16/2/003", amper_wywolania_pomiar: 27, czas_pomiar: 17,
        - producent: "MOELLER", nr: 7, miejsce instalacji: "garaż", volt: 230, typ: "CFI6 25/4/003", amper_wywolania_pomiar: 26, czas_pomiar: 21,

        rezystancja izolacji mieszkania:
            miejsce instalacji: "budynek jednorodzinny",
            - YKY_5x10_mm2: 1,
            - YDYp_3x2_5_mm2: 8,
            - YDYp_3x1_5_mm2: 7,
            - YDYp_5x2_5_mm2: 1,
            - ileFaz: 3
            
        uklad_zasilania: TN-C-S,
	    napięcie sieci zasilającej: 400V
    """
    json_details_of_offer(query)
