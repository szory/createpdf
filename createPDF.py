from xhtml2pdf import pisa
from bs4 import BeautifulSoup
import urllib.request
from io import BytesIO
from xhtml2pdf.files import pisaFileObject
import json

from models.dataProtocol import DataProtocol, PetlaZwarcia, Rcd

# enable logging
pisa.showLogging()

# use for Polish signs like "ęążć itp"
font_url = "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
font_path = "./NotoSans-Regular.ttf"
# it is used by link_callback to find the font file
urllib.request.urlretrieve(font_url, font_path)


def getPdfTemplate(file_path):
    filehandle = open(file_path, 'r', encoding='utf-8')
    redDom = filehandle.read()
    soup = BeautifulSoup(redDom, 'html.parser')
    return str(soup)


def parse_html_protocol_badanie_izolacji(json: DataProtocol, html_source):
    for key, value in dict(json.__dict__).items():
        try:
            key = str(key)
            html_source = html_source.replace("{{" + key + "}}", value)
        except:
            continue
    return html_source


def parse_html_tables_izolacja(json: DataProtocol, html_source):
    pass
    generated_html = "<tr>"
    i = 0
    j = 0
    output_html = ""
    for key, value in dict(json.__dict__).items():
        try:
            value = int(value)
        except (TypeError, ValueError):
            continue
        for _ in range(int(value)):
            i = i + 1
            if key == "YKY_5x10_mm2":
                name = "Obwód YKY 5x10 mm2"
                output_html += "<tr><td>" + str(
                    i) + "</td><td>" + name + "</td><td>180</td><td>180</td><td>180</td><td>180</td><td>180</td><td>180</td><td class='td60px'>180</td><td>dobra</td></tr>"

            if key == "YDYp_3x2_5mm2":
                name = "Obwód YDYp 3x2,5 mm2"
                if j == 3:
                    j = 0
                output_html += """
                    <tr>
                        <td>""" + str(i) + """</td><td>""" + name + """</td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass">""" + ('180' if j == 0 else '') + """</td>
                        <td class="tdClass">""" + ('180' if j == 1 else '') + """</td>
                        <td class="tdClass">""" + ('180' if j == 2 else '') + """</td>
                        <td class="td60px">180</td><td class="td60px">dobra</td>
                    </tr>"""
                j = j + 1
            if key == "YDYp_3x1_5_mm2":
                name = "Obwód YDYp 3x1,5 mm2"
                if j == 3:
                    j = 0
                output_html += """
                    <tr>
                        <td>""" + str(i) + """</td><td>""" + name + """</td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass">""" + ('180' if j == 0 else '') + """</td>
                        <td class="tdClass">""" + ('180' if j == 1 else '') + """</td>
                        <td class="tdClass">""" + ('180' if j == 2 else '') + """</td>
                        <td class="td60px">180</td><td class="td60px">dobra</td>
                    </tr>"""
                j = j + 1

            if key == "YDYp_5x2_5_mm2":
                name = "Obwód YDYp 5x2,5 mm2"
                output_html += "<tr><td>" + str(
                    i) + "</td><td>" + name + "</td><td>180</td><td>180</td><td>180</td><td>180</td><td>180</td><td>180</td><td class='td60px'>180</td><td>dobra</td></tr>"

    html_source = html_source.replace("{{data}}", json.data)
    html_source = html_source.replace("{{adres}}", json.adres)
    html_source = html_source.replace("{{miejsce_badan}}", json.miejsce_badan)
    return html_source.replace("{{tabela_rezystancji_izolacji_html}}", output_html)


def parse_html_tables_izolacja_precise(json: DataProtocol, html_source):
    output_html = ""
    location = ""

    for item in json.rezystancjaIzolacji:
        if location != item["lokalizacja"]:
            location = item["lokalizacja"]
            output_html += """
                    <tr>
                        <td class="lp"></td>
                        <td class='boldTd'>""" + location + """</td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="tdClass"></td>
                        <td class="td60px"></td>
                        <td class="td60px"></td>
                    </tr>
                """
        output_html += """
                <tr>
                    <td class="lp">""" + item["nr"] + """</td>
                    <td>Obwód """ + item["nazwaObwodu"] + """</td>
                    <td class="tdClass">""" + ('' if item["l1l2"] == 0 else str(item["l1l2"])) + """</td>
                    <td class="tdClass">""" + ('' if item["l2l3"] == 0 else str(item["l2l3"])) + """</td>
                    <td class="tdClass">""" + ('' if item["l1l3"] == 0 else str(item["l1l3"])) + """</td>
                    <td class="tdClass">""" + ('' if item["l1n"] == 0 else str(item["l1n"])) + """</td>
                    <td class="tdClass">""" + ('' if item["l2n"] == 0 else str(item["l2n"])) + """</td>
                    <td class="tdClass">""" + ('' if item["l3n"] == 0 else str(item["l3n"])) + """</td>
                    <td class="td60px">""" + ('' if item["l1l2l3n"] == 0 else str(item["l1l2l3n"])) + """</td>
                    <td class="td60px">""" + item["uwagi"] + """</td>
                </tr>
            """

    return html_source.replace("{{tabela_rezystancji_izolacji_html}}", output_html)


def parse_html_tables_petla_zwarcia(json: DataProtocol, html_source):
    output_html = ""
    location = ""
    tabela_legenda = ""
    isFailure = False

    for item in json.petla_zwarcia:
        if location != item["lokalizacja"]:
            location = item["lokalizacja"]
            output_html += """
                      <tr>
                            <td class='lp'></td>
                            <td class='boldTd'>""" + item["lokalizacja"] + """</td>
                            <td class='td100px'></td>
                            <td class='tdClass'></td>
                            <td class='tdClass'></td>
                            <td class='tdClass'></td>
                            <td></td>
                            <td></td>
                            <td></td>
                      </tr>"""
        ia = countIA(item)
        # obliczanie pętli zwarcia dla gniazda 3 fazowego bierze się pod uwagę
        # zawsze napięcie 230V (między fazą a uziemieniem)
        za_obl = 230 / ia

        ocena = ""
        # ocena = ('tak' if item["pomiar"] <= za_obl else 'nie')
        if type(item["pomiar"]) == float:
            ocena = ('tak' if item["pomiar"] <= za_obl else 'nie')
        elif type(item["pomiar"]) == str:
            if (item["pomiar"] == "NU" or item["pomiar"] == "BU"):
                ocena = "nie"
                isFailure = True

        output_html += """
                    <tr>
                        <td class="lp">""" + str(item["nr"]) + """</td>
                        <td>Gniazdo """ + str(item["volt"]) + """V + PE</td>
                        <td class='td100px'>""" + item["typ"] + """</td>
                        <td>""" + str(item["amper"]) + """</td>
                        <td>0.4</td>
                        <td>""" + str(ia) + """</td>
                        <td class='td60px'>""" + str(item["pomiar"]) + """</td>
                        <td class='td70px'>""" + str(format(za_obl, '.2f')) + """</td>
                        <td class='td70px'>""" + ocena + """</td>
                    </tr>"""

    if isFailure:
        tabela_legenda += """
                <table>
                    <tbody>
                        <tr>
                            <td class='lp'>Lp.</td>
                            <td class="td100px">skrót</td>
                            <td class="td200px">opis</td>
                        </tr>
                        <tr>
                            <td class='lp'>1</td>
                            <td class="td100px">BU</td>
                            <td class="td200px">Brak Uziemienia</td>
                        </tr>
                        <tr>
                            <td class='lp'>2</td>
                            <td class="td100px">NU</td>
                            <td class="td200px">Nieskuteczne Uziemienie</td>
                        </tr>
                     </tbody>
                </table>"""
        html_source = html_source.replace("{{tabela_legenda}}", tabela_legenda)
    else:
        html_source = html_source.replace("{{tabela_legenda}}", "")


    html_source = html_source.replace("{{data}}", json.data)
    html_source = html_source.replace("{{adres}}", json.adres)
    html_source = html_source.replace("{{miejsce_badan}}", json.miejsce_badan)
    html_source = html_source.replace("{{tabela_pomiaru_petli_zwarcia}}", output_html)
    return html_source


def countIA(item: PetlaZwarcia):
    if item["typ"] == "B":
        return 5 * item["amper"]
    if item["typ"] == "C":
        return 10 * item["amper"]
    if item["typ"] == "gF":
        return 2.5 * item["amper"]
    if item["typ"] == "L":
        return 4.9 * item["amper"]
    return None


def parse_html_protocol_rcd(json: DataProtocol, html_source):
    pass
    output_html = ""
    rcd_items: list[Rcd] = json.rcd
    producent = ""
    miejsce_instalacji = ""
    i = 0
    for rcd_item in rcd_items:
        if rcd_item["producent"] != producent or rcd_item["miejsce_instalacji"] != miejsce_instalacji:
            producent = rcd_item["producent"]
            miejsce_instalacji = rcd_item["miejsce_instalacji"]
            output_html += """
                    <div class="container">
                        <div>Producent: """ + rcd_item["producent"] + """</div>
                        <div>Miejsce zainstalowania TR: """ + rcd_item["miejsce_instalacji"] + """</div>
                    </div>
                    <table><tbody>
                      <tr>
                        <td class="lp">Lp.</td>
                        <td>Obwody chronione wyłącznikiem</td>
                        <td class='td100px'>Typ wyłącznika</td>
                        <td class="tdClass">In [A]</td>
                        <td class="tdClass">In [mA]</td>
                        <td class="tdClass">I [mA]</td> 
                        <td class="tdClass">Ta [ms]</td>
                    </tr>
            """

        output_html += """
                      <tr>
                        <td class='lp'>""" + rcd_item["nr"] + """</td>
                        <td>Gniazdo """ + str(rcd_item["volt"]) + """ V+PE</td>
                        <td class='td100px'>""" + rcd_item["typ"] + """</td>
                        <td class='td70px'>""" + str(rcd_item["amper_rcd"]) + """</td>
                        <td class='td70px'>""" + str(rcd_item["amper_wywolania"]) + """</td>
                        <td class='td70px'>""" + str(rcd_item["amper_wywolania_pomiar"]) + """</td>
                        <td class='td70px'>""" + str(rcd_item["czas_pomiar"]) + """</td>
                      </tr>"""
        # print("len(rcd_items)", len(rcd_items))
        if ((i + 1) < len(rcd_items)):
            if (rcd_items[i]["producent"] != rcd_items[i + 1]["producent"] or
                    rcd_items[i]["miejsce_instalacji"] != rcd_items[i + 1]["miejsce_instalacji"]):
                output_html += "</tbody></table>"
                output_html += "Orzeczenie końcowe: wyłączniki różnicowo-prądowe działają prawidłowo"
                output_html += "<br/><br/><br/>"
        else:
            output_html += "</tbody></table>"
            output_html += "Orzeczenie końcowe: wyłączniki różnicowo-prądowe działają prawidłowo"
        i = i + 1

    html_source = html_source.replace("{{miejsce_badan}}", json.miejsce_badan)
    html_source = html_source.replace("{{adres}}", json.adres)
    html_source = html_source.replace("{{data}}", json.data)
    html_source = html_source.replace("{{protocol_rcd}}", output_html)
    return html_source


def parse_html_protokol_petli_zwarcia(json: DataProtocol, html_source):
    html_source = html_source.replace("{{miejsce_badan}}", json.miejsce_badan)
    html_source = html_source.replace("{{adres}}", json.adres)
    html_source = html_source.replace("{{data}}", json.data)
    html_source = html_source.replace("{{napiecie_sieci_zasilajacej}}", json.napiecie_sieci_zasilajacej)
    html_source = html_source.replace("{{uklad_zasilania}}", json.uklad_zasilania)

    usterki_lista: list[str] = []
    lista_petla_zwarcia: list[PetlaZwarcia] = json.petla_zwarcia

    i = 1
    for item in lista_petla_zwarcia:
        getCountIA = countIA(item)
        computedPetla = item["volt"] / getCountIA

        if type(item["pomiar"]) == float:
            if (item["pomiar"] > computedPetla):
                usterki_lista.append(str(i) + ") Lokalizacja: " + item["lokalizacja"] + ", Gniazdo nr: " + item["nr"])
                i = i + 1
        elif type(item["pomiar"]) == str:
            if (item["pomiar"] == "BU" or item["pomiar"] == "NU"):
                usterki_lista.append(str(i) + ") Lokalizacja: " + item["lokalizacja"] + ", Gniazdo nr: " + item["nr"])
                i = i + 1
    orzeczenie = """
        Pomiary impedancji pętli zwarcia spełniają wymagania normy PN-HD 60364-4-41:2017-09
        <br/><br/>
        Pomiary i próby impedancji pętli zwarciowej wykonano zgodnie z normą PN-HD 60364-6:2016-07
    """

    if (len(usterki_lista) > 0):
        orzeczenie = """
                Przeprowadzone pomiary wykazały braki skuteczności uziemienia gniazd wtykowych.<br/><br/>
                Wykaz obiektów dotyczących braku skuteczności uziemienia:
                <br/><br/>
        """
        for item in usterki_lista:
            orzeczenie += item + "<br/>"
        orzeczenie += "<br/>(wskazanie miejsc usterek w poszczególnych obiektach - patrz schematy/rysunki obiektów)"

        if (len(usterki_lista) < len(lista_petla_zwarcia)):
            orzeczenie += """<br/><br/>
                    Pozostałe pomiarowane obiekty: Pomiar impedancji pętli zwarcia spełnia wymagania normy PN-HD 60364-4-41:2017-09
                    <br/>
                    Pomiary i próby impedancji pętli zwarciowej wykonano zgodnie z normą PN-HD 60364-6:2016-07
                """

    html_source = html_source.replace("{{orzeczenie}}", orzeczenie)

    return html_source


# use for Polish signs like "ęążć itp"
def link_callback(uri, rel):
    if uri.startswith("file:///"):
        path = uri[7:]
        return path
    if uri == font_url:
        return "NotoSans-Regular.ttf"
    return uri


def create_pdf_file(html_source, file_name):
    pdf_data = BytesIO()
    pisaFileObject.getNamedFile = lambda self: self.uri

    conversion_result = pisa.CreatePDF(
        html_source, dest=pdf_data, encoding="UTF-8", link_callback=link_callback
    )

    # Check for errors
    if conversion_result.err:
        print(f"Error during PDF creation: {conversion_result.err}")
    else:
        # Write PDF to file
        with open(file_name, "wb") as f:
            f.write(pdf_data.getvalue())
        print("PDF created: " + file_name)


if __name__ == "__main__":
    #
    # E:\\POMIARY\\ELEKTRYCZNE\\schematy\\Borkowo_Mietowa\\Borkowo - Mietowa - 3.j
    # son
    with open("""E:\POMIARY\ELEKTRYCZNE\schematy\Centrum-Handlowe-Chełm\BUDYNEK_B\PELLOWSKI\zdrofit-parter--TR.json""", 'r',
              encoding='utf-8') as file:
        data = json.load(file)

    # commonData = """
    #             {
    #                 "data": "2025-08-05",
    #                 "adres": "82-300 Elbląg, Konopnickiej 2B/2",
    #                 "miejsce_badan": "Budynek wielorodzinny",
    #
    #                 "YKY_5x10_mm2": "1",
    #                 "YDYp_3x2_5mm2": "10",
    #                 "YDYp_3x1_5_mm2": "10",
    #                 "YDYp_5x2_5_mm2": "9",
    #
    #                 "petla_zwarcia":[
    #                     {
    #                         "lokalizacja":"kuchnia",
    #                         "nr":"1",
    #                         "pomiar":0.4,
    #                         "typ":"B",
    #                         "amper":32,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"kuchnia",
    #                         "nr":"2",
    #                         "pomiar":0.4,
    #                         "typ":"B",
    #                         "amper":20,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"kuchnia",
    #                         "nr":"3",
    #                         "pomiar":0.7,
    #                         "typ":"B",
    #                         "amper":25,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"kuchnia",
    #                         "nr":"4",
    #                         "pomiar":0.2,
    #                         "typ":"C",
    #                         "amper":32,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"kuchnia",
    #                         "nr":"5",
    #                         "pomiar":0.6,
    #                         "typ":"B",
    #                         "amper":16,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"Łazienka",
    #                         "nr":"6",
    #                         "pomiar":0.41,
    #                         "typ":"B",
    #                         "amper":16,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"Łazienka",
    #                         "nr":"7",
    #                         "pomiar":0.5,
    #                         "typ":"L",
    #                         "amper":16,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"Łazienka",
    #                         "nr":"8",
    #                         "pomiar":0.2,
    #                         "typ":"gF",
    #                         "amper":16,
    #                         "volt":230
    #                     },
    #                     {
    #                         "lokalizacja":"Łazienka",
    #                         "nr":"9",
    #                         "pomiar":0.8,
    #                         "typ":"gF",
    #                         "amper":16,
    #                         "volt":230
    #                     }
    #                 ],
    #
    #                 "rcd":[
    #                     {
    #                         "producent": "EATON",
    #                         "nr": "1",
    #                         "miejsce_instalacji": "Wejście",
    #                         "volt": 230,
    #                         "typ": "CFI6 25/4/003",
    #                         "amper_rcd": 25,
    #                         "amper_wywolania": 30,
    #                         "amper_wywolania_pomiar": 21,
    #                         "czas_pomiar": 23
    #                     },
    #                     {
    #                         "producent": "EATON",
    #                         "nr": "2",
    #                         "miejsce_instalacji": "I Piętro",
    #                         "volt": 230,
    #                         "typ": "CFI6 25/4/003",
    #                         "amper_rcd": 25,
    #                         "amper_wywolania": 30,
    #                         "amper_wywolania_pomiar": 21,
    #                         "czas_pomiar": 23
    #                     },
    #                     {
    #                         "producent": "EATON",
    #                         "nr": "3",
    #                         "miejsce_instalacji": "Piwnica",
    #                         "volt": 230,
    #                         "typ": "CFI6 25/4/003",
    #                         "amper_rcd": 25,
    #                         "amper_wywolania": 30,
    #                         "amper_wywolania_pomiar": 21,
    #                         "czas_pomiar": 23
    #                     },
    #                     {
    #                         "producent": "LEGRAND",
    #                         "nr": "1",
    #                         "miejsce_instalacji": "Wejście",
    #                         "volt": 400,
    #                         "typ": "10 234 25/4/003",
    #                         "amper_rcd": 25,
    #                         "amper_wywolania": 30,
    #                         "amper_wywolania_pomiar": 21,
    #                         "czas_pomiar": 23
    #                     },
    #                     {
    #                         "producent": "LEGRAND",
    #                         "nr": "2",
    #                         "miejsce_instalacji": "Wejście",
    #                         "volt": 230,
    #                         "typ": "10 234 25/4/003",
    #                         "amper_rcd": 25,
    #                         "amper_wywolania": 30,
    #                         "amper_wywolania_pomiar": 21,
    #                         "czas_pomiar": 23
    #                     }
    #                 ],
    #
    #                 "rezystancjaIzolacji":[
    #                     {
    #                         "nr": "1",
    #                         "lokalizacja": "kuchnia",
    #                         "nazwaObwodu": "YKY 5x10mm2",
    #                         "l1l2": 180,
    #                         "l2l3": 180,
    #                         "l1l3": 180,
    #                         "l1n": 180,
    #                         "l2n": 180,
    #                         "l3n": 180,
    #                         "l1l2l3n": 180,
    #                         "uwagi": "dobra"
    #                     },
    #                     {
    #                         "nr": "2",
    #                         "lokalizacja": "kuchnia",
    #                         "nazwaObwodu": "YDYp 5x2,5mm2",
    #                         "l1l2": 180,
    #                         "l2l3": 180,
    #                         "l1l3": 180,
    #                         "l1n": 180,
    #                         "l2n": 180,
    #                         "l3n": 180,
    #                         "l1l2l3n": 180,
    #                         "uwagi": "dobra"
    #                     },
    #                     {
    #                         "nr": "1",
    #                         "lokalizacja": "łazienka",
    #                         "nazwaObwodu": "YDYp 3x2,5mm2",
    #                         "l1l2": 0,
    #                         "l2l3": 0,
    #                         "l1l3": 0,
    #                         "l1n": 180,
    #                         "l2n": 0,
    #                         "l3n": 0,
    #                         "l1l2l3n": 180,
    #                         "uwagi": "dobra"
    #                     },
    #                     {
    #                         "nr": "2",
    #                         "lokalizacja": "łazienka",
    #                         "nazwaObwodu": "YDYp 3x2,5mm2",
    #                         "l1l2": 0,
    #                         "l2l3": 0,
    #                         "l1l3": 0,
    #                         "l1n": 0,
    #                         "l2n": 180,
    #                         "l3n": 0,
    #                         "l1l2l3n": 180,
    #                         "uwagi": "dobra"
    #                     },
    #                     {
    #                         "nr": "3",
    #                         "lokalizacja": "łazienka",
    #                         "nazwaObwodu": "YDYp 3x2,5mm2",
    #                         "l1l2": 0,
    #                         "l2l3": 0,
    #                         "l1l3": 0,
    #                         "l1n": 0,
    #                         "l2n": 0,
    #                         "l3n": 180,
    #                         "l1l2l3n": 180,
    #                         "uwagi": "dobra"
    #                     }
    #                 ],
    #                 "uklad_zasilania": "TN-S",
    #                 "napiecie_sieci_zasilajacej": "400V"
    #             }
    # """
    # data = json.loads(commonData)

    dr = DataProtocol(**data)

    htmlTemplate = getPdfTemplate("templates/badanie_stanu_izolacji.html")
    html_source = parse_html_protocol_badanie_izolacji(dr, htmlTemplate)
    create_pdf_file(html_source, "protokoly_pdf/badanie_stanu_izolacji_new.pdf")

    htmlTemplate = getPdfTemplate("templates/tabela_rezystancji_izolacji.html")
    html_source = parse_html_tables_izolacja(dr, htmlTemplate)
    create_pdf_file(html_source, "protokoly_pdf/tabela_rezystancji_izolacji.pdf")

    # htmlTemplate = getPdfTemplate("templates/tabela_rezystancji_izolacji.html")
    # html_source = parse_html_tables_izolacja_precise(dr, htmlTemplate)
    # create_pdf_file(html_source, "protokoly_pdf/tabela_rezystancji_izolacji_dokladna.pdf")

    htmlTemplate = getPdfTemplate("templates/tabela_pomiaru_petli_zwarcia.html")
    html_source = parse_html_tables_petla_zwarcia(dr, htmlTemplate)
    create_pdf_file(html_source, "protokoly_pdf/tabela_pomiaru_petli_zwarcia.pdf")

    htmlTemplate = getPdfTemplate("templates/protokol_rcd.html")
    html_source = parse_html_protocol_rcd(dr, htmlTemplate)
    create_pdf_file(html_source, "protokoly_pdf/badanie_wylacznika_roznicowo_pradowego.pdf")

    htmlTemplate = getPdfTemplate("templates/protokol_pomiaru_petli_zwarcia_parter.html")
    html_source = parse_html_protokol_petli_zwarcia(dr, htmlTemplate)
    create_pdf_file(html_source, "protokoly_pdf/protokol_pomiaru_petli_zwarcia_parter.pdf")

    htmlTemplate = getPdfTemplate("templates/strona_tytulowa.html")
    html_source = htmlTemplate.replace("{{adres}}", dr.adres)
    create_pdf_file(html_source, "protokoly_pdf/strona_tytulowa.pdf")
