# Ближайшие бары

Скрипт считывает из файла информацию по московским барам с сайта data.mos.ru, рассчитывая:
1. самый большой бар;
1. самый маленький бар;
1. самый близкий бар (текущие gps-координаты пользователь введет с клавиатуры).

# Как запустить

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

Запуск на Linux:

```bash

$ python bars.py <path to file> # possibly requires call of python3 executive instead of just python
```
Пример вывода:

```bash
Самый большой бар - "Спорт бар «Красная машина», Автозаводская улица, дом 23, строение 1", 450 мест

Самый маленький бар - "БАР. СОКИ, Дубравная улица, дом 34/29", 0 мест

Для нахождения ближайшего бара введите текущие gps-координатыв десятичном формате.
долгота:37.733707
широта:55.645426

Ближайший бар - "Ночной клуб «Орфей», Новочеркасский бульвар, дом 57, корпус 1", расстояние 0.57км

```
Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
