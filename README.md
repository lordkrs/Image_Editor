# IMAGE_EDITOR
Computer vision using python image library(PIL)

usage: ./image_editor [-h] [-s S] [-d D] [-g] [-c C] [-t] [-r R]
                    [-rotate ROTATE] [-crop CROP] [-paste PASTE]
                    [-transpose TRANSPOSE]

optional arguments:

  -h, --help            show this help message and exit
  
  -s S                  Source path of the Image

  -d D                  Destination path of the Image
  
  -g                    converts image to greyscale
  
  -c C                  converts image extention to some other image extension
  
  -t                    To create thumbnail of source image, by default
                        resolution will be 128x128 to specify resolution --res
                        128x128
  
  -r R                  Changes resolution syntax should be widthxheight, can
                        be used with option -t or --thumb
  
  -rotate ROTATE        Rotate image syntax should be degree ex 45
  
  -crop CROP            Crop image syntax should be left,upper,right,lower ex
                        100,100,400,400
  
  -paste PASTE          Should be used with crop syntax should be
                        left,upper,right,lower ex 100,100,400,400
  
  -transpose TRANSPOSE  Rotate crpped image syntax should be degree ex 90
                        (180,270) Can only be used on cropped image
