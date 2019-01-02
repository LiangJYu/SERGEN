#!/usr/bin/env python

import pdftotext
import os

def pdf_to_text(pdf_path, pdf_start=0):
    text = ''
    if os.path.isfile(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf = pdftotext.PDF(f)
            for i in range(pdf_start, len(pdf)):
                text += pdf[i]
    return text.split('\n')

if __name__ == '__main__':
    import sys

    print(file_to_text(sys.argv[1]))

