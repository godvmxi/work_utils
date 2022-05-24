#!/usr/bin/env python3
import cv2
import numpy as np
import os
import subprocess as sp
import argparse
args = None

def get_args_parse():
    parser = argparse.ArgumentParser('传入参数：***.py')
    parser.add_argument('-iw','--width', type=int, default=1920, help="input frame width")
    parser.add_argument('-ih','--height', type=int, default=1088, help="input frame height")
    parser.add_argument('-ox','--offset_x', type=int, default=64, help="watermark start offset x")
    parser.add_argument('-oy','--offset_y', type=int, default=128, help="watermark start offset y")
    parser.add_argument('-i','--input', default="input.yuv")
    parser.add_argument('-o','--output', default="out.yuv")
    parser.add_argument('-th','--text_height', type=int, default=100, help="watermark text height")
    parser.add_argument('-prefix','--prefix', default="", help="watermarker prefix, such as AMD-0")
    parser.add_argument('-s','--show',help="show image one by one", action="store_true")
    parser.add_argument('-n','--frame_number',type=int, default=0,help="handle n frames")
    parser.add_argument('-f','--font_file',type=str, default="/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",help="handle n frames")
    return parser
def add_watermark_to_frame(frame, txt, text_height, offset, fontname="/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"):
    ft = cv2.freetype.createFreeType2()
    ft.loadFontData(fontFileName=fontname,
                    id=0)
    ft_size, baseline= ft.getTextSize(txt, text_height, -1)
    #print("Msg: {0} {1} dat: {2}".format(ft_size, baseline, txt))
    magin_pixel = 5
    rectangle_start = (offset[0] + baseline - magin_pixel, offset[1] - ft_size[1] - baseline - magin_pixel )
    rectangle_end = (offset[0] + ft_size[0] + magin_pixel ,  offset[1] + baseline + magin_pixel) #
    #print("start: {0} -> end: {1}".format(rectangle_start, rectangle_end))
    cv2.rectangle(frame,
        rectangle_start,
        rectangle_end,
        (250,240,240),
        -1
        )
    ft.putText(img=frame,
            text=txt,
            org=(offset[0], offset[1]),
            fontHeight=text_height,
            color=(255,  10, 10),
            thickness=-1,
            line_type=cv2.LINE_AA,
            bottomLeftOrigin=True)
    return frame

if __name__ == "__main__":
    args = get_args_parse().parse_args()
    print(args)
    print(args.width)
    #get_watermark("temp")
    cap = cv2.VideoCapture(args.input)
    total_frames = int( cap.get(cv2.CAP_PROP_FRAME_COUNT) )
    input_width = int(cap.get(3))
    input_height = int(cap.get(4))
    video_info = 'video : {0}x{1} frames:{2}'.format(input_width, input_height, total_frames)
    print(video_info)
    print("total frames :", total_frames)

    fourcc = cv2.VideoWriter_fourcc(*'X264')
    video_output = cv2.VideoWriter(args.output, fourcc, 30.0, (input_width, input_height))
    if args.frame_number > 0 and args.frame_number < total_frames:
        total_frames = args.frame_number
        print("processing frame number is : ", total_frames)
    for index in range(total_frames):
        # set frame position
        #cap.set(cv2.CAP_PROP_POS_FRAMES,index)
        ret, frame = cap.read()
        marker_text = '{0}{1:0>2}'.format(args.prefix, index)
        add_watermark_to_frame(frame, marker_text,args.text_height, (args.offset_x, args.offset_y), args.font_file)
        video_output.write(frame)
        if args.show:
            cv2.imshow("Video", frame)
            if cv2.waitKey(5000) & 0xFF == ord('q'):
                break
    cap.release()
    video_output.release()
    cv2.destroyAllWindows()

