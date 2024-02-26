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
pip install tensorflow-addons
```

If you've installed tensorflow from cuda, de-install it and make sure to get the latest version from pip

if you want to access the server from the arduino and this here is running WSL2 you have to enter port-forwarding:

```
netsh interface portproxy add v4tov4 listenport=6060 listenaddress=0.0.0.0 connectport=6060 connectaddress=192.168.70.81
```