import moviepy.editor as me
import time
from random import randint

SECONDS_PER_POSITION = 4
POSITIONS = [
    {"left": 50, "top": 50}, 
    {"left": 50, "top": 50}, 
    {"left": 50, "top": 50}, 
    {"left": 50, "top": 50} 
]



def get_output_filepath(input_filepath, output_dir=None):
    parts = input_filepath.split('/')
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    parts[-1] = "%s_%s_marked" % (parts[-1], timestamp) \
        if parts[-1][-4] != '.' \
            else "%s_%s_marked%s" % (parts[-1][:-4], timestamp, parts[-1][-4:])
    if output_dir is not None:
        if output_dir[-1] != '/':
            output_dir += '/'
        return output_dir + parts[-1]
    else:
        return "/".join(parts)


def calculate_margins(video_size, logo_size):
    # add a top and bottom padding if the video is portrait
    padding = 0
    if video_size[1] > video_size[0]:
        padding = int((video_size[1] - video_size[0]) / 2)

    pos = randint(1, 4)
    left = 0
    top = 0
    if pos == 1:   # top left
        left = 50
        top = 50 + padding
    elif pos == 2: # top right
        left = video_size[0] - 50 - logo_size[0]
        top = 50 + padding
    elif pos == 3: # bottom left
        left = 50
        top = video_size[1] - 50 - logo_size[1] - padding
    elif pos == 4: # bottom right
        left = video_size[0] - 50 - logo_size[0]
        top = video_size[1] - 50 - logo_size[1] - padding
    return (left, top)


def build_logo(logo_filepath, duration, height, video_size):
    image = me.ImageClip(logo_filepath).set_duration(duration).resize(height=height)
    margins = calculate_margins(video_size, image.size)
    return image.margin(left=margins[0], top=margins[1], opacity=0)
            


def add_watermark(video_filepath, logo_filepath, output_dir=None):
    video = me.VideoFileClip(video_filepath)
    # image = me.ImageClip(logo_filepath)

    # calculate different position count based on video duration
    # change position every 5 second
    pos_count = int(video.duration / SECONDS_PER_POSITION)
    last_part_duration = video.duration % SECONDS_PER_POSITION

    if pos_count:
        logos = []
        for i in range(pos_count):
            logos.append(build_logo(logo_filepath, SECONDS_PER_POSITION, 150, video.size))
        logos.append(build_logo(logo_filepath, last_part_duration, 150, video.size))

        logo = me.concatenate_videoclips(logos)
    else:
        logo = build_logo(logo_filepath, last_part_duration, 150, video.size)

    final = me.CompositeVideoClip([video, logo])
    output_filepath = get_output_filepath(video_filepath, output_dir)
    final.write_videofile(output_filepath)