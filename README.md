# Jak spustit python aplikaci pomocí Docker engine

## 1. Krok
První je dobré se zamyslet, zdali je deployment dané aplikace pomocí Docker engine vhodné, většinou jde o aplikace určené pro spoštění na serverech, jako například webové aplikace, aplikace pro IoT nebo databáze, Docker není vhodný pro desktopové aplikace pro koncové uživatele, nebo pro aplikace kde je potřeba "low-level" přístup k hardwaru.
## 2. Krok - Python skript
Poté co jsme se rozhodli, že docker je ideálním řešením pro deployment, začneme přemýšlet nad "architekturou" kontejneru, například u webové aplikace:
1. ### Dependencies
Jestliže jsme využili jiné než nativní moduly pythonu, je nutné je v kontejneru nainstalovat, například modul requests nebo Flask, jde také o jiné aplikace, je li na ně skript vázán.

3. ### Síť
Webová aplikace musí být přístupná z vnějšku kontejneru, jelikož je Docker kontejner oddělený sub-systém od systému na kterém běží, je nutno manuálně zpřístupnit porty spojené s aplikací, například port 5000 pro Flask.

4. ### Uložiště
Uložiště v kontejnerech není perzistentní, a nelze se do něj dostat z vněj kontejneru, v případech, kde je potřeba ukládat data / sdílet data mezi kontejnery, musíme manuálně kontejneru zpřístupnit složky z systému, na kterém běží. 

5. ### Spouštění
Skript se spouští obdobně jako na klasické linuxové distribuci,
`python skript.py`. 


## 3. Krok složka pro aplikaci
Zdůvodu organizace si vytvoříme složku, která obsahuje všechno nutné ke spuštění aplikace. 
```
application
|
└─ skript.py
└─ Dockerfile
└─ requirements.txt
└─ .dockerignore
```

## 4. Krok Dockerfile
Dockerfile slouží jako návod pro Docker na to, jak postavit daný kontejner.

```
FROM python:3
WORKDIR

```
