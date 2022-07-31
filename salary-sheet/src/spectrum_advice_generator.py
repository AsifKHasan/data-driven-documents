#!/usr/bin/env python3
'''
    spectrum_advice_generator.py
'''
import os
import json
import time
import datetime

import pygsheets
import num2words

from helper.latex.latex2pdf import Latex2Pdf
from helper.google.google_helper import GoogleHelper

GSHEET_NAME = 'FAU__SalarySheet__2022-2023'

class AdviceGenerator:

    def get_data(self, selection, json_path):
        ws = self.context['gsheet'].worksheet('title', selection['selected-month'])
        vals = ws.get_all_values(returnas='matrix', majdim='ROWS', include_tailing_empty=True)

        salary = list(map(lambda v: {'wing' : v[4].strip(), 'unit' : v[5].strip(), 'name' : v[2].strip(), 'type' : v[6].strip().replace('-', ''), 'account' : v[9].strip(), 'payable' : v[59].strip().replace('-', ''), 'paythrough' : v[61].strip(), 'paystatus' : v[62].strip()}, vals[5:]))
        if selection['selected-mode'] in ['Cash', 'Cheque']:
            data = {'wing': selection['selected-wing']}
            salary = list(filter(lambda v: v['wing'] == selection['selected-wing'] and v['paythrough'] == selection['selected-mode'] and v['paystatus'] == 'In Process', salary))

        elif selection['selected-mode'] == 'Bank':
            data = {'refno': selection['selected-reference']}
            if selection['selected-filter'] == 'Software':
                salary = list(filter(lambda v: v['unit'] == 'Software Services' and v['type'] != 'BdREN' and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

            elif selection['selected-filter'] == 'BdREN':
                salary = list(filter(lambda v: v['type'] == 'BdREN' and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

            else:
                salary = list(filter(lambda v: v['unit'] != 'Software Services' and v['type'] != 'BdREN' and v['account'] != '' and v['paythrough'] == 'Bank' and v['paystatus'] == 'In Process', salary))

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
        if not self.context['gsheet']:
            return {'success': False, 'msg': 'Salary Sheet not accessible'}

        # get the paths
        template_file, json_path, pdf_path = self.get_paths(selection)
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
        if selection['selected-mode'] == 'Bank' and selection['selected-filter'] in ['BdREN', 'Software']:
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
