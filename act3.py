# -*- coding: utf-8 -*-
"""M23CSA015_DLOps_ClassAssignment_2_Q_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FohmbIk3PcXdOBuaknRBB09Yj49LClPT
"""

from google.colab import drive
drive.mount('/content/drive')

pip  install  tensorboardX

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, precision_recall_curve
from tensorboardX import SummaryWriter
import matplotlib.pyplot as plt

# Commented out IPython magic to ensure Python compatibility.
# Load TensorBoard extension
# %load_ext tensorboard

# Load TensorBoard
# %tensorboard --logdir=/content/

import os

# Define the root directory for downloading the dataset
root_dir = '/content/drive/MyDrive/dlopps_class/'

# Check if the directory exists, if not, create it
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# Load USPS dataset with the new root directory
train_data = datasets.USPS(root=root_dir, train=True, download=True, transform=transform)
test_data = datasets.USPS(root=root_dir, train=False, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)





dataiter = iter(train_loader)
images, labels = next(dataiter)
print(images.size())  # Check the size of the images



import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt


transform = transforms.Compose([
    transforms.Resize((28, 28)),  # Resize to 28x28 pixels
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_data = datasets.USPS(root='./data', train=True, download=True, transform=transform)
test_data = datasets.USPS(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)  # Flatten input images
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

mlp_model = MLP()
optimizer_mlp = optim.Adam(mlp_model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

def train(model, optimizer, criterion, train_loader, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            inputs, labels = data

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f'Epoch {epoch + 1}, Loss: {running_loss / len(train_loader)}')

def evaluate_multiclass(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    y_true = []
    y_pred = []
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            y_true.extend(labels.numpy())
            y_pred.extend(predicted.numpy())

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    confusion = confusion_matrix(y_true, y_pred)

    class_precision = precision_score(y_true, y_pred, average=None)
    class_recall = recall_score(y_true, y_pred, average=None)

    return accuracy, f1, confusion, class_precision, class_recall

# Train MLP
train(mlp_model, optimizer_mlp, criterion, train_loader, epochs=10)

mlp_accuracy, mlp_f1, mlp_confusion, mlp_precision, mlp_recall = evaluate_multiclass(mlp_model, test_loader)

print('MLP Accuracy:', mlp_accuracy)
print('MLP F1 Score:', mlp_f1)
print('MLP Confusion Matrix:')
print(mlp_confusion)
print('MLP Precision:', mlp_precision)
print('MLP Recall:', mlp_recall)

plt.figure(figsize=(8, 6))
plt.imshow(mlp_confusion, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('MLP Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()



import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_curve
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter

transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_data = datasets.USPS(root='./data', train=True, download=True, transform=transform)
test_data = datasets.USPS(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

cnn_model = CNN()
optimizer_cnn = optim.Adam(cnn_model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

writer = SummaryWriter()

def train(model, optimizer, criterion, train_loader, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, data in enumerate(train_loader):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(train_loader)
        writer.add_scalar('Loss/train', avg_loss, epoch+1)
        print(f'Epoch {epoch + 1}, Loss: {avg_loss}')

def evaluate_multiclass(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    y_true = []
    y_pred = []
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            y_true.extend(labels.numpy())
            y_pred.extend(predicted.numpy())
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    confusion = confusion_matrix(y_true, y_pred)
    return accuracy, f1, confusion, y_true, y_pred

train(cnn_model, optimizer_cnn, criterion, train_loader, epochs=10)

cnn_accuracy, cnn_f1, cnn_confusion, y_true, y_pred = evaluate_multiclass(cnn_model, test_loader)

print('CNN Accuracy:', cnn_accuracy)
print('CNN F1 Score:', cnn_f1)
print('CNN Confusion Matrix:')
print(cnn_confusion)

plt.figure(figsize=(8, 6))
plt.imshow(cnn_confusion, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('CNN Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Convert multiclass labels to binary (one class as positive, rest as negative)
y_true_bin = [1 if label == 0 else 0 for label in y_true]
y_pred_bin = [1 if label == 0 else 0 for label in y_pred]

precision, recall, _ = precision_recall_curve(y_true_bin, y_pred_bin, pos_label=1)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='.')
plt.title('Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.show()

writer.close()

print("version1 hello")

print('version2update')




