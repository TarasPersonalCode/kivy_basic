import argparse
import json
import os
import re
import subprocess
import urllib.request, urllib
import pdfkit

RU_ALPHABET = 'абвгдеёжзийклмнопрстуфхччшщьъыэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЧШЩЬЪЫЭЮЯ'
UA_ALPHABET = 'абвгдеєжзіиїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗІИЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'

def process_query(query_txt, output_dir):
    query_lower = str.lower(query_txt)
    output_fname = re.sub(f'[^0-9a-zA-Z'\
                          f'{RU_ALPHABET}'\
                          f'{UA_ALPHABET}]+', 
                          '.', 
                           query_lower.replace('\n', ''))
    pdfkit.from_url(query_txt, f'{output_dir}/{output_fname}.pdf')
    return f'{output_fname}.pdf'

