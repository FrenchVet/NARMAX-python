# NARMAX-python

W celu uruchomienia programu należy:

1) Ściągnąć i zainstalować pythona https://www.python.org/ , najlepiej wersję 3.5; ZAZNACZYĆ ŻEBY DODAŁ ZMIENNE ŚRODOWISKOWE ORAZ ZMIENNE DO PATH - wazna rzecz
2) Ściągnąć i zainstalować jakieś IDE, polecam PyCharm Community Edition (darmowe, calkiem dobre), https://www.jetbrains.com/pycharm/?fromMenu ;
3) Zainstalować dodatkowe biblioteki (schody). Generalnie, biblioteki powinno się instalować lekko, latwo i przyjemnie z wierza poleceń. Wraz z pythonem instalujesię coś takiego jak "pip" i to się uruchamia z wiersza poleceń. Przykładowa komenda: "pip install pyqt5" i on robi resztę. Tak można zrobić z większością bibliotek, ale akurat 2 z 4 których używam robią problemy. Dlatego, resztę trzeba zainstalować ręcznie. Najpierw trzeba pobrać odpowiednie pliki ze strony http://www.lfd.uci.edu/~gohlke/pythonlibs/ (Proszę się nie przerażać, tu jest wszystko dobre i aktualne!) adekwatne do używanej wersji pythona i architektury procesora. Następnie po ściągnięciu odpowiedniego pliku, uruchomić pipa z wiersza poleceń komendą "pip install nazwa_paczki" znajdując się oczywiście w folderze gdzie jest paczka. Wrzuciłbym je tutaj, ale są za duże i github się pluje, bo mają więcej niż 25mb. Wobec tego, wymagane są biblioteki:

    a)PyQt5 - komenda w wierszu poleceń: "pip install pyqt5"
    b)matplotlib - komenda w wierszu poleceń: "pip install matplotlib"
    c)numpy+mkl - komenda w wierszu poleceń: "pip install numpy-1.13.0+mkl-cp35-cp35m-win_amd64.whl" lub inna paczka
    d)scipy - komenda w wierszu poleceń: "pip install scipy-0.19.1-cp35-cp35m-win_amd64.whl" lub inna paczka
    
4) Po zainstalowaniu z powodzeniem 4 bibliotek mozna uruchomić plik main.py (z IDE albo z wiersza poleceń za pomocą komendy "python main.py") i się bawić.

W razie pytań proszę dzwonić/pisać

W folderach dodalem też pliki pracy mgr oraz prezentację, ale najpewniej są one nieaktualne, chociaż praca jest już nawet.
