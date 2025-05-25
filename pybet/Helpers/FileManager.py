from pybet.models.ReturningData import ReturningData
from chromologger import Logger as Log
from chromolog import Print
import csv
from csv import reader, writer
import json
from pathlib import Path

# File to save logs
log: Log = Log('./pybet/logs/log.log')
# Messages in console with colors
printer: Print = Print()

class FileManager:
    """ Manage files, read, write and more """
    @staticmethod
    def read_file_plain(filename:str) -> ReturningData:
        """ Trying to get the contents of a plain text file
            :param filename: Name of the file to read (including path)
            :return: Data with information and errors (if any). **{ok: bool, data: any | None, error: any | None}**
        """
        __data: ReturningData = ReturningData(False)
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content:str = file.read()
                if len(content.strip()) > 0:
                    __data.data = content
                    __data.ok = True
                else:
                    __data.error = f'The file "{filename}" is null'
                    FileManager.null_warn(filename)
        except Exception as e:
            FileManager.__save_data_error(__data,f'read_file_plain(): {e}', e)
            FileManager.print_exception_message()
        return __data

    @staticmethod
    def write_file(file_name:str, content:any = None, mode:str = 'w') -> bool:
        """ Writing content to plain text files
        :param file_name: Plain text file name (including path)
        :param content: Content to be added
        :param mode: Writing mode (`a`, `w`), default `w`
        :return: A boolean that will indicate whether the content could be written into the file
        """
        __written:bool = False
        is_json:bool = Path(file_name).suffix == '.json'
        # Check if open mode is valid
        if mode.strip() in ['a', 'w']:
            try:
                # Check the content first
                if content is not None and len(content.strip()) > 0:
                    with open(file_name, mode, encoding='utf-8') as file:
                        # Write the content into the file
                        # Is a JSON file (Write as JSON)
                        if is_json: json.dump(content, file, indent=4, ensure_ascii=False)
                        # Is other file type (Write as plain text)
                        else: file.write(f'{content}\n')
                        __written = True
                else: FileManager.null_warn()
            except Exception as e:
                log.log_e(e)
                FileManager.print_exception_message()
        return __written

    @staticmethod
    def read_file_csv(csv_filename:str | None = None) -> ReturningData:
        """ Trying to get the contents of a plain **CSV** file
        :param csv_filename: Name of the file to read (including path)
        :return: Data with information and errors (if any). **{ok: bool, data: any | None, error: any | None}**
        """
        __data:ReturningData = ReturningData()
        try:
            with open(csv_filename, 'r', encoding='utf-8') as file:
                reader_csv:reader = csv.reader(file)
                # Skip the header
                next(reader_csv)
                # Contain data in a list format
                __list_from_reader:list[list[str]] = list(reader_csv)
                # Senda data or error in the returning
                if len(__list_from_reader) > 0: __data.data = __list_from_reader
                else:
                    FileManager.__save_data_error(__data,f'The "{csv_filename}" is empty')
                    FileManager.null_warn(csv_filename)
        except Exception as e:
            FileManager.__save_data_error(__data, f'read_file_csv(): {e}', e)
        return __data

    @staticmethod
    def read_file_json(json_filename:str) -> ReturningData:
        """ Trying to get the contents of a plain **JSON** file
                :param json_filename: Name of the file to read (including path)
                :return: Data with information and errors (if any). **{ok: bool, data: any | None, error: any | None}**
        """
        __data:ReturningData = ReturningData()
        try:
            with open(json_filename, 'r', encoding='utf-8') as file:
                json_content:dict | list = json.load(file)
                if type(json_content) == dict and len(json_content.keys()) == 0 or len(json_content) == 0:
                    __data.error = f'The file "{json_filename}" is null'
                    FileManager.null_warn(json_filename)
                else:
                    __data.data = json_content
        except Exception as e:
            FileManager.__save_data_error(__data,f'read_file_json(): {e}', e)
        return __data

    @staticmethod
    def __save_data_error(return_instance: ReturningData, msg_error: str | None = None, error: Exception | None = None) -> None:
        """ Add the Exception in a file "log.log" and add to ReturningData.
        :param return_instance: ReturningData instance to save information.
        :param msg_error: Information to add to the instance of ReturningData.
        :param error: If data error is an Exception.
        :return: None
        """
        # Save the error in a file "log.log"
        if error is not None: log.log_e(error)
        return_instance.error = msg_error

    @staticmethod
    def print_exception_message() -> None:
        """ Indicates to the user/developer that there was an exception """
        printer.err(f'[Error] Has been a error, please try again')

    @staticmethod
    def null_warn(filename:str | None = None) -> None:
        """ Displays a warning about a file or content that is empty/no data
        :param filename: Name of the file that was attempted to be read (Optional)
        :return: None
        """
        if filename is not None: printer.warn(f'The file "{filename}" is null')
        else: printer.warn(f'[Warn] Did not pass any content to write')