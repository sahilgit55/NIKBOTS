import os
import math
import re
import json
import time
import asyncio
from humanfriendly import format_timespan
from helper_fns.helper import TimeFormatter
from pyrogram.errors.exceptions.flood_420 import FloodWait
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE, STDOUT
from helper_fns.helper import hrb, getbotuptime, Timer, timex, create_backgroud_task, get_readable_time, delete_trash, get_human_size
from asyncio import sleep as assleep
from helper_fns.pbar import get_progress_bar_string
from helper_fns.process import get_sub_process, get_master_process
from os.path import getsize

all_data = []
msg_data = ['Processing']
running_process = []
wpositions = {'5:5': 'Set Top Left', 'main_w-overlay_w-5:5': 'Set Top Right', '5:main_h-overlay_h': 'Set Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Set Bottom Right'}


#############Checker################
async def check_task(tid, pid, process_id):
    while True:
        await asyncio.sleep(1)
        if tid not in get_sub_process():
            Cancel = True
            print("🔶Task Cancelled Checker")
            break
        if process_id not in get_master_process():
            Cancel = True
            print("🔶Task Cancelled Checker")
            break
        if pid not in running_process:
            Cancel = False
            print("🔶Task Completed Checker")
            break
    return Cancel


###########Logger###################
async def get_logs(process, tid, pid, process_id):
        Cancel = False
        while True:
                    try:
                            async for line in process:
                                        line = line.decode('utf-8').strip()
                                        print(line)
                                        all_data.append(line)
                                        if len(line)<3800:
                                            msg_data[-1] = line
                                        if tid not in get_sub_process():
                                            Cancel = True
                                            print("🔶Task Cancelled Logger")
                                            break
                                        if process_id not in get_master_process():
                                            Cancel = True
                                            print("🔶Task Cancelled Logger")
                                            break
                                        if pid not in running_process:
                                            print("🔶Task Completed Logger")
                                            break
                    except ValueError:
                            continue
                    else:
                            break
        return Cancel

############Update_Message################
async def update_message(working_dir, COMPRESSION_START_TIME, total_time, mode,message, position, pid, datam, incoming, out_file, subprocess_id, process_id):
    txt = ''
    name = datam[0]
    opt = datam[1]
    remnx = datam[2]
    ptype = datam[3]
    stime = datam[4]
    mtime = datam[5]
    muxing = ['HardMux']
    Cancel = False
    infilesize = get_human_size(getsize(incoming))
    ctext = f"⛔Skip Video: `/cancel sp {str(subprocess_id)}`"
    ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
    if position in muxing:
        position = f'🧬Mode: {str(position)}'
    else:
        try:
            position = wpositions[position]
        except:
            position = position
        position = f'🧬Position: {str(position)}'
    while True:
            await assleep(5)
            print("🔶Updating Message", pid)
            if subprocess_id not in get_sub_process():
                Cancel = True
                print("🔶Task Cancelled Updater")
                break
            if process_id not in get_master_process():
                Cancel = True
                print("🔶Task Cancelled Updater")
                break
            if pid not in running_process:
                print("🔶Task Completed Updater")
                break
            with open(working_dir, 'r+') as file:
                                    text = file.read()
                                    frame = re.findall("frame=(\d+)", text)
                                    time_in_us=re.findall("out_time_ms=(\d+)", text)
                                    bitrate = re.findall("bitrate=(\d+)", text)
                                    fps = re.findall("fps=(\d+)", text)
                                    progress=re.findall("progress=(\w+)", text)
                                    speed=re.findall("speed=(\d+\.?\d*)", text)
                                    if len(frame):
                                        frame = int(frame[-1])
                                    else:
                                        frame = 1;
                                    if len(speed):
                                        speed = speed[-1]
                                    else:
                                        speed = 1;
                                    if len(time_in_us):
                                        time_in_us = time_in_us[-1]
                                    else:
                                        time_in_us = 1;
                                    if len(progress):
                                        if progress[-1] == "end":
                                            break
                                    if len(bitrate):
                                        bitrate = bitrate[-1].strip()
                                    else:
                                        bitrate = "0kbits/s"
                                    if len(fps):
                                        fps = fps[-1].strip()
                                    else:
                                        fps = "0"
                                    execution_time = get_readable_time(time.time() - COMPRESSION_START_TIME)
                                    sptime = get_readable_time(time.time() - stime)
                                    mptime = get_readable_time(time.time() - mtime)
                                    elapsed_time = int(time_in_us)/1000000
                                    out_time = get_readable_time(elapsed_time)
                                    difference = math.floor( (total_time - elapsed_time) / float(speed) )
                                    ETA = "-"
                                    if difference > 0:
                                        ETA = get_readable_time(difference)
                                    perc = f"{elapsed_time * 100 / total_time:.1f}%"
                                    progressx = get_progress_bar_string(elapsed_time, total_time)
                                    botupt = getbotuptime()
                                    try:
                                            logs = all_data[-2] + "\n" + msg_data[-1]
                                    except:
                                        logs = msg_data[-1]
                                    if len(logs)>3800:
                                        logs = msg_data[-1]
                                    pro_bar = f"{str(ptype)} ({opt})\n🎟️File: {name}\n🧶Remaining: {str(remnx)}\n{str(position)}\n♒Preset: {mode}\n🧭Duration: {get_readable_time(total_time)}\n💽In Size: {str(infilesize)}\n\n\n{progressx}\n\n ┌ 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜:【 {perc} 】\n ├ 𝚂𝚙𝚎𝚎𝚍:【 {speed}x 】\n ├ 𝙱𝚒𝚝𝚛𝚊𝚝𝚎:【 {bitrate} kbits/s 】\n ├ 𝙵𝙿𝚂:【 {fps} 】\n ├ 𝚁𝚎𝚖𝚊𝚒𝚗𝚒𝚗𝚐:【 {get_readable_time((total_time - elapsed_time))} 】\n └ 𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚎𝚍:【 {str(out_time)} 】\n\n\n⚡️●●●● 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 ●●●●⚡️\n\n⚙{str(logs)}\n\n\n💾Ot Size: {str(get_human_size(getsize(out_file)))}\n⏰️ETA: {ETA}\n⛓Ex Time: {str(execution_time)}\n🔸Sp Time: {str(sptime)}\n🔹Mp Time: {str(mptime)}\n♥️Bot Uptime: {str(botupt)}\n{str(ctext)}\n{str(ptext)}"
                                    if txt!=pro_bar:
                                            txt=pro_bar
                                            try:
                                                await message.edit(text=pro_bar)
                                            except FloodWait as e:
                                                await asyncio.sleep(e.value)
                                            except Exception as e:
                                                print(e)
    return Cancel


#############Generating Screenshoot######################
async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


######################WaterMark2#############################
async def vidmarkx(the_media, msg, working_dir, watermark_path, output_vid, total_time, mode, position, size, datam, subprocess_id, process_id):
    global all_data
    global msg_data
    Cancel = False
    all_data = []
    msg_data = ['Processing']
    COMPRESSION_START_TIME = time.time()
    command = [
        "ffmpeg", "-hide_banner", "-progress", working_dir, "-i", the_media, "-i", watermark_path,
        "-filter_complex", f"[1][0]scale2ref=w='iw*{size}/100':h='ow/mdar'[wm][vid];[vid][wm]overlay={position}", "-preset", mode, "-codec:a", "copy", output_vid
    ]
    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = asyncio.create_task(check_task(subprocess_id, pid, process_id))
    log_task = asyncio.create_task(get_logs(process.stderr,subprocess_id, pid, process_id))
    update_msg = asyncio.create_task(update_message(working_dir, COMPRESSION_START_TIME, total_time, mode, msg, position, pid, datam, the_media, output_vid, subprocess_id, process_id))
    done, pending = await asyncio.wait([task, process.wait()], return_when=asyncio.FIRST_COMPLETED)
    print("🔶WaterMark Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    print("🔶HardMuxing Return Code", return_code)
    if task not in pending:
                try:
                        print("🔶Terminating Process")
                        process.terminate()
                        print("🔶Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print("🔶Cancelling Task")
                        task.cancelled()
                        print("🔶Awaiting Task")
                        await task
                        print("🔶Checker Task Cancelled")
                except Exception as e:
                        print(e)
    try:
            print("🔶Cancelling Message Updater")
            update_msg.cancelled()
            print("🔶Awaiting Message Updater")
            await update_msg
            print("🔶Message Updater Cancelled")
    except Exception as e:
            print(e)
    try:
            print("🔶Cancelling Logger")
            log_task.cancelled()
            print("🔶Awaiting Logger")
            await log_task
            print("🔶Logger Cancelled")
    except Exception as e:
            print(e)
    if subprocess_id not in get_sub_process():
                Cancel = True
                print("🔶Task Cancelled Watermark")
    if process_id not in get_master_process():
                Cancel = True
                print("🔶Task Cancelled Watermark")
    if Cancel:
        return [True, True]
    elif return_code == 0:
        return [True, False]
    else:
        return [False, all_data]


    
###################HardMuxing########################
async def hardmux_vidx(vid_filename, sub_filename, output, msg, subprocess_id, preset, duration, progress, process_id, datam):
    global all_data
    global msg_data
    Cancel = False
    all_data = []
    msg_data = ['Processing']
    COMPRESSION_START_TIME = time.time()
    command = [
            'ffmpeg','-hide_banner',
            '-progress', progress, '-i', vid_filename,
            '-vf', f"subtitles='{sub_filename}'",
            '-c:v','h264',
            '-map','0:v:0',
            '-map','0:a:0?',
            '-preset', preset,
            '-y',output
            ]
    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = asyncio.create_task(check_task(subprocess_id, pid, process_id))
    log_task = asyncio.create_task(get_logs(process.stderr,subprocess_id, pid, process_id))
    update_msg = asyncio.create_task(update_message(progress, COMPRESSION_START_TIME, duration, preset, msg, 'HardMux', pid, datam, vid_filename, output, subprocess_id, process_id))
    done, pending = await asyncio.wait([task, process.wait()], return_when=asyncio.FIRST_COMPLETED)
    print("🔶HardMuxing Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    print("🔶HardMuxing Return Code", return_code)
    if task not in pending:
                try:
                        print("🔶Terminating Process")
                        process.terminate()
                        print("🔶Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print("🔶Cancelling Task")
                        task.cancelled()
                        print("🔶Awaiting Task")
                        await task
                        print("🔶Checker Task Cancelled")
                except Exception as e:
                        print(e)
    try:
            print("🔶Cancelling Message Updater")
            update_msg.cancelled()
            print("🔶Awaiting Message Updater")
            await update_msg
            print("🔶Message Updater Cancelled")
    except Exception as e:
            print(e)
    try:
            print("🔶Cancelling Logger")
            log_task.cancelled()
            print("🔶Awaiting Logger")
            await log_task
            print("🔶Logger Cancelled")
    except Exception as e:
            print(e)
    if subprocess_id not in get_sub_process():
                Cancel = True
                print("🔶Task Cancelled HardMuxing")
    if process_id not in get_master_process():
                Cancel = True
                print("🔶Task Cancelled HardMuxing")
    if Cancel:
        return [True, True]
    if return_code == 0:
        return [True, False]
    else:
        return [False, all_data]
    
    
    


###################Soft Muxing########################
async def softmux_vidx(vid_filename, sub_filename, output, msg, subprocess_id, preset, duration, progress, process_id, datam):
    global all_data
    global msg_data
    Cancel = False
    all_data = []
    msg_data = ['Processing']
    COMPRESSION_START_TIME = time.time()
    command = [
            'ffmpeg','-hide_banner',
            '-progress', progress, '-i', vid_filename,
            '-i',sub_filename,
            '-map','1:0','-map','0',
            '-disposition:s:0','default',
            '-c:v','copy',
            '-c:a','copy',
            '-c:s','copy',
            '-y',output
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = asyncio.create_task(check_task(subprocess_id, pid, process_id))
    log_task = asyncio.create_task(get_logs(process.stderr,subprocess_id, pid, process_id))
    update_msg = asyncio.create_task(update_message(progress, COMPRESSION_START_TIME, duration, preset, msg, 'SoftMux', pid, datam, vid_filename, output, subprocess_id, process_id))
    done, pending = await asyncio.wait([task, process.wait()], return_when=asyncio.FIRST_COMPLETED)
    print("🔶SoftMuxing Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    print("🔶SoftMuxing Return Code", return_code)
    if task not in pending:
                try:
                        print("🔶Terminating Process")
                        process.terminate()
                        print("🔶Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print("🔶Cancelling Task")
                        task.cancelled()
                        print("🔶Awaiting Task")
                        await task
                        print("🔶Checker Task Cancelled")
                except Exception as e:
                        print(e)
    try:
            print("🔶Cancelling Message Updater")
            update_msg.cancelled()
            print("🔶Awaiting Message Updater")
            await update_msg
            print("🔶Message Updater Cancelled")
    except Exception as e:
            print(e)
    try:
            print("🔶Cancelling Logger")
            log_task.cancelled()
            print("🔶Awaiting Logger")
            await log_task
            print("🔶Logger Cancelled")
    except Exception as e:
            print(e)
    if subprocess_id not in get_sub_process():
                Cancel = True
                print("🔶Task Cancelled SoftMuxing")
    if process_id not in get_master_process():
                Cancel = True
                print("🔶Task Cancelled SoftMuxing")
    if Cancel:
        return [True, True]
    if return_code == 0:
        return [True, False]
    else:
        return [False, all_data]
    


###################Softremove Muxing########################
async def softremove_vidx(vid_filename, sub_filename, output, msg, subprocess_id, preset, duration, progress, process_id, datam):
    global all_data
    global msg_data
    Cancel = False
    all_data = []
    msg_data = ['Processing']
    COMPRESSION_START_TIME = time.time()
    command = [
            'ffmpeg','-hide_banner',
            '-progress', progress, '-i', vid_filename,
            '-i',sub_filename,
            '-map','0:v:0',
            '-map','0:a?',
            '-map','1:0',
            '-disposition:s:0','default',
            '-c:v','copy',
            '-c:a','copy',
            '-c:s','copy',
            '-y',output
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = asyncio.create_task(check_task(subprocess_id, pid, process_id))
    log_task = asyncio.create_task(get_logs(process.stderr,subprocess_id, pid, process_id))
    update_msg = asyncio.create_task(update_message(progress, COMPRESSION_START_TIME, duration, preset, msg, 'Softremove', pid, datam, vid_filename, output, subprocess_id, process_id))
    done, pending = await asyncio.wait([task, process.wait()], return_when=asyncio.FIRST_COMPLETED)
    print("🔶SoftremoveMuxing Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    print("🔶SoftremoveMuxing Return Code", return_code)
    if task not in pending:
                try:
                        print("🔶Terminating Process")
                        process.terminate()
                        print("🔶Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print("🔶Cancelling Task")
                        task.cancelled()
                        print("🔶Awaiting Task")
                        await task
                        print("🔶Checker Task Cancelled")
                except Exception as e:
                        print(e)
    try:
            print("🔶Cancelling Message Updater")
            update_msg.cancelled()
            print("🔶Awaiting Message Updater")
            await update_msg
            print("🔶Message Updater Cancelled")
    except Exception as e:
            print(e)
    try:
            print("🔶Cancelling Logger")
            log_task.cancelled()
            print("🔶Awaiting Logger")
            await log_task
            print("🔶Logger Cancelled")
    except Exception as e:
            print(e)
    if subprocess_id not in get_sub_process():
                Cancel = True
                print("🔶Task Cancelled SoftremoveMuxing")
    if process_id not in get_master_process():
                Cancel = True
                print("🔶Task Cancelled SoftremoveMuxing")
    if Cancel:
        return [True, True]
    if return_code == 0:
        return [True, False]
    else:
        return [False, all_data]