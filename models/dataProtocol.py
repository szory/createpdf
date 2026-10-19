from enum import Enum


class RezystancjaIzolacji:
    def __init__(self, nr: str, lokalizacja: str, nazwaObwodu:str, l1l2: int, l2l3: int, l1l3: int, l1n: int, l2n: int, l3n: int, l1l2l3n: int,
                 uwagi: str):
        self.nr = nr
        self.lokalizacja = lokalizacja
        self.nazwaObwodu = nazwaObwodu
        self.l1l2 = l1l2
        self.l2l3 = l2l3
        self.l1l3 = l1l3
        self.l1n = l1n
        self.l2n = l2n
        self.l3n = l3n
        self.l1l2l3n = l1l2l3n
        self.uwagi = uwagi

class TypPrzewodu(Enum):
    # nazwa = klucz używany w pliku JSON, wartość = nazwa wyświetlana w protokole
    YAKXS_5x120_mm2 = "YAKXS 5x120 mm2"
    YAKXS_4x70_mm2 = "YAKXS 4x70 mm2"
    YAKXS_4x50_mm2 = "YAKXS 4x50 mm2"
    YAKXS_5x25_mm2 = "YAKXS 5x25 mm2"
    YKY_4x25_mm2 = "YKY 4x25 mm2"
    YKY_4x10_mm2 = "YKY 4x10 mm2"
    YKY_5x10_mm2 = "YKY 5x10 mm2"
    OWY_5x6_mm2 = "OWY 5x6 mm2"
    YDY_5x16_mm2 = "YDY 5x16 mm2"
    YDY_5x10_mm2 = "YDY 5x10 mm2"
    YDY_5x6_mm2 = "YDY 5x6 mm2"
    YDY_3x6_mm2 = "YDY 3x6 mm2"
    YDY_5x4_mm2 = "YDY 5x4 mm2"
    YDY_3x4_mm2 = "YDY 3x4 mm2"
    YDY_3x2_5_mm2 = "YDY 3x2,5 mm2"
    YDYp_3x2_5mm2 = "YDYp 3x2,5 mm2"
    YDYp_5x2_5_mm2 = "YDYp 5x2,5 mm2"
    YDYp_4x2_5_mm2 = "YDYp 4x2,5 mm2"
    YDYp_3x2_5_mm2 = "YDYp 3x2,5 mm2"
    YDYp_3x1_5_mm2 = "YDYp 3x1,5 mm2"
    YDYp_2x2_5_mm2 = "YDYp 2x2,5 mm2"
    YDYp_2x1_5_mm2 = "YDYp 2x1,5 mm2"

    # aliasy - zapis bez "_" przed mm2 używany w starszych plikach JSON
    YKY_4x25mm2 = "YKY 4x25 mm2"
    YDY_3x2_5mm2 = "YDY 3x2,5 mm2"
    YDYp_3x1_5mm2 = "YDYp 3x1,5 mm2"
    YDYp_5x2_5mm2 = "YDYp 5x2,5 mm2"


    @property
    def ile_zyl(self) -> int:
        # "YDYp 3x2,5 mm2" -> 3
        return int(self.value.split()[1].split("x")[0])


def wczytaj_przewody(przewody: dict | None, stare_przewody: dict) -> dict[TypPrzewodu, int]:
    # przewody: {"YDYp_3x2_5_mm2": "10"} lub {"YDYp 3x2,5 mm2": "10"}
    # stare_przewody: przewody podane jako osobne klucze (stary format JSON)
    wynik: dict[TypPrzewodu, int] = {}
    for nazwa, ilosc in {**(przewody or {}), **stare_przewody}.items():
        if nazwa in TypPrzewodu.__members__:
            typ = TypPrzewodu[nazwa]
        else: typ = TypPrzewodu(nazwa)

        if int(ilosc) > 0:
            wynik[typ] = wynik.get(typ, 0) + int(ilosc)
    return wynik


class RezystancjaIzolacjiMieszkania:
    def __init__(self, nr: str, miejsce_instalacji: str, ileFaz: str = "1",
                 przewody: dict[str, str] | None = None, **stare_przewody: str):
        self.nr = nr
        self.miejsce_instalacji = miejsce_instalacji
        self.ileFaz = ileFaz
        self.przewody = wczytaj_przewody(przewody, stare_przewody)

class Rcd:
    def __init__(self,producent: str, nr: str, miejsce_instalacji: str, volt: int,
                 typ: str, amper_rcd: int, amper_wywolania: int, amper_wywolania_pomiar: int, czas_pomiar: int,usterki: "brak"):
        self.producent = producent
        self.nr = nr
        self.miejsce_instalacji = miejsce_instalacji
        self.volt = volt
        self.typ = typ
        self.amper_rcd = amper_rcd
        self.amper_wywolania = amper_wywolania
        self.amper_wywolania_pomiar = amper_wywolania_pomiar
        self.czas_pomiar = czas_pomiar
        self.usterki = usterki



class PetlaZwarcia:
    def __init__(self,lokalizacja: str, nr: str, pomiar: float | str, typ:str, amper: int, volt: int):
        self.lokalizacja = lokalizacja
        self.nr = nr
        self.pomiar = pomiar
        self.typ = typ
        self.amper = amper
        self.volt = volt


class DataProtocol:
    def __init__(self,data: str,adres: str, miejsce_badan: str,
                 petla_zwarcia: list[PetlaZwarcia], rcd: list[Rcd], rezystancjaIzolacji: list[RezystancjaIzolacji],uklad_zasilania: str, napiecie_sieci_zasilajacej: str,
                 rezystancjaIzolacjiMieszkania: list[dict]=[],ileFaz: str= "3",
                 przewody: dict[str, str] | None = None, **stare_przewody: str):
        self.data = data
        self.adres = adres
        self.miejsce_badan = miejsce_badan
        self.przewody = wczytaj_przewody(przewody, stare_przewody)
        self.petla_zwarcia = petla_zwarcia
        self.rcd = rcd
        self.rezystancjaIzolacji = rezystancjaIzolacji
        self.uklad_zasilania = uklad_zasilania
        self.napiecie_sieci_zasilajacej = napiecie_sieci_zasilajacej
        self.rezystancjaIzolacjiMieszkania = [RezystancjaIzolacjiMieszkania(**m) for m in rezystancjaIzolacjiMieszkania]
        self.ileFaz = ileFaz
