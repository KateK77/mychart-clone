import {Activity,CalendarDays,ClipboardList,FlaskConical,Users,Wallet} from 'lucide-react';
import {type Field} from './ui';
const clinical=['Physician','Nurse'];
const scheduling=[...clinical,'Front Desk'];
const billing=['Billing Staff'];
const visitTypes=['Primary Care','Follow-up','Annual Physical','Specialist Consultation','Telehealth','Laboratory Visit'];
const docTypes=['After Visit Summary','Laboratory Report','Clinical Letter','Visit Instructions','Medication List','Billing Statement','Care Plan'];
const entries=['Conditions','Allergies','Immunizations','Medical history','Surgical history','Family history','Social history','Care team','Vital signs','Preventive care'];
export const scopes=['appointments','results','medications','health','visits','billing','documents'];
const f=(name:string,label:string,kind?:string,optional=false):Field=>({name,label,kind,optional,step:kind==='number'?'any':undefined});
const opt=(name:string,label:string,options:Field['options'],optional=false):Field=>({name,label,options,optional});
const patient=f('patient','Patient','number');
const provider=f('provider','Provider','number');
const encounter=f('encounter','Encounter','number');
export const schema:Record<string,{title:string;roles:string[];fields:Field[];icon:typeof Activity}> = {
 appointments:{title:'Appointments',roles:scheduling,fields:[patient,f('slot','Available slot','number')],icon:CalendarDays},
 slots:{title:'Provider availability',roles:scheduling,fields:[provider,f('starts_at','Start (UTC)','datetime-local'),opt('kind','Visit type',visitTypes),f('instructions','Instructions','textarea',true),{...f('active','Available','checkbox'),value:true}],icon:CalendarDays},
 providers:{title:'Providers',roles:scheduling,fields:[f('name','Name'),f('department','Department','number'),{...f('active','Active','checkbox'),value:true}],icon:Users},
 departments:{title:'Departments',roles:scheduling,fields:[f('name','Department name')],icon:Users},
 results:{title:'Laboratory results',roles:clinical,fields:[patient,provider,f('name','Test name'),f('collected_at','Collection date','date'),f('resulted_at','Result date','date',true),f('value','Value','number',true),f('unit','Units','text',true),f('reference_low','Reference low','number',true),f('reference_high','Reference high','number',true),opt('status','Result status',['Pending','Preliminary','Final','Corrected']),f('comments','Comments','textarea',true)],icon:FlaskConical},
 medications:{title:'Medications',roles:clinical,fields:[patient,provider,f('name','Medication'),f('strength','Strength'),f('dosage','Dosage'),f('route','Route'),f('frequency','Frequency'),f('start_date','Start date','date'),f('end_date','End date','date',true),f('pharmacy','Pharmacy'),opt('status','Status',['Active','Discontinued']),f('instructions','Instructions','textarea',true)],icon:ClipboardList},
 refills:{title:'Refill requests',roles:clinical,fields:[],icon:ClipboardList},
 health:{title:'Clinical history',roles:clinical,fields:[patient,opt('section','Section',entries),f('title','Title'),f('details','Details','textarea'),f('date','Date','date',true)],icon:ClipboardList},
 reports:{title:'Patient correction requests',roles:clinical,fields:[],icon:ClipboardList},
 visits:{title:'Encounters',roles:clinical,fields:[patient,provider,f('date','Visit date','date'),opt('kind','Visit type',visitTypes),f('reason','Reason'),f('summary','Summary','textarea'),f('follow_up','Follow-up','textarea',true)],icon:ClipboardList},
 diagnoses:{title:'Diagnoses',roles:clinical,fields:[encounter,f('label','Diagnosis'),f('code','Code','text',true)],icon:ClipboardList},
 notes:{title:'Clinical notes',roles:clinical,fields:[encounter,f('title','Title'),f('body','Note','textarea'),f('shared','Share with patient','checkbox')],icon:ClipboardList},
 documents:{title:'Documents',roles:clinical,fields:[patient,{...encounter,optional:true},f('title','Title'),opt('kind','Type',docTypes),f('content','Document content','textarea')],icon:ClipboardList},
 billing:{title:'Invoices and payments',roles:billing,fields:[patient,f('number','Invoice number'),f('service_date','Service date','date'),f('description','Description'),f('amount','Billed amount','number'),f('adjustment','Insurance adjustment','number',true),f('due_date','Due date','date'),f('voided','Voided','checkbox')],icon:Wallet},
 insurance:{title:'Insurance policies',roles:billing,fields:[patient,f('carrier','Carrier'),f('plan','Plan'),f('member_id','Member ID')],icon:Wallet},
 proxy:{title:'Family proxy access',roles:[],fields:[patient,f('proxy','Proxy account','number'),opt('section','Initial permission',scopes)],icon:Users},
};
