# Flashcards

##Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan korttipakkoja.
* Käyttäjä pystyy lisäämään kortteja korttipakkoihin (kortit sisältää kysymyksen ja vastauksen)
* Käyttäjä näkee sovellukseen lisätyt korttipakat.
* Käyttäjä pystyy etsimään korttipakkoja hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät korttipakat.
* Käyttäjä pystyy valitsemaan korttipakalle yhden tai useamman luokittelun (esim. kielet, termit, kuva/sana yhteydet).
* Toissijaiseksi tietokohteeksi käyttäjät pystyvät lisäämään pakkoihin arvostelun.

##Ohjeet sovelluksen testaamiseen
Asenna virtuaaliympäristö:
$ python3 -m venv venv

Käynnistä virtuaaliympäristö:
$ source venv/bin/activate

Asenna flask-kirjasto:
$ pip install flask

luo tietokanta:
$ sqlite3 database.db < schema.sql

käynnistä sovellus:
$ flask run

Luo käyttäjä tai useampi ja kokeile lisätä, muokata ja poistaa tietokohteita
