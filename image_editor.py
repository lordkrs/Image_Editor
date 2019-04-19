#!/usr/bin/env python
import os
import sys
from PIL import Image

import logging
import logging.handlers
import argparse

def get_logger(logger_path=None, log_data=False):
    logger = logging.getLogger()
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s")
    if log_data:
        if not logger_path:
            raise Exception("logger path not specified")
        logger_dir = os.path.dirname(logger_path)
        if not os.path.exists(logger_dir):
            raise Exception("Invalid logger directory, directory doesn't exists")
        logger_name = os.path.basename(os.path.splitext(logger_path)[0])
        logger = logging.getLogger(logger_name)
        fileHandler = logging.handlers.RotatingFileHandler(logger_dir+ os.path.sep + logger_name + ".log", maxBytes=1*1024*1024*1021, backupCount=2)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger


def image_editor(src_image, dst_image, grayscale=False, convert_to=None, thumb=False,resolution=None, rotate=False, rotate_degree=None, crop=None, paste=None):
    logger.info("[image_editor]:[src_image:({}),dst_image:({}),grayscale:({}),convertto({}),thumnail({}),resolution({}), rotate({}), \
                  rotate_degree({}), crop({}), paste({})]".format(src_image,dst_image,grayscale,convert_to,thumb,resolution,rotate, rotate_degree,crop,paste))
    status = -1
    try:
        pil_im = Image.open(src_image)
        if grayscale:
            pil_im = pil_im.convert("L")

        if crop:
            region = pil_im.crop(crop["points"])
            if crop.get("transpose"):
                region = region.transpose(crop["transpose"])
            
            if paste:
                pil_im.paste(region, paste["points"])
            else:
                pil_im = region                

        if thumb:
            pil_im.thumbnail(resolution)      

        if rotate:
            pil_im = pil_im.rotate(rotate_degree)

        if resolution:
            pil_im = pil_im.resize(resolution)

        #pil_im.show()
        pil_im.save(dst_image)

        file_stat_info = os.stat(dst_image)
        if not file_stat_info.st_size:
            os.remove(dst_image)
            raise Exception("Invalid dst file size")

    except Exception as ex:
        logger.error("[image_editor]:[Error while converting {} to {}, exception({}) ".format(src_image,dst_image, ex))
        status = -1
    
    return status


if __name__ == "__main__":
    status = -1
    logger = get_logger()
    parser = argparse.ArgumentParser("Image Editor")
    parser.add_argument("-s", action="store", help="Source path of the Image",)
    parser.add_argument("-d", action="store", help="Destination path of the Image")
    parser.add_argument("-g", action="store_true", help="converts image to greyscale")
    parser.add_argument("-c", action="store", help="converts image extention to some other image extension")
    parser.add_argument("-t", action="store_true", help="To create thumbnail of source image, by default resolution will be 128x128 to specify resolution --res 128x128")
    parser.add_argument("-r", action="store", help="Changes resolution syntax should be widthxheight, can be used with option -t or --thumb ")
    parser.add_argument("-rotate", action="store", help="Rotate image syntax should be degree ex 45")
    parser.add_argument("-crop", action="store", help="Crop image syntax should be left,upper,right,lower ex 100,100,400,400")
    parser.add_argument("-paste", action="store", help="Should be used with crop syntax should be left,upper,right,lower ex 100,100,400,400")
    parser.add_argument("-transpose", action="store", help="Rotate crpped image syntax should be degree ex 90 (180,270) Can only be used on cropped image")

    try:

        args = parser.parse_args()
        src_path = args.s if args.s else None
        dst_path = None
        convert_to = args.c if args.c else None
        grayscale = True if args.g else False
        thumbnail = True if args.t else False
        resolution = None
        rotate = True if args.rotate else False
        rotate_degree = None
        crop = {}
        paste = {}
 
        if thumbnail or args.r:
            hw = []
            resolution = args.r if args.r else "128x128"
            for data in resolution.split("x"):
                hw.append(int(data))
                
            resolution =tuple(hw)
            if len(resolution) != 2:
                raise Exception("Invalid value given for resolution")

        if rotate:
            rotate_degree = int(args.rotate)

        if args.crop:
            crop_details = []
            for data in args.crop.split(","):
                crop_details.append(int(data))
            crop["points"] = tuple(crop_details)
            if args.transpose:
                degree_dict = {"90":Image.ROTATE_90,"180":Image.ROTATE_180, "270":Image.ROTATE_270}
                if args.transpose not in degree_dict:
                    raise Exception("Invalid transpose option provided [90,180,270]")
                crop["transpose"] = degree_dict[args.transpose]

        if args.paste:
            if crop is None:
                raise Exception("paste can only be used with crop")
            paste_details = []
            for data in args.paste.split(","):
                paste_details.append(int(data))
            paste["points"] = tuple(paste_details)

        if convert_to is not None:
            if not convert_to.startswith("."):
                convert_to = "." + convert_to

        if src_path is None:
            raise Exception("Source path not provided")
        elif not os.path.exists(src_path):
            raise Exception("Invalid src path->({}) provided".format(src_path))

        if convert_to is None:
            dst_path = args.d if args.d else None 
        elif convert_to and not args.d:
            dst_path = os.path.splitext(src_path)[0] + convert_to
        
        if dst_path is None:
            raise Exception("Destination path not provided")
        elif os.path.exists(dst_path):
            raise Exception(" Destination path->({}) already exists".format(dst_path)) 

        if src_path == dst_path:
            raise Exception("src_path{} and dst_path{} should not be same".format(src_path,dst_path))
        

        status = image_editor(src_path, dst_path,grayscale=grayscale,convert_to=convert_to,thumb=thumbnail,resolution=resolution, rotate=rotate, rotate_degree=rotate_degree,\
                              crop=crop, paste=paste)

    except Exception as ex:
        logger.info("for help: {} --help".format(sys.argv[0]))
        logger.error("[Main]:[Error occurred in main function {} to {}, exception({}) ".format(src_path,dst_path, ex))
    sys.exit(status)