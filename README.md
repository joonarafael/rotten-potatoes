# Rotten Potatoes

Koodi on englanniksi. Dokumentaatiosta osa suomeksi, osa englanniksi. En tiedä mitä olen sekoillut.

## TILANNE 22.9.

- Käyttäjän rekisteröinti ja kirjautuminen toimii
- Elokuvan lisääminen toimii

## Asennusohjeet / Installation Manual

Asennusohjeet (ENG) löytyvät [täältä](./docs/installation_manual.md "Installation Manual").

Installation Manual can be found [here](./docs/installation_manual.md "Installation Manual").

## Sovelluksen kuvaus

Sovellus on yksinkertainen ja suppea elokuvien arvosteluun tarkoitettu sivusto. Käyttäjä voi rekisteröityä ja kirjautua sisään, lisätä uusia elokuvia ja arvostella niitä (omia sekä muiden lisäämiä). Arvostelu koostuu tähtiarvosanasta 1-10 ja vapaamuotoisesta kommentista. Elokuvaa lisättäessä käyttäjän tulee kertoa elokuvan nimi & kategoria (esim. komedia, draama, toiminta, jne.).

Käyttäjä voi myös poistaa omia arvostelujaan. Omaa elokuvaa ei voi poistaa, **mikäli joku muu on arvostellut sitä**. Käyttäjä voi myös tarkastella muiden käyttäjien arvosteluja ja elokuvia. Elokuvia voi hakea otsikon perusteella ja ne voi järjestää saatujen arvostelujen mukaan.

Elokuvat jaetaan kategorioihin.

Sovelluksessa on myös superkäyttäjiä (ei rekisteröintimahdollisuutta, lisätään tietokannan luonnin yhteydessä), jotka voivat (kaikkien tavallisen käyttäjän ominaisuuksien lisäksi) poistaa mitä tahansa elokuvia ja arvosteluja. Superkäyttäjät voivat myös vaihtaa yksittäisten elokuvien nimeä ja kategoriaa.

## Tekninen toteutus

Sovellus rakennetaan _Python Flask_ -frameworkillä. Tietokantana käytetään _PostgreSQL_-tietokantaa (_Docker_-konttina).
