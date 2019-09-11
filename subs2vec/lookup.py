"""Look up items in large lists of frequencies, norms, or vectors."""
import argparse


def lookup(big_fname, items_fname):
    """Line-wise Lookup of a list of items in a large file.

    :param big_fname: filename of large file to look up items in
    :param items_fname: filename of list of items to look up
    """
    out_fname = f'lookup.{items_fname}'
    with open(big_fname, 'r') as big_file, open(items_fname, 'r') as items_file, open(out_fname, 'w') as out_file:
        items = items_file.read().split('\n')
        items = [item for item in items if item != '']
        for line in big_file:
            for item in items:
                if item in line:
                    out_file.write(line)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count words in files in a given directory')
    argparser.add_argument('big_fname', help='large file to look up items in')
    argparser.add_argument('items_fname', help='file containing list of items to look up')
    args = argparser.parse_args()
    
    lookup(**vars(args))
