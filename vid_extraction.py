import os
import subprocess

# Paths
videos_directory = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Videos"
frames_directory = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Frames"
output_directory = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Videos"

# Known frames per second (fps) of the videos
fps = 100

# Calculate start and end times based on frame numbers
def frames_to_time(frame, fps):
    return frame / fps

def extract_frame_pairs(tsv_file_path):
    with open(tsv_file_path, 'r') as file:
        lines = file.readlines()

    frame_pairs = []
    start_frame = None

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            frame_number = int(parts[0])
            column_two = int(parts[1])
            frame_value = float(parts[2])

            if column_two == 1:
                if start_frame is None:
                    # Store start frame and value
                    start_frame = (frame_number, frame_value)
                else:
                    # Store end frame and value, and match with previous start frame
                    end_frame = (frame_number, frame_value)
                    frame_pairs.append((start_frame[0], end_frame[0]))
                    start_frame = None
    
    return frame_pairs

# Extract and save each segment using ffmpeg
def extract_segment(video_path, start_frame, end_frame, segment_index, camera_name):
    start_time = frames_to_time(start_frame, fps)
    duration = frames_to_time(end_frame - start_frame, fps)
    
    output_file = f'{output_directory}/{os.path.basename(video_path).replace(".mp4", "")}_segment_{segment_index + 1}_{camera_name}.mp4'
    
    command = [
        'ffmpeg', '-i', video_path, '-ss', str(start_time), '-t', str(duration),
        '-c', 'copy', output_file
    ]
    
    subprocess.run(command)

# Process each frame range file
segment_index = 0
for frame_file in os.listdir(frames_directory):
    if frame_file.endswith('.tsv'):
        frame_file_path = os.path.join(frames_directory, frame_file)
        
        # Extract trial name from frame file (e.g., beetle_x_trial_x.txt)
        trial_name = frame_file.replace('xypts.tsv', '')

        # Process camera-1 and camera-2 videos for each trial
        for camera in ['camera-1', 'camera-2']:
            video_filename = f'{trial_name}_{camera}.mp4'
            video_path = os.path.join(videos_directory, video_filename)
            
            if not os.path.exists(video_path):
                print(f"No video file found for {video_filename}. Skipping.")
                continue
            


            frame_pairs = extract_frame_pairs(frame_file_path)
            for pair in frame_pairs: 
                    start_frame = pair[0]
                    end_frame = pair[1]
                    
                    extract_segment(video_path, start_frame, end_frame, segment_index, camera)
                    segment_index += 1
        
        
print("All segments have been successfully extracted.")