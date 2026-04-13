# Jak spustit python aplikaci pomocí Docker engine
Tento krátký návod na příkladu jednoduché webové aplikace popisuje postup deploymentu aplikace pomocí Docker engine
## 1. Krok
První je dobré se zamyslet, zdali je deployment dané aplikace pomocí Docker engine vhodné, většinou jde o aplikace určené pro spoštění na serverech, jako například webové aplikace, aplikace pro IoT nebo databáze, Docker není vhodný pro desktopové aplikace pro koncové uživatele, nebo pro aplikace kde je potřeba "low-level" přístup k hardwaru a vysoký výkon.
## 2. Krok - Python skript
Poté co jsme se rozhodli, že docker je ideálním řešením pro deployment, začneme přemýšlet nad "architekturou" kontejneru, například u webové aplikace:
1. ### Dependencies
Jestliže jsme využili jiné než nativní moduly pythonu, je nutné je v kontejneru nainstalovat, například modul requests nebo Flask, jde také o jiné aplikace, je li na ně skript vázán.

3. ### Síť
Webová aplikace musí být přístupná z vnějšku kontejneru, jelikož je Docker kontejner oddělený sub-systém od systému na kterém běží, je nutno manuálně zpřístupnit porty spojené s aplikací, například port 5000 pro Flask.

4. ### Uložiště
Uložiště v kontejnerech není perzistentní, a nelze se do něj dostat z vněj kontejneru, v případech, kde je potřeba ukládat data / sdílet data mezi kontejnery, musíme manuálně kontejneru zpřístupnit složky z systému, na kterém běží. 

5. ### Spouštění
Skript se spouští podobně jako na klasické linuxové distribuci,
```python skript.py``` 
hlavním rozdílem je formát zapisování
```CMD ["python","skript.py"]```
řádek CMD v Dockerfile určuje příkazy spouštěny, až po spuštění kontejneru pomocí `docker run`.


## 3. Krok složka pro aplikaci
Zdůvodu organizace si vytvoříme složku, která obsahuje všechno nutné ke spuštění aplikace. 
```
src
|
└─ skript.py
└─ Dockerfile
└─ requirements.txt
└─ .dockerignore
```

## 4. Krok Dockerfile
Dockerfile slouží jako návod pro Docker na to, jak postavit daný kontejner.

```
FROM python:3-alpine # využijeme předlohu alpine, ma menší velikost

WORKDIR /usr/src/app # umístění aplikace v kontejneru

# instalace python modulů pomocí pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

# kopírování všech souborů ve složce do WORKDIR 
COPY . .

# spuštění python skriptu
CMD [ "python", "app.py" ]
```

## 5. Krok sestavení docker image
Pomocí dockerfile vytvoříme spustitelný image a uložíme jej pod jménem *aplikace*, Docker hledá Dockerfile ve složce /src.
```
sudo docker build -t aplikace src/.
```


## 5. Krok spuštění Docker kontejneru
Po sestavení Docker image lze aplikaci spustit následujícím příkazem, do něj vložíme název, pod kterým jsme si uložili image, tedy *aplikace*.
```
sudo docker run -it -p 5000:5000 -v "$PWD/data:/usr/src/app/volume" aplikace
```
Po spuštění se můžeme pomocí webového prohlížeče připojit na adresu localhost:5000, která obsahuje webobou aplikaci zobrazující nadpis a data obsažená v souboru data.txt. Nyní je na čase porozumět samotnému spouštěcímu příkazu, hlavními parametry jsou `-p` a `-v`. Parametr -p zajišťuje konektivitu mezi vnitřní sítí Docker engine a hostovským systémem, zapisuje se ve formátu ```-p <vnější port>:<vnitřní port>``` tedy ```-p 5000:5000``` znamená, že port 5000 je přístupný z hostovského zařízení, port lze také měnit například `88:5000`, pokud chceme, aby port 5000 byl přístupný z portu 80.
```
sudo docker run
-it                                # terminálový výstup, pokud chceme oddělit od terminálu, využijeme -d
-p 5000:5000                       # zpřístupnění portu 5000
-v "$PWD/data:/usr/src/app/volume" # připojení složky z hostovského zařízení do kontejneru
aplikace                           # název image, který chceme spustit, vždy až na konci příkazu
```
Parametr -v značí Docker volume, jednoduše řečeno, složku z hostovského zařízení zpřístupníme kontejneru, naší aplikaci, zapisuje se ve formátu ```-v <složka na host zařízení>:<složka v kontejneru>``` v našem případě zpřistupňujeme data ve složce `/data` v tomto repozitáři, do složky WORKDIR, neboli `/usr/src/app/volume`, do které má python skript přístup
```-v "$PWD/data:/usr/src/app/volume```
v tomto případě důležité je využití proměnné `$PWD`, která obsahuje informaci "od kud spouštíme příkaz", vyhneme se tím potřeby zadávat absolutní cestu ke složce. 


## 6. Krok aplikace spuštěna
Tímto jste ůspěšně spustili aplikaci pomocí Docker engine, v případě dotazů, dodatků nebo problému mě neváhejte kontaktovat pomocí emailu, dále dávám k dispozici pár odkazů:
## Zdroje

- [Docker Get Started](https://docs.docker.com/get-started/)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker volumes](https://docs.docker.com/storage/volumes/)
- [Python documentation](https://docs.python.org/3/)
- [Flask documentation](https://flask.palletsprojects.com/en/latest/)
- [pip requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/)



