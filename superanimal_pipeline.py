import os
import deeplabcut
import sys

def segment_videos(video_file):
    bitrate_factor = 16
    segment_duration = 600 # 10 minutes

    root_dir = os.path.dirname(video_file)
    #input_video = [f for f in os.listdir(cwd) if f.endswith('.avi')][0] # gets the first video in the folder
    

    output_dir = os.path.join(root_dir, "segmented_videos") # creates an output folder for our filtered videos
    segment_duration = 10 # in minutes

    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created {output_dir}")

    # Use ffmpeg to get video duration
    command = f'ffprobe -i {video_file} -show_entries format=duration -v quiet -of csv="p=0"'
    output = os.popen(command).read()
    video_duration = float(output)

    # Calculate number of segments needed
    num_segments = int(video_duration // (segment_duration * 60)) + 1

    # Execute the ffmpeg command to get the bitrate of the video
    # see https://write.corbpie.com/getting-video-bitrate-with-ffprobe/
    command = f"ffprobe -v quiet -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 {video_file}"
    output = os.popen(command).read().split('\n')

    if output[0].isnumeric():
        # divide by 1000 to get it in kbps
        video_bitrate = int(output[0])/1000
    else:
        print(f"Could not determine bitrate from ffprobe output: {output}. Exiting")
        sys.exit()


    # Modify our bitrate by our bitrate factor
    video_bitrate/=bitrate_factor

    #input_video_prefix = video_file[:-4]
    input_video_prefix = os.path.splitext(os.path.basename(video_file))[0]

    # Loop through each segment
    for i in range(num_segments):
        start_time = i * segment_duration * 60
        count_for_file = str(i)
        count_for_file = count_for_file.zfill(3)
        segment_filename = os.path.join(output_dir, f"{input_video_prefix}_{count_for_file}.avi")
        print(segment_filename)

        # Use ffmpeg to segment video
        command = f'ffmpeg -i {video_file} -ss {start_time} -t {segment_duration * 60} -b:v {video_bitrate}k -vf format=gray {segment_filename}'
        os.system(command)



def pipeline(folder_name):
    segmented_folder = os.path.join(folder_name, "segmented_videos")
    segmented_list = os.listdir(segmented_folder)

    segmented_videos = []

    for file in segmented_list:
        file_path = os.path.join(segmented_folder, file)
        # might need to actually check if this is a video
        if os.path.isfile(file_path):
            segmented_videos.append(repr(file_path))

    # TODO: change this at some point
    project_name = f'{folder_name}_DLCproject'
    your_name = 'CY'

    config_path, train_config_path = deeplabcut.create_pretrained_project(
        project_name,
        your_name,
        segmented_videos,
        videotype="avi",
        model="superanimal_topviewmouse",
        analyzevideo=True,
        createlabeledvideo=False,
        copy_videos=True, #must leave copy_videos=True
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    args = parser.parse_args()
    video_file = args.path
    segment_videos(video_file)
    folder_name = os.path.dirname(video_file)
    pipeline(folder_name)

