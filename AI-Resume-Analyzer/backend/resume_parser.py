try:
    import fitz
except ImportError:  # pragma: no cover
    fitz = None

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None

try:
    import docx
except ImportError:  # pragma: no cover
    docx = None


def extract_text_from_pdf(pdf_path):
    if fitz is not None:
        document = fitz.open(pdf_path)
        text = "".join(page.get_text() for page in document)
        document.close()
        return text

    if PdfReader is not None:
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text

    raise ImportError("No PDF reader is available. Install PyMuPDF or pypdf.")


def extract_text_from_file(file_path):
    ext = file_path.lower().rsplit('.', 1)[-1] if '.' in file_path else ''

    if ext == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()

    if ext == 'pdf':
        return extract_text_from_pdf(file_path)

    if ext == 'docx':
        if docx is None:
            raise ImportError('python-docx is not installed.')
        document = docx.Document(file_path)
        return '\n'.join(paragraph.text for paragraph in document.paragraphs)

    raise ValueError(f'Unsupported file type: {file_path}')


def extract_resume_sections(text):
    text = (text or '').lower()
    sections = {
        'contact_information': any(keyword in text for keyword in ['contact information', 'email', 'phone', 'linkedin', 'address']),
        'education': any(keyword in text for keyword in ['education', 'b.tech', 'bachelor', 'master', 'degree', 'university']),
        'skills': any(keyword in text for keyword in ['skills', 'technologies', 'tools', 'programming languages']),
        'projects': any(keyword in text for keyword in ['projects', 'project', 'portfolio']),
        'certifications': any(keyword in text for keyword in ['certifications', 'certification', 'aws certified', 'azure', 'oracle']),
        'experience': any(keyword in text for keyword in ['experience', 'work experience', 'professional experience', 'employment'])
    }
    return sections