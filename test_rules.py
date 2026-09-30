from rules import qualify, SCENARIOS


def arts(flags):
    return [f.article for f in qualify(flags).findings]


def test_ransomware():
    assert arts(SCENARIOS["Атака шифровальщика-вымогателя"]) == ["205", "206", "210", "194"]


def test_site_hack():
    assert arts(SCENARIOS["Взлом сайта"]) == ["205", "206"]


def test_phishing():
    assert arts(SCENARIOS["Фишинг"]) == ["205", "190"]


def test_no_intent():
    v = qualify({"access", "data_damaged"})
    assert not v.criminal


def test_no_signs():
    assert not qualify({"intent"}).criminal


def test_ddos():
    assert arts({"intent", "disruption"}) == ["207"]


def test_qualifiers():
    v = qualify({"intent", "access", "group", "official"})
    assert len(v.qualifiers) == 2


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)
