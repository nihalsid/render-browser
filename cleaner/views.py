from django.shortcuts import render
from pathlib import Path
import os

def sample_elem_name(x):
    return "_".join(x.name.split(".")[0].split("_")[:-1])


def get_all_data():
    experiment_root = Path(os.path.abspath(os.path.dirname(__file__)), "..", "static", "renders")
    sample_data = {}
    for x in experiment_root.iterdir():
        if sample_elem_name(x) not in sample_data:
            sample_data[sample_elem_name(x)] = []
        sample_data[sample_elem_name(x)].append(f"/static/renders/{x.name}")
    return sample_data


def update_list(name, sample):
    all_items = []
    if Path(os.path.abspath(os.path.dirname(__file__)), "..", "static", name).exists():
        with open(Path(os.path.abspath(os.path.dirname(__file__)), "..", "static", name), "r") as fptr:
            all_items = [x.strip() for x in fptr.readlines() if x.strip() != ""]
    if sample not in all_items:
        all_items.append(sample)
    with open(Path(os.path.abspath(os.path.dirname(__file__)), "..", "static", name), "w") as fptr:
        fptr.write("\n".join(all_items))


def index(request, cmd, sample_idx):
    all_data = get_all_data()
    total_samples = len(all_data.keys())
    if sample_idx >= len(all_data.keys()):
        sample_idx = len(all_data.keys()) - 1
    sample = list(all_data.keys())[sample_idx]
    if cmd == 13:
        update_list(f"bad.txt", sample)
    image_list = all_data[sample]
    if len(image_list) > 12:
        image_list = image_list[0:len(image_list):len(image_list) // 12]
    return render(request, 'index.html', {'image_list': image_list, 'sample': sample, 'sample_idx': sample_idx})
