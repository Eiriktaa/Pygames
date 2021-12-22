from os import name
from sau import Sau
from spillbrett import Spillbrett
from sauehjerne import Sauehjerne
from gress import Gress


def test_avstand():
    brett = Spillbrett(3000)
    sauen = Sau("sau", 400, 500, brett)
    gresset = Gress("gress", 100, 100)

    test_fail = "Fail: avstanden er feil"
    t1 = sauen.sauehjerne().avstand_til_objekt(gresset)
    assert t1 == 14, test_fail

    sauen = Sau("sau", 100, 100, brett)
    gresset = Gress("gress", 100, 100)
    t2 = sauen.sauehjerne().avstand_til_objekt(gresset)
    assert t2 == 0, test_fail

    sauen = Sau("sau", 400, 100, brett)
    gresset = Gress("gress", 100, 100)
    t3 = sauen.sauehjerne().avstand_til_objekt(gresset)
    assert t3 == 6, test_fail

    print("Pass: Test_avstand")


def test_retning():
    brett = Spillbrett(3000)
    sauen = Sau("sau", 400, 500, brett)
    gress1 = Gress("gress", 100, 100)
    gress2 = Gress("gress", 450, 500)
    gress3 = Gress("gress", 300, 600)

    t1 = sauen.sauehjerne().retninger_mot_objekt(gress1)
    t2 = sauen.sauehjerne().retninger_mot_objekt(gress2)
    t3 = sauen.sauehjerne().retninger_fra_objekt(gress3)

    assert all(elem in ["opp", "venstre"] for elem in t1)
    assert "hoeyre" in t2
    assert all(elem in ["opp", "hoeyre"] for elem in t3)

    print("Pass: Test_retning")


def main_test():
    test_avstand()
    test_retning()


if __name__ == "__main__":
    main_test()
