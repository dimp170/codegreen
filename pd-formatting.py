import torch
print(torch.cuda.is_available())  # Should return True if GPU is available
print(torch.cuda.device_count())  # Shows number of GPUs
print(torch.cuda.get_device_name(0))