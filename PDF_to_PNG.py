from pathlib import Path
from pdf2image import convert_from_path

def convert_all_pdfs():
    '''Function that takes PDF's from a dir convert them to png and put 
    them to an output dir with the file being dirs and contains their "png" 
    converted content 
    '''
    #* init dirs
    pdf_dir = Path("PDFs")
    output_dir = Path("PDF_Images")
    #* create it if doesn't exist
    output_dir.mkdir(exist_ok=True)
    #* parsing pdf's
    for pdf_file in pdf_dir.glob("*.pdf"):
        #*printing message to indicate the name of the current converting file
        print(f"Converting {pdf_file.name}...")
        
        pdf_output_dir = output_dir / pdf_file.stem
        pdf_output_dir.mkdir(exist_ok=True)
        #* conversion process
        images = convert_from_path(str(pdf_file), size=(800, None))
        
        for i, img in enumerate(images, 1):
            img_path = pdf_output_dir / f"page_{i:03d}.png"
            img.save(img_path, "PNG", optimize=True)
        #* printing statement to indicate how many pages converted in the file  
        print(f" Converted {len(images)} pages")

if __name__ == "__main__":
    convert_all_pdfs()