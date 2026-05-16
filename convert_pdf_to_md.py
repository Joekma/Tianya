import os
import sys
import re
import PyPDF2

print("Script started...")

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            lines.append(line)
    return '\n\n'.join(lines)

def extract_text_from_pdf(pdf_path):
    print(f"  extract_text_from_pdf called for: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"  PDF has {len(reader.pages)} pages")
            text_parts = []
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"## 第 {i+1} 页\n\n{page_text}")
                except Exception as e:
                    print(f"  Warning: Failed to extract page {i+1}: {e}")
                    continue
            return '\n\n'.join(text_parts)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def convert_pdf_to_md(pdf_path, md_path):
    print(f"Converting: {os.path.basename(pdf_path)}")
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        print(f"  [FAIL] Could not extract text")
        return False
    cleaned = clean_text(text)
    if not cleaned or len(cleaned.strip()) < 100:
        print(f"  [WARN] Extracted text too short, might be image-based PDF")
    try:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {os.path.splitext(os.path.basename(pdf_path))[0]}\n\n")
            f.write(cleaned)
        size = os.path.getsize(md_path)
        print(f"  [OK] -> {os.path.basename(md_path)} ({size//1024}KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] Write error: {e}")
        return False

base = r"e:\Workspace\项目\天涯论坛合集\天涯合集（无水印）"
print(f"Base path: {base}")
print(f"Base exists: {os.path.exists(base)}")

test_pdfs = []
for root, dirs, files in os.walk(base):
    if "markdown_test" in root:
        continue
    for f in files:
        fp = os.path.join(root, f)
        if f.lower().endswith('.pdf') and os.path.isfile(fp):
            test_pdfs.append(fp)

print(f"Found {len(test_pdfs)} PDFs total")
test_pdfs = test_pdfs[:5]
print(f"Testing with {len(test_pdfs)} PDFs: {test_pdfs}")

output_dir = os.path.join(base, "markdown_test")
os.makedirs(output_dir, exist_ok=True)
success = 0
fail = 0
for pdf in test_pdfs:
    md_name = os.path.splitext(os.path.basename(pdf))[0] + ".md"
    md_path = os.path.join(output_dir, md_name)
    if convert_pdf_to_md(pdf, md_path):
        success += 1
    else:
        fail += 1

print(f"\n{'='*50}")
print(f"Done! Success: {success}, Failed: {fail}")
print("Script finished.")