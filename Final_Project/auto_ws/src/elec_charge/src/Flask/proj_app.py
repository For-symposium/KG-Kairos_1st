from flask import Flask, render_template

app = Flask(__name__)

@app.route('/call/<value>')
def call_from(value):
   return render_template('service.html', value=value)

@app.route('/control') # url for manual control panel
def control():
  return render_template("control.html")

#host = '192.168.0.10'
host = '172.30.1.60'
port = '9900'

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
