import base64
import mimetypes
from pathlib import Path
from typing import Any, Dict

import google.generativeai as genai
import yaml


DEFAULT_CONFIG_PATH = Path("configs/app.yaml")


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def create_client(api_key: str) -> None:
    genai.configure(api_key=api_key)


def _build_prompt() -> str:
    return (
        "You are an invoice extraction assistant. Extract the invoice information "
        "as JSON with keys: vendor, date, total, line_items (list of {description, quantity, unit_price, line_total})."
    )


def extract_invoice_data(file_path: str, config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    config = load_config(config_path)
    api_key = config["api_key"]
    model_name = config["model"]["name"]

    create_client(api_key)
    model = genai.GenerativeModel(model_name)

    file_path_obj = Path(file_path)
    mime_type, _ = mimetypes.guess_type(file_path_obj)
    if mime_type is None:
        mime_type = "application/octet-stream"

    try:
        uploaded_file = genai.upload_file(path=str(file_path_obj))
        response = model.generate_content([_build_prompt(), uploaded_file])
        return response.text or ""
    except Exception:
        file_bytes = file_path_obj.read_bytes()
        encoded = base64.b64encode(file_bytes).decode("utf-8")
        fallback_prompt = f"{_build_prompt()}\nFile MIME type: {mime_type}\nFile (base64): {encoded}"
        response = model.generate_content(fallback_prompt)
        return response.text or ""
