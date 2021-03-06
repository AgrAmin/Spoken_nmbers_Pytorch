import matplotlib.pyplot as plt
import numpy as np

import torch
import torchvision

import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models

from os import listdir
from os.path import isfile, join

#Listing the labels training & test set
mypathTrain=r"C:\data\imgTrain" #images for training should be placed here
trainlabel = [f for f in listdir(mypathTrain) if isfile(join(mypathTrain, f))]

mypathTest=r"C:\Data\imgTest" # """ testing """
testlabel = [g for g in listdir(mypathTest) if isfile(join(mypathTest, g))]

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# Transforms for the training, validation, and testing sets
#training_transforms, testing_transforms = processing_functions.data_transforms()

# Load the datasets with ImageFolder
#training_dataset, testing_dataset = processing_functions.load_datasets(mypathTrain, transform, mypathTest, transform)

testing_dataset=datasets.ImageFolder(root=mypathTrain,transform=transform)
training_dataset=datasets.ImageFolder(root=mypathTest,transform=transform)

train_loader=torch.utils.data.DataLoader(training_dataset,batch_size=8, shuffle= True)
test_loader=torch.utils.data.DataLoader(training_dataset,batch_size=8, shuffle= True)

print(type(test_loader))
print(type(testing_dataset))
class_names= testing_dataset.classes
print(class_names)
#torchvision.datasets.folder.ImageFolder

# Build and train your network
# Transfer Learning
device = torch.device("cuda" if torch.cuda.is_available()
                                  else "cpu")

##### load and show some images for fun #####
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# get some random training images
dataiter = iter(train_loader)
images, labels = dataiter.next()

# show images
imshow(torchvision.utils.make_grid(images))
# print labels
print(' '.join('%5s' % class_names[labels[j]] for j in range(8)))  #range(batch_size)
####End test loading images ### note the number of image showed = batch size ###########

### CNN ###
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 *117*157, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        #print(x.size(3))
        x = x.view(-1,16*117*157)#(len(x[0]),len(x))#(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

####### loss fucntion and optimizer ###
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
########"

for epoch in range(10):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        # get the inputs
        inputs, labels = data
        #print(torch.Tensor.size(inputs))

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')

##########
#############Test the Model ###########
dataiter = iter(test_loader)
images, labels = dataiter.next()

# print images
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join('%5s' % class_names[labels[j]] for j in range(8)))  #range(batch_size)
outputs = net(images)
####################

'''The outputs are energies for the 10 classes. The higher the energy for a class,
 the more the network thinks that the image is of the particular class.
  So, let’s get the index of the highest energy:'''

_, predicted = torch.max(outputs, 1)

print('Predicted: ', ' '.join('%5s' % class_names[predicted[j]]
                              for j in range(8)))
##########accuracy for the whole dataset ##########
correct = 0
total = 0
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))

############ performance evaluation of every class #########
class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1


for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
        class_names[i], 100 * class_correct[i] / class_total[i]))

