from src.file_loaders.base_loader import BaseFileLoader
import os

try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class ImageLoader(BaseFileLoader):
    """Load images with OCR"""
    
    def load(self, file_path: str) -> str:
        if not TESSERACT_AVAILABLE:
            return "OCR not available. Install pytesseract and Pillow to process images."
        
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return f"[OCR from image: {os.path.basename(file_path)}]\n\n{text}"
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")


