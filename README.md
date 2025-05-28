```markdown
# Parapente Tracker (Flask)

App Dockerizada para rastrear parapentistas en tiempo real en Parapente Paraíso (Cundinamarca, Colombia).

## Características
- Recibe datos por Webhook/API REST
- Muestra ubicación en mapa (Leaflet)
- Panel lateral con nombres y siguientes vuelos
- Sin base de datos: almacenamiento en JSON

## Ejecutar localmente
```bash
docker compose up --build
```

## Endpoints

### POST `/webhook/location`
```json
{
  "id": "gps123",
  "lat": 4.80012,
  "lng": -74.40612,
  "alt": 2400,
  "accuracy": 5
}
```

### POST `/webhook/nombre`
```json
{
  "id": "gps123",
  "nombre": "Carlos Pérez",
  "siguientes": ["Lucía Gómez", "Mateo Torres"]
}
```

### GET `/data`
Retorna el estado completo:
```json
{
  "parapentistas": { "gps123": { ... } },
  "cola": ["Lucía Gómez"]
}
```

## Despliegue en Easypanel
1. Sube este repositorio a GitHub
2. Crea aplicación Docker en Easypanel apuntando a este repo
3. Expón el puerto `8000`
4. Agrega volumen persistente para `data/`

---

Licencia MIT
```
