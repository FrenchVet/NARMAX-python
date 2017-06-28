# NARMAX-python

W celu uruchomienia programu należy:

1) Ściągnąć i zainstalować pythona https://www.python.org/ , najlepiej wersję 3.5; ZAZNACZYĆ ŻEBY DODAŁ ZMIENNE ŚRODOWISKOWE ORAZ ZMIENNE DO PATH - wazna rzecz
2) Ściągnąć i zainstalować jakieś IDE, polecam PyCharm Community Edition (darmowe, calkiem dobre), https://www.jetbrains.com/pycharm/?fromMenu ;
3) Zainstalować dodatkowe biblioteki (schody). Generalnie, biblioteki powinno się instalować lekko, latwo i przyjemnie z wierza poleceń. Wraz z pythonem instalujesię coś takiego jak "pip" i to się uruchamia z wiersza poleceń. Przykładowa komenda: "pip install pyqt5" i on robi resztę. Tak można zrobić z większością bibliotek, ale 2 z 4 których używam robią problemy. Dlatego, trzeba je zainstalować ręcznie. To znaczy, pobrać pliki z folderu "wheels", nie zmieniać ich nazwy, w wierszu poleceń przejśc do ich lokalizacji i uruchomić komendą "pip install scipy-19.blablabla". To śa dwie metody. W folderze są pliki dla procesora x64 i Pthona 3.5. Jesli środowisko jest inne, trzeba pobrać biblioteki z tej strony: http://www.lfd.uci.edu/~gohlke/pythonlibs/ . Proszę się nie przerażać, tu jest wszystko i to aktualne! Wobec tego, wymagane są biblioteki:

    a)PyQt5 - komenda w wierszu poleceń: "pip install pyqt5"
    b)matplotlib - komenda w wierszu poleceń: "pip install matplotlib"
    c)numpy - komenda w wierszu poleceń: "pip install numpy-1.13.0+mkl-cp35-cp35m-win_amd64.whl" lub inna paczka
    d)scipy - komenda w wierszu poleceń: "pip install scipy-0.19.1-cp35-cp35m-win_amd64.whl" lub inna paczka
    
4) Po zainstalowaniu z powodzeniem 4 bibliotek mozna uruchomić plik main.py (z IDE albo z wiersza poleceń za pomocą komendy "python main.py") i się bawić.

W razie pytań proszę dzwonić/pisać

W folderach dodalem też pliki pracy mgr oraz prezentację, ale najpewniej są one nieaktualne, chociaż praca jest już nawet.
