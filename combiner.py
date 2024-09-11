import os
import ffmpeg



def combine_mp4_files_from_directory(directory, output_directory, output_filename='output.mp4'):
    input_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp4')]
    # Make output directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Create a concat.txt file holding paths to the clips
    concat_file = os.path.join(output_directory, 'concat.txt')
    with open(concat_file, 'w', encoding='utf-8') as f:
        for input_path in input_paths:
            # Write the absolute path of each file into concat.txt
            absolute_path = os.path.abspath(input_path)
            f.write(f"file '{absolute_path}'\n")
    output_path = os.path.join(output_directory, output_filename)
    # Concatenate the clips
    try:
        ffmpeg.input(concat_file, format='concat', safe=0).output(output_path, c='copy').global_args('-loglevel', 'quiet').run()
        print(f"Successfully combined files into {output_path}")
    except ffmpeg.Error as e:
        print(f"Error during combining files: {e.stderr.decode()}")

if __name__ == '__main__':
    combine_mp4_files_from_directory('league_clips', 'output_directory', 'combined_video.mp4')
