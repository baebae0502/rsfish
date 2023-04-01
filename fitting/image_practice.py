
#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


arr_test = np.array(
    [  # 1차 array
        [[1, 2, 1, 3],  # 2차 array
        [2, 1, 2, 3],
        [1, 2, 1, 3],],
        [[2, 3, 4, 5],  # 2차 array
        [2, 1, 2, 3],
        [1, 2, 1, 3]]
    ]
)

plt.imshow(arr_test[0])

plt.show()

print(arr_test[1,0,3])
# %%
