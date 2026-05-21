import torch
print("CUDA disponível:", torch.cuda.is_available())
print("Versão do PyTorch:", torch.__version__)
print("Versão do CUDA:", torch.version.cuda)