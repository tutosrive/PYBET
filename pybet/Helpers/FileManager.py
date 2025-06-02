from pathlib import Path
import csv
import json
from chromologger import Logger as Log
from chromolog import Print
from pybet.models.OperationResult import OperationResult

# Logger to save errors and information
log: Log = Log('./pybet/logs/log.log')
# Printer to show colored messages on console
printer: Print = Print()

class FileManager:
    """Manage files (plain text, JSON, CSV), returning OperationResult."""

    @staticmethod
    def read_file_plain(filename: str) -> OperationResult:
        """
        Reads a plain text file and returns its content.

        Args:
            filename (str): Path to the file.

        Returns:
            OperationResult: ok/data (str) or error.
        """
        result = OperationResult(ok=False)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            if content.strip():
                result.ok = True
                result.data = content
            else:
                FileManager.__save_data_error(result, f'The file "{filename}" is empty')
                printer.warn(result.error)
        except Exception as e:
            FileManager.__save_data_error(result, f'read_file_plain(): {e}', e)
            FileManager.print_exception_message()
        return result

    @staticmethod
    def write_file(file_name: str, content: any = None, mode: str = 'w') -> OperationResult:
        """
        Writes content to a file. If .json extension, serializes as JSON; otherwise writes plain text.

        Args:
            file_name (str): Path to the file.
            content (any): Data to write.
            mode (str): 'w' or 'a'.

        Returns:
            OperationResult: ok True if written; error otherwise.
        """
        result = OperationResult(ok=False)
        if mode not in ('w', 'a'):
            FileManager.__save_data_error(result, f'Invalid mode "{mode}".')
            return result

        is_json = Path(file_name).suffix == '.json'
        try:
            # Ensure directory exists
            Path(file_name).parent.mkdir(parents=True, exist_ok=True)
            with open(file_name, mode, encoding='utf-8') as f:
                if is_json:
                    json.dump(content, f, indent=4, ensure_ascii=False)
                else:
                    f.write(str(content))
            result.ok = True
        except Exception as e:
            FileManager.__save_data_error(result, f'write_file(): {e}', e)
            FileManager.print_exception_message()
        return result

    @staticmethod
    def read_file_csv(csv_filename: str) -> OperationResult:
        """
        Reads a CSV file (skipping optional header) and returns rows as List[List[str]].

        Args:
            csv_filename (str): Path to CSV.

        Returns:
            OperationResult: ok/data (List[List[str]]) or error.
        """
        result = OperationResult(ok=False)
        try:
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader_csv = csv.reader(f)
                next(reader_csv, None)  # Skip header if present
                rows = list(reader_csv)
            if rows:
                result.ok = True
                result.data = rows
            else:
                FileManager.__save_data_error(result, f'The CSV file "{csv_filename}" is empty')
                printer.warn(result.error)
        except Exception as e:
            FileManager.__save_data_error(result, f'read_file_csv(): {e}', e)
            FileManager.print_exception_message()
        return result

    @staticmethod
    def write_file_csv(file_name: str, rows: list[list[str]], header: list[str] | None = None, mode: str = 'w') -> OperationResult:
        """
        Writes a list of rows (optionally with header) to a CSV file.
        """
        result = OperationResult(ok=False)
        if mode not in ('w', 'a'):
            FileManager.__save_data_error(result, f'Invalid CSV mode "{mode}"')
            return result
        try:
            Path(file_name).parent.mkdir(parents=True, exist_ok=True)
            with open(file_name, mode, newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if header:
                    writer.writerow(header)
                writer.writerows(rows)
            result.ok = True
        except Exception as e:
            FileManager.__save_data_error(result, f'write_file_csv(): {e}', e)
            FileManager.print_exception_message()
        return result

    @staticmethod
    def read_file_json(json_filename: str) -> OperationResult:
        """
        Reads a JSON file and returns the parsed object (dict or list).

        Args:
            json_filename (str): Path to JSON.

        Returns:
            OperationResult: ok/data or error.
        """
        result = OperationResult(ok=False)
        try:
            with open(json_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # If data is empty list or dict, warn but still return ok with empty data
            if (isinstance(data, list) and not data) or (isinstance(data, dict) and not data):
                printer.warn(f'The JSON file "{json_filename}" is empty')
            result.ok = True
            result.data = data
        except Exception as e:
            FileManager.__save_data_error(result, f'read_file_json(): {e}', e)
            FileManager.print_exception_message()
        return result

    @staticmethod
    def print_exception_message() -> None:
        """Prints a generic error message to console."""
        printer.err('[Error] An exception occurred, please try again.')

    @staticmethod
    def null_warn(filename: str | None = None) -> None:
        """
        Prints a warning when content is null or missing.

        Args:
            filename (str | None): Name of the affected file.
        """
        if filename:
            printer.warn(f'The file "{filename}" is null or empty')
        else:
            printer.warn('[Warn] No content provided to write')

    @staticmethod
    def __save_data_error(result: OperationResult, msg_error: str, error: Exception = None) -> None:
        """
        Centralizes error handling: logs the exception and sets the OperationResult.

        Args:
            result (OperationResult): The result object to populate.
            msg_error (str): Error message to assign.
            error (Exception, optional): The caught exception to log.
        """
        if error is not None:
            log.log_e(error)
        result.ok = False
        result.error = msg_error