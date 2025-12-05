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


class Rcd:
    def __init__(self,producent: str, nr: str, miejsce_instalacji: str, volt: int,
                 typ: str, amper_rcd: int, amper_wywolania: int, amper_wywolania_pomiar: int, czas_pomiar: int):
        self.producent = producent
        self.nr = nr
        self.miejsce_instalacji = miejsce_instalacji
        self.volt = volt
        self.typ = typ
        self.amper_rcd = amper_rcd
        self.amper_wywolania = amper_wywolania
        self.amper_wywolania_pomiar = amper_wywolania_pomiar
        self.czas_pomiar = czas_pomiar


class PetlaZwarcia:
    def __init__(self,lokalizacja: str, nr: str, pomiar: float | str, typ:str, amper: int, volt: int):
        self.lokalizacja = lokalizacja
        self.nr = nr
        self.pomiar = pomiar
        self.typ = typ
        self.amper = amper
        self.volt = volt


class DataProtocol:
    def __init__(self,data: str,adres: str, miejsce_badan: str, YKY_5x10_mm2: str, YDYp_3x2_5mm2: str, YDYp_3x1_5_mm2: str, YDYp_5x2_5_mm2: str,
                 petla_zwarcia: list[PetlaZwarcia], rcd: list[Rcd], rezystancjaIzolacji: list[RezystancjaIzolacji],uklad_zasilania: str, napiecie_sieci_zasilajacej: str):
        self.data = data
        self.adres = adres
        self.miejsce_badan = miejsce_badan
        self.YKY_5x10_mm2 =YKY_5x10_mm2
        self.YDYp_3x2_5mm2=YDYp_3x2_5mm2
        self.YDYp_3x1_5_mm2=YDYp_3x1_5_mm2
        self.YDYp_5x2_5_mm2=YDYp_5x2_5_mm2
        self.petla_zwarcia = petla_zwarcia
        self.rcd = rcd
        self.rezystancjaIzolacji = rezystancjaIzolacji
        self.uklad_zasilania = uklad_zasilania
        self.napiecie_sieci_zasilajacej = napiecie_sieci_zasilajacej
