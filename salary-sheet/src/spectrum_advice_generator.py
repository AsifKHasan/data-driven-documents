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

GSHEET_NAME = 'FAU__SalarySheet__2023-2024'
COL_BANK_ACCOUNT_NAME = 2
COL_WING = 4
COL_UNIT = 5
COL_TYPE = 6
COL_BANK_ACCOUNT_NUMBER = 9
COL_NET_PAYABLE = 60
COL_PAY_THROUGH = 62
COL_PAY_STATUS = 63

ROW_DATA_START = 5

class AdviceGenerator:

    def get_data(self, selection, json_path):
        ws = self.context['gsheet'].worksheet('title', selection['selected-month'])
        vals = ws.get_all_values(returnas='matrix', majdim='ROWS', include_tailing_empty=True)

        salary = list(map(lambda v: {'wing' : v[COL_WING].strip(), 'unit' : v[COL_UNIT].strip(), 'name' : v[COL_BANK_ACCOUNT_NAME].strip(), 'type' : v[COL_TYPE].strip().replace('-', ''), 'account' : v[9].strip(), 'payable' : v[COL_NET_PAYABLE].strip().replace('-', ''), 'paythrough' : v[COL_PAY_THROUGH].strip(), 'paystatus' : v[COL_PAY_STATUS].strip()}, vals[5:]))
        if selection['selected-mode'] in ['Cash', 'Cheque']:
            data = {'wing': selection['selected-wing']}
            salary = list(filter(lambda v: v['wing'] == selection['selected-wing'] and v['paythrough'] == selection['selected-mode'] and v['paystatus'] == 'In Process', salary))

        elif selection['selected-mode'] == 'Bank':
            data = {'refno': selection['selected-reference']}
            
            # filters like Software, BdREN, R&D
            if selection['selected-filter'] == 'Software':
                salary = list(filter(lambda v: v['unit'] == 'Software Services' and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

            elif selection['selected-filter'] == 'R&D':
                salary = list(filter(lambda v: v['unit'] == 'Research and Development' and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

            else:
                salary = list(filter(lambda v: v['unit'] not in ['Software Services', 'Research and Development'] and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

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
        if selection['selected-mode'] == 'Bank' and selection['selected-filter'] in ['R&D', 'Software']:
            prefix = '{0}-{1}'.format(prefix, selection['selected-filter']).lower()

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
