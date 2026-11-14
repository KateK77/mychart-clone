import {useState} from 'react';
import {useQuery} from '@tanstack/react-query';
import {useSearchParams} from 'react-router-dom';
import {ArrowLeft,ArrowRight,CalendarDays,ChevronRight,ClipboardList,FileText,FlaskConical,LayoutGrid,Plus,Search,ShieldCheck,Users,Wallet} from 'lucide-react';
import {api,date,money,withParams,type RecordData} from './api';
import {Action,Empty,ErrorNotice,Facts,Heading,Loading,Modal,Panel,Tag,type Field} from './ui';
import {schema,scopes} from './staff-schema';

const workGroups=[
 {name:'Scheduling',icon:CalendarDays,keys:['appointments','slots','providers','departments']},
 {name:'Clinical care',icon:FlaskConical,keys:['results','medications','refills','health','reports']},
 {name:'Visits & documents',icon:FileText,keys:['visits','diagnoses','notes','documents']},
 {name:'Billing',icon:Wallet,keys:['billing','insurance']},
 {name:'Family access',icon:Users,keys:['proxy']},
];
const descriptions:Record<string,string>={appointments:'Book, confirm and reschedule visits.',slots:'Maintain available dates and times.',providers:'Manage your care team directory.',departments:'Organize clinical departments.',results:'Create, review and publish lab results.',medications:'Maintain current prescriptions.',refills:'Review requests and share decisions.',health:'Keep clinical history up to date.',reports:'Review patient correction requests.',visits:'Create and publish encounter summaries.',diagnoses:'Manage diagnoses associated with visits.',notes:'Write shared or private clinical notes.',documents:'Publish medical documents to patients.',billing:'Manage statements and simulated payments.',insurance:'Maintain synthetic coverage information.',proxy:'Control access to linked family profiles.'};
const scopeLabels:Record<string,string>={appointments:'Appointments',results:'Test results',medications:'Medications',health:'Health summary',visits:'Visits',billing:'Billing',documents:'Documents'};
const select=(name:string,label:string,options:Field['options']):Field=>({name,label,options});
const note=(name:string,label:string):Field=>({name,label,kind:'textarea',optional:true});
const options=(rows:RecordData[]|undefined,label:(row:RecordData)=>string,key='id')=>(rows??[]).map(row=>({value:row[key],label:label(row)}));

export function Staff(){
 const [params,setParams]=useSearchParams();
 const resource=params.get('area')??'',patientId=Number(params.get('person'))||undefined,selected=Number(params.get('record'))||undefined;
 const [creating,setCreating]=useState(false),[search,setSearch]=useState(''),[group,setGroup]=useState('All areas');
 const [paymentKey,setPaymentKey]=useState(()=>crypto.randomUUID());
 const session=useQuery({queryKey:['session'],queryFn:()=>api('session/')});
 const roles:string[]=session.data?.user?.roles??[];
 const allowed=(key:string)=>!!schema[key]&&(roles.includes('Administrator')||schema[key].roles.some(role=>roles.includes(role)));
 const directory=useQuery({queryKey:['api','staff/patients/'],queryFn:()=>api('staff/patients/')});
 const providers=useQuery({queryKey:['api','staff/providers/'],queryFn:()=>api('staff/providers/'),enabled:allowed('providers')});
 const departments=useQuery({queryKey:['api','staff/departments/'],queryFn:()=>api('staff/departments/'),enabled:allowed('departments')});
 const slots=useQuery({queryKey:['api','staff/slots/'],queryFn:()=>api('staff/slots/'),enabled:allowed('slots')});
 const visits=useQuery({queryKey:['api','staff/visits/'],queryFn:()=>api('staff/visits/'),enabled:allowed('visits')});
 const config=allowed(resource)?schema[resource]:undefined;
 const listPath='staff/'+resource+'/';
 const list=useQuery({queryKey:['api',withParams(listPath,{patient:patientId})],queryFn:()=>api(withParams(listPath,{patient:patientId})),enabled:!!config});
 const detailPath=listPath+selected+'/';
 const detail=useQuery({queryKey:['api',detailPath],queryFn:()=>api(detailPath),enabled:!!config&&!!selected&&!creating});
 const people:RecordData[]=directory.data??[];
 const activePatient=people.find(row=>row.id===patientId);
 function change(values:Record<string,string|number|undefined>){const next=new URLSearchParams(params);Object.entries(values).forEach(([key,value])=>value===undefined?next.delete(key):next.set(key,String(value)));setParams(next);}
 function choose(area:string){setCreating(false);setSearch('');change({area:area||undefined,record:undefined});}
 function close(){setCreating(false);change({record:undefined});}
 const submitted=(row:RecordData)=>{setCreating(false);change({record:row.id});};
 const available=(slots.data??[]).filter((row:RecordData)=>row.active&&row.available).sort((a:RecordData,b:RecordData)=>a.starts_at.localeCompare(b.starts_at));
 const slotOptions=options(available,row=>row.provider_name+' · '+row.kind+' · '+date(row.starts_at));
 const resolve=(field:Field):Field=>{
  const values:Record<string,Field['options']>={patient:options(people,row=>row.name),provider:options(providers.data,row=>row.name),department:options(departments.data,row=>row.name),encounter:options(visits.data?.filter((row:RecordData)=>!patientId||row.patient===patientId),row=>(people.find(p=>p.id===row.patient)?.name??'Patient')+' · '+row.kind+' · '+date(row.date)),slot:slotOptions,proxy:options(people,row=>row.name,'user')};
  return values[field.name]?{...field,options:values[field.name],value:field.name==='patient'?patientId:field.value}:field;
 };
 const fields=(config?.fields??[]).map(resolve);
 const recordTitle=(row:RecordData)=>row.name||row.title||row.subject||row.description||row.medication_name||row.label||row.kind||row.carrier||row.topic||row.reason||(resource==='proxy'?(people.find(p=>p.id===row.patient)?.name??'Family')+' proxy access':'Record '+row.id);
 const patientName=(row:RecordData)=>people.find(p=>p.id===row.patient)?.name;
 const recordSubtitle=(row:RecordData)=>[patientName(row),row.provider_name,row.starts_at?date(row.starts_at):row.collected_at?date(row.collected_at):row.date?date(row.date):row.created_at?date(row.created_at):null].filter(Boolean).join(' · ');
 const visible=(list.data??[]).filter((row:RecordData)=>(recordTitle(row)+' '+recordSubtitle(row)+' '+(row.status??'')).toLowerCase().includes(search.toLowerCase()));
 const groups=workGroups.filter(g=>g.keys.some(allowed));
 function facts(row:RecordData){
  const hidden=['id','patient','provider','slot','predecessor','encounter','proxy','provider_name','medication','name','title','subject','description','kind'];
  const values:[string,any][]=[];
  if(patientName(row))values.push(['Patient',patientName(row)]);
  if(row.provider_name)values.push(['Provider',row.provider_name]);
  if(row.proxy)values.push(['Proxy account',people.find(p=>p.user===row.proxy)?.name??'Linked account']);
  if(row.encounter){const visit=visits.data?.find((v:RecordData)=>v.id===row.encounter);if(visit)values.push(['Linked visit',visit.kind+' · '+date(visit.date)]);}
  Object.entries(row).filter(([key,value])=>!hidden.includes(key)&&value!==null&&value!=='').forEach(([key,value])=>{
   const display=key==='sections'?(value as string[]).map(s=>scopeLabels[s]??s).join(', '):typeof value==='boolean'?(value?'Yes':'No'):['status'].includes(key)?<Tag value={String(value)}/>:['created_at','starts_at','collected_at','resulted_at','date','service_date','due_date','start_date','end_date'].includes(key)?date(String(value)):['amount','paid','balance','responsibility','adjustment'].includes(key)?money(value):Array.isArray(value)?value.join(', '):String(value);
   values.push([key==='published'?'Shared with patient':key.replaceAll('_',' '),display]);
  });return values;
 }
 const row=detail.data;
 const appointmentStates:Record<string,string[]>={Scheduled:['Confirmed','Checked In','Cancelled','No Show'],Confirmed:['Checked In','Cancelled','No Show'],'Checked In':['Completed','Cancelled']};
 const refillStates:Record<string,string[]>={Requested:['Under Review','Approved','Denied'],'Under Review':['Approved','Denied'],Approved:['Completed']};
 return <>
  <Heading title="Staff workspace" description="A clear view of your patients. A simpler way to manage their care."><span className="role-badge"><ShieldCheck size={16}/>{roles.join(' · ')}</span></Heading>
  <div className="staff-toolbar"><div className="patient-picker"><Users size={19}/><label>Patient context<select aria-label="Patient context" value={patientId??''} onChange={e=>{setCreating(false);change({person:e.target.value||undefined,record:undefined});}}><option value="">All patients</option>{people.map(p=><option key={p.id} value={p.id}>{p.name} ({p.username})</option>)}</select></label></div><div className="context-explanation">{activePatient?<><strong>{activePatient.name}</strong><span>Patient records are filtered to this profile.</span></>:<><strong>Your care workspace</strong><span>Select a patient to focus the record list.</span></>}</div>{activePatient&&<button className="text-button" onClick={()=>change({person:undefined,record:undefined})}>Clear patient filter</button>}</div>
  {directory.isError&&<ErrorNotice error={directory.error}/>}
  {!config?<>
   <div className="workarea-heading"><h2>Choose a work area</h2><label className="search-field"><Search size={18}/><input aria-label="Find a work area" placeholder="Find a work area…" value={search} onChange={e=>setSearch(e.target.value)}/></label></div>
   <div className="work-tabs" aria-label="Work area groups">{['All areas',...groups.map(g=>g.name)].map(name=><button key={name} aria-pressed={group===name} onClick={()=>setGroup(name)}>{name==='All areas'&&<LayoutGrid size={16}/ >}{name}</button>)}</div>
   {groups.filter(g=>group==='All areas'||group===g.name).map(g=>{const keys=g.keys.filter(allowed).filter(key=>(schema[key].title+' '+descriptions[key]).toLowerCase().includes(search.toLowerCase()));return keys.length?<section className="workarea-group" key={g.name}><h3><g.icon size={17}/>{g.name}</h3><div className="workarea-grid">{keys.map(key=>{const Icon=schema[key].icon;return <button className="workarea-card" aria-label={schema[key].title} key={key} onClick={()=>choose(key)}><span className="workarea-icon"><Icon size={21}/></span><strong>{schema[key].title}</strong><p>{descriptions[key]}</p><ArrowRight size={17}/></button>;})}</div></section>:null;})}
   {search&&!groups.some(g=>(group==='All areas'||group===g.name)&&g.keys.some(key=>allowed(key)&&(schema[key].title+' '+descriptions[key]).toLowerCase().includes(search.toLowerCase())))&&<Empty text="No matching work areas. Try a different search."/>}
  </>:<>
   <div className="module-toolbar"><button className="button secondary" onClick={()=>choose('')}><ArrowLeft size={16}/>All work areas</button><label>Work area<select aria-label="Work area" value={resource} onChange={e=>choose(e.target.value)}>{groups.map(g=><optgroup key={g.name} label={g.name}>{g.keys.filter(allowed).map(key=><option key={key} value={key}>{schema[key].title}</option>)}</optgroup>)}</select></label></div>
   <Panel className="record-list"><div className="record-list-heading"><div><span className="eyebrow">{activePatient?.name??'ALL PATIENTS'}</span><h2>{config.title}</h2><p className="muted">{descriptions[resource]}</p></div>{fields.length>0&&<button className="button" onClick={()=>{change({record:undefined});setCreating(true);}}><Plus size={17}/>Create record</button>}</div>
    <div className="record-search"><label className="search-field"><Search size={18}/><input aria-label="Search records" placeholder="Search names, dates or status…" value={search} onChange={e=>setSearch(e.target.value)}/></label><span>{visible.length} {visible.length===1?'record':'records'}</span></div>
    {list.isPending?<Loading/>:list.isError?<ErrorNotice error={list.error}/>:visible.length?visible.map((record:RecordData)=><button className="record-button" key={record.id} onClick={()=>change({record:record.id})}><span className="record-list-icon"><config.icon size={19}/></span><span className="record-copy"><strong>{recordTitle(record)}</strong><small>{recordSubtitle(record)}</small></span><span className="record-tags">{record.status&&<Tag value={record.status}/ >}{record.published!==undefined&&<Tag value={record.published?'Published':'Unpublished'}/>}</span><ChevronRight size={18}/></button>):<Empty text="No records match this view. Choose another patient or create a record."/>}
   </Panel>
  </>}
  {config&&(creating||selected)&&<Modal key={creating?'new':selected} title={creating?'Create '+config.title.toLowerCase():row?recordTitle(row):'Record details'} drawer onClose={close}>
   {creating?<><p className="muted drawer-intro">{descriptions[resource]} All records in this workspace are synthetic.</p>{resource==='proxy'?<ProxyGrant path={listPath} fields={fields} onSuccess={submitted}/>:<Action path={listPath} fields={fields} label="Save record" onSuccess={submitted}/>}</>:detail.isPending?<Loading/>:detail.isError?<ErrorNotice error={detail.error}/>:row&&<>
    <p className="drawer-intro muted">{recordSubtitle(row)}</p><Facts values={facts(row)}/>
    {['results','visits','documents'].includes(resource)&&<section className="drawer-section"><h3>Patient visibility</h3><p className="muted">{row.published?'This record is visible in the patient portal.':'This record is private until you publish it.'}</p><Action path={detailPath} label={row.published?'Unpublish':'Publish to patient'} confirm={row.published?'Remove this record from the patient portal? It will remain available to your care team.':'Share this synthetic record with the patient?'} fixed={{published:!row.published}} success={row.published?'Publication updated.':'Publication updated.'}/></section>}
    {resource==='appointments'&&<>{appointmentStates[row.status]?.length>0&&<section className="drawer-section"><h3>Update appointment</h3><Action path={detailPath} label="Update appointment status" fixed={{action:'status'}} fields={[select('status','New status',appointmentStates[row.status]),note('note','Cancellation reason')]}/></section>}{['Scheduled','Confirmed'].includes(row.status)&&new Date(row.starts_at)>new Date()&&<section className="drawer-section"><h3>Reschedule</h3><p className="muted">Choose a new time. The previous booking stays in the appointment history.</p><Action path={detailPath} label="Reschedule appointment" confirm="Move this appointment to the selected time?" fixed={{action:'reschedule'}} fields={[select('slot','New slot',slotOptions)]} onSuccess={submitted}/></section>}</>}
    {resource==='refills'&&refillStates[row.status]?.length>0&&<section className="drawer-section"><h3>Review request</h3><Action path={detailPath} label="Save refill decision" fields={[select('status','New status',refillStates[row.status]),note('decision','Decision note')]}/></section>}
    {resource==='billing'&&Number(row.balance)>0&&<section className="drawer-section"><h3>Simulated payment</h3><Action path={detailPath} label="Record simulated payment" confirm="Record this synthetic payment? No real money will be collected." fixed={{key:paymentKey}} fields={[{name:'amount',label:'Payment amount (USD)',kind:'number',min:.01,step:'.01'}]} onSuccess={()=>setPaymentKey(crypto.randomUUID())}/></section>}
    {resource==='reports'&&<Action path={detailPath} method="PATCH" label={row.reviewed?'Reopen request':'Mark reviewed'} fixed={{reviewed:!row.reviewed}}/>}
    {resource==='proxy'&&<><section className="drawer-section"><h3>Access status</h3><Action path={detailPath} method="PATCH" label={row.active?'Revoke access':'Restore access'} confirm="Change this account's access to the family profile?" fixed={{active:!row.active}}/></section><section className="drawer-section"><h3>Shared sections</h3><p className="muted">{row.active?'Choose what this account can access.':'Access is revoked. These settings apply when access is restored.'}</p><div className="permission-list">{scopes.map(scope=><div key={scope}><span>{scopeLabels[scope]}</span><Action path={detailPath} method="PATCH" label={row.sections.includes(scope)?'Remove access':'Allow access'} fixed={{sections:row.sections.includes(scope)?row.sections.filter((s:string)=>s!==scope):[...row.sections,scope]}}/></div>)}</div></section></>}
    {fields.length>0&&!['appointments','proxy'].includes(resource)&&<details className="drawer-section"><summary>Edit record</summary><Action key={row.id} path={detailPath} method="PATCH" label="Save edits" fields={fields.filter(field=>!['patient','encounter'].includes(field.name)||resource==='documents'&&field.name==='encounter').filter(field=>resource!=='slots'||!row.booked||!['starts_at','kind','provider'].includes(field.name)).map(field=>({...field,value:field.kind==='datetime-local'?row[field.name]?.slice(0,16):row[field.name]??undefined}))}/></details>}
   </>}
  </Modal>}
 </>;
}
function ProxyGrant({path,fields,onSuccess}:{path:string;fields:Field[];onSuccess:(value:RecordData)=>void}){
 const [section,setSection]=useState('appointments');
 return <><label>Initial permission<select value={section} onChange={e=>setSection(e.target.value)}>{scopes.map(scope=><option key={scope} value={scope}>{scopeLabels[scope]}</option>)}</select></label><Action path={path} fields={fields.filter(f=>f.name!=='section')} label="Grant proxy access" fixed={{sections:[section]}} onSuccess={onSuccess}/></>;
}
