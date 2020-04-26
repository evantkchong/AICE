from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Perceptron
import matplotlib.pyplot as plt

def run_model(X, y, model_select='linear_regression'):

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.33,
                                                        random_state=123)
    if model_select == 'linear_regression':
        model = LinearRegression()
    elif model_select == 'perceptron':
        model = Perceptron()
    else:
        print('please select only between "linear_regression" and "perceptron"')
        raise Exception

    model = model.fit(X_train, y_train)

    preds = model.predict(X_test)
    plt.scatter(y_test, preds)
    plt.title('Predicted Results (Prediction Score: {}'.format(model.score(X_test, y_test)))
    plt.xlabel('Actual Number of Active E-Scooter Users')
    plt.ylabel('Predicted Number of Active E-Scooter Users')
    plt.show()

    return model.score(X_test, y_test)