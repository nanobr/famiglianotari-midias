import sys, os, subprocess
import cairo
from draw import *

ep = None  # episode module, set in main()
RW, RH = 1080, 1920
STAGE_Y = 400
BAND_H = 330


def comic(path, w=1080, h=1350):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(*hexc("#FFF8EE"))
    ctx.paint()
    m = 16
    pw = (w - 3 * m) / 2
    s = pw / W
    crop_top, crop_bot = 10, 1200
    ph = (crop_bot - crop_top) * s
    top = h - (2 * ph + 2 * m)
    # title
    set_font(ctx, 54)
    ctx.set_source_rgba(*INK)
    tw = ctx.text_extents(ep.HOOK).x_advance
    ctx.move_to((w - tw) / 2, top / 2 + 20)
    ctx.show_text(ep.HOOK)
    for i, ((fn, _), ft) in enumerate(zip(ep.SCENES, ep.FINAL_T)):
        col, row = i % 2, i // 2
        x = m + col * (pw + m)
        y = top + row * (ph + m)
        ctx.save()
        rrect(ctx, x, y, pw, ph, 22)
        ctx.clip()
        ctx.translate(x, y)
        ctx.scale(s, s)
        ctx.translate(0, -crop_top)
        fn(ctx, ft)
        ctx.restore()
        rrect(ctx, x, y, pw, ph, 22)
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(6)
        ctx.stroke()
    surf.write_to_png(path)


def hook_band(ctx):
    ctx.set_source_rgba(*hexc("#C2502E"))
    ctx.rectangle(0, 0, RW, BAND_H)
    ctx.fill()
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.move_to(0, BAND_H)
    ctx.line_to(RW, BAND_H)
    ctx.stroke()
    lines = wrap(ctx, ep.HOOK, 66, 900)
    set_font(ctx, 66)
    ctx.set_source_rgba(1, 1, 1, 1)
    lh = 80
    y0 = 200 - (len(lines) - 1) * lh / 2
    for i, l in enumerate(lines):
        tw = ctx.text_extents(l).x_advance
        ctx.move_to((RW - tw) / 2, y0 + i * lh)
        ctx.show_text(l)


def end_card(ctx, k):
    if k <= 0:
        return
    y = 1440 + (1 - ease_out(k)) * 600
    ctx.save()
    rrect(ctx, 50, y, 860, 140, 40)
    ctx.set_source_rgba(*hexc("#2B1E18", 0.93))
    ctx.fill()
    lines = wrap(ctx, ep.END_CARD, 48, 820)
    set_font(ctx, 48)
    ctx.set_source_rgba(1, 1, 1, 1)
    lh = 66
    y0 = y + 70 - (len(lines) - 1) * lh / 2 + 17
    for i, l in enumerate(lines):
        tw = ctx.text_extents(l).x_advance
        ctx.move_to(480 - tw / 2, y0 + i * lh)
        ctx.show_text(l)
    ctx.restore()


def reel_frame(ctx, idx, t):
    fn, _ = ep.SCENES[idx]
    ctx.save()
    ctx.translate(0, STAGE_Y)
    fn(ctx, t)
    ctx.restore()
    hook_band(ctx)
    if idx == len(ep.SCENES) - 1:
        end_card(ctx, (t - ep.END_CARD_AT) / 0.45)


def still(idx, t, path):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, RW, RH)
    ctx = cairo.Context(surf)
    reel_frame(ctx, idx, t)
    surf.write_to_png(path)


def render_scene(idx, path, fps=30):
    _, dur = ep.SCENES[idx]
    n = int(round(dur * fps))
    tmp = path[:-4] + ".part.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{RW}x{RH}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "18",
                          "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(fps), tmp],
                         stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, RW, RH)
    for f in range(n):
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
        reel_frame(ctx, idx, f / fps)
        surf.flush()
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, path)
    else:
        raise SystemExit(f"ffmpeg failed on scene {idx}")


def main():
    import importlib.util, shutil
    global ep
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    spec = importlib.util.spec_from_file_location("episode", src)
    ep = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    spec.loader.exec_module(ep)
    assert len(ep.SCENES) == 4, "a tirinha precisa de exatamente 4 cenas"
    work = os.path.join(out, "_work")
    os.makedirs(work, exist_ok=True)
    comic(os.path.join(out, "tirinha.png"))
    if "--stills" in sys.argv:
        for idx, t in enumerate(ep.FINAL_T):
            still(idx, t, os.path.join(work, f"still_s{idx+1}.png"))
        return
    parts = []
    for idx in range(4):
        p = os.path.join(work, f"scene{idx+1}.mp4")
        render_scene(idx, p)
        parts.append(p)
    with open(os.path.join(work, "list.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    from audio import make_audio
    make_audio(ep, os.path.join(work, "audio.wav"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(work, "list.txt"), "-c", "copy", os.path.join(work, "video.mp4")], check=True)
    tmp = os.path.join(out, "reel.part.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(work, "video.mp4"), "-i",
                    os.path.join(work, "audio.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, os.path.join(out, "reel.mp4"))
    shutil.rmtree(work)


if __name__ == "__main__":
    main()
