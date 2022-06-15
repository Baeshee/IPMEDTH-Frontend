# IPMEDTH-Frontend

Eerste variant, dit is puur de basis nog niet alle pagina's verwerkt.

## Pagina's
1. Home (indien ingelogd)
2. Meting (komt de OpenCV + Mediapipe dingen)
3. Resultaten (PD dataframe van alle resultaten)
4. Login (eerste pagina indien niet ingelogd)

## Development

### Packages benodigd

- PyQt5 (heeft wat betere run-time dan 5)
- functools (indien je deze nog niet standaard geinstalleerd hebt)

### Omgeving opzetten

1. Clone the repository
2. Maak een virtual environment aan en activeer deze
```py
python3 -m venv venv
source venv/bin/activate
```
3. Installeer de benodigde packages met `pip install -r requirements.txt`

**Note:** PyQt5 kan niet omgaan met runnen vanaf een VPS.