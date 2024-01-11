from torchvision.datasets import MNIST
from my_dataloader import MyAsyncIterableClass
from torchvision.transforms import ToTensor, Normalize, RandomHorizontalFlip, Compose, RandomVerticalFlip
from torchvision.models import resnet152
import asyncio
transforms = Compose([RandomVerticalFlip(),RandomHorizontalFlip(),ToTensor()])

mnist = MNIST(root="./", download=True,train=True, transform=transforms)

dataloader = MyAsyncIterableClass(mnist)

model = resnet152(weights=False).to("cuda")
async def main():
    async for i,j in dataloader:
        # print(i)
        i = i.to("cuda")
        print("we are on gpu now")
        for _ in range(20):
            try:model(i)
            except:pass
        print("now we are on cpu")

asyncio.run(main())
