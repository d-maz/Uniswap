import numpy as np
import math

def calc_liquidity(current_price, upper_price, lower_price, x_real, x):

    coeff = np.array([current_price - upper_price,2*x_real*current_price,current_price*x_real**2]).flatten()

    x_virtual_upper = np.roots(coeff)

    L = math.sqrt(upper_price)*x_virtual_upper[(x_virtual_upper > 0)]
    
    y_real = L**2/(x_real+L/math.sqrt(upper_price)) - L*math.sqrt(lower_price)

    #print(x['POOL_NAME'], 'cp', current_price, 'up', upper_price, 'xreal', x_virtual_upper, 'L', L)
    return L#, y_real

