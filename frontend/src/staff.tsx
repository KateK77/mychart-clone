import {useState} from 'react';
import {useQuery} from '@tanstack/react-query';
import {Activity,CalendarDays,ClipboardList,FlaskConical,Users,Wallet} from 'lucide-react';
import {api,date,withParams,type RecordData} from './api';
import {Action,Data,Empty,Facts,Filters,Heading,Panel,Row,type Field} from './ui';

const clinical=['Physician','Nurse'];
const scheduling=[...clinical,'Front Desk'];
const billing=['Billing Staff'];
const visitTypes=['Primary Care','Follow-up','Annual Physical','Specialist Consultation','Telehealth','Laboratory Visit'];
const docTypes=['After Visit Summary','Laboratory Report','Clinical Letter','Visit Instructions','Medication List','Billing Statement','Care Plan'];
const entries=['Conditions','Allergies','Immunizations','Medical history','Surgical history','Family history','Social history','Care team','Vital signs','Preventive care'];
const scopes=['appointments','results','medications','health','visits','billing','documents'];
const f=(name:string,label:string,kind?:string,optional=false):Field=>({name,label,kind,optional,step:kind==='number'?'any':undefined});
const opt=(name:string,label:string,options:Field['options'],optional=false):Field=>({name,label,options,optional});
const patient=f('patient','Patient','number');
const provider=f('provider','Provider','number');
const encounter=f('encounter','Encounter','number');
const schema:Record<string,{title:string;roles:string[];fields:Field[];icon:typeof Activity}> = {
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
export function Staff(){
 const [resource,setResource]=useState('');
 const [patientId,setPatientId]=useState<number>();
 const [search,setSearch]=useState('');
 const [selected,setSelected]=useState<number>();
 const [creating,setCreating]=useState(false);
 const [paymentKey,setPaymentKey]=useState(()=>crypto.randomUUID());
 const session=useQuery({queryKey:['session'],queryFn:()=>api('session/')});
 const roles:string[]=session.data?.user?.roles??[];
 const allowed=(key:string)=>roles.includes('Administrator')||schema[key].roles.some(role=>roles.includes(role));
 const directory=useQuery({queryKey:['api','staff/patients/'],queryFn:()=>api('staff/patients/')});
 const lookup=(resource:string)=>allowed(resource)||(['providers','departments','slots'].includes(resource)&&roles.some(role=>clinical.includes(role)));
 const providers=useQuery({queryKey:['api','staff/providers/'],queryFn:()=>api('staff/providers/'),enabled:lookup('providers')});
 const departments=useQuery({queryKey:['api','staff/departments/'],queryFn:()=>api('staff/departments/'),enabled:lookup('departments')});
 const slots=useQuery({queryKey:['api','staff/slots/'],queryFn:()=>api('staff/slots/'),enabled:allowed('slots')});
 const visits=useQuery({queryKey:['api','staff/visits/'],queryFn:()=>api('staff/visits/'),enabled:allowed('visits')});
 const choose=(key:string)=>{setResource(key);setSelected(undefined);setCreating(false)};
 const listPath='staff/'+resource+'/';
 const detailPath=listPath+selected+'/';
 const config=schema[resource];
 const activePatient=directory.data?.find((row:RecordData)=>row.id===patientId);
 const options=(rows:RecordData[]|undefined,label:(row:RecordData)=>string,key='id')=>(rows??[]).map(row=>({value:row[key],label:label(row)}));
 const slotOptions=options(slots.data?.filter((row:RecordData)=>row.active&&row.available),row=>row.provider_name+' · '+row.kind+' · '+date(row.starts_at));
 const resolve=(field:Field):Field=>{
  const values:Record<string,Field['options']>={patient:options(directory.data,row=>row.name),provider:options(providers.data,row=>row.name),department:options(departments.data,row=>row.name),encounter:options(visits.data?.filter((row:RecordData)=>!patientId||row.patient===patientId),row=>row.reason+' · '+date(row.date)),slot:slotOptions,proxy:options(directory.data,row=>row.name,'user')};
  return values[field.name]?{...field,options:values[field.name],value:field.name==='patient'?patientId:field.value}:field;
 };
 const label=(row:RecordData)=>row.name||row.title||row.subject||row.description||row.medication_name||row.label||row.reason||row.kind||row.carrier||row.topic||(resource==='proxy'?(directory.data?.find((person:RecordData)=>person.id===row.patient)?.name??'Patient')+' proxy access':'Record '+row.id);
 const submitted=(value:RecordData)=>{setCreating(false);setSelected(value.id)};
 const createFields=(config?.fields??[]).map(resolve);
 return <><Heading title="Staff workspace" description="Manage synthetic patient records and portal workflows."/>
 <div className="staff-layout"><div className="stack">
 <Panel title="Find a patient"><Filters label="Search" fields={[f('q','Patient or username','search',true)]} onChange={value=>setSearch(value.q??'')}/>
  <Data path={withParams('staff/patients/',{q:search})}>{(rows:RecordData[])=><div className="directory">
   {rows.length?rows.map(row=><button type="button" key={row.id} aria-pressed={patientId===row.id} onClick={()=>{setPatientId(row.id);setSelected(undefined);setCreating(false)}}>{row.name}<small>{row.username}</small></button>):<Empty text="No matching patients."/>}
  </div>}</Data>{activePatient&&<button className="text-button" onClick={()=>{setPatientId(undefined);setSelected(undefined)}}>Clear patient filter</button>}</Panel>
 <Panel title="Work areas"><div className="staff-nav">{Object.entries(schema).filter(([key])=>allowed(key)).map(([key,entry])=><button key={key} aria-pressed={resource===key} onClick={()=>choose(key)}><entry.icon size={17}/>{entry.title}</button>)}</div></Panel></div>
 <div className="stack">{!config?<Panel title="Patient records"><Empty text="Choose a work area to view or manage records." /></Panel>:<>
 <Panel title={config.title}>
  {activePatient&&<p className="muted">Patient filter · {activePatient.name}</p>}
  {config.fields.length>0&&<button className="button secondary" onClick={()=>{setCreating(!creating);setSelected(undefined)}}>{creating?'Close form':'Create record'}</button>}
  {creating&&(resource==='proxy'?<><p className="muted">Select a patient, proxy account and initial permission. Add further permissions after saving.</p>
   <ProxyGrant path={listPath} fields={createFields} onSuccess={submitted}/></>:<Action key={resource} path={listPath} fields={createFields} label="Save record" onSuccess={submitted}/>)}
  {!creating&&<Data path={withParams(listPath,{patient:patientId})}>{(rows:RecordData[])=>rows.length?rows.map(row=><button className="record-button" aria-pressed={selected===row.id} key={row.id} onClick={()=>setSelected(row.id)}><Row title={label(row)} detail={row.starts_at?date(row.starts_at):row.provider_name} status={row.status??(row.published===undefined?undefined:row.published?'Published':'Unpublished')}/></button>):<Empty/>}</Data>}
 </Panel>
 {selected&&!creating&&<Data path={detailPath}>{(row:RecordData)=><Panel title={label(row)}>
  <Facts values={Object.entries(row).filter(([key,value])=>key!=='id'&&value!==null&&value!=='').map(([key,value])=>[key.replaceAll('_',' '),Array.isArray(value)?value.join(', '):typeof value==='boolean'?(value?'Yes':'No'):String(value)])}/>
  {['results','visits','documents'].includes(resource)&&<Action path={detailPath} label={row.published?'Unpublish':'Publish to patient'} confirm={row.published?'Unpublish this record?':'Publish this synthetic record to the patient portal?'} fixed={{published:!row.published}}/>}
  {resource==='appointments'&&<><Action path={detailPath} label="Update appointment status" fixed={{action:'status'}} fields={[opt('status','New status',({Scheduled:['Confirmed','Checked In','Cancelled','No Show'],Confirmed:['Checked In','Cancelled','No Show'],'Checked In':['Completed','Cancelled']} as Record<string,string[]>)[row.status]??[]),f('note','Cancellation reason','textarea',true)]}/>
   <Action path={detailPath} label="Reschedule appointment" confirm="Move this appointment to a new slot?" fixed={{action:'reschedule'}} fields={[opt('slot','New slot',slotOptions)]}/></>}
  {resource==='refills'&&<Action path={detailPath} label="Save refill decision" fields={[opt('status','New status',({Requested:['Under Review','Approved','Denied'],'Under Review':['Approved','Denied'],Approved:['Completed']} as Record<string,string[]>)[row.status]??[]),f('decision','Decision note','textarea',true)]}/>}
  {resource==='billing'&&Number(row.balance)>0&&<Action path={detailPath} label="Record simulated payment" confirm="Record this synthetic payment?" fixed={{key:paymentKey}} fields={[{...f('amount','Payment amount','number'),min:.01,step:'.01'}]} onSuccess={()=>setPaymentKey(crypto.randomUUID())}/>}
  {resource==='reports'&&<Action path={detailPath} method="PATCH" label={row.reviewed?'Reopen request':'Mark reviewed'} fixed={{reviewed:!row.reviewed}}/>}
  {resource==='proxy'&&<><Action path={detailPath} method="PATCH" label={row.active?'Revoke access':'Restore access'} confirm="Change access for this proxy account?" fixed={{active:!row.active}}/>
    <div className="inline-actions">{scopes.map(scope=><Action key={scope} path={detailPath} method="PATCH" label={(row.sections.includes(scope)?'Remove ':'Add ')+scope} fixed={{sections:row.sections.includes(scope)?row.sections.filter((item:string)=>item!==scope):[...row.sections,scope]}}/>)}</div></>}
  {config.fields.length>0&&!['appointments','proxy'].includes(resource)&&<details><summary>Edit record</summary><Action key={row.id} path={detailPath} method="PATCH" label="Save edits" fields={createFields.filter(field=>!['patient','encounter'].includes(field.name)||resource==='documents'&&field.name==='encounter').filter(field=>resource!=='slots'||!row.booked||!['starts_at','kind','provider'].includes(field.name)).map(field=>({...field,value:row[field.name]??undefined}))}/></details>}
 </Panel>}</Data>}
 </>}</div></div></>;
}
function ProxyGrant({path,fields,onSuccess}:{path:string;fields:Field[];onSuccess:(value:RecordData)=>void}){
 const [section,setSection]=useState(scopes[0]);
 return <><label>Initial permission<select value={section} onChange={event=>setSection(event.target.value)}>{scopes.map(scope=><option key={scope}>{scope}</option>)}</select></label>
 <Action path={path} fields={fields.filter(field=>field.name!=='section')} label="Grant proxy access" fixed={{sections:[section]}} onSuccess={onSuccess}/></>;
}
