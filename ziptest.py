'''Unpacking the OpenSubtitles archive is a bad idea if there is any chance you might run out of inodes.
Use the file handling functions in this module instead.'''
import zipfile
import os


if __name__ == '__main__':

    read_zip = zipfile.ZipFile('af.zip', 'r')
    write_zip = zipfile.ZipFile('af_test.zip', 'a')
    in_dir = 'OpenSubtitles/raw'
    lang = 'af'
    subset_years = (1990, 2018)
    ioformat = 'xml'

    filepaths = []
    for filepath in read_zip.namelist():
        if filepath.endswith(ioformat):
            if filepath.startswith(os.path.join(in_dir, lang)):
                if int(filepath.split('/')[3]) in range(*subset_years):
                    filepaths += [filepath]
    for filename in filepaths:
        #thing = read_zip.open(filename).read().decode('utf-8')
        print(filename)
        write_zip.writestr(filename, read_zip.open(filename).read())
