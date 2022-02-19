#!/usr/bin/env python3
'''
    generate templated document from data
'''

def process():
    # get the configuration

    # get to Google

    # get the gsheet

    # load the appropriate gsheet data parser module

    # parse the data

    # load the appropriate gsheet data parser module

class DocumentFromData(object):

    def __init__(self, config_path):
        self.start_time = time.time()
        self._config_path = os.path.abspath(config_path)
        self._log = {'pipeline-reader': []}
        self._data = {}

    def run(self):

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True, help="configuration yml path")
    args = vars(ap.parse_args())

    generator = DocumentFromData(args["config"])
    generator.run()
