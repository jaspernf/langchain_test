import logging
from pathlib import Path
from datetime import datetime
import time
import pandas as pd

class Runner:
    """For data collectionn""" #pylint: disable=too-many-instance-attributes
    def __init__(self, project_name='',  output_type='csv', **kwargs):
        self.project_name = project_name
        self.outdir = f'../../output/{project_name}'
        self.inputdir = f'../../input/{project_name}'
        self.timestamp = datetime.now().strftime('%Y%m%d')
        self.prefix = f"{project_name}_{self.timestamp}"
        self.output_subdir = project_name
        self.checkpoint = None
        self.__output_type = output_type
        self.headers = ['PDF', 'Company', 'Owner Name', 'Owner Email', 'Order Type', 'Line Item Number',
                        'SKU Name', 'SKU Sub Name', 'SKU Price', 'SKU Quantity', 'SKU Discount', 'SKU Total',
                        'SKU Term in Months', 'Order Subtotal', 'Order Tax', 'Order Total', 'Currency', 'Renewal',
                        'Payment Terms', 'Special Terms', 'Start Date', 'Duration', 'End Date', 'Buyer Address',
                        'Buyer Name', 'Buyer Email', 'Seller Name', 'Seller Email', 'sku_format_index', 'date_format_accuracy']


    def run(self, **kwargs):
        """ Run the process """
        start_time = time.time()

        logging.info("Making Directory if directory empty")

        Path(f'{self.outdir}').mkdir(parents=True, exist_ok=True)


        logging.info("Get raw data")
        raw = self.get_raw(**kwargs)

        logging.info("Save raw data")
        self.save_raw(raw,**kwargs)

        logging.info("Normalize data")
        data = self.normalize(raw, **kwargs)

        logging.info("Save normalized data to output")
        self.save_output(data, **kwargs)

        logging.info("Clean up")
        self.cleanup()

        print("--- %s seconds ---" % (time.time() - start_time))
        return data

    def get_raw(self, **kwargs):
        """Get raw data from the source"""
        raise ImplementationException('get_raw')

    def normalize(self,raw,**kwargs):
        """Normalize raw and return final result"""
        logging.info('Implement normalize() in your sub-class if needed, otherwise return raw: raw=%s, kwargs=%s',type(raw),kwargs)
        data_frame = pd.DataFrame(raw, columns=self.out.header(), )
        data_frame.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"],
                           value=["", ""], regex=True, inplace=True)
        return data_frame

    def save_raw(self,raw,**kwargs):
        """Save raw data to file"""
        logging.info('Implement save_raw() yourself if needed: raw=%s, kwargs=%s', type(raw),kwargs)

    def save_output(self, data, **kwargs):
        """Save final data to output file"""
        if self.__output_type == 'csv':
            func = self.save_output_csv
        elif self.__output_type == 'json':
            func = self.save_output_json
        elif self.__output_type == 'excel':
            func = self.save_output_excel
        else:
            raise UnsupportedOutputTypeException(self.__output_type)
        return func(data,**kwargs)

    def save_output_csv(self, data, index=False, **kwargs):
        """Save data into csv file
        :param data: pandas DataFrame
        """
        file = self.get_output_file('csv')
        logging.info("Save final output: file=%s, index=%s, kwargs=%s",file,index,kwargs)
        data.to_csv(file, index=index, encoding='utf-8', **kwargs)
        return file

    def save_output_json(self, data, index=False, **kwargs):
        """Save data into csv file
        :param data: pandas DataFrame
        """
        file = self.get_output_file('json')
        logging.info("Save final output: file=%s, index=%s, kwargs=%s",file,index,kwargs)
        data.to_json(file, orient="split")
        return file

    def save_output_excel(self, data, index=False, **kwargs):
        """ Save final data to output file
        :param data: pandas DataFrame
        """
        file = self.get_output_file('xlsx')
        logging.info("Save final output: file=%s, index=%s, kwargs=%s", file,index,kwargs)
        data.to_excel(file,index=index, encoding='utf-8', **kwargs)
        return file

    def get_output_file(self,suffix):
        """Return output file path"""
        _path = self.outdir
        _path = f'{_path}/{self.project_name}_{datetime.now().strftime("%Y%m%d")}.{suffix}'
        return _path

    def cleanup(self):
        """Clean up"""
        if self.checkpoint:
            self.checkpoint.clean()



class UnsupportedOutputTypeException(Exception):
    '''Exception raised for unsupported file type'''
    def __init__(self,output_type):
        self.output_type = output_type
        super().__init__(f'Supported output types are [csv,excel]: output_type={self.output_type}'
                         'Implement save_output() in your sub-class')

class ImplementationException(Exception):
    """Exception raised for implementing a method"""
    def __init__(self,method):
        self.method = method
        super().__init__(f'Please implement {self.method}() in your sub-class')
