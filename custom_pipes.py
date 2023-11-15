import comfy
from .generic_pipe import create_pipe_classes

# Usage:
# create_pipe_classes(<Pipe Name>, <Pipe Items Dict>)
# Items are defined as <Item Name>: (<Item Type>, <Item Options Dict (optional)>)

create_pipe_classes("Sampler", {
    "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
    "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
    "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
    "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
})

create_pipe_classes("Model", {
    "model": ("MODEL", ),
    "clip": ("CLIP", ),
    "vae": ("VAE", ),
    "positive": ("CONDITIONING", ),
    "negative": ("CONDITIONING", ),
})
