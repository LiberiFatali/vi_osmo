"""
Author: HieuNM

Flipping, and Mirroring
Transpose and Transverse, Diagonally
Rectangular Rotates
#Imploding Images
#Exploding Images
http://www.imagemagick.org/Usage/warping/


rotation: [0-45] [45-90] [90-135] [135-180], seam_carve, (translation, shear, stretch)

relight, noise...

Seam Carving
http://scikit-image.org/docs/dev/auto_examples/plot_seam_carving.html

"""

import argparse
import imghdr
import numpy as np
import os
# import skimage
import random
import shutil
from scipy import ndimage
from scipy.misc import imread, imsave, imshow
from skimage import *

# import matplotlib.pyplot as plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate augumented version of input image')
    parser.add_argument('--filepath', type=str, help="Path to input image")
    parser.add_argument('--folder', type=str, help="Path to input folder")
    args = parser.parse_args()

    if args.folder:  # process folder tree
        for dirpath, dirnames, filenames in os.walk(args.folder):
            for d in dirnames:
                if ' ' in d:
                    d_nospace = d.replace(' ', '_')
                    os.rename((os.path.join(dirpath, d)), os.path.join(dirpath, d_nospace))
                    # prepare folder structure
                # aug_list = ['flipud', 'fliplr', 'rot90', 'rot45', 'rotRand', 'angle_rotated', 'augmented']
        aug_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # for a in aug_list:
        # aug_folder = '/'.join([args.folder, a])
        # if not os.path.exists(aug_folder):
        # os.makedirs(aug_folder)

        for dirpath, dirnames, filenames in os.walk(args.folder, topdown=True):
            # skip augmented folders
            if os.path.basename(dirpath) in aug_list:
                continue
            # prepare augmented folder structure
            for a in aug_list:
                aug_folder = os.path.join(dirpath, a)
                if os.path.exists(aug_folder):
                    shutil.rmtree(aug_folder)
                if len(filenames) > 0:
                    os.makedirs(aug_folder)
                    # process files
            for f in filenames:
                # Process image files only
                file_local = os.path.join(dirpath, f)
                # if any(file_ext in f for file_ext in IMG_EXT):
                # if ('.' + str(imghdr.what(file_local)) in IMG_EXT):
                if (str(imghdr.what(file_local)) != 'None'):
                    # Remove whitespaces in filename
                    if ' ' in f:
                        f_nospace = f.replace(' ', '_')
                        os.rename((os.path.join(dirpath, f)), os.path.join(dirpath, f_nospace))
                        f = f_nospace
                        file_local = os.path.join(dirpath, f)
                    # Do augumentation
                    # load file
                    img = imread(file_local)
                    try:
                        # up <-> down flip
                        flip_ud_img = np.flipud(img)
                        # left <-> right flip
                        flip_lr_img = np.fliplr(img)
                        ##rotation
                        # rotated_90_img = np.rot90(img)
                        # rotated_45_img = ndimage.rotate(img, 45)
                        # rotated_random_img = ndimage.rotate(img, random.random()*360)
                        # augmented version from 0 -> 360 degree
                        augmented_path = os.path.join(dirpath, f[1:2])
                        for angle in xrange(0, 360):
                            augmented_org_img = ndimage.rotate(img, angle, reshape=False)
                            augmented_flipud_img = ndimage.rotate(flip_ud_img, angle, reshape=False)
                            augmented_fliplr_img = ndimage.rotate(flip_lr_img, angle, reshape=False)
                            # save to disk
                            imsave(os.path.join(augmented_path, 'org_' + str(angle) + f), augmented_org_img)
                            imsave(os.path.join(augmented_path, 'flipud_' + str(angle) + f), augmented_flipud_img)
                            imsave(os.path.join(augmented_path, 'fliplr_' + str(angle) + f), augmented_fliplr_img)

                            ## save augumented images to disk
                            ##toname = file_local[:-4]
                            ##fname = os.path.splitext(f)[0]
                            ##ext = file_local[-3:]
                        # imsave(os.path.join(dirpath, 'flipud', 'flipud_'+f), flip_ud_img)
                        # imsave(os.path.join(dirpath, 'fliplr', 'fliplr_'+f), flip_lr_img)
                        # imsave(os.path.join(dirpath, 'rot90', 'rot90_'+f), rotated_90_img)
                        # imsave(os.path.join(dirpath, 'rot45', 'rot45_'+f), rotated_45_img)
                        # imsave(os.path.join(dirpath, 'rotRand', 'rotRand_'+f), rotated_random_img)
                    except Exception, e:
                        print "Error: ", str(e)
                        continue


    elif args.filepath:  # process a single file
        # read image
        # filepath = 'data/cat.jpg'
        # img=plt.imread('cat.jpg')
        filepath = args.filepath
        img = imread(filepath)

        # up <-> down flip
        flip_ud_img = np.flipud(img)
        # left <-> right flip
        flip_lr_img = np.fliplr(img)
        # rotation
        rotated_90_img = np.rot90(img)
        rotated_45_img = ndimage.rotate(img, 45)
        rotated_random_img = ndimage.rotate(img, random.random() * 360)

        ## display
        # imshow(img)
        # imshow(flip_ud_img)
        # imshow(flip_lr_img)
        # imshow(rotated_90_img)
        # imshow(rotated_45_img)
        # imshow(rotated_random_img)

        # save augumented images to disk
        # tokens = filepath.split(".")
        # toname = tokens[:-1]
        # ext = tokens[-1]
        toname = filepath[:-4]
        ext = filepath[-3:]

        imsave(toname + '_flipud.' + ext, flip_ud_img)
        imsave(toname + '_fliplr.' + ext, flip_lr_img)
        imsave(toname + '_rot90.' + ext, rotated_90_img)
        imsave(toname + '_rot45.' + ext, rotated_45_img)
        imsave(toname + '_rotRand.' + ext, rotated_random_img)


    # %%
    # Seam Carving

    # from skimage import data, draw
    # from skimage import transform, util
    # import numpy as np
    # from skimage import filters, color
    # from matplotlib import pyplot as plt
    #
    #
    ##img = data.rocket()
    # img = imread('cat.jpg')
    # img = util.img_as_float(img)
    # eimg = filters.sobel(color.rgb2gray(img))
    #
    # plt.title('Original Image')
    # plt.imshow(img)
    #
    ##%%
    # resized = transform.resize(img, (img.shape[0], img.shape[1] - 200))
    # plt.figure()
    # plt.title('Resized Image')
    # plt.imshow(resized)
    #
    ##%%
    ##out = transform.seam_carve(img, eimg, 'vertical', 200)
    # out = transform.seam_carve(img, eimg, 'vertical', 200, border=1)
    # plt.figure()
    # plt.title('Resized using Seam-Carving')
    # plt.imshow(out)

    # %%
