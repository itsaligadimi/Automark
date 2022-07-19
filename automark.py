import marker
import minparser as argp
from os import walk
import magic


argp.app_name = "Automark"
argp.app_description = "Add watermark to video one by one or in bulk"
argp.app_footer_description = "Have fun :P"


def single():
    videos = argp.get_param_arr('v')
    logo = argp.get_param('l')
    output_dir = argp.get_param('out_dir', "")
    for vid in videos:
        marker.add_watermark(vid, logo, output_dir if len(output_dir) else None)



def bulk():
    directory = argp.get_param('d')
    logo = argp.get_param('l')
    output_dir = argp.get_param('out_dir', "")

    if directory[-1] != '/':
        directory += '/'

    mime = magic.Magic(mime=True)
    filenames = next(walk(directory), (None, None, []))[2]
    for fname in filenames:
        if mime.from_file(directory + fname).startswith('video'):
            marker.add_watermark(directory + fname, logo, output_dir if len(output_dir) else None)
    


argp.add_command("single", "mark single file", single)
argp.add_command("bulk", "mark all files in folder", bulk)
argp.run()