import cv2
import numpy as np
from numpy.linalg import inv
from numpy.linalg.linalg import LinAlgError

import argparse
import os

def get_parser():
    parser = argparse.ArgumentParser()

    # File I/O
    parser.add_argument("--datapath", default='../data/output',
                        help="Path to the directory containing the source image.")
    parser.add_argument("--file", default='linear_single_vertical_gaussian_g1.jpg',
                        help="Name of the source image file.")
    parser.add_argument("--savepath", default='../data/output',
                        help="Path to the output storage directory \
                                (automatically generated if not yet there).")
    parser.add_argument("--save", type=str, default=None,
                        help="Name of the output file storing the results \
                                (not saved if not provided).")
    parser.add_argument("--save-format", type=str, default='jpg',
                        help="File format of the output file (default: JPEG).")
    parser.add_argument("--seed", type=int, default=0,
                        help="Seed value for 'np.random.seed'.")
    return parser

def warp_image(image):
    pass

def main():
    parser = get_parser()
    args = parser.parse_args()

    # Load image
    original = cv2.imread(os.path.join(args.datapath,args.file), cv2.IMREAD_COLOR)
    H, W, _ = original.shape

    # Warp the input image
    '''
    # Test I: Transform an image so that a distorted item in the image is recovered

    src_points = np.zeros((4,2), dtype="float32")
    src_points[0] = [165,775]    # top-left
    src_points[1] = [1470,750]    # top-right
    src_points[2] = [1690,1680]    # bottom-right
    src_points[3] = [350,1915]    # bottom-left

    dst_H = 600
    dst_W = 800
    dst_points = np.zeros((4,2), dtype="float32")
    dst_points[0] = [dst_W // 4, dst_H // 4]    # top-left
    dst_points[1] = [dst_W // 4 * 3, dst_H // 4]   # top-right
    dst_points[2] = [dst_W // 4 * 3, dst_H // 4 * 3]   # bottom-right
    dst_points[3] = [dst_W // 4, dst_H // 4 * 3]   # bottom-left
    '''

    # Test II: Warp an image

    ### Set the corners of the image as source points
    src_points = np.zeros((4,2), dtype="float32")
    src_points[0] = [0,0]    # top-left (w,h)
    src_points[1] = [W-1,0]    # top-right (w,h)
    src_points[2] = [W-1,H-1]    # bottom-right (w,h)
    src_points[3] = [0,H-1]    # bottom-left (w,h)

    ### Dest image dimensions
    dst_H = 600
    dst_W = 800

    ### Randomly generate dest points within the given margins
    t_margin = [0,0.1]
    b_margin = [0.9,1]
    l_margin = [0,0.1]
    r_margin = [0.9,1]
    np.random.seed(args.seed)
    tl_h, tr_h = np.random.randint(*[H * val for val in t_margin], size=2)
    bl_h, br_h = np.random.randint(*[H * val for val in b_margin], size=2)
    tl_w, bl_w = np.random.randint(*[W * val for val in l_margin], size=2)
    tr_w, br_w = np.random.randint(*[W * val for val in r_margin], size=2)

    dst_points = np.zeros((4,2), dtype="float32")
    dst_points[0] = [tl_w, tl_h]    # top-left
    dst_points[1] = [tr_w, tr_h]   # top-right
    dst_points[2] = [br_w, br_h]   # bottom-right
    dst_points[3] = [bl_w, bl_h]   # bottom-left

    ### Compute warp matrices
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(original, M, (dst_W, dst_H))

    test_img = np.zeros((H,W,3), dtype=np.uint8)
    for col in range(0,W,4):
        for row in range(H):
            test_img[row,col,:] = 255
    for row in range(0,H,4):
        for col in range(W):
            test_img[row,col,:] = 255
    test_warped = cv2.warpPerspective(test_img, M, test_img.shape[-2::-1])

    # Define windows
    #cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    #cv2.namedWindow("warped", cv2.WINDOW_NORMAL)
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.namedWindow("test_warped", cv2.WINDOW_NORMAL)

    # Display result
    #cv2.imshow("original", original)
    #cv2.imshow("warped", warped)
    cv2.imshow("test", test_img)
    cv2.imshow("test_warped", test_warped)
    cv2.waitKey(0)

    '''
    # Save output
    if args.save:
        if not os.path.isdir(args.savepath):
            os.makedirs(args.savepath)
        save_name = args.save + '.' + args.save_format
        cv2.imwrite(os.path.join(args.savepath, save_name), warped)
    '''

if __name__ == "__main__":
    main()
