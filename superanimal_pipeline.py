import os
import deeplabcut

def segment_videos(folder_name):
    bitrate_factor = 16
    segment_duration = 600 # 10 minutes

    os.chdir(folder_name)
    cwd = os.getcwd()
    input_video = [f for f in os.listdir(cwd) if f.endswith('.avi')][0] # gets the first video in the folder
    output_dir = f"{cwd}/segmented_videos" # creates an output folder for our filtered videos
    segment_duration = 10 # in minutes

    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use ffmpeg to get video duration
    command = f'ffprobe -i {input_video} -show_entries format=duration -v quiet -of csv="p=0"'
    output = os.popen(command).read()
    video_duration = float(output)

    # Calculate number of segments needed
    num_segments = int(video_duration // (segment_duration * 60)) + 1

    # Execute the ffmpeg command to get the bitrate of the video
    command = f"ffmpeg -i {input_video} 2>&1 | grep bitrate"
    output = os.popen(command).read()

    # Extract the bitrate value from the output
    bitrate_index = output.find("kb/s")
    if bitrate_index != -1:
        bitrate_str = output[bitrate_index-6:bitrate_index].strip()
        video_bitrate = int(bitrate_str)
    else:
        return -1

    # Modify our bitrate by our bitrate factor
    video_bitrate/=bitrate_factor

    input_video_prefix = input_video[:-4]

    # Loop through each segment
    for i in range(num_segments):
        start_time = i * segment_duration * 60
        count_for_file = str(i)
        count_for_file = count_for_file.zfill(3)
        segment_filename = f"{output_dir}/{input_video_prefix}_{count_for_file}.avi"

        # Use ffmpeg to segment video
        command = f'ffmpeg -i {input_video} -ss {start_time} -t {segment_duration * 60} -b:v {video_bitrate}k -vf format=gray {segment_filename}'
        os.system(command)

def pipeline(folder_name):
    os.chdir(folder_name)
    cwd = os.getcwd()
    # vvv if we want to run multiple folders at the same time vvv
    # folders = [f.path for f in os.scandir(cwd) if f.is_dir()]
    # video_folders = [f for f in folders if f[:3]=="MLA"]
    # for folder_name in video_folders:

    segmented_videos = os.path.join(cwd, "segmented_videos")

    segmented_videos = os.listdir(segmented_videos)

    # for video_path in segmented_videos:
    project_name = f'{folder_name}_DLCproject'
    your_name = 'Cameron Young'
    # video_path = deeplabcut.DownSampleVideo(video_path, width=300)
    config_path, train_config_path = deeplabcut.create_pretrained_project(
        project_name,
        your_name,
        segmented_videos,
        videotype="avi",
        model="superanimal_topviewmouse",
        analyzevideo=True,
        createlabeledvideo=True,
        copy_videos=True, #must leave copy_videos=True
    )
if __name__ == "__main__":
    pipeline('MLA109')



    

