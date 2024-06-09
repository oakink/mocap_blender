import os
from . import file, environ
import subprocess
import time
import threading
import psutil
from queue import Queue
import platform

fileQ = Queue()


# Yield successive n-sized
# chunks from l.
def __divide_chunks(list, n):
    # looping till length l
    for i in range(0, len(list), n):
        yield list[i : i + n]


def __startProcessThread(q, index):
    while True:
        path = q.get()
        if path == "end":
            print(f"[THREAD-{index}] Exit On End")
            q.task_done()
            break
        if not os.path.exists(path):
            print(f"THREAD-{index}] Command File Not Found: {path}")
            q.task_done()
            continue
        print(f"[THREAD-{index}] Working On: {path}")
        with open(os.path.splitext(path)[0] + ".log", "w") as f:
            if platform.system().lower() == "windows":
                process = subprocess.Popen(f"{path}", shell=True, stdout=f, stderr=f)
            elif platform.system().lower() == "linux":
                process = subprocess.Popen(f"chmod +x {path}&&{path}", shell=True, stdout=f, stderr=f)
            else:
                q.task_done()
                raise Exception("系统未支持: " + platform.system().lower())
            process.wait()
        q.task_done()
        print(f"[THREAD-{index}] Done")


def batchProcess(workspace_home, script, file_list, batch_size=1, process_count=1, args={}):
    index = 0
    pid = os.getpid()
    for i in range(process_count):
        thread = threading.Thread(
            None,
            __startProcessThread,
            args=(
                fileQ,
                i,
            ),
            daemon=True,
        )
        thread.start()

    for f in __divide_chunks(file_list, batch_size):
        script_path = os.path.abspath(os.path.join(workspace_home, script))
        if platform.system().lower() == "windows":
            cmd = (
                f"set MOCAP_BLENDER_PKL_LIST=\"{';'.join(f)}\"\n"
                + "@echo off\n"
                + f"set PARENT_PID={str(pid)}\n"
                + f"set WORKSPACE_HOME={workspace_home}\n"
                + r"set PYTHONPATH=%PYTHONPATH%;%WORKSPACE_HOME%\package;%WORKSPACE_HOME%\startup"
                + "\n"
                + r"set BLENDER_SYSTEM_SCRIPTS=%WORKSPACE_HOME%\startup;%BLENDER_SYSTEM_SCRIPTS%"
                + "\n"
            )
            for k, v in args.items():
                assert isinstance(k, str) and isinstance(v, str)
                cmd = cmd + f"set BLENDER_ARGS_{k}={v}\n"
            cmd = cmd + f"blender.exe --background --log-level -1 --python {script_path}"
            t = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            tempFile = os.path.join(workspace_home, "temp", f"{t}---{index}.bat")
        elif platform.system().lower() == "linux":
            cmd = (
                f"export MOCAP_BLENDER_PKL_LIST=\"{':'.join(f)}\"\n"
                + "#!/bin/bash\n"
                + f"export PARENT_PID={str(pid)}\n"
                + f"export WORKSPACE_HOME={workspace_home}\n"
                + "export PYTHONPATH=${PYTHONPATH}:${WORKSPACE_HOME}/package:${WORKSPACE_HOME}/startup\n"
                + "export BLENDER_SYSTEM_SCRIPTS=${WORKSPACE_HOME}/startup:${BLENDER_SYSTEM_SCRIPTS}\n"
            )
            for k, v in args.items():
                assert isinstance(k, str) and isinstance(v, str)
                cmd = cmd + f"export BLENDER_ARGS_{k}={v}\n"
            cmd = cmd + f"blender --background --log-level -1 --python {script_path}"
            t = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            tempFile = os.path.join(workspace_home, "temp", f"{t}---{index}.sh")
        else:
            raise Exception("系统未支持: " + platform.system().lower())
        file.createTmpFile(tempFile, content=cmd)
        fileQ.put(tempFile)
        # process = subprocess.Popen(f"chmod +x {tempFile}&&{tempFile}", shell=True)
        # process_list.append(process)
        index = index + 1

    for i in range(process_count):
        fileQ.put("end")

    fileQ.join()


def acquireFileList():
    return environ.getEnvVarAsList("MOCAP_BLENDER_PKL_LIST")


def acquireArgs():
    args = {}
    for k, v in os.environ.items():
        if k.startswith("BLENDER_ARGS_"):
            args[k[13:]] = v
    return args


def __kill():
    if platform.system().lower() == "windows":
        subprocess.run(f"taskkill /f /pid {str(os.getpid())}", shell=True)
    elif platform.system().lower() == "linux":
        subprocess.run(f"kill -9 {str(os.getpid())}", shell=True)


def __checkParentProcess(pid):
    print(f"ChildProcess[{os.getpid()}] monitor ParentProcess[{pid}] status")
    while True:
        try:
            if not pid or psutil.Process(pid) is None:
                __kill()
        except Exception as e:
            __kill()
        time.sleep(2)


def startSelfSupervising():
    ppid = int(os.environ.get("PARENT_PID"))
    t = threading.Thread(None, __checkParentProcess, "CheckParentProcess", (ppid,), daemon=True)
    t.start()
