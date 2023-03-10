from asyncio import sleep as asynciosleep
from pyrogram.errors import FloodWait
from helper_fns.helper import hrb, getbotuptime, Timer, timex



def get_progress_bar_string(current,total):
    completed = int(current) / 8
    total = int(total) / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 6
    p_str = 'β ' * cFull
    p_str += 'β‘' * (16 - cFull)
    p_str = f"[{p_str}]"
    return p_str

timer = Timer(7)

async def progress_bar(current,total,reply,start,*datam):
      if timer.can_send():
        now = timex()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            sp=str(hrb(speed))+"ps"
            tot=hrb(total)
            cur=hrb(current)
            progress = get_progress_bar_string(current,total)
            try:
                name = datam[0]
                opt = datam[1]
                remnx = datam[2]
                ptype = datam[3]
                ps = datam[4]
                botupt = getbotuptime()
                pro_bar = f"{str(ptype)} ({opt})\nποΈFile: {name}\nπ§ΆRemaining: {str(remnx)}\n\n\n {str(progress)}\n\n β πΏπππππππ:γ {perc} γ\n β πππππ:γ {sp} γ\n β {ps}:γ {cur} γ\n β πππ£π:γ {tot} γ\n\n\nβ₯οΈBot Uptime: {str(botupt)}"
                await reply.edit(pro_bar)
            
            except FloodWait as e:
                    await asynciosleep(e.value)
            except Exception as e:
                    print(e)
