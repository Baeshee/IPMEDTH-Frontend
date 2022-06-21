# IPMEDTH-Frontend

Een uitgewerkte versie van de handbogen applicatie voor het IPMEDTH project in opdracht van Revalidatie Friesland.

## Pagina's
1. Home (indien ingelogd)
2. Meting (maakt gebruik van OpenCV + Mediapipe)
3. Resultaten (PD dataframe van alle resultaten)
4. Login (eerste pagina indien niet ingelogd)

## Development

### Packages benodigd

- PyQt5 (heeft wat betere run-time dan 6)
- functools (indien je deze nog niet standaard geinstalleerd hebt)

### Omgeving opzetten

1. Clone the repository
2. Maak een virtual environment aan en activeer deze
```py
python3 -m venv venv
source venv/bin/activate
```
3. Installeer de benodigde packages met `pip install -r requirements.txt`

#### Gebruik van pre-commit

Dit project bied de optie om gebruik te maken van pre-commit, zodat elke commit eerst wordt gechecked voor code-review alvorens deze wordt doorgezet.

Binnen je virtual environment kun je deze commando gebruiken om het te installeren:

```bash
pre-commit install
```

Wil je tussentijds een volledige check uitvoeren:

```bash
pre-commit run --all-files
```

**Note:** PyQt5 kan niet omgaan met runnen vanaf een VPS.
