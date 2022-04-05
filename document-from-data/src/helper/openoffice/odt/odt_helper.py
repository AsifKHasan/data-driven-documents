#!/usr/bin/env python3
'''
    helper routines for odt files
'''

import subprocess
import platform

from ooopy.OOoPy        import OOoPy
from ooopy.Transformer  import Transformer
import ooopy.Transforms as     Transforms


if platform.system() == 'Windows':
    LIBREOFFICE_EXECUTABLE = 'C:/Program Files/LibreOffice/program/soffice.exe'
else:
    LIBREOFFICE_EXECUTABLE = 'soffice'

''' given an input template odt and field value list, outputs a file with fields replaced with values
'''
def replace_fields(infile, outfile, fields):
    o = OOoPy (infile=infile, outfile=outfile)
    t = Transformer \
        ( o.mimetype
        , Transforms.Editinfo      ()
        , Transforms.Field_Replace (replace = fields)
        , Transforms.Fix_OOo_Tag   ()
        )
    t.transform (o)
    o.close ()


''' given a list of input files, merges them into an output file
'''
def merge_files(files, outfile):
    o = OOoPy(infile=files[0], outfile=outfile)
    if len(files) > 1 :
        t = Transformer \
            ( o.mimetype
            , Transforms.get_meta        (o.mimetype)
            , Transforms.Concatenate     (* (files[1:]))
            , Transforms.renumber_all    (o.mimetype)
            , Transforms.set_meta        (o.mimetype)
            , Transforms.Fix_OOo_Tag     ()
            , Transforms.Manifest_Append ()
            )
        t.transform (o)
    o.close ()


''' given an odt file generates pdf in the given directory
'''
def generate_pdf(infile, outdir):
    command_line = f'"{LIBREOFFICE_EXECUTABLE}" --headless --convert-to pdf --outdir "{outdir}" "{infile}"'
    subprocess.call(command_line, shell=True);
