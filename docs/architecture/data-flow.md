# Data Flow

## Asset Manager Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Gmail     │────▶│   Review    │────▶│   Manual    │────▶│   Drive     │
│   Scanner   │     │   Queue     │     │   Finder    │     │   Uploader  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  purchases.json     Human Review        manuals/           Organized
                     (confidence <80%)    (PDFs)            Drive folders
```

## Data Formats

### Purchase Record (gmail_scanner → review_queue)

```json
{
  "id": "abc123",
  "vendor": "amazon",
  "product_name": "Samsung Refrigerator",
  "model_number": "RF28R7551SR",
  "purchase_date": "2026-01-15",
  "price": 1999.99,
  "confidence": 0.92,
  "suggested_property": "DAL",
  "suggested_category": "APPL",
  "status": "approved"
}
```

### Review Item

```json
{
  "id": "review123",
  "type": "purchase",
  "created_at": "2026-01-15T12:00:00Z",
  "data": { ... },
  "status": "pending"
}
```

### Manual Result

```json
{
  "purchase_id": "abc123",
  "manual_url": "https://...",
  "manual_path": "/path/to/manual.pdf",
  "source": "manufacturer",
  "confidence": 0.9
}
```

## Confidence Routing

```
Confidence Score
       │
       ▼
   ┌───────┐
   │ ≥ 80% │───▶ Auto-approved
   └───────┘
       │
       ▼
   ┌───────┐
   │ < 80% │───▶ Review Queue ───▶ Human Decision
   └───────┘
```

## Storage Locations

| Data | Location |
|------|----------|
| OAuth Token | `~/.config/treehouse/token.json` |
| Review Queue | `~/.config/treehouse/review_queue.json` |
| Archive | `~/.config/treehouse/review_queue_archive.json` |
| Logs | `~/.config/treehouse/logs/` |
| Manuals (local) | `./manuals/` |
| Manuals (cloud) | Google Drive `Treehouse-Assets/` |
