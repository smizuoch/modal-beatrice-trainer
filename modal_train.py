import modal

app = modal.App("beatrice-trainer")

# 永続ボリュームの取得（なければ自動作成する場合は create_if_missing=True を指定）
volume = modal.Volume.from_name("beatrice-models", create_if_missing=True)

image = (
    modal.Image.from_registry("python:3.10-slim")
    .apt_install("g++", "build-essential")
    .pip_install("poetry")
    .add_local_dir(".", remote_path="/workspace")
)

# Function の volumes 引数で Volume を /workspace/out_dir にマウントする
@app.function(image=image, volumes={"/workspace/out_dir": volume}, gpu="A100", timeout=36000)
def train(data_dir: str):
    import subprocess
    cmd = (
        "cd /workspace && "
        "poetry config virtualenvs.create false && "
        "poetry install && "
        "python3 beatrice_trainer -d {data_dir} -o /workspace/out_dir"
        # "python3 beatrice_trainer -d {data_dir} -o /workspace/out_dir -c assets/my_config.json" # コンフィグファイルを指定する場合
    ).format(data_dir=data_dir)
    subprocess.run(cmd, shell=True, check=True)
