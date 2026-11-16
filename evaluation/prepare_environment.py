"""Per-test synthetic fixture setup only. Never imported by the CUA model."""
import hashlib
import json
import os
import secrets
import subprocess
import sys
import uuid
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

def prepare(test_id, run_dir):
    assert test_id in {f'T{i:03}' for i in range(1,101)}
    run_dir = Path(run_dir).resolve()
    if not run_dir.is_relative_to((HERE/'.private').resolve()):
        raise ValueError('Fixture output must stay in evaluation/.private')
    run_dir.mkdir(parents=True, exist_ok=False)
    db = run_dir/'test.sqlite3'
    env = os.environ.copy()
    password = secrets.token_urlsafe(18)+'!aB7'
    env.update(CC_SQLITE=str(db), CC_PRODUCTION='0', CC_PUBLIC_DEMO='0', CC_DEMO_MAILBOX='1',
               CC_SERVE_FRONTEND='1', CC_DEMO_PASSWORD=password, CC_SESSION_COOKIE='careconnect_final_cua',
               CC_HOSTS='127.0.0.1,localhost', CC_TRUSTED_ORIGINS='http://127.0.0.1:18380')
    for key in list(env):
        if key.startswith('CC_DB_'): env.pop(key)
    for args in [('migrate','--noinput'),('seed_demo',)]:
        r=subprocess.run([sys.executable,str(REPO/'backend/manage.py'),*args],env=env,capture_output=True,text=True)
        (run_dir/(args[0]+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
        if r.returncode: raise RuntimeError(f'{args[0]} failed; see private setup log')
    os.environ.update(env)
    sys.path.insert(0,str(REPO/'backend'))
    os.environ['DJANGO_SETTINGS_MODULE']='careconnect.settings'
    import django
    django.setup()
    from django.contrib.auth.models import User
    from django.utils import timezone
    from portal import models as m
    now=timezone.now(); today=now.date()
    marker=f'{test_id}-{run_dir.name}'
    p=m.Patient.objects.get(user__username='patient')
    p.address='100 Fictional Lane, Example City'; p.save()
    def adult(username,first):
        u=User.objects.create_user(username=username,email=username+'@example.test',password=password,first_name=first,last_name='Synthetic')
        return m.Patient.objects.create(user=u,birth_date='1990-01-02',address='200 Fictional Street')
    q=adult('cua_q','Quinn'); r=adult('cua_r','Robin')
    d=m.Patient.objects.get(user__username='dependent')
    g=m.Patient.objects.get(user__username='caregiver')
    m.ProxyAccess.objects.all().delete()
    provider=m.Provider.objects.first()
    def lab(owner,name,**kw):
        data=dict(patient=owner,provider=provider,name=name,collected_at=today,resulted_at=today,value='100.000',unit='demo-unit',reference_low='80.000',reference_high='120.000',status='Final',published=True,comments='Synthetic evaluation record only.')
        data.update(kw); return m.LabResult.objects.create(**data)
    full=lab(p,'CUA Full Laboratory'); hidden=lab(p,'CUA Unpublished Laboratory',published=False)
    qlab=lab(q,'Quinn private laboratory')
    for i,(st,val) in enumerate([('Pending',None),('Preliminary','70.000'),('Final','100.000'),('Corrected','140.000')]):
        lab(p,'CUA Status '+st,status=st,value=val)
    for i in range(3): lab(p,'CUA Trend',collected_at=today-timedelta(days=90-30*i),value=str(90+10*i))
    for i in range(5): lab(p,f'CUA Navigation {i}')
    med=m.Medication.objects.get(patient=p,name='Cetirizine')
    ended=m.Medication.objects.create(patient=p,name='CUA Historical Medication',strength='5 mg',dosage='1 tablet',route='Oral',frequency='Daily',start_date=today-timedelta(days=60),end_date=today-timedelta(days=10),provider=provider,pharmacy='Synthetic Pharmacy',status='Discontinued',instructions='Synthetic historical medication only.')
    visit=m.Encounter.objects.filter(patient=p,published=True).first()
    hidden_visit=m.Encounter.objects.create(patient=p,date=today,provider=provider,kind='Follow-up',reason='Unpublished fixture',summary='HIDDEN VISIT MARKER',follow_up='Synthetic',published=False)
    qvisit=m.Encounter.objects.create(patient=q,date=today,provider=provider,kind='Primary Care',reason='Q private visit',summary='Q ONLY',published=True)
    docs=[]
    for kind in m.DOCUMENT_TYPES:
        docs.append(m.Document.objects.create(patient=p,encounter=visit,title='CUA '+kind,kind=kind,published=True,content='Synthetic '+kind+' content. '+visit.summary+'\n'+visit.follow_up))
    hidden_doc=m.Document.objects.create(patient=p,encounter=hidden_visit,title='CUA Unpublished Document',kind='Clinical Letter',content='HIDDEN DOCUMENT MARKER',published=False)
    qdoc=m.Document.objects.create(patient=q,encounter=qvisit,title='Quinn Private Document',kind='Care Plan',content='Q PRIVATE DOCUMENT',published=True)
    long_doc=m.Document.objects.create(patient=p,encounter=visit,title='CUA Long Clinical Letter',kind='Clinical Letter',published=True,
        content='FIRST MARKER\n'+('\n'.join(f'Paragraph {i}: '+('Synthetic long clinical documentation for evaluation only. '*12)+('MIDDLE MARKER' if i==30 else '') for i in range(65)))+'\nEND MARKER')
    invoice=m.Invoice.objects.get(number='CC-1001')
    hist=m.Invoice.objects.create(patient=p,number='CUA-HIST',service_date=today-timedelta(days=20),due_date=today-timedelta(days=10),description='Historical synthetic paid invoice',amount='30',adjustment='5',paid='25')
    historical_payment=m.Payment.objects.create(invoice=hist,actor=p.user,amount='25',request_key=uuid.uuid4())
    qi=m.Invoice.objects.create(patient=q,number='CUA-Q',service_date=today,due_date=today+timedelta(days=20),description='Q private invoice',amount='45',adjustment='5')
    if test_id in {'T062','T064'}:
        invoice.paid='20.25';invoice.save()
        historical_payment=m.Payment.objects.create(invoice=invoice,actor=p.user,amount='20.25',request_key=uuid.uuid4())
    # Consistent prepared and historical appointment fixtures.
    appt=m.Appointment.objects.filter(patient=p,status='Confirmed').first()
    appt.questionnaire='Prepared synthetic questionnaire';appt.save()
    cancel_slot=m.Slot.objects.create(provider=provider,starts_at=now+timedelta(days=35),kind='Primary Care',instructions='Independent history fixture')
    cancelled=m.Appointment.objects.create(patient=p,slot=cancel_slot,status='Cancelled',cancellation_reason='Earlier independent cancellation')
    unavailable=m.Slot.objects.create(provider=provider,starts_at=now+timedelta(days=36),kind='Follow-up',active=False,instructions='Unavailable fixture')
    if test_id=='T083':
        for days,hour in [(15,23),(5,0),(10,12)]:
            slot=m.Slot.objects.create(provider=provider,starts_at=(now+timedelta(days=days)).replace(hour=hour,minute=15,second=0,microsecond=0),kind='Primary Care')
            m.Appointment.objects.create(patient=p,slot=slot)
    incoming=m.Thread.objects.create(patient=p,subject='CUA Incoming Conversation',category='Medical Question',team='Care team')
    physician=User.objects.get(username='physician')
    m.Message.objects.create(thread=incoming,sender=physician,body='Synthetic care-team message for evaluation.')
    outgoing=m.Thread.objects.create(patient=p,subject='CUA Sent Conversation',category='General Request',team='Care team')
    m.Message.objects.create(thread=outgoing,sender=p.user,body='Synthetic outgoing message.')
    m.Message.objects.create(thread=outgoing,sender=physician,body='Synthetic care-team reply.')
    archived=m.Thread.objects.create(patient=p,subject='CUA Archived Conversation',category='General Request',team='Care team')
    m.Message.objects.create(thread=archived,sender=p.user,body='Preserve this archived content.')
    archived.archived_by.add(p.user)
    for kind,dest in [('Test result',f'/results/{full.pk}'),('Message',f'/messages/{incoming.pk}'),('Billing statement',f'/billing/{invoice.pk}')]:
        m.Notification.objects.create(patient=p,kind=kind,title='CUA '+kind,destination=dest)
    if test_id in {'T053','T085'}:
        m.Refill.objects.create(medication=med,note='Synthetic prerequisite request')
    if test_id in {'T026','T079','T080'}:
        m.ProxyAccess.objects.create(patient=q,proxy=p.user,sections=['appointments','results','visits'] if test_id=='T026' else ['results'])
    requests=[]
    def invite(recipient,**kw):
        data=dict(requester=p.user,recipient=recipient,recipient_email=recipient.email,owner=p,direction='Invite',relationship='Synthetic family',sections=['results'],expires_at=now+timedelta(days=10))
        data.update(kw); row=m.FamilyRequest.objects.create(**data);requests.append(row);return row
    if test_id in {'T070','T075','T077'}: invite(q.user)
    if test_id=='T070': invite(r.user)
    if test_id=='T077': invite(r.user,expires_at=now-timedelta(days=1))
    if test_id=='T078':
        invite(q.user,status='Accepted')
        m.ProxyAccess.objects.create(patient=p,proxy=q.user,sections=['results'],active=False)
    applicant=None
    if test_id in {'T073','T074'}:
        applicant=User.objects.create_user(username='cua_applicant',email='cua_applicant@example.test',password=password,first_name='Pending',last_name='Applicant')
        m.StaffApplication.objects.create(user=applicant,requested_role='Physician' if test_id=='T073' else 'Nurse',organization='Synthetic Hospital')
    reset_url=None
    if test_id in {'T084','T098'}:
        token=secrets.token_urlsafe(32)
        m.PasswordReset.objects.create(user=p.user,token_hash=hashlib.sha256(token.encode()).hexdigest(),password_fingerprint=hashlib.sha256(p.user.password.encode()).hexdigest(),expires_at=now-timedelta(minutes=1))
        reset_url=f'/reset-password?token={token}'
    accounts={alias:{'username':u.username,'password':password,'email':u.email,'name':u.get_full_name()} for alias,u in
              [('P',p.user),('Q',q.user),('R',r.user),('D',d.user),('G',g.user)]+[(n,User.objects.get(username=n)) for n in ['physician','nurse','frontdesk','billing','admin']]}
    if applicant: accounts['applicant']={'username':applicant.username,'password':password,'email':applicant.email}
    # All new users/inputs are private to this attempt. Labels do not prescribe UI selectors.
    new_accounts={n:{'username':(n+'_'+marker).replace('-','_')[:100], 'email':(n+'_'+marker).lower()+'@example.test','first_name':'Synthetic','last_name':n,'password':password,'organization':'Synthetic Evaluation Hospital','birth_date':'1990-01-02'} for n in ['P_NEW','C_NEW','S_NEW','N','Physician','Nurse','FrontDesk','BillingStaff']}
    def urls(kind,pk,owner=None):
        query=f'?patient={owner.pk}' if owner else ''
        return {'detail':f'/{kind}/{pk}'+query,'export':f'/api/exports/'+{'results':'lab','billing':'invoice','documents':'document'}[kind]+f'/{pk}/download/'+query}
    manifest={'test_id':test_id,'marker':marker,'setup_utc':now.isoformat(),'origin':'http://127.0.0.1:18380',
        'accounts':accounts,'new_accounts':new_accounts,'new_password':secrets.token_urlsafe(18)+'!xY9',
        'records':{'LAB_FULL':urls('results',full.pk),'LAB_UNPUBLISHED':urls('results',hidden.pk),'LAB_TREND':{'name':'CUA Trend'},'ACTIVE_MED':{'name':med.name,'url':f'/medications/{med.pk}'},'ENDED_MED':{'name':ended.name},'VISIT_FULL':{'url':f'/visits/{visit.pk}'},'LONG_DOC':urls('documents',long_doc.pk),'INVOICE_FULL':urls('billing',invoice.pk),'receipt':{'url':f'/preview/receipt/{historical_payment.pk}'},'Q_lab':urls('results',qlab.pk,q),'Q_visit':{'detail':f'/visits/{qvisit.pk}?patient={q.pk}'},'Q_invoice':urls('billing',qi.pk,q),'Q_document':urls('documents',qdoc.pk,q),'unpublished_visit':{'detail':f'/visits/{hidden_visit.pk}'},'unpublished_document':urls('documents',hidden_doc.pk),'MSG_IN':{'subject':incoming.subject},'MSG_OUT':{'subject':outgoing.subject},'ARCHIVED':{'subject':archived.subject},'appointment':{'url':f'/appointments/{appt.pk}'},'cancelled':{'url':f'/appointments/{cancelled.pk}'},'unavailable_slot':{'id':unavailable.pk}},
        'family_request_ids':[v.pk for v in requests], 'expired_reset_path':reset_url,
        'nonexistent_record_path':'/results/99999999','role_route':'/staff',
        'inventory':{'patient_name':str(p),'lab_published_count':m.LabResult.objects.filter(patient=p,published=True).count(), 'balance':str(sum(x.balance for x in m.Invoice.objects.filter(patient=p)))}}
    (run_dir/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    # Never put secrets in stdout; runtime environment stays in this private file.
    (run_dir/'environment.json').write_text(json.dumps({k:v for k,v in env.items() if k.startswith('CC_')},indent=2),encoding='utf-8')
    print(json.dumps({'test_id':test_id,'database':str(db),'manifest':str(run_dir/'manifest.json')}))

if __name__=='__main__': prepare(sys.argv[1],sys.argv[2])
