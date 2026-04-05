import pandas as pd

def load_rules(file_path: str) -> str:  # No default here, path comes from groq_client
    if file_path.endswith(".xlsx"):
        return _load_excel(file_path)
    elif file_path.endswith(".txt"):
        return _load_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Use .xlsx or .txt")

def _load_excel(file_path: str) -> str:  # Receives the path, doesn't hardcode it
    excel_file = pd.ExcelFile(file_path)
    all_content = []

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df.dropna(how="all")

        all_content.append(f"[ {sheet_name} ]")
        all_content.append(df.to_string(index=False))
        all_content.append("")

    return "\n".join(all_content)

def _load_txt(file_path: str) -> str:  # Same here
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
