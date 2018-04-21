import unicodedata, datetime, re, io
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])



def result():
	if request.method =='GET':
		client = request.remote_addr
		user = request.user_agent
		return render_template('index.html', MAC='Please enter a MAC address to find out the vendor', IP=client, user=user)
	if request.method == 'POST':
		user = request.user_agent
		MAC = request.form['MAC']
		query = MAC
		string = re.sub('[^A-Za-z0-9]+','',MAC)
		MAC = string.upper()
		if len(MAC) < 6:
			MAC = "INVALID MAC length, it must be 6 characters long"
		else:
			MAC = MAC[0:5] 
		with open('oui','r') as f:
			found = False
			for line in f:
				if MAC in line:
					MAC = line
					found = True
			if not found:
				MAC = "MAC ADDRESS not found"
		f.close()
		IP = request.remote_addr
		F = open("queries","w")
		now = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
		F.write(now + "," + str(IP)+ ","+query+","+str(user) + '\n')
		F.close() 
		return render_template("index.html", MAC=MAC,IP=IP, user=user)


if __name__ == '__main__':
#   app.run(host='0.0.0.0',debug=False,port=80)
   app.run(host='0.0.0.0',debug=False,port=443, ssl_context=('cert.pem', 'key.pem'))
