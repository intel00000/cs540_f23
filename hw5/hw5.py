import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Plot Year vs. Number of Frozen Days from your dataset as a line plot.
    df = pd.read_csv(sys.argv[1])
    plt.figure(figsize=(10, 5))
    plt.plot(df['year'], df['days'])
    plt.xlabel('Year')
    plt.ylabel('Number of Frozen Days')
    plt.savefig("plot.jpg")

    # convert the pandas to n x 2 numpy array, convert each data point into a feature vector
    X = df.to_numpy(dtype=np.int64)
    # convert each data point into a full feature vector
    X = np.array([[1, array[0]] for array in X], dtype=np.int64)
    print("Q3a:")
    print(X)

    Y = np.array(df['days'], dtype=np.int64).T
    print("Q3b:")
    print(Y)

    Z = X.T @ X
    print("Q3c:")
    print(Z)

    I = np.linalg.inv(Z)
    print("Q3d:")
    print(I)

    PI = I @ X.T
    print("Q3e:")
    print(PI)

    coef = PI @ Y
    print("Q3f:")
    print(coef)

    X_text = 2022
    Y_text = coef[0] + coef[1] * X_text
    print("Q4: " + str(Y_text))

    if Y_text > 0:
        print("Q5a: " + str('>'))
    elif Y_text == 0:
        print("Q5a: " + str('='))
    elif Y_text < 0:
        print("Q5a: " + str('<'))

    print("Q5b: " + str('If the sign of this coef[1] is positive, the number of frozen days will increase over time. If the sign of the coef[1] is negative, the number of frozen days will decrease over time. If the sign of the coef[1] is zero, the number of frozen days will stay constant over time. For hw5.csv, the sign of the coef[1] is negative, so the number of frozen days will decrease over time.'))

    print("Q6a: " + str(-coef[0] / coef[1]))

    print("Q6b: " + str('This is a compelling prediction since coefficient[1] is negative, the number of frozen days will decrease over the years. Thus it is reasonable to predict that number of frozen days will be zero in the year 2455.'))

if __name__ == "__main__":
    main()