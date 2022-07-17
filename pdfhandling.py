import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import concurrent.futures
from multiprocessing import freeze_support
from pathlib import Path




'''

information = [(filename1,startpage1,endpage1), (filename2, startpage2, endpage2), ...,(filename19,startpage19,endpage19)].

reader = PdfFileReader("example.pdf")

for page in range(len(information)):
    pdf_writer = PyPDF2.PdfFileWriter()
    start = information[page][1]
    end = information[page][2]
    while start<=end:
        pdf_writer.addPage(pdfReader.getPage(start-1))
        start+=1
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    output_filename = '{}_{}_page_{}.pdf'.format(information[page][0],information[page][1], information[page][2])
    with open(output_filename,'wb') as out:
        pdf_writer.write(out)

'''


def pdf_extract(pdf, segments):
    """
    pdf: str | Path
    segments: [(start, end), {'start': int, 'end': int}]
    """
    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfFileReader(read_stream)
        for segment in segments:
            pdf_writer = PdfFileWriter()
            # support {'start': 3, 'end': 3} or (start, end)
            try:
                start_page, end_page = segment['start'], segment['end']
            except TypeError:
                start_page, end_page = segment
            for page_num in range(start_page - 1, end_page):
                pdf_writer.addPage(pdf_reader.getPage(page_num))
            p = Path(pdf)
            ouput = p.parent / p.with_stem(f'{p.stem}_pages_{start_page}-{end_page}')
            with open(ouput, 'wb') as out:
                pdf_writer.write(out)


def __pdf_extract(pair):
    return pdf_extract(*pair)


def pdf_extract_batch(pdfs, workers=20):
    """
    pdfs = {pdf_name: [(1, 1), ...], ...}
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(__pdf_extract, pdfs.items())


if __name__ == '__main__':
    freeze_support()
    pdf_name = r'C:\Users\maste\Documents\long.pdf'
    segments = [(1, 1), {'start': 3, 'end': 5}]
    # Single
    pdf_extract(pdf_name, segments)
    # Batched (Concurrent)
    pdfs = {pdf_name: segments}
    # pdf_extract_batch(pdfs)