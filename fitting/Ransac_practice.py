import numpy as np
import matplotlib
import matplotlib.pyplot as plt

a_true = -1
b_true = 8 
c_true = 1
num_samples = 100

def good_data(sigma = 1, num_samples = 100) :
    x = np.linspace(0.0, 10.0, num_samples)
    y = a_true*x*x + b_true*x + c_true \
        + np.random.normal(0, sigma, num_samples)
    return x, y

def bad_data(sigma = 1, num_samples = 100) :
    x= np.linspace(0.0, 10.0, num_samples)
    # noise 생성
    noise = np.zeros(num_samples)
    x_left_idx = x > 4
    x_right_idx = x < 6
    x_idx = x_left_idx & x_right_idx
    noise[x_idx] = -10
    
    y = a_true*x*x + b_true*x + c_true \
        + np.random.normal(0, sigma, num_samples) + noise
    return x, y

x_good, y_good = good_data(num_samples = num_samples)
x_bad, y_bad = bad_data(num_samples = num_samples)


'''

max_inlier = 0으로 초기화한다.
무작위로 세 점을 뽑는다.(parameter를 만들 때 필요한 최소 갯수의 observation)
2에서 뽑은 점으로 model을 만든다 = parameter setting
3에서 만든 모델에서 예측한 값과 일정 threshold안에 있는 inlier들의 갯수를 센다.
4에서 센 갯수가 max_inlier보다 크면 max_inlier를 갱신하고, model을 저장한다.
2~5를 N번 반복한 후 최종 저장된 model을 반환한다.
(optional) 최종 inlier로 뽑힌 애들로 model을 refine한다.

'''

def get_y(x, a, b, c) :
    return a*x*x + b*x + c

def RANSAC(x, y, threshold = 0.3, N = 10) :
    
    max_inlier = 0
    a, b, c = 0, 0, 0
    inlier = None
    
    for i in range(N) :
        samples = np.random.uniform(0, num_samples, 3)
        samples = [int(sample) for sample in samples]
        x_sampled = x[samples]
        y_sampled = y[samples]
        
        a_tmp, b_tmp, c_tmp = np.polyfit(x_sampled, y_sampled, 2)
        y_pred = get_y(x, a_tmp, b_tmp, c_tmp)
        
        tmp_inlier = abs(y_pred - y) < threshold
        count_inlier = sum(tmp_inlier)
        
        if count_inlier > max_inlier :
            max_inlier = count_inlier
            inlier = tmp_inlier
            a, b, c = a_tmp, b_tmp, c_tmp
    print(count_inlier)
    a, b, c = np.polyfit(x[inlier], y[inlier], 2)
    return a, b, c

a_good, b_good, c_good = RANSAC(x_good, y_good)
a_bad, b_bad, c_bad = RANSAC(x_bad, y_bad)

print(a_good,b_good,c_good)
print(a_bad,b_bad,c_bad)

        
    
        
        