# Flashcards

##Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan korttipakkoja.
* Käyttäjä pystyy lisäämään kortteja korttipakkoihin (kortit voi sisältää tekstiä ja kuvia)
* Käyttäjä näkee sovellukseen lisätyt korttipakat.
* Käyttäjä pystyy etsimään korttipakkoja hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät korttipakat.
* Käyttäjä pystyy valitsemaan korttipakalle yhden tai useamman luokittelun (esim. kielet, termit, kuva/sana yhteydet).
* Toissijaiseksi tietokohteeksi käyttäjät pystyvät lisäämään pakkoihin arvostelun.

##Ohjeet sovelluksen testaamiseen
Asenna flask-kirjasto:
$ pip install flask

luo tietokanta:
$ sqlite3 database.db < schema.sql

käynnistä sovellus:
$ flask --app app run

Luo käyttäjä tai useampi ja kokeile lisätä tietokohteita