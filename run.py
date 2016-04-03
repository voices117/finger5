import os
import encoder
import subprocess

from stat import ST_SIZE


COL_WIDTH = 11


def fsize(filename):
    return os.path.getsize(filename)


def print_table_header():
    print '|', ' | '.join(s.center(COL_WIDTH) for s in ['filename', 'original', 'gz', 'encoded', 'encoded gz']), '|'


def print_separator():
    print '|', '-' * (5 * COL_WIDTH + 12), '|'


def print_table_entry(file, original, gz, encoded, enc_gz):
    print '|', ' | '.join(str(x).rjust(COL_WIDTH) for x in [file, original, gz, encoded, enc_gz]), '|'


if __name__ == '__main__':
    print_table_header()
    print_separator()

    for file in os.listdir('.'):
        try:
            if file.endswith('.txt'):
                os.system('gzip -fk9 %s' % file)
                encoder.encode(file)
                os.system('gzip -fk9 %s.encoded' % file)

                print_table_entry(file, fsize(file), fsize(file + '.gz'), fsize(file + '.encoded'), fsize(file + '.encoded.gz'))

                encoder.decode(file + '.encoded')
                assert fsize(file + '.encoded.decoded') == fsize(file), file

                with open(file + '.encoded.decoded', 'r') as fp:
                    with open(file, 'r') as fp2:
                        assert fp.read() == fp2.read()
        except:
            print 'error in', file
            raise

    print_separator()
