import os
import shutil
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
    if not os.path.exists('target'):
        os.mkdir('target')

    print_table_header()
    print_separator()

    for file in os.listdir('data'):
        try:
            if file.endswith('.txt'):
                os.system('gzip -fk9 data/%s' % file)
                shutil.move('data/%s.gz' % file, 'target/%s.gz' % file)
                encoder.encode('data/'+file, 'target/'+file+'.encoded')
                os.system('gzip -fk9 target/%s.encoded' % file)

                print_table_entry(file, fsize('data/'+file), fsize('target/'+file + '.gz'), fsize('target/'+file + '.encoded'), fsize('target/'+file + '.encoded.gz'))

                encoder.decode('target/'+file + '.encoded')
                assert fsize('target/'+file + '.encoded.decoded') == fsize('data/'+file), file

                with open('target/'+file + '.encoded.decoded', 'r') as fp:
                    with open('data/'+file, 'r') as fp2:
                        assert fp.read() == fp2.read()
        except:
            print 'error in', file
            raise

    print_separator()
