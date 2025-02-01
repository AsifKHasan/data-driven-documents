#!/usr/bin/env python3
'''
    spectrum_advice_generator.py
'''
import os
import json
import datetime

import pygsheets
import num2words

from helper.latex.latex2pdf import Latex2Pdf
from helper.google.google_helper import GoogleHelper

GSHEET_NAME = 'Cybernetics__SalarySheet__2024-2025'
COL_BANK_ACCOUNT_NAME = 2       # C
COL_WING = 6                    # G
COL_UNIT = 7                    # H
COL_TYPE = 8                    # I
COL_BANK_ACCOUNT_NUMBER = 11    # L
# COL_NET_PAYABLE = 62          # BK
# COL_PAY_THROUGH = 64          # BM
# COL_PAY_STATUS = 65           # BN
COL_NET_PAYABLE = 57            # BF
COL_PAY_THROUGH = 59            # BH
COL_PAY_STATUS = 60             # BI

ROW_DATA_START = 5

class AdviceGenerator:

    def get_data(self, selection, json_path):
        ws = self.context['gsheet'].worksheet('title', selection['selected-month'])
        vals = ws.get_all_values(returnas='matrix', majdim='ROWS', include_tailing_empty=True)

        salary = list(map(lambda v: {'wing' : v[COL_WING].strip(), 'unit' : v[COL_UNIT].strip(), 'name' : v[COL_BANK_ACCOUNT_NAME].strip(), 'type' : v[COL_TYPE].strip().replace('-', ''), 'account' : v[COL_BANK_ACCOUNT_NUMBER].strip(), 'payable' : v[COL_NET_PAYABLE].strip().replace('-', ''), 'paythrough' : v[COL_PAY_THROUGH].strip(), 'paystatus' : v[COL_PAY_STATUS].strip()}, vals[ROW_DATA_START:]))
        data = {}
        if selection['selected-mode'] in ['Cash', 'Cheque']:
            salary = list(filter(lambda v: v['paythrough'] == selection['selected-mode'] and v['paystatus'] == 'In Process', salary))

        elif selection['selected-mode'] == 'Bank':
            data = {'refno': selection['selected-reference']}
            salary = list(filter(lambda v: v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

        else:
            return None

        totalamount = sum(float(a['payable'].replace(',', '') or 0) for a in salary)
        totalamountinwords = num2words.num2words(totalamount, to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')
        data['month'] = selection['selected-month']
        data['date'] = datetime.datetime.now().strftime('%B %d, %Y')
        data['selectedaccount'] = selection['selected-account']
        data['totalamount'] = '{:,.2f}'.format(totalamount)
        data['totalamountinwords'] = totalamountinwords
        data['salary'] = salary

        with open(json_path, 'w') as f:
            f.write(json.dumps(data, sort_keys=False, indent=4))

        return data

    def gnerate_pdf(self, selection):
        # get the paths
        template_file, json_path, pdf_path = self.get_paths(selection)

        if not self.context['gsheet']:
            return {'success': False, 'msg': 'Salary Sheet not accessible'}

        # get the data
        data = self.get_data(selection, json_path)
        if not data:
            return {'success': False, 'msg': 'Failed to get any data from selection'}

        if len(data['salary']) == 0:
            return {'success': False, 'msg': 'No data ready for salary advice generation'}

        # generate pdf
        pdfgenerator = Latex2Pdf(self.context['template-dir'], template_file, pdf_path)
        if pdfgenerator.generate_pdf(data):
            return {'success': True, 'pdf-path': pdf_path}
        else:
            return {'success': False, 'msg': 'Salary Advice could not be generated'}

    def init(self, json_cred_path, template_dir, out_dir):
        self._google_helper = GoogleHelper()
        if self._google_helper.authorize(json_cred_path):
            gsheet = self._google_helper.open_gsheet(GSHEET_NAME)
            if gsheet:
                self.context['gsheet'] = gsheet
                self.context['template-dir'] = template_dir
                self.context['out-dir'] = out_dir
                return {'success': True}
            else:
                return {'success': False, 'msg': 'Could not open Salary Sheet'}
        else:
            return {'success': False, 'msg': 'Google authorization failed'}

    def get_paths(self, selection):
        prefix = 'salary-advice-{0}'.format(selection['selected-mode']).lower()

        out_dir = '{0}/{1}'.format(self.context['out-dir'], selection['selected-month'])
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        month_time = '{0}__{1}'.format(selection['selected-month'], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d__%H-%M-%S'))

        template_file = '{0}.tex'.format(prefix)
        json_path = '{0}/{1}__{2}.json'.format(out_dir, prefix, month_time)
        pdf_path = '{0}/{1}__{2}.pdf'.format(out_dir, prefix, month_time)

        return template_file, json_path, pdf_path

    def __init__(self):
        self.context = {'gsheet': None, 'template-dir': None, 'out-dir': None}
