#/bin/env python3
'''
    common template code for document generation
'''

import os
import re

from odf import table, text
from pprint import pprint

from helper.google.google_helper import *
from helper.openoffice.odt.odt_helper import *
from helper.openoffice.odf_helper import *
from helper.logger import *

DATA_CONNECTORS = {
    'spectrum' : {
        'google': {
            'credential-json': '../conf/credential.json'
        },
    },
    'SSCL' : {
        'google': {
            'credential-json': '../conf/credential.json'
        },
    },
    'celloscope' : {
        'google': {
            'credential-json': '../conf/credential.json'
        },
    },
}

DATA_SOURCES = {
    'spectrum' : {
        'appointment-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'appointment',
            'data-range': 'A3:N'
        },
        'confirmation-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'confirmation',
            'data-range': 'A3:N'
        },
        'experience-certificate': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'experience-certificate',
            'data-range': 'A3:K'
        },
        'introduction-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'introduction',
            'data-range': 'A3:M'
        },
        'internship-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'internship',
            'data-range': 'A3:M'
        },
        'offer-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'offer',
            'data-range': 'A3:L'
        },
        'release-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'release',
            'data-range': 'A3:J'
        },
        'salary-certificate': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'salary-certificate',
            'data-range': 'A3:Q'
        },
        'salary-enhancement-letter': {
            'sheet': 'spectrum__salary-revision__2022',
            'worksheet': 'spectrum-2022',
            'data-range': 'A5:V'
        },
        'separation-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'separation',
            'data-range': 'A3:I'
        },
        'showcause-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'showcause',
            'data-range': 'A3:J'
        },
        'transfer-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'transfer',
            'data-range': 'A3:M'
        },
        'warning-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'warning',
            'data-range': 'A3:H'
        },
    },
    'SSCL' : {
        'payment-voucher': {
            'sheet': 'SSCL__vouchers',
            'worksheet': 'payment-vouchers',
            'data-range': 'A3:N'
        },
        'receipt-voucher': {
            'sheet': 'SSCL__vouchers',
            'worksheet': 'receipt-vouchers',
            'data-range': 'A3:M'
        },
        'issued-invoice': {
            'sheet': 'SSCL__po-invoice',
            'worksheet': 'issued-invoice',
            'data-range': 'A3:Y'
        },
    },
    'celloscope' : {
        'salary-enhancement-letter': {
            'sheet': 'celloscope__salary-revision__2022',
            'worksheet': 'celloscope-2022',
            'data-range': 'A5:V'
        },
    },
}

DATA_PROCESSORS = {
    'spectrum': {
        'appointment-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'address'},
                {'column': 5, 'key': 'effectivefrom'},
                {'column': 6, 'key': 'designation'},
                {'column': 7, 'key': 'grade'},
                {'column': 8, 'key': 'wing'},
                {'column': 9, 'key': 'unit'},
                {'column': 10, 'key': 'supervisor'},
                {'column': 11, 'key': 'remuneration'},
                {'column': 12, 'key': 'site'},
                {'column': 13, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'confirmation-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'wing'},
                {'column': 5, 'key': 'unit'},
                {'column': 6, 'key': 'grade'},
                {'column': 7, 'key': 'designation'},
                {'column': 8, 'key': 'effectivefrom'},
                {'column': 9, 'key': 'raise'},
                {'column': 10, 'key': 'remuneration'},
                {'column': 11, 'key': 'increment'},
                {'column': 12, 'key': 'supervisor'},
                {'column': 13, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'experience-certificate': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'designation'},
                {'column': 5, 'key': 'unit'},
                {'column': 6, 'key': 'joiningdate'},
                {'column': 7, 'key': 'separationdate'},
                {'column': 8, 'key': 'employmenttype'},
                {'column': 9, 'key': 'signatory'},
                {'column': 10, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'introduction-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'name'},
                {'column': 3, 'key': 'birthdate'},
                {'column': 4, 'key': 'citizenship'},
                {'column': 5, 'key': 'presentaddress'},
                {'column': 6, 'key': 'permanentaddress'},
                {'column': 7, 'key': 'joiningdate'},
                {'column': 8, 'key': 'designation'},
                {'column': 9, 'key': 'employmenttype'},
                {'column': 10, 'key': 'remuneration'},
                {'column': 11, 'key': 'signatory'},
                {'column': 12, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'internship-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'address'},
                {'column': 5, 'key': 'position'},
                {'column': 6, 'key': 'months'},
                {'column': 7, 'key': 'startdate'},
                {'column': 8, 'key': 'enddate'},
                {'column': 9, 'key': 'remuneration'},
                {'column': 10, 'key': 'exitcriteria'},
                {'column': 11, 'key': 'signatory'},
                {'column': 12, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'offer-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'address'},
                {'column': 5, 'key': 'effectivefrom'},
                {'column': 6, 'key': 'designation'},
                {'column': 7, 'key': 'grade'},
                {'column': 8, 'key': 'wing'},
                {'column': 9, 'key': 'unit'},
                {'column': 10, 'key': 'remuneration'},
                {'column': 11, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'release-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'address'},
                {'column': 5, 'key': 'effectivefrom'},
                {'column': 6, 'key': 'designation'},
                {'column': 7, 'key': 'unit'},
                {'column': 8, 'key': 'signatory'},
                {'column': 9, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'salary-certificate': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'designation'},
                {'column': 5, 'key': 'unit'},
                {'column': 6, 'key': 'joiningdate'},
                {'column': 7, 'key': 'employmenttype'},
                {'column': 8, 'key': 'basic'},
                {'column': 9, 'key': 'houserent'},
                {'column': 10, 'key': 'medical'},
                {'column': 11, 'key': 'conveyance'},
                {'column': 12, 'key': 'gross'},
                {'column': 13, 'key': 'tax'},
                {'column': 14, 'key': 'net'},
                {'column': 15, 'key': 'signatory'},
                {'column': 16, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'salary-enhancement-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'wing'},
                {'column': 5, 'key': 'unit'},
                {'column': 6, 'key': 'supervisor'},
                {'column': 12, 'key': 'salary'},
                {'column': 13, 'key': 'increment'},
                {'column': 16, 'key': 'currentgrade'},
                {'column': 17, 'key': 'promotion'},
                {'column': 18, 'key': 'grade'},
                {'column': 19, 'key': 'designation'},
                {'column': 20, 'key': 'effectivefrom'},
                {'column': 21, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'separation-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'address'},
                {'column': 5, 'key': 'effectivefrom'},
                {'column': 6, 'key': 'clause'},
                {'column': 7, 'key': 'reasontext'},
                {'column': 8, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'showcause-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'subject'},
                {'column': 5, 'key': 'incidence'},
                {'column': 6, 'key': 'submitto'},
                {'column': 7, 'key': 'submissiondate'},
                {'column': 8, 'key': 'signatory'},
                {'column': 9, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'transfer-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'effectivefrom'},
                {'column': 5, 'key': 'address'},
                {'column': 8, 'key': 'fromunit'},
                {'column': 9, 'key': 'tounit'},
                {'column': 10, 'key': 'supervisor'},
                {'column': 11, 'key': 'superdesignation'},
                {'column': 12, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
        'warning-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'subject'},
                {'column': 5, 'key': 'incidence'},
                {'column': 6, 'key': 'signatory'},
                {'column': 7, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
    },
    'SSCL': {
        'payment-voucher': {
            'columns': [
                {'column': 3, 'key': 'voucherno'},
                {'column': 4, 'key': 'voucherdate'},
                {'column': 5, 'key': 'paymentto'},
                {'column': 6, 'key': 'paymentmode'},
                {'column': 7, 'key': 'paymentmodedetails'},
                {'column': 12, 'key': 'vouchertotal'},
                {'column': 13, 'key': 'being'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
            'tabular-data': [
                {
                    'table-name': 'TableItem',
                    'rows-for-data': (2, 11),
                    'columns': [
                        {'column': 2, 'key': 'seq', 'cell': 0},
                        {'column': 8, 'key': 'accounthead', 'cell': 1},
                        {'column': 9, 'key': 'mrno', 'cell': 2},
                        {'column': 10, 'key': 'accountcode', 'cell': 3},
                        {'column': 11, 'key': 'amount', 'cell': 4},
                    ],
                    'include-column': 1,
                    'include-value': 'yes',
                },
            ],
        },
        'receipt-voucher': {
            'columns': [
                {'column': 3, 'key': 'voucherno'},
                {'column': 4, 'key': 'voucherdate'},
                {'column': 5, 'key': 'receivedfrom'},
                {'column': 6, 'key': 'receptionmode'},
                {'column': 7, 'key': 'receptionmodedetails'},
                {'column': 11, 'key': 'vouchertotal'},
                {'column': 12, 'key': 'being'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
            'tabular-data': [
                {
                    'table-name': 'TableItem',
                    'rows-for-data': (2, 11),
                    'columns': [
                        {'column': 2, 'key': 'seq', 'cell': 0},
                        {'column': 8, 'key': 'accounthead', 'cell': 1},
                        {'column': 9, 'key': 'accountcode', 'cell': 2},
                        {'column': 10, 'key': 'amount', 'cell': 3},
                    ],
                    'include-column': 1,
                    'include-value': 'yes',
                },
            ],
        },
        'issued-invoice': {
            'columns': [
                {'column': 3, 'key': 'invoicedate'},
                {'column': 4, 'key': 'invoiceref'},
                {'column': 5, 'key': 'clientname'},
                {'column': 11, 'key': 'invoicenet'},
                {'column': 12, 'key': 'invoicevat'},
                {'column': 13, 'key': 'invoicetotal'},
                {'column': 14, 'key': 'podate'},
                {'column': 15, 'key': 'povalue'},
                {'column': 16, 'key': 'vatpct'},
                {'column': 17, 'key': 'poref'},
                {'column': 18, 'key': 'claimterms'},
                {'column': 19, 'key': 'clientaddress'},
                {'column': 20, 'key': 'clientphone'},
                {'column': 21, 'key': 'clientfax'},
                {'column': 22, 'key': 'clienturl'},
                {'column': 23, 'key': 'contactname'},
                {'column': 24, 'key': 'contactphone'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
            'tabular-data': [
                {
                    'table-name': 'TableItem',
                    'rows-for-data': (2, 11),
                    'columns': [
                        {'column': 2, 'key': 'seq', 'cell': 0},
                        {'column': 6, 'key': 'item', 'cell': 1},
                        {'column': 7, 'key': 'uom', 'cell': 2},
                        {'column': 8, 'key': 'qty', 'cell': 3},
                        {'column': 9, 'key': 'unitprice', 'cell': 4},
                        {'column': 10, 'key': 'itemtotal', 'cell': 5},
                    ],
                    'include-column': 1,
                    'include-value': 'yes',
                },
            ],
        },
    },
    'celloscope': {
        'salary-enhancement-letter': {
            'columns': [
                {'column': 1, 'key': 'seq'},
                {'column': 2, 'key': 'salutation'},
                {'column': 3, 'key': 'name'},
                {'column': 4, 'key': 'designation'},
                {'column': 17, 'key': 'salary'},
                {'column': 18, 'key': 'increment'},
                {'column': 20, 'key': 'effectivefrom'},
                {'column': 21, 'key': 'letterdate'},
            ],
            'filter-column': 0,
            'filter-value': 'yes',
        },
    },
}

DATA_SERIALIZERS = {
    'spectrum' : {
        'appointment-letter': {
            'input-template': '../template/spectrum/appointment-letter/HR__appointment-letter-template__2022.odt',
            'output-dir': '../out/spectrum/appointment-letter',
            'output-file-pattern': 'spectrum__appointment-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': False,
            'merged-file-pattern': 'spectrum__appointment-letter__2022.odt',
            'pdf-output-for-merged-file': False,
        },
        'confirmation-letter': {
            'input-template': '../template/spectrum/confirmation-letter/HR__confirmation-letter-template__2022.odt',
            'output-dir': '../out/spectrum/confirmation-letter',
            'output-file-pattern': 'spectrum__confirmation-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__confirmation-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'experience-certificate': {
            'input-template': '../template/spectrum/experience-certificate/HR__experience-certificate-template__2022.odt',
            'output-dir': '../out/spectrum/experience-certificate',
            'output-file-pattern': 'spectrum__experience-certificate__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__experience-certificate__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'introduction-letter': {
            'input-template': '../template/spectrum/introduction-letter/HR__introduction-letter-template__2022.odt',
            'output-dir': '../out/spectrum/introduction-letter',
            'output-file-pattern': 'spectrum__introduction-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__introduction-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'internship-letter': {
            'input-template': '../template/spectrum/internship-letter/HR__internship-letter-template__2022.odt',
            'output-dir': '../out/spectrum/internship-letter',
            'output-file-pattern': 'spectrum__internship-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__internship-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'offer-letter': {
            'input-template': '../template/spectrum/offer-letter/HR__offer-letter-template__2022.odt',
            'output-dir': '../out/spectrum/offer-letter',
            'output-file-pattern': 'spectrum__offer-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__offer-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'release-letter': {
            'input-template': '../template/spectrum/release-letter/HR__release-letter-template__2022.odt',
            'output-dir': '../out/spectrum/release-letter',
            'output-file-pattern': 'spectrum__release-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__release-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'salary-certificate': {
            'input-template': '../template/spectrum/salary-certificate/HR__salary-certificate-template__2022.odt',
            'output-dir': '../out/spectrum/salary-certificate',
            'output-file-pattern': 'spectrum__salary-certificate__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__salary-certificate__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'salary-enhancement-letter': {
            'input-template': '../template/spectrum/salary-enhancement-letter/HR__salary-enhancement-letter-template__2022.odt',
            'output-dir': '../out/spectrum/salary-enhancement-letter',
            'output-file-pattern': 'spectrum__salary-enhancement-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__salary-enhancement-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'separation-letter': {
            'input-template': '../template/spectrum/separation-letter/HR__separation-letter-template__2022.odt',
            'output-dir': '../out/spectrum/separation-letter',
            'output-file-pattern': 'spectrum__separation-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__separation-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'showcause-letter': {
            'input-template': '../template/spectrum/showcause-letter/HR__showcause-letter-template__2022.odt',
            'output-dir': '../out/spectrum/showcause-letter',
            'output-file-pattern': 'spectrum__showcause-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__showcause-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'transfer-letter': {
            'input-template': '../template/spectrum/transfer-letter/HR__transfer-letter-template__2022.odt',
            'output-dir': '../out/spectrum/transfer-letter',
            'output-file-pattern': 'spectrum__transfer-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__transfer-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'warning-letter': {
            'input-template': '../template/spectrum/warning-letter/HR__warning-letter-template__2022.odt',
            'output-dir': '../out/spectrum/warning-letter',
            'output-file-pattern': 'spectrum__warning-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__warning-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
    },
    'SSCL' : {
        'payment-voucher': {
            'input-template': '../template/sscl/payment-voucher/SSCL__payment-voucher-template__2022.odt',
            'output-dir': '../out/sscl/payment-voucher',
            'output-file-pattern': 'sscl__payment-voucher__2022__{voucherno}__{voucherdate}.odt',
            'pdf-output-for-files': True,
            'merge-files': False,
            'merged-file-pattern': 'sscl__payment-voucher__2022.odt',
            'pdf-output-for-merged-file': False,
        },
        'receipt-voucher': {
            'input-template': '../template/sscl/receipt-voucher/SSCL__receipt-voucher-template__2022.odt',
            'output-dir': '../out/sscl/receipt-voucher',
            'output-file-pattern': 'sscl__receipt-voucher__2022__{voucherno}__{voucherdate}.odt',
            'pdf-output-for-files': True,
            'merge-files': False,
            'merged-file-pattern': 'sscl__receipt-voucher__2022.odt',
            'pdf-output-for-merged-file': False,
        },
        'issued-invoice': {
            'input-template': '../template/sscl/issued-invoice/SSCL__issued-invoice-template__2022.odt',
            'output-dir': '../out/sscl/issued-invoice',
            'output-file-pattern': 'sscl__issued-invoice__2022__{invoiceref}.odt',
            'pdf-output-for-files': True,
            'merge-files': False,
            'merged-file-pattern': 'sscl__issued-invoice__2022.odt',
            'pdf-output-for-merged-file': False,
        },
    },
    'celloscope' : {
        'salary-enhancement-letter': {
            'input-template': '../template/celloscope/salary-enhancement-letter/celloscope__salary-enhancement-letter-template__2022.odt',
            'output-dir': '../out/celloscope/salary-enhancement-letter',
            'output-file-pattern': 'celloscope__salary-enhancement-letter__2022__{seq}__{name}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'celloscope__salary-enhancement-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
    },
}

''' authenticate to data service
'''
def authenticate_to_data_service(org, provider):
    google_data_connector_spec = DATA_CONNECTORS[org][provider]

    debug(f'{org} : authenticating with {provider}')
    client = connector_client(google_data_connector_spec)
    debug(f'{org} : authenticating with {provider} ... done')

    # wrap the connector in a data-connector object
    data_connector = {'client': client}

    return data_connector


''' acquire data from data source
'''
def acquire_data(org, source, data_connector):
    gsheet_data_source_spec = DATA_SOURCES[org][source]

    debug(f'{org} : acquiring data from {source}')
    values = gsheet_data(data_connector['client'], gsheet_data_source_spec)
    debug(f'{org} : acquiring data from {source} ... done')

    # wrap the data in a source-data object
    source_data = {'data': values}

    return source_data


''' process, transform, prepare data
'''
def process_data(org, data_processor, source_data):
    data_processor_spec = DATA_PROCESSORS[org][data_processor]

    raw_data = source_data['data']

    debug(f'{org} : processing data for [{data_processor}]')

    # the data is in a list (rows) of list (columns)
    data = []
    for row in raw_data:
        columns = {}
        # filter rows as specified
        if row[data_processor_spec['filter-column']] == data_processor_spec['filter-value']:
            for col_spec in data_processor_spec['columns']:
                if len(row) > col_spec['column']:
                    columns[col_spec['key']] = row[col_spec['column']]

            data.append(columns)

    # now process tabular data if there is any
    if 'tabular-data' in data_processor_spec:
        # tabular_data_specs is a list
        for tabular_data_spec in data_processor_spec['tabular-data']:
            tabular_data = []
            for row in raw_data:
                columns = {}
                # filter rows as specified
                if row[tabular_data_spec['include-column']] == tabular_data_spec['include-value']:
                    for col_spec in tabular_data_spec['columns']:
                        columns[col_spec['key']] = row[col_spec['column']]

                    tabular_data.append(columns)

            tabular_data_spec['data-map'] = tabular_data


    debug(f'{org} : processing data for [{data_processor}] ... done')

    # wrap the data in a processed-data object
    processed_data = {'data-processor': data_processor_spec, 'data': data}

    return processed_data


''' generate documents from data
'''
def output_data(org, output_processor, processed_data):
    output_spec = DATA_SERIALIZERS[org][output_processor]

    data = processed_data['data']
    tmp_dir = output_spec['output-dir'] + '/tmp'

    # crete directories in case they do not exist
    os.makedirs(tmp_dir, exist_ok=True)

    debug(f'{org} : generating output for [{output_processor}]')

    # generate files for each data row
    temp_files = []
    for item in data:
        # output-file-pattern may have variables/placeholders (enclosed in {}), let us identify those
        file_name = output_spec['output-file-pattern']
        r1 = re.findall(r"{\w+}", file_name)
        for var in r1:
            key = var[1:-1]
            file_name = file_name.replace(var, item[key].lower().replace(' ', '-'))

        temp_file_path = tmp_dir + '/' + file_name
        temp_files.append(temp_file_path)

        # generate the file
        replace_fields(output_spec['input-template'], temp_file_path, item)
        debug(f'.. {org} : generating odt for {temp_file_path} ... done')

        # here we may need to run another pass with odfpy to serialize tabular_data if there is any
        if 'tabular-data' in processed_data['data-processor']:
            output_tabular_data(temp_file_path, processed_data['data-processor']['tabular-data'])

        # generate pdf if instructed to do so
        if output_spec['pdf-output-for-files']:
            debug(f'.. {org} : generating pdf from {temp_file_path}')
            generate_pdf(temp_file_path, tmp_dir)
            debug(f'.. {org} : generating pdf from {temp_file_path} ... done')

    # merge files if instructed to do so
    if output_spec['merge-files']:
        output_file_path = output_spec['output-dir'] + '/' + output_spec['merged-file-pattern'].format()
        debug(f'{org} : merging odt files')
        merge_files(temp_files, output_file_path)
        debug(f'{org} : merging odt files ... done')

    # generate pdf if instructed to do so
    if output_spec['pdf-output-for-merged-file']:
        debug(f'{org} : generating pdf from merged odt')
        generate_pdf(output_file_path, output_spec["output-dir"])
        debug(f'{org} : generating pdf from merged odt ... done')

    debug(f'{org} : generating output for [{output_processor}] ... done')

    return


'''modify document with tabular data
'''
def output_tabular_data(document_path, tabular_data_specs):
    # open the document
    odt = load_document(document_path)

    for tabular_data_spec in tabular_data_specs:
        table_name = tabular_data_spec["table-name"]

        # get the table
        tbl = get_table(odt, table_name)

        if tbl is None:
            warn(f'Table {table_name} not found')
            # return

        # get number of rows
        # debug(f'Table {table_name} has {number_of_rows(tbl)} rows')

        # put values in rows and columns
        rows_not_populated = populate_table(tbl, tabular_data_spec["rows-for-data"], tabular_data_spec["columns"], tabular_data_spec["data-map"])

        # remove unnecesary rows - from current_row_index to data_end_at_table_row
        remove_rows(tbl, rows_not_populated)

    # save odt
    save_document(odt, document_path)
