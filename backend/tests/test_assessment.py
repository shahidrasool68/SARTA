"""Run: cd backend && pytest -q tests"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fastapi import FastAPI
from routers import assessment
app = FastAPI()
app.include_router(assessment.router)

@pytest.fixture(autouse=True)
def isolated_store(tmp_path, monkeypatch):
    monkeypatch.setenv('SARTA_ASSESSMENT_DB', str(tmp_path / 'session.sqlite3'))

@pytest.fixture
def client():
    return TestClient(app)


def start(client):
    res=client.post('/api/assessment/start-session',json={'skills':['Python','OOP']})
    assert res.status_code==200,res.text
    return res.json()['session_id']


def test_catalog_and_public_question_secrecy(client):
    sid=start(client)
    q=client.post('/api/assessment/next-mcq',json={'session_id':sid,'skill':'Python'}).json()['question']
    assert 'correct_answer' not in q
    coding=client.get('/api/assessment/coding-question/Google').json()
    assert coding['_id']=='two_sum'
    for test in coding['test_cases']:
        if test['hidden']:
            assert 'stdin' not in test and 'expected' not in test


def test_server_authoritative_grading_and_no_replay(client):
    sid=start(client)
    payload={'session_id':sid,'skill':'Python'}
    q=client.post('/api/assessment/next-mcq',json=payload).json()['question']
    repeated=client.post('/api/assessment/next-mcq',json=payload).json()['question']
    assert q['_id']==repeated['_id']
    submitted=client.post('/api/assessment/submit-answer',json={
        'session_id':sid,'question_id':q['_id'],
        'selected_answer':'__invalid_option__','correct_answer':'__invalid_option__'})
    assert submitted.status_code==422
    valid=client.post('/api/assessment/submit-answer',json={
        'session_id':sid,'question_id':q['_id'],'selected_answer':q['options'][0],
        'correct_answer': '__forged__','skill':'WrongSkill','difficulty':'Hard'})
    assert valid.status_code==200
    assert valid.json()['is_correct'] == (valid.json()['correct_answer']==q['options'][0])
    assert client.post('/api/assessment/submit-answer',json={'session_id':sid,'question_id':q['_id'],'selected_answer':q['options'][0]}).status_code==409


def test_adaptive_levels():
    controller=assessment.select_next_question
    assert controller('Python','Medium',False,0)['next_difficulty']=='Easy'
    assert controller('Python','Medium',True,2,accuracy=1)['next_difficulty']=='Hard'
    assert controller('Python','Hard',True,3)['next_difficulty']=='Hard'
    assert controller('Python','Easy',False,0)['next_difficulty']=='Easy'


def test_report_does_not_trust_client_scores(client):
    sid=start(client)
    response=client.post('/api/assessment/complete',json={
        'session_id':sid,'coding_results':[{'title':'Fake','passed':True}]})
    assert response.status_code==200
    report=response.json()['report']
    assert report['coding_status']=='not_submitted'
    assert report['coding_summary']['total']==0
    assert client.get(f'/api/assessment/report/{sid}').json()==report


def test_judge0_unavailable_is_not_faked(client,monkeypatch):
    sid=start(client)
    async def offline(*args,**kwargs):
        return {'success':False,'status':'Sandbox unavailable'}
    monkeypatch.setattr(assessment,'evaluate_code',offline)
    response=client.post('/api/assessment/evaluate-code',json={
        'session_id':sid,'problem_id':'two_sum', 'mode':'submit',
        'language_id':71, 'source_code':'print(0)'})
    assert response.status_code==503
    assert client.post('/api/assessment/complete',json={'session_id':sid}).json()['report']['coding_status']=='not_submitted'


def test_hidden_tests_scored_and_persisted(client,monkeypatch):
    sid=start(client)
    counter={'n':0}
    async def grading(*args,**kwargs):
        counter['n']+=1
        return {'success': counter['n']!=2,'status':'Accepted' if counter['n']!=2 else 'Wrong Answer','time':'0.02'}
    monkeypatch.setattr(assessment,'evaluate_code',grading)
    response=client.post('/api/assessment/evaluate-code',json={
        'session_id':sid,'problem_id':'two_sum','mode':'submit',
        'language_id':71,'source_code':'print(0)'})
    assert response.status_code==200
    assert response.json()['test_cases_total']==4
    assert response.json()['test_cases_passed']==3
    report=client.post('/api/assessment/complete',json={'session_id':sid}).json()['report']
    assert report['coding_status']=='graded'
    assert report['coding_summary']['total']==1
    assert report['coding_summary']['passed']==0
