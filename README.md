# Przenoszenie danych z bazy danych PostgreSQL do MySQL
## Problem
Za pomocą [starego projektu](https://github.com/Isdre/Tworzenie_bazy_z_losowymi_danymi) wygenerowałem 2 tablice do bazy danych PostgreSQL.
Niestety popełniłem parę błędów:
  - id nie jest typem serial. Jest integerem, więc wygenerowało też wartości ujemne
  - nie potrzebuje 2 tablic, starczyła by na te dane 1
  - skróciłbym wartości dla kolumn city i country

Dane w czasie ekstrackji są zapisywane do plików [test_0.csv](https://github.com/Isdre/From_PostgreSQL_To_MySQL/blob/master/test_0.csv) i [test_1.csv](https://github.com/Isdre/From_PostgreSQL_To_MySQL/blob/master/test_1.csv)
## Rozwiązanie
W skryptcie [connect.py](https://github.com/Isdre/From_PostgreSQL_To_MySQL/blob/master/connect.py) i notebooku [transform](https://github.com/Isdre/From_PostgreSQL_To_MySQL/blob/master/transform.ipynb)
znajduje się pierwsze rozwiązanie na ten problem, ale uznałem, że można to zrobić w 1 skryptcie, aby było czytelniejsze i wystarczyło wywołać komende.

Potem powstał [main.py](https://github.com/Isdre/From_PostgreSQL_To_MySQL/blob/master/main.py)
Opis funckcji:
- extract
  - wczytuje dane z bazy danych, dla każdej tablicy tworzy oddzielny DataFrame oraz plik .csv.
  - Zwraca list[DataFrame]
- transform
  - usuwa kolumne "id"
  - zmienia nazwę indeksu na "id"
  - zmienia typ kolumny "salary" na decimal[2]
  - zmiania wielkość liter oraz skraca nazwy w kolumnach "city" i "country"
  - Zwraca dane połaczone w 1 DataFrame
- load
  - dodaje do bazy danych mysql tablice 
