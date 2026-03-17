import requests, json
BASE = 'http://localhost:8000/api'
H = {'X-API-Key': 'kd_dreaming007'}
r = requests.post(BASE+'/auth/login', json={'username':'DebK','password':'password123'}, headers=H)
print('Login:', r.status_code)
token = r.json().get('access_token')
H['Authorization'] = 'Bearer ' + token
r = requests.post(BASE+'/learning/start', json={'topic':'Photosynthesis','difficulty_level':5,'duration_minutes':5,'visual_style':'cartoon','story_style':'fun','play_mode':'solo'}, headers=H)
print('Start:', r.status_code)
sid = r.json()['session_id']
print('SID:', sid)
r = requests.get(BASE+'/learning/session/'+sid+'/content', headers=H, timeout=120)
print('Content:', r.status_code)
d = r.json()
segs = d.get('story_segments', [])
print('Segments:', len(segs))
for i, seg in enumerate(segs):
    print('--- Seg', i+1, '---')
    print('narrative:', str(seg.get('narrative',''))[:120])
    print('image:', seg.get('scene_image_url',''))
    q = seg.get('quiz', {})
    print('quiz:', str(q.get('question_text',''))[:120])
    for o in q.get('options', []):
        print('  ', o.get('key'), ':', str(o.get('text',''))[:80])
