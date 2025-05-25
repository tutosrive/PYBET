from pybet.helpers.FileManager import FileManager

def run():
    # Missing check that content is a real JSON ({key:value}
    write = FileManager.write_file('pybet/data/write_test1.json', "{'key':'value'}", 'a')