# Arbitium

**API backend para arbitraje de criptomonedas**

## 📖 Descripción

Arbitium es una API desarrollada en Python y FastAPI que:

- Obtiene precios de distintos exchanges (Binance, Kraken, KuCoin).
- Calcula oportunidades de arbitraje con umbral configurable.
- Ejecuta órdenes de mercado automáticamente cuando se cumple un umbral de probabilidad.
- Persiste snapshots de precios, oportunidades y trades en MongoDB.
- Envía notificaciones vía Telegram.

## ⚙️ Requisitos

- Python 3.8+
- MongoDB
- (Opcional) Docker y Docker Compose

## 🚀 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Aced10/arbitium.git
   cd arbitium/backend
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Renombra y configura variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env y asigna tus claves y tokens
   ```
5. Inicia la aplicación:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🔧 Variables de entorno

Define en `.env`:

```dotenv
# Símbolos a monitorear (separados por comas)
SYMBOLS=BTC/USDT,ETH/USDT,SOL/USDT
# Umbral mínimo de beneficio (%)
MIN_PROFIT=0.3

# Clave de autenticación API para endpoints protegidos\ nAPI_KEY=tu_api_key_secreta

# API Keys de exchanges\ nBINANCE_API_KEY=...
BINANCE_SECRET=...
KRAKEN_API_KEY=...
KRAKEN_SECRET=...
KUCOIN_API_KEY=...
KUCOIN_SECRET=...

# MongoDB\ nMONGODB_URI=mongodb://usuario:pass@host:puerto/db

# Telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

## 📂 Estructura del proyecto

```
arbitium/
├── backend/
│   ├── app/
│   │   ├── core/            # Config, DB, seguridad, scheduler
│   │   ├── routers/         # Rutas FastAPI (prices, opportunities, execute)
│   │   ├── services/        # Lógica de negocio y persistencia
│   │   ├── ml/              # Entrenamiento y modelo de ML (opcional)
│   │   └── main.py          # Punto de entrada FastAPI
│   ├── model/               # Modelos y artefactos ML (scaler.pkl, .h5)
│   ├── requirements.txt     # Dependencias de producción
│   ├── requirements-dev.txt # Dependencias de desarrollo (linters, tests)
│   ├── .env.example         # Ejemplo de variables de entorno
│   └── Dockerfile           # Opcional, para contenerizar
├── docs/                    # Documentación adicional (arquitectura, diagramas)
│   └── architecture.md      
├── .gitignore               # Archivos y carpetas ignorados por Git
├── docker-compose.yml       # Orquestación de servicios (MongoDB, app)
└── README.md                # Este archivo
```

## 🤝 Contribuciones

1. Haz fork de este repositorio.
2. Crea una rama con tu mejora: `git checkout -b feature/nombre`.
3. Realiza tus cambios y commitea: `git commit -m "feat: descripción breve"`.
4. Envía tu pull request y pasa el pipeline de CI.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

