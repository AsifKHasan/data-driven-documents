#!/usr/bin/env python3
'''
    Tkinter GUI for salary advice generation
    python sscl-salary-advice-app.py
'''
import os
import yaml
import time

import threading
import queue
import subprocess

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from sscl_advice_generator import AdviceGenerator


class SalaryAdviceApp:
    def __init__(self, master, config):
        self.config = config

        # master.geometry('500x250')

        # month and mode selection
        self.top_frame = tk.LabelFrame(master, text='Month and disbursement mode')
        self.top_frame.pack(padx=10, pady=10)

        self.selected_month = tk.StringVar(master)
        self.selected_month.set(self.config['selection']['selected-month'])

        self.selected_mode = tk.StringVar(master)
        self.selected_mode.set(self.config['selection']['selected-mode'])

        self.month_label = tk.Label(self.top_frame, text='Month')
        self.month_option = tk.OptionMenu(self.top_frame, self.selected_month, *self.config['master-data']['months'], command = lambda x: self.save_selection(None))
        self.mode_label = tk.Label(self.top_frame, text='Mode')
        self.mode_frame = tk.Frame(self.top_frame)
        for v in self.config['master-data']['modes']:
            rb = tk.Radiobutton(self.mode_frame, text=v, variable=self.selected_mode, value=v, command = lambda : self.show_options(None))
            rb.pack(side=tk.RIGHT)

        self.month_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        self.month_option.grid(row=0, column=1, padx=10, sticky=tk.E)
        self.mode_label.grid(row=1, column=0, padx=10, sticky=tk.W)
        self.mode_frame.grid(row=1, column=1, padx=10, sticky=tk.E)

        # separator
        separator = ttk.Separator(self.top_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        # option frame bank
        self.selected_bank_account = tk.StringVar(master)
        self.selected_bank_account.set(self.config['selection']['selected-account'])

        self.selected_bank_reference = tk.StringVar(master)
        self.selected_bank_reference.set(self.config['selection']['selected-reference'])

        self.bank_account_label = tk.Label(self.top_frame, text='Account')
        self.bank_account_option = tk.OptionMenu(self.top_frame, self.selected_bank_account, *self.config['master-data']['bank-accounts'], command = lambda x: self.save_selection(None))

        self.bank_reference_label = tk.Label(self.top_frame, text='Reference')
        self.bank_reference_entry = tk.Entry(self.top_frame, textvariable=self.selected_bank_reference, validate='key', validatecommand = lambda: self.save_selection(None))

        current_row = 3
        self.bank_account_label.grid(row=current_row, column=0, padx=10, sticky=tk.W)
        self.bank_account_option.grid(row=current_row, column=1, padx=10, sticky=tk.E)
        current_row = 4
        self.bank_reference_label.grid(row=current_row, column=0, padx=10, sticky=tk.W)
        self.bank_reference_entry.grid(row=current_row, column=1, padx=10, sticky=tk.E)

        self.show_options(None)

        # buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill='both', expand='yes', padx=10, pady=5)

        self.quit_button = tk.Button(self.button_frame, text='QUIT', bg="#FFC0CB", command=master.quit)
        self.quit_button.pack(side=tk.RIGHT, pady=5)

        self.generate_button = tk.Button(self.button_frame, text='Generate', fg="#008000", command=self.process, state=tk.DISABLED)
        self.generate_button.pack(side=tk.LEFT, pady=5)

        self.top_frame.grid_columnconfigure(0, minsize=80)
        self.top_frame.grid_columnconfigure(1, minsize=300)

    def show_options(self, _):

        if self.selected_mode.get() in ['Cash', 'Cheque']:
            self.bank_account_label.grid_forget()
            self.bank_account_option.grid_forget()
            self.bank_reference_label.grid_forget()
            self.bank_reference_entry.grid_forget()

        elif self.selected_mode.get() == 'Bank':
            current_row = 3
            self.bank_account_label.grid(row=current_row, column=0, padx=10, sticky=tk.W)
            self.bank_account_option.grid(row=current_row, column=1, padx=10, sticky=tk.E)
            current_row = 4
            self.bank_reference_label.grid(row=current_row, column=0, padx=10, sticky=tk.W)
            self.bank_reference_entry.grid(row=current_row, column=1, padx=10, sticky=tk.E)

        else:
            pass

        self.save_selection(None)

    def save_selection(self, _):
        self.config['selection']['selected-month'] = self.selected_month.get()
        self.config['selection']['selected-mode'] = self.selected_mode.get()
        self.config['selection']['selected-account'] = self.selected_bank_account.get()
        self.config['selection']['selected-reference'] = self.selected_bank_reference.get()
        yaml.dump(self.config, open('../conf/config-sscl.yml', 'w', encoding='utf-8'))

        return True

    def init_generator(self):

        self.advice_generator = AdviceGenerator()
        result = self.advice_generator.init(os.path.abspath('../conf/credential-spectrum-895-221613.json'), os.path.abspath('../template/sscl'), os.path.abspath('../out/sscl'))
        if result and result['success'] == False:
            messagebox.showerror('Error', result['msg'])
            self.generate_button.configure(state=tk.DISABLED)
        else:
            self.generate_button.configure(state=tk.NORMAL)

    def process(self):
        self.save_selection(None)

        # call the genarator
        result = self.advice_generator.generate_pdf(self.config['selection'])
        if result and result['success']:
            subprocess.Popen(result['pdf-path'], shell=True)
        else:
            messagebox.showerror('Error', result['msg'])


class ThreadedClient(threading.Thread):

    def __init__(self, queue, fcn):
        threading.Thread.__init__(self)
        self.queue = queue
        self.fcn = fcn

    def run(self):
        time.sleep(1)
        self.queue.put(self.fcn())


def spawnthread(fcn, queue):
    thread = ThreadedClient(queue, fcn)
    thread.start()
    periodical(thread)

def periodical(thread):
    if(thread.is_alive()):
        root.after(100, lambda: periodical(thread))

if __name__ == '__main__':
    # configuration
    config = yaml.load(open('../conf/config-sscl.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)

    root = tk.Tk()
    root.title('SSCL : Salary advice generator')

    app = SalaryAdviceApp(root, config)
    queue = queue.Queue()
    spawnthread(app.init_generator, queue)
    root.mainloop()

    root.destroy()
