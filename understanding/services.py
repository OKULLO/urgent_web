import os
import json
import requests
import time
import uuid
import jwt



class Calls:

    def __init__(self,STT_URL =None,NLP_URL =None):

        self.STT_URL =STT_URL
        self.NLP_URL =NLP_URL

    def convert_speech_to_text(self,audio,dump=None):
            try:

              fl ={'audio_file':audio}
              #run transcript analysis
              self.stt = requests.post('/'.join([self.STT_URL,'run']),files=fl
                ,params={'api_type': 'IBM'})

              if not dump is None: 
                  with open(dump, 'w') as out: 
                      json.dump(self.stt, out)

              # req = json.loads(stt.content)
              # return req

            except Exception as e:return json.dumps(e)


    def understand_transcript(self,transcription):

            params = {'message':transcription}
            # headers =''

            req = requests.post('/'.join([self.NLP_URL, 'run_nlp']), params=params)
            # arg = {'status': 200, 'mimetype': 'application/json'}
            
            try: 
                req = json.loads(req.content)
                req['score'] = 300*req['score']
                return req
            except: 
                return json.dumps({'emotion': 0.0, 'score': 0.0,'keywords':'None' ,'class': 'unknown'})


    def priority_analysis(self,log=None):


        if not log is None and log['keywords'] is not None:

            dic = dict()
            
            for i, wrd in enumerate(log['keywords']['text']):

                mtc = [w for w in dic.keys() if w in log['keywords']['text']]

                for key in mtc: sco[i] += np.clip(dic[key], -1, 0)
                
                sco = np.cumsum(sco)
                self.sco = sco.copy().astype(str)

                self.sco[sco > -2.5] = 'HIGH'
                self.sco[sco > -1.5] = 'MEDIUM'
                self.sco[sco > -0.5] = 'LOW'


    def download_recording(self,recording_url, recording_uuid):
            iat = int(time.time())

            with open("private.key", "rb") as key_file:
                private_key = key_file.read()

            payload = {
                "application_id": os.environ["APPLICATION_ID"],
                "iat": iat,
                "exp": iat + 60,
                "jti": str(uuid.uuid4()),
            }

            token = jwt.encode(payload, private_key, algorithm="RS256")

            header = {"Authorization": b"Bearer " + token, "User-Agent": "voice-journal"}

            req = requests.get(recording_url,headers=header,)

            if req.status_code == 200:
                recordingfile = f"./recordings/{recording_uuid}.mp3"
                os.makedirs(os.path.dirname(recordingfile), exist_ok=True)

                with open(recordingfile, "wb") as f:
                    f.write(req.content)

                return req.content
            else:
                raise Exception(f"Error downloading recording {recording_uuid}")
