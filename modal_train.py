import modal

app = modal.App("beatrice-trainer")

# 永続ボリュームの取得（なければ自動作成する場合は create_if_missing=True を指定）
volume = modal.Volume.from_name("beatrice-models", create_if_missing=True)

# ローカルディレクトリのマウントは、add_local_dir を利用（※ Modal SDK の最新推奨方法）
image = (
    modal.Image.from_registry("python:3.10-slim")
    .apt_install("g++", "build-essential")
    .pip_install("poetry")
    .add_local_dir(".", remote_path="/workspace")
)

# Function の volumes 引数で Volume を /workspace/model にマウントする
# GPU は A100 などに変更可能
@app.function(image=image, volumes={"/workspace/model": volume}, gpu="A10G", timeout=3600)
def train(data_dir: str, out_dir: str):
    import subprocess
    cmd = (
        "cd /workspace && "
        "poetry config virtualenvs.create false && "
        "poetry install && "
        "python3 beatrice_trainer -d {data_dir} -o {out_dir}"
        # "python3 beatrice_trainer -d {data_dir} -o {out_dir} -c assets/my_config.json" # コンフィグファイルを指定する場合
    ).format(data_dir=data_dir, out_dir=out_dir)
    subprocess.run(cmd, shell=True, check=True)
