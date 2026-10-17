% Pylint raportti

Pylint antoi seuraavan raportin sovelluksesta:


************* Module app
app.py:64:0: C0301: Line too long (104/100) (line-too-long)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:1:0: C0410: Multiple imports on one line (datetime, math) (multiple-imports)
app.py:10:0: C0410: Multiple imports on one line (decks, users) (multiple-imports)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:55:0: R0911: Too many return statements (7/6) (too-many-return-statements)
app.py:55:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:109:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:116:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:176:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:201:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:217:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:243:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:259:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:267:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:279:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:293:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:300:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:310:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:317:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:336:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:350:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:363:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:370:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:377:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:395:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:408:0: C0116: Missing function or method docstring (missing-function-docstring)

## Docstring ilmoitukset
Sovelluksen kehityksessä tehty tietoisesti päätös, ettei käytetä docstring-kommentteja

## Import-ilmoitukset
Multiple imports on one line
Importit joissa useampi samalla rivillä ovat käyttötarkoitukseltaan samankaltaisia esim datetime ja math. decks, users ja config ovat projektin omia moduuleja.

## Liian pitkä rivi
Sovelluksessa on yksi if rivi joka on pitkä, mutta ei mielestäni mahdottoman pitkä, joten en muuttanut sitä

## Too many return statements
En muuttanut tätä, koska return jokaisen poikkeuksen kohdalla selvensi itselleni sitä missä kohtaa pitää palauttaa mitäkin.
