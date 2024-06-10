from mocap_blender import batch_process
from mocap_blender import environ
import traceback
import itertools

if not environ.RUN_IN_BLENDER:
    import glob
    import argparse
    import os

    parser = argparse.ArgumentParser(description="batch bulid hand scenes")
    parser.add_argument("input_dir", type=str, help="data path")
    parser.add_argument("output_dir", type=str, help="output path")
    args = parser.parse_args()
    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)

    files = sorted(os.listdir(input_dir))
    home = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    batch_process.batchProcess(home, __file__, files, process_count=4, args={"INPUT": input_dir, "OUTPUT": output_dir})

else:
    from render_scene.example import build_scene
    import os
    from mocap_blender import file, render

    batch_process.startSelfSupervising()
    args = batch_process.acquireArgs()
    input_dir = args["INPUT"]
    output_dir = args["OUTPUT"]

    files = batch_process.acquireFileList()

    for f in files:
        try:
            input_path = os.path.join(input_dir, f)
            output_path = os.path.join(output_dir, f"{f}.png")
            if os.path.exists(output_path):
                continue

            def _render():
                # file.saveFile(output_path)
                render.render(output_path, 1920, 1080) # slight distortion

            build_scene(input_path, _render)
        except Exception as e:
            print(f"error: {f}:\n{traceback.format_exc(e)}")
            continue
