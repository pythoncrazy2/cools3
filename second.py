import textwrap
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence


def caption(fn: str, text: str):
    old_im = Image.open(fn)
    ft = old_im.format
    W = old_im.size[0]
    font = ImageFont.truetype('./Fonts/One-Regular.ttf', 10) # replace with your own font

    width = 10
    while True:
        lines = textwrap.wrap(text, width=width)
        if (font.getsize(max(lines, key=len))[0]) > (0.9 * W):
            break
        width += 1

    # amount of lines * height of one line
    bar_height = len(lines) * (font.getsize(lines[0])[1])
    frames = []
    for frame in ImageSequence.Iterator(old_im):
        frame = ImageOps.expand(
            frame,
            border=(0, bar_height, 0, 0),
            fill='white'
        )
        draw = ImageDraw.Draw(frame)
        for i, line in enumerate(lines):
            w, h = draw.multiline_textsize(line, font=font)
            # Position is x: centered, y: line number * height of line
            draw.text(
                ((W - w) / 2, i * h),
                line,
                font=font,
                fill='black'
            )

        del draw
        b = BytesIO()
        frame.save(b, format=ft)
        b.seek(0)
        frames.append(Image.open(b))

    frames[0].save(
        f'out.{ft}',
        save_all=True,
        append_images=frames[1:],
        format=ft,
        loop=0,
        optimize=True
    )
caption(
'./memeimg/1984.gif',
'sus'
)