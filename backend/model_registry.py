MODELS = {
    'wan2.1-t2v-1.3b': {
        'name': 'Wan 2.1 T2V 1.3B',
        'license': 'Apache-2.0',
        'modes': ['text-to-video'],
        'free_model': True,
        'model_id': 'Wan-AI/Wan2.1-T2V-1.3B',
    },
    'wan2.1-vace-1.3b': {
        'name': 'Wan 2.1 VACE 1.3B',
        'license': 'Apache-2.0',
        'modes': ['image-to-video', 'reference-to-video', 'video-to-video'],
        'free_model': True,
        'model_id': 'Wan-AI/Wan2.1-VACE-1.3B',
    },
}

def list_models():
    return list(MODELS.values())

def get_model(model_id):
    return MODELS[model_id]
