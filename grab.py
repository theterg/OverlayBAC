import bug2v4l2 as bg
import sys, time
import Image, ImageDraw, ImageFont

# open the bug camera full resolution
bg.open(dev_code=bg.V4L2_DEVNODE_RESIZER,
        raw_fmt=bg.format(2048,1536, bg.V4L2_PIX_FMT_YUYV),
        resizer_fmt=bg.format(2048,1536))

# start the image stream
bg.start()

bg.flush()
yuv_img = bg.grab()
filename = sys.argv[1]
bg.saveimg(yuv_img, filename)
bac = sys.argv[2]
print "Grabbed", filename


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
draw_image.text((0, 0), bac, font=font, fill=color)
im.save(filename, "PNG")

bg.stop()
bg.close()


