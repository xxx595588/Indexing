from flask import Flask, request, jsonify, render_template
from search import search


# create the flask app
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('template.html', prediction_text="")


@app.route('/search', methods=['GET','POST'])
def predict():
    #Get search query
    query = request.form.get('Query')
    retString = search(query)
    return render_template('template.html', prediction_text = retString)




# boilerplate flask app code
if __name__ == "__main__":
    app.run()
