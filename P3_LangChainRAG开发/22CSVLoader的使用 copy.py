from pathlib import Path
from langchain_community.document_loaders import CSVLoader

csv_path = Path(__file__).parent / "data" / "stu.csv"

loader = CSVLoader(
    file_path=str(csv_path),
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
    },
    encoding="utf-8",
)

for document in loader.lazy_load():
    print(document)