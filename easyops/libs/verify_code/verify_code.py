import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter

def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))

def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill="black", width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    width, height = 120, 50
    im = Image.new("RGB", (width, height), "#F9F9F9")
    font = ImageFont.truetype("arial.ttf", 40)
    draw = ImageDraw.Draw(im)
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=rndColor(), font=font)

    draw_lines(draw, 2, width, height)

    im = im.filter(ImageFilter.GaussianBlur(radius=1.0))
    return im, code