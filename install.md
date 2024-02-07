Install anaconda3

Switch to conda env

Create new Environment which uses python 3.9

```bash
conda create -n tensorflow_39_env python=3.9 tensorflow
```

Maybe do

conda init

Enable it as an environment

```bash
conda activate tensorflow_39_env
```

and set it as Jupyter Server in PyCharm 

```bash
python -m ipykernel install --user --name=tensorflow_39_env
```

We somehow still need pip for some actions like the installation of this

```bash
pip install tensorflow-model-optimization
```

```bash
conda install -c conda-forge cudatoolkit
conda install cudnn
```

If you've installed tensorflow from cuda, de-install it and make sure to get the latest version from pip