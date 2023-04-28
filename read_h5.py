import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

def overlay_points_on_video(video_path, df1, df2):
    # Load the video
    cap = cv2.VideoCapture(video_path)
    
    # Get the video width and height
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the color of the points
    color1 = (0, 0, 255) # Red
    color2 = (255, 0, 0) # Blue

    bodyparts = ["nose", "left_ear", "right_ear", "neck", "mid_backend", "tail_base"]

    for b in bodyparts:
        df1_filtered = [col for col in df1.columns if col[1]==b]
        df1_x = df1[df1_filtered[0]]
        df1_y = df1[df1_filtered[1]]
        df2_filtered = [col for col in df2.columns if col[1]==b]
        df2_x = df2[df2_filtered[0]]
        df2_y = df2[df2_filtered[1]]

        for f in range(len(df1_x)):
            ret, frame = cap.read()
            print(df1_x[f], "within vid func", b, end ="\r")
            if ret:
                if not math.isnan(df1_x[f]):
                    cv2.circle(frame, (int(df1_x[f]), int(df1_y[f])), 5, color1, -1)
                if not math.isnan(df2_x[f]):
                    cv2.circle(frame, (int(df2_x[f]), int(df2_y[f])), 5, color2, -1)
                # Display the frame with the overlaid points
                cv2.imshow('frame', frame)

            # Exit if 'q' is pressed
                if cv2.waitKey(25) & 0xFF == ord('q'):
                      break
            else:
                break

    # Release the video and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

def read_h5(filename):
     

    #Use Euclidian distance between two video's x and y coords to determine how accurate our videos are

    # Create csv file
    df = pd.read_hdf(filename)

    # Filter data to only include body parts we want
    # df.filter(items=['left_ear', 'right_ear'])
    df.to_csv(f'{filename[:-3]}.csv')

    # Use deeplabcut's make_labeled_video.py (bookmarked) to create a labeled video from our new table.

def compare_h5(path1, path2):
    df1 = pd.read_hdf(path1)
    df2 = pd.read_hdf(path2)

    bodyparts = ["nose", "left_ear", "right_ear", "neck", "mid_backend", "tail_base"]

    data = {}

    for b in bodyparts:
        data[b] = {}
        df1_filtered = [col for col in df1.columns if col[1]==b]
        df1_x = df1[df1_filtered[0]]
        df1_y = df1[df1_filtered[1]]
        df2_filtered = [col for col in df2.columns if col[1]==b]
        df2_x = df2[df2_filtered[0]]
        df2_y = df2[df2_filtered[1]]

        # for f in [frame for frame in df1.index if "frame" in frame]:

        distance = np.linalg.norm([df2_x - (4*df1_x), df2_y - (4*df1_y)], axis=0)
        data[b] = distance

    fig, ax = plt.subplots()

    # Loop through the dictionary and plot each list of values as a line
    for key, values in data.items():
        ax.plot(values, label=key)

    # Add a legend and axis labels
    ax.legend()
    ax.set_xlabel('Frames')
    ax.set_ylabel('Distance')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path1')
    parser.add_argument('--path2')
    parser.add_argument('--videopath')
    args = parser.parse_args()
    first_h5 = args.path1
    second_h5 = args.path2
    video_path = args.videopath
    read_h5(second_h5)
    read_h5(first_h5)
    compare_h5(first_h5, second_h5)
    df1 = pd.read_hdf(first_h5)
    df2 = pd.read_hdf(second_h5)
    overlay_points_on_video(video_path, df1, df2)

# C:\Users\dlc\MLA109\segmented_videos_color\behavior_video2023-02-22T12_07_56_000DLC_snapshot-1000.h5

# C:\Users\dlc\MLA109\segmented_videos\behavior_video2023-02-22T12_07_56_000DLC_snapshot-1000.h5

# C:\Users\dlc\MLA109\segmented_videos_color\behavior_video2023-02-22T12_07_56_000.mp4

# python read_h5.py --path1 C:\Users\dlc\MLA109\segmented_videos_color\behavior_video2023-02-22T12_07_56_000DLC_snapshot-1000.h5 --path2 C:\Users\dlc\MLA109\segmented_videos\behavior_video2023-02-22T12_07_56_000DLC_snapshot-1000.h5 --videopath C:\Users\dlc\MLA109\segmented_videos_color\behavior_video2023-02-22T12_07_56_000.mp4

# C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_000DLC_snapshot-200000.h5

# C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_001DLC_snapshot-200000.h5

# C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_000.mp4

# python read_h5.py --path1  C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_000DLC_snapshot-200000.h5 --path2 C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_001DLC_snapshot-200000.h5 --videopath C:\Users\dlc\MLA086\2022-11-24\segmented_videos_color2\behavior_video2022-11-24T08_07_02_000.mp4

# C:\Users\dlc\MLA086\2022-11-24\segmented_videos\behavior_video2022-11-24T08_07_02_000.avi

# C:\Users\dlc\MLA086\2022-11-24\segmented_videos2\behavior_video2022-11-24T08_07_02_000.avi

# python read_h5.py --path1 C:\Users\dlc\MLA086\2022-11-24\segmented_videos2\behavior_video2022-11-24T08_07_02_000DLC_snapshot-1000.h5 --path2 C:\Users\dlc\MLA086\2022-11-24\predictions\behavior_video2022-11-24T08_07_02_000DLC_snapshot-1000.h5 --videopath C:\Users\dlc\MLA086\2022-11-24\segmented_videos2\behavior_video2022-11-24T08_07_02_000.avi