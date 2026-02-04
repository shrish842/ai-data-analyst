import io
from pathlib import Path
import pandas as pd


# -------------------------
# Format sniffing
# -------------------------
def _looks_like_csv(raw: bytes) -> bool:
    """
    Heuristic check to identify CSV-like content.
    """
    try:
        sample = raw[:1024].decode(errors="ignore")
        return "," in sample and "\n" in sample
    except Exception:
        return False


# -------------------------
# Robust CSV reader
# -------------------------
def _read_csv_robust(buffer: io.BytesIO) -> pd.DataFrame:
    """
    Enterprise-grade CSV reader.

    Strategy:
    1. Try common UTF encodings with fast C engine
    2. Fall back to Python engine for malformed rows
    """

    encodings = ("utf-8", "utf-8-sig", "cp1252", "latin1")
    last_error = None

    # Fast path: strict parsing
    for enc in encodings:
        buffer.seek(0)
        try:
            return pd.read_csv(buffer, encoding=enc)
        except Exception as e:
            last_error = e

    # Slow but tolerant path
    buffer.seek(0)
    try:
        return pd.read_csv(
            buffer,
            encoding="latin1",
            engine="python",
            sep=None,            # auto-detect delimiter
            on_bad_lines="skip"  # skip malformed rows
        )
    except Exception as e:
        raise ValueError(
            f"Failed to parse CSV file. Last error: {last_error}"
        ) from e


# -------------------------
# Public API
# -------------------------
def load_data(file_or_path) -> pd.DataFrame:
    """
    Load CSV / Excel / JSON from:
    - File path
    - Streamlit UploadedFile
    - File-like object

    Always returns a pandas DataFrame or raises a clear error.
    """

    # -------- Case 1: path on disk --------
    if isinstance(file_or_path, (str, Path)):
        path = Path(file_or_path)
        ext = path.suffix.lower()

        if ext == ".csv":
            with open(path, "rb") as f:
                return _read_csv_robust(io.BytesIO(f.read()))

        if ext in {".xls", ".xlsx"}:
            return pd.read_excel(path)

        if ext == ".json":
            return pd.read_json(path)

        raise ValueError(f"Unsupported file type: {ext}")

    # -------- Case 2: Streamlit UploadedFile --------
    try:
        file_or_path.seek(0)
    except Exception:
        pass

    raw = file_or_path.read()
    if not raw:
        raise ValueError("Uploaded file is empty")

    bio = io.BytesIO(raw)
    name = getattr(file_or_path, "name", "")
    ext = Path(name).suffix.lower()

    if ext == ".csv" or _looks_like_csv(raw):
        return _read_csv_robust(bio)

    if ext in {".xls", ".xlsx"}:
        return pd.read_excel(bio)

    if ext == ".json":
        return pd.read_json(bio)

    raise ValueError(f"Unsupported uploaded file type: {ext}")
