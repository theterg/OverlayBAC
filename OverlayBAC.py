import bug2v4l2 as bg
import sys, time
import Image, ImageDraw, ImageFont

def takePicture(filename):
   # open the bug camera full resolution
   bg.open(dev_code=bg.V4L2_DEVNODE_RESIZER,
           raw_fmt=bg.format(2048,1536, bg.V4L2_PIX_FMT_YUYV),
           resizer_fmt=bg.format(2048,1536))
   
   bg.set_ctrl(bg.V4L2_CID_EXPOSURE, 255) # turn up exposure level
   # start the image stream
   bg.start()
   
   bg.flush()
   bg.set_ctrl(bg.V4L2_CID_FLASH_STROBE, 2) # turn up exposure level
   yuv_img = bg.grab()
   bg.saveimg(yuv_img, filename)
   print "[OVERLAY]  Grabbed ", filename
   bg.stop()
   bg.close()
   
def overlayBAC(filename, bac):
   if bac < 60:
   	color = "green"
   elif bac < 120:
   	color = "yellow"
   else: 
   	color = "red"
   
   font = ImageFont.truetype(
       '/usr/share/fonts/truetype/LiberationSans-Bold.ttf', 300
   )
   im = Image.open(filename)
   draw_image = ImageDraw.Draw(im)
   draw_image.text((0, 0), str(bac), font=font, fill=color)
   im.save(filename, "JPEG")
   
if __name__ == '__main__':
   takePicture(sys.argv[1])
   overlayBAC(sys.argv[1], sys.argv[2])

