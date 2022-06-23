from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template("crime_pred.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    output=model.predict(final)

    if output==0:
        return render_template('crime_pred.html',pred='Less crime ,Happy journey (crime less than 13) {}'.format(output))
    elif output==1:
        return render_template('crime_pred.html',pred='Moderate crime, be precautious {}'.format(output))
    else:
        return render_template('crime_pred.html',pred='High crime rate,change your time travel {}'.format(output))
        


if __name__ == '__main__':
    app.run(debug=True)
