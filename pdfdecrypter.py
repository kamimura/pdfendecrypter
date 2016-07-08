#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import PyPDF2

length = len(sys.argv)
if length >= 2:
    PASSWORD = sys.argv[1]
else:
    print('usage: cmd password [path]')
    sys.exit(1)

if length == 3:
    PATH = sys.argv[2]
else:
    PATH = os.curdir

for folder_name, _, filenames in os.walk(PATH):
    for filename in filenames:
        if filename.endswith('.pdf'):
            filename = folder_name + os.sep + filename
            with open(filename, 'rb') as pdf_file:
                try:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    if pdf_reader.isEncrypted:
                        pdf_reader.decrypt(PASSWORD)
                        pdf_writer = PyPDF2.PdfFileWriter()
                        for page_num in range(pdf_reader.numPages):
                            page = pdf_reader.getPage(page_num)
                            pdf_writer.addPage(page)
                        with open(filename + '_decrypted.pdf', 'wb') as f:
                            pdf_writer.write(f)
                        os.rename(filename + '_decrypted.pdf', filename)
                except Exception as err:
                    print('{0}: {1}'.format(filename, err))
