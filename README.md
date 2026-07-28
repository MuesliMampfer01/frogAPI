# 🐸 FrogAPI

Eine modulare REST-API, entwickelt in **FastAPI**, die exklusiv als Microservice für meinen privaten Discord-Bot [BabyBirneBot](https://github.com/MuesliMampfer01/BabyBirneBot) betrieben wird. Die API läuft als Container auf einem Raspberry Pi Server und stellt Backend-Dienste wie Bildauslieferung, System-Monitoring und Wetterdaten bereit.

---

## 🏗️ Architektur & Design

Die Anwendung setzt auf eine **modulare Router-Architektur**, um zukünftige Erweiterungen sauber voneinander zu trennen. Das Projekt läuft vollständig gekapselt in Docker-Containern und kommuniziert isoliert über ein internes Docker-Netzwerk ausschließlich mit dem Discord-Bot.

```text
frogapi/
│
├── main.py              # Startpunkt & Router-Zusammenführung
├── Dockerfile           # Build-Konfiguration (inkl. System-Abhängigkeiten)
├── requirements.txt     # Python-Pakete
│
└── routers/             # Modulare Endpunkte
    ├── __init__.py      # Python-Modul-Initialisierung
    └── <feature>.py     # Die jeweiligen Endpunkte
```

---

## 🚀 Kernfunktionen (Endpoints)

| Modul | Endpoint | Methode | Beschreibung |
| --- | --- | --- | --- |
| **Frösche** | `/frogs/random` | `GET` | Liefert ein zufälliges Froschbild aus dem lokalen Storage-Verzeichnis aus. |
| **System** | `/system/stats` | `GET` | Liest via `psutil` Live-Daten des Hosts aus (CPU-Auslastung, RAM-Status, Uptime). |
| **Wetter** | `/weather?city=...` | `GET` | Agiert als Microservice: Übersetzt einen Städtenamen in Koordinaten und holt Wetterdaten von Open-Meteo. |

---

## 🔒 Security & Deployment

* **Netzwerk-Isolierung:** Die API ist nach außen hin nicht exponiert. Der Zugriff erfolgt ausschließlich intern über ein dediziertes Docker-Netzwerk (`shared-frog-net`), an das auch der Discord-Bot gebunden ist.
* **Volume-Mapping:** Bilder und persistente Daten werden sauber über Docker-Volumes auf das Host-System des Raspberry Pis gespiegelt.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python 3.10-slim)
* **Software-Server:** Uvicorn
* **Monitoring:** `psutil`
* **HTTP Client:** `aiohttp` (für asynchrone API-Abfragen)
* **Containerization:** Docker & Docker Compose
