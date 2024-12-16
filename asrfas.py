import random
def perdict(data:tuple,model:list):
    return model[0 ] * data[0] + model[1]
def calculate_gradient(data:tuple,model:list):
    w_grad =2* (model[0]* data[0]+ model[1]-data[1])*data[0]
    b_grad =2* (model[0]* data[0]+ model[1]-data[1])
    return w_grad,b_grad
def train(dataset:list,model:list,T:int,lr:float):
    n= len(dataset)
    for iter in range(1,T+1):
        w_grad_sum=0.0
        b_grad_sum=0.0
        for data in dataset:
            w_grad,b_grad = calculate_gradient(data,model)
            w_grad_sum+=w_grad
            b_grad_sum+=b_grad
        w_grad_mean = w_grad_sum/n
        b_grad_mean = b_grad_sum/n

        model[0] = model[0] - lr * w_grad_mean 
        model[1] = model[1] - lr * b_grad_mean 
    
dataset= []
for _ in range(100):
    x= random.uniform(0.0,1.0)
    y= 0.73 * x + 0.32
    dataset.append((x,y))

#initalize model
w0 =random.uniform(-1.0,1.0)
b0 =random.uniform(-1.0,1.0)
model = [w0,b0]
#train mdodel
train(dataset, model, T=10000,lr = 0.01)

#result
print("w:%6.3f b:%6.3f"%(model[0],model[1]))