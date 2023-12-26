import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

def get_data_loader(training = True):
    # define custom_transform
    custom_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    # download the dataset
    train_set=datasets.FashionMNIST('./data',train=True,download=True,transform=custom_transform)
    test_set=datasets.FashionMNIST('./data', train=False,transform=custom_transform)
    
    # return the dataloader depend on the argument
    if training == True:
        return torch.utils.data.DataLoader(train_set, batch_size = 64)
    elif training == False:
        # set shuffle=False for the test loader
        return torch.utils.data.DataLoader(test_set, batch_size = 64, shuffle=False)

def build_model():
    # define the model
    model = nn.Sequential (
        # flatten the 2D image into 1D array
        nn.Flatten(),
        # A Dense layer with 128 nodes and a ReLU activation.
        nn.Linear(784, 128),
        nn.ReLU(),
        # A Dense layer with 64 nodes and a ReLU activation.
        nn.Linear(128, 64),
        nn.ReLU(),
        # A Dense layer with 10 nodes
        nn.Linear(64, 10),
        )
    
    return model

def train_model(model, train_loader, criterion, T):
    # train the model
    model.train()

    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(T):
        correct = 0
        total_loss = 0
        for images, labels in train_loader:
            # zero the parameter gradients
            optimizer.zero_grad()
            
            result = model(images)
            # get the max possibility
            predicted = torch.argmax(result, dim=1)
            # get the number of correct predictions
            correct += (predicted == labels).sum().item()
            
            loss = criterion(result, labels)

            # accumulate the total loss, account for the batch size
            total_loss += loss.item() * len(images)

            loss.backward()
            optimizer.step()
            
        # print statistics after each epoch
        print('Train Epoch: {} Accuracy: {}/{}({:.2f}%) Loss: {:.3f}'.format(
            epoch, correct, len(train_loader.dataset),
            correct / len(train_loader.dataset) * 100, total_loss / len(train_loader.dataset)))
    
def evaluate_model(model, test_loader, criterion, show_loss = True):
    # evaluate the model
    model.eval()

    correct = 0
    total_loss = 0

    with torch.no_grad():
        for images, labels in test_loader:
            result = model(images)
            predicted = torch.argmax(result, dim=1)
            correct += (predicted == labels).sum().item()

            # accumulate the loss, account for the batch size
            total_loss += criterion(result, labels).item() * len(images)

    if show_loss == False:
        print('Accuracy: {:.2f}%'.format(correct / len(test_loader.dataset) * 100))
    elif show_loss == True:
        print('Average loss: {:.4f}\nAccuracy: {:.2f}%'.format(total_loss / len(test_loader.dataset), correct / len(test_loader.dataset) * 100))
        
def predict_label(model, test_images, index):
    # assume the class names
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt'
,'Sneaker','Bag','Ankle Boot']
    
    # pick the image at the specific index
    result = model(test_images[index])
    # convert from logits to probability
    probability = F.softmax(result, dim=1)

    # return values and indices of the top k largest elements
    n = 3
    values,indices = probability.topk(n, largest=True, sorted=True, dim=1)

    top_n_classes = []
    top_n_probabilities = []

    for i in range(n):
        top_n_classes.append(class_names[indices[0][i]])
        top_n_probabilities.append(values[0][i].item())

    for i in range(n):
        print('{}: {:.2f}%'.format(top_n_classes[i], top_n_probabilities[i] * 100))


if __name__ == '__main__':
    '''
    Feel free to write your own test code here to examine the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()

    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)

    test_loader = get_data_loader(False)

    model = build_model()
    print(model)

    train_model(model, get_data_loader(), criterion, 5)

    evaluate_model(model, test_loader, criterion, show_loss = False)
    evaluate_model(model, test_loader, criterion, show_loss = True)

    test_images, labels = next(iter(get_data_loader(False)))
    predict_label(model, test_images, 1)