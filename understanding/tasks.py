from tinydb import TinyDB, where
from .services import Calls
from .celery import app


@app.task
def understand_recording(recording_url, recording_uuid):
    db = TinyDB("db.json")
    stt_url =""
    nlp_url =""

    audio = Calls().download_recording(recording_url, recording_uuid)
    transcription = Calls(STT_URL=stt_url).convert_speech_to_text(audio)
    call_analysis = Calls(NLP_URL=nlp_url).understand_transcript(' '.join(transcription['words']))
    # sentiments = Call_analysis().priority_analysis(log=call_analysis)

    db.update(
        {
            # "transcription": transcription["results"][0]["alternatives"][0][
            #     "transcript"
            # ],
            # "sentiments":sentiments
            "emotions": call_analysis["emotion"],
            "keywords": call_analysis["keywords"],
            "score": call_analysis["score"],
            "class": call_analysis["class"],
        },
        where("recording_uuid") == recording_uuid,
    )

    #add connection to the app service here(store nlp results)#to be added in feature
