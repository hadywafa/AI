# layout_analysis.py

import os
from typing import List
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeResult,
    AnalyzeDocumentRequest,
    DocumentSpan,
    DocumentWord,
    DocumentLine,
    DocumentPage,
)

# 🔐 Load .env values
load_dotenv()

# 🔧 Secure config
AZURE_DOC_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOC_INTELLIGENCE_ENDPOINT")
AZURE_DOC_INTELLIGENCE_KEY = os.getenv("AZURE_DOC_INTELLIGENCE_KEY")

if not AZURE_DOC_INTELLIGENCE_ENDPOINT or not AZURE_DOC_INTELLIGENCE_KEY:
    raise EnvironmentError("Missing Azure Document Intelligence credentials in .env")


def _word_in_span(word: DocumentWord, spans: List[DocumentSpan]) -> bool:
    """Check if a word's span is within the span of a line."""
    return any(
        span.offset <= word.span.offset < span.offset + span.length for span in spans
    )


def get_words_for_line(page: DocumentPage, line: DocumentLine) -> List[DocumentWord]:
    """Extract words associated with a line using spans."""
    return [word for word in page.words if _word_in_span(word, line.spans)]


def analyze_layout_from_url(doc_url: str) -> None:
    """Analyze the layout of a document using Azure's prebuilt-layout model."""
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DOC_INTELLIGENCE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_DOC_INTELLIGENCE_KEY),
    )

    print(f"📄 Starting analysis for: {doc_url}")
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=AnalyzeDocumentRequest(url_source=doc_url),
    )

    result: AnalyzeResult = poller.result()
    print("✅ Layout analysis complete.\n")

    # ✍️ Check for handwriting
    if result.styles and any(style.is_handwritten for style in result.styles):
        print("🖋️ Document contains handwritten content.")
    else:
        print("📝 No handwriting detected.")

    # 📄 Page layout info
    for page in result.pages:
        print(
            f"\n📄 Page {page.page_number} ({page.unit}) — Size: {page.width} x {page.height}"
        )

        for i, line in enumerate(page.lines or []):
            words = get_words_for_line(page, line)
            print(
                f"  🧾 Line {i}: '{line.content}' — Words: {len(words)} — Bounds: {line.polygon}"
            )
            for word in words:
                print(f"     ↳ Word: '{word.content}' — Confidence: {word.confidence}")

        for mark in page.selection_marks or []:
            print(
                f"  ☑️ Selection mark: {mark.state} — Confidence: {mark.confidence} — Bounds: {mark.polygon}"
            )

    # 📊 Table layout info
    for table_index, table in enumerate(result.tables or []):
        print(
            f"\n📊 Table {table_index} — {table.row_count} rows × {table.column_count} cols"
        )
        for region in table.bounding_regions or []:
            print(f"  ↳ Location: Page {region.page_number} — Bounds: {region.polygon}")

        for cell in table.cells:
            print(
                f"    • Cell[{cell.row_index}][{cell.column_index}]: '{cell.content}'"
            )
            for region in cell.bounding_regions or []:
                print(f"      ↳ Page {region.page_number} — Bounds: {region.polygon}")

    print("\n✅ Done analyzing layout.\n" + "-" * 50)


if __name__ == "__main__":
    # Sample test document (public URL)
    SAMPLE_DOCUMENT_URL = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
    analyze_layout_from_url(SAMPLE_DOCUMENT_URL)

# ======================= OUTPUT ===========================
# 📄 Starting analysis for: sample-layout.pdf
# ✅ Layout analysis complete.

# 📝 No handwriting detected.

# 📄 Page 1 (unit: inch) — Size: 8.5 x 11.0
#   🧾 Line 0: 'Contoso Headquarters' — Words: 2
#      ↳ Word: 'Contoso' — Confidence: 0.99
#      ↳ Word: 'Headquarters' — Confidence: 0.98

# 📊 Table 0 — 3 rows × 4 cols
#     • Cell[0][0]: 'Name'
#     • Cell[1][0]: 'John Smith'
# ...
# ✅ Done analyzing layout.
# ==========================================================
