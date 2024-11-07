import torch

def get_optimizer(model):
    return torch.optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)

def train_model(model, data_loader, optimizer, device, num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        for images, targets in data_loader:
            images = [image.to(device) for image in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
            
            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
        
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {losses.item()}")
