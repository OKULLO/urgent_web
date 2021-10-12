

try: from service_WEB.imports import *
except: from imports import *


SQL_URL = ''
NLP_URL = 'http://192.168.0.164:5001/'
API_KEY = ''
THMBL_KEY = ''
MAIL_PASSWORD = ''


# Secure application
application = Flask(__name__)

application.secret_key = 'UrgentOkullo12345' + str(random.randint(1, 1000000000))

@application.context_processor
def inject_api_keys():
    return dict(googlemaps_key='googlemaps_api')

@application.route('/',methods=['GET'])
def index():
    return render_template('home.html')


@application.route('/analysis')
def call_analysis():


    # warnings.simplefilter('ignore')
    
    # header = {'apikey': API_KEY}
    params = {'message': request.args.get('message')}

    req = requests.post('/'.join([NLP_URL, 'run_nlp']), params=params)
    arg = {'status': 200, 'mimetype': 'application/json'}
    
    try: 
        req = json.loads(req.content)
        req['score'] = 300*req['score']
        return Response(response=json.dumps(req), **arg)
    except: 
        return Response(response=json.dumps({'emotion': 0.0, 'score': 0.0, 'keywords': [], 'class': 'unknown'}), **arg)


    
    return Response(response=json.dumps(req,indent=4),**arg)



@application.route('/register')
def register():
    return render_template('analysis.html')


@application.route('/login')
def login():
    return render_template('login.html')




@application.route('/run_analysis')
def calls_content():
    return render_template('dashboard/dashboard_calls.html')
    



       


if __name__ == '__main__':
    application.run(host='127.0.0.1',debug=True, port=8081)
   

    
