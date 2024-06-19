# OakInk2-Blender-Tools

## Setup

1. Install blender 3.6.9 and setup `PATH` envvar to call `blender` from command line.
   
    ```bash
    blender --version
    ```

2. Create a virtual env of python 3.10. This can be done by either `conda` or python package `venv`.
    
    1. `conda` approach
        
        ```bash
        conda create -p ./.conda python=3.10
        conda activate ./.conda
        ```

    2. `venv` approach
        First use `pyenv` or other tools to install a python intepreter of version 3.10. Here 3.10.14 is used as example:

        ```bash
        pyenv install 3.10.14
        pyenv shell 3.10.14
        ```

        Then create a virtual environment:

        ```bash
        python -m venv .venv --prompt mocap_blender
        . .venv/bin/activate
        ```

3. Install `mocap_blender` package.
    
    ```bash
    pip install -e ./package
    ```

4. Start blender / Batch render.
    
    1. Start blender for scene editing. Debug the blender python script, adjust the lights, setup the materials and save them in the scene. The provided example scene is `asset/base.blend` and the linked script is `script/preview/example.py`.

    ```bash
    ./blender.sh
    ```

    2. Batch rendering. Implement the interface script (an example is `batch_render_example.py`), then place the data pickles in corresponding directories.

    Then call the interface from the command line.
    ```bash
    python ./script/batch_render_example.py  data/example  data/example_render
    ```

    The output logs are generated under directory `temp`. Check these logs for debug usage.

View the introductory video on [youtube](https://www.youtube.com/watch?v=VmMDvRdfMmM).

<!--```bibtex

```-->
