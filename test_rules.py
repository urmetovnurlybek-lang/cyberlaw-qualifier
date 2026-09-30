"""Тесттер: үш сценарий және шекаралық жағдайлар."""
from rules import qualify, SCENARIOS


def arts(flags):
    """Белгілер жиыны бойынша баптардың тізімін қайтарады."""
    return [f.article for f in qualify(flags).findings]


def test_ransomware():
    """Шифрлаушы-бопсалаушы шабуылы: 205, 206, 210, 194."""
    assert arts(SCENARIOS["Шифрлаушы-бопсалаушы шабуылы"]) == ["205", "206", "210", "194"]


def test_site_hack():
    """Сайтты бұзу: 205, 206."""
    assert arts(SCENARIOS["Сайтты бұзу"]) == ["205", "206"]


def test_phishing():
    """Фишинг: 205, 190."""
    assert arts(SCENARIOS["Фишинг"]) == ["205", "190"]


def test_no_intent():
    """Қасақаналық жоқ - қылмыстық құрам жоқ."""
    v = qualify({"access", "data_damaged"})
    assert not v.criminal


def test_no_signs():
    """Тек қасақаналық - басқа белгілер жоқ."""
    assert not qualify({"intent"}).criminal


def test_ddos():
    """DDoS шабуылы: 207."""
    assert arts({"intent", "disruption"}) == ["207"]


def test_qualifiers():
    """Квалификациялаушы белгілер: топтық + қызметтік."""
    v = qualify({"intent", "access", "group", "official"})
    assert len(v.qualifiers) == 2


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)
