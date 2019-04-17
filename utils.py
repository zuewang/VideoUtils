import glob
import os
import argparse
from tqdm import tqdm
import cv2


def video2image(video_path, output_dir):
    vidcap = cv2.VideoCapture(video_path)
    in_fps = vidcap.get(cv2.CAP_PROP_FPS)
    print('video fps:', in_fps)

    if_continue = False
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        if_continue = True
    elif len(os.listdir(output_dir) ) != 0:
        if_continue = input('{} is not empty. Do you want to continue (y/n)? '.format(output_dir)) == 'y'

    if not if_continue:
        print('stop here')
        return
    
    loaded, frame = vidcap.read()
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('frames processed')
    for i_frame in tqdm(range(total_frames)):
        frame_name = os.path.join(output_dir, f'{i_frame:05}' + '.jpg')
        cv2.imwrite(frame_name, frame)
        loaded, frame = vidcap.read()


def image2video(image_dir, video_path, fps, image_ext):
    image_files = sorted(glob.glob(os.path.join(image_dir, '*.{}'.format(image_ext))))
    print(len(image_files))
    height, width, _ = cv2.imread(image_files[0]).shape
    
    out_fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out_video = cv2.VideoWriter(video_path, out_fourcc, fps, (width, height))

    for image_file in tqdm(image_files):
        img = cv2.imread(image_file)
        out_video.write(img)
    
    out_video.release()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Process videos')
    subparser = parser.add_subparsers()

    video2image_parser = subparser.add_parser('video2image', help = 'parse video to images')
    video2image_parser.add_argument('video_path', type = str, help = 'path to the video file')
    video2image_parser.add_argument('output_dir', type = str, help = 'path to the directory to place parsed images')
    video2image_parser.set_defaults(func = lambda args: video2image(args.video_path, args.output_dir))

    image2video_parser = subparser.add_parser('image2video', help = 'convert images in directory to video')
    image2video_parser.add_argument('image_dir', type = str, help = 'path to the directory containing images')
    image2video_parser.add_argument('video_path', type = str, help = 'path to the output video file (mp4)')
    image2video_parser.add_argument('fps', type = float, help = 'frame per second of output video')
    image2video_parser.add_argument('--image_ext', type = str, default = 'jpg', help = 'extension for the images (default as jpg)')
    image2video_parser.set_defaults(func = lambda args: image2video(args.image_dir, args.video_path, args.fps, args.image_ext))
    
    args = parser.parse_args()
    args.func(args)
    