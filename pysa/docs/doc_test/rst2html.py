from docutils import core

def convert_files(file_name):
    source = open(file_name, 'r')
    file_dest = file_name[:-4] + '.html'
    destination = open(file_dest, 'w')
    core.publish_file(source=source, destination=destination, writer_name='html')
    source.close()
    destination.close()

convert_files('PYSA.MAN.rst')
