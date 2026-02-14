# Gemini Invoice Parser

This repository contains a minimal project structure for extracting invoice data with the Gemini API and normalizing it into a fixed JSON schema.

## Project Structure

```
configs/
  app.yaml
src/
  gemini_client.py
  invoice_parser.py
tests/
```

## Configuration

Update `configs/app.yaml` with your Gemini API key and settings:

```yaml
api_key: "YOUR_GEMINI_API_KEY"
model:
  name: "gemini-1.5-pro"
  region: "us-central1"
timeouts:
  request_seconds: 60
  upload_seconds: 120
```

## Usage

Install dependencies:

```bash
pip install google-generativeai pyyaml
```

Extract invoice data and normalize it:

```python
from src.gemini_client import extract_invoice_data
from src.invoice_parser import normalize_invoice_output

raw_text = extract_invoice_data("/path/to/invoice.pdf")
invoice = normalize_invoice_output(raw_text)
print(invoice)
```

### Example Output

```json
{
  "vendor": "ACME Supplies",
  "date": "2024-01-31",
  "total": "1520.25",
  "line_items": [
    {
      "description": "Printer paper",
      "quantity": 10,
      "unit_price": "12.50",
      "line_total": "125.00"
    }
  ]
}
```
