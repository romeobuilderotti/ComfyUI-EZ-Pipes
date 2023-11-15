from abc import ABC, abstractmethod

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class GenericPipe(ABC):
    """
    'Edit pipe' - contains input and output items as well as pipe in/out
    """

    CATEGORY = "utils"
    FUNCTION = "process"

    @classmethod
    @abstractmethod
    def get_items(self):
        ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__dict__.get("get_items", None) is None:
            return
        cls.RETURN_NAMES = ("pipe", ) + tuple(cls.get_items().keys())
        cls.RETURN_TYPES = ("PIPE", ) + tuple(v[0] for v in cls.get_items().values())

    @classmethod
    def INPUT_TYPES(cls):
        return { "required": {}, "optional": {"pipe": ("PIPE",)} | {k: (v[0], {"forceInput": True, "default": None}) for k, v in cls.get_items().items()}}
    
    def process(self, pipe=None, **kwargs):
        if pipe is None:
            pipe = {}

        for k, v in kwargs.items():
            if v is not None:
                pipe[k] = v

        return (pipe, ) + tuple(pipe.get(k, None) for k in self.get_items().keys())

class GenericPipeInput(GenericPipe):
    """
    'New pipe' - contains input items and pipe output
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__dict__.get("get_items", None) is None:
            return
        cls.RETURN_NAMES = ("pipe", )
        cls.RETURN_TYPES = ("PIPE", )

    @classmethod
    def INPUT_TYPES(cls):
        return { "required": cls.get_items() }
    
    def process(self, **kwargs):
        return (super().process(**kwargs)[0],)
    
class GenericPipeOutput(GenericPipe):
    """
    'End pipe' - contains input pipe and output items
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__dict__.get("get_items", None) is None:
            return
        cls.RETURN_NAMES = cls.RETURN_NAMES[1:]
        cls.RETURN_TYPES = cls.RETURN_TYPES[1:]
    
    @classmethod
    def INPUT_TYPES(cls):
        return { "required": {"pipe": ("PIPE",)} }
    
    def process(self, pipe, **kwargs):
        return super().process(pipe, **kwargs)[1:]

def create_pipe_classes(prefix, items):
    base_classes = {
        '': GenericPipe,
        'Input': GenericPipeInput,
        'Output': GenericPipeOutput
    }

    for base_class_suffix, base_class in base_classes.items():
        class_name = f'{prefix}Pipe{base_class_suffix}'
        display_name = f'{prefix} Pipe {base_class_suffix}'
        new_class = type(class_name, (base_class,), {
            'get_items': classmethod(lambda cls: items)
        })
        NODE_CLASS_MAPPINGS[class_name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[class_name] = display_name