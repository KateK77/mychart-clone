import {useState} from 'react';
import {Link,useLocation,useNavigate,useParams} from 'react-router-dom';
import {ArrowRight,Bell,CalendarDays,Clock3,FlaskConical,MessageCircle,Pill,Plus,Wallet,Download,ChevronRight,HeartPulse} from 'lucide-react';
import {date,money,withParams,type RecordData} from './api';
import {Action,Data,Empty,Facts,Filters,Heading,Panel,Row,Tag,Trend,type Field} from './ui';

const titles:Record<string,string>={appointments:'Appointments',messages:'Messages',results:'Test Results',medications:'Medications',health:'Health Summary',visits:'Visits',billing:'Billing',documents:'Documents',family:'Family Access',settings:'Account Settings',notifications:'Notifications'};
const categories=['Medical Question','Appointment Question','Medication Question','Billing Question','General Request'];
const documentTypes=['After Visit Summary','Laboratory Report','Clinical Letter','Visit Instructions','Medication List','Billing Statement','Care Plan'];
const note=(label:string,name='note',optional=false):Field=>({name,label,kind:'textarea',optional});
const items=(rows:RecordData[],render:(row:RecordData)=>React.ReactNode,text?:string)=>rows.length?rows.map(render):<Empty text={text}/>;
const DownloadLink=({href,label}:{href:string;label:string})=><a className="button secondary" href={href}><Download size={16}/>{label}</a>;

export function Dashboard(){
 const actions=[['/appointments/new','Schedule appointment',CalendarDays],['/messages/new','Send message',MessageCircle],['/results','View test results',FlaskConical],['/medications','Request refill',Pill],['/billing','Pay bill',Wallet]] as const;
 return <Data path="dashboard/">{data=><>
   <section className="hero"><div><p className="hero-label"><HeartPulse size={17}/> YOUR HEALTH OVERVIEW</p><h1>Welcome, {data.name.split(' ')[0]}</h1><p>Here’s what’s happening with your care.</p></div>
   <div className="hero-art" aria-hidden="true"><svg viewBox="0 0 350 150" fill="none"><path d="M4 90h84l18-36 23 69 30-104 23 71h162" stroke="currentColor" strokeWidth="3"/><circle cx="160" cy="75" r="70" stroke="currentColor"/><circle cx="160" cy="75" r="49" stroke="currentColor"/></svg></div></section>
   <section className="quick"><h2>Quick actions</h2><div className="quick-grid">{actions.map(([href,label,Icon])=><Link key={href} to={href}><span><Icon size={22}/></span>{label}<ChevronRight className="quick-arrow" size={14}/></Link>)}</div></section>
   <div className="dashboard-grid"><div className="stack">
    <Panel title="Upcoming appointments" action={['/appointments','View all']}>{items(data.appointments,row=><div key={row.id} className="appointment-card"><div className="appointment-mark"><CalendarDays size={24}/></div><div><Tag value={row.status}/><h3>{row.kind}</h3><p>{row.provider_name} · {row.department}</p><p><Clock3 size={15}/>{date(row.starts_at)}</p><Link to={'/appointments/'+row.id}>View appointment <ArrowRight size={15}/></Link></div></div>,'No upcoming appointments.')}</Panel>
    <Panel title="Recent test results" action={['/results','View all']}>{items(data.results,row=><Row key={row.id} title={row.name} detail={date(row.collected_at)} status={row.flag||row.status} to={'/results/'+row.id} icon={<FlaskConical size={17}/>}/>)}</Panel>
    <Panel title="Recent visits" action={['/visits','View all']}>{items(data.visits,row=><Row key={row.id} title={row.kind} detail={date(row.date)+' · '+row.provider_name} to={'/visits/'+row.id}/>)}</Panel>
   </div><div className="stack">
    <Panel title="Messages" action={['/messages','Open inbox']}><div className="metric"><span><MessageCircle size={20}/></span><div><strong>{data.unread}</strong><p>Unread {data.unread===1?'message':'messages'}</p></div></div></Panel>
    <Panel title="Billing" action={['/billing','View billing']}><div className="metric"><span><Wallet size={20}/></span><div><strong>{money(data.balance)}</strong><p>Outstanding balance</p></div></div></Panel>
    <Panel title="Current medications" action={['/medications','View all']}>{items(data.medications,row=><Row key={row.id} title={row.name} detail={row.strength+' · '+row.frequency} to={'/medications/'+row.id}/>)}</Panel>
    <Panel title="Notifications" action={['/notifications','View all']}>{items(data.notifications,(row)=><Row key={row.id} title={row.title} detail={date(row.created_at)} to={row.destination} icon={<Bell size={16}/>}/>)}</Panel>
   </div></div>
 </>}</Data>;
}

export function PatientPage({staff=false}:{staff?:boolean}){
 const {section='',id}=useParams();
 const location=useLocation();
 const navigate=useNavigate();
 const patient=new URLSearchParams(location.search).get('patient');
 const path=(part:string,params={})=>withParams(part,{patient,...params});
 const href=(part:string)=>withParams('/'+part,{patient});
 const root=href(section);
 const back:[string,string]=[root,titles[section]];
 const [filter,setFilter]=useState<Record<string,string>>({});
 const [mode,setMode]=useState('');
 const [paymentKey,setPaymentKey]=useState(()=>crypto.randomUUID());
 const list=(route:string,children:(data:any)=>React.ReactNode)=> <Data path={path(route,filter)}>{children}</Data>;
 const detail=(children:(data:RecordData)=>React.ReactNode)=><Data path={path(section+'/'+id+'/')}>{children}</Data>;
 const go=(route:string)=>navigate(href(route));
 const nested=(part:string)=>href(section+'/'+part);
 const open=(value:number)=>nested(String(value));
 const header=(description?:string,action?:React.ReactNode)=><Heading title={titles[section]} description={description}>{action}</Heading>;
 const invoiceRows=(rows:RecordData[])=>items(rows,row=><Row key={row.id} title={row.description} detail={row.number+' · '+money(row.balance)+' due'} status={row.status} to={open(row.id)}/>);
 const paymentRows=(rows:RecordData[])=>items(rows,row=><Row key={row.id} title={money(row.amount)} detail={date(row.created_at)} to={'/billing?'+new URLSearchParams({receipt:String(row.id),...(patient?{patient}:{})})}/>);
 const action=(label:string,fields:Field[],fixed:object={},confirm?:string)=><Action path={path(section+'/'+id+'/')} label={label} fields={fields} fixed={fixed} confirm={confirm}/>;
 if(staff&&!['messages','settings'].includes(section))return <Heading title="Page unavailable" back={['/','Staff workspace']}/>;

 switch(section){
 case 'appointments': {
  if(id==='new')return <><Heading title="Schedule an appointment" back={back}/><Data path={path('slots/')}>{options=><Panel><Filters onChange={setFilter} label="Find appointments" fields={[
   {name:'provider',label:'Provider',optional:true,options:options.providers.map((p:RecordData)=>({value:p.id,label:p.name}))},
   {name:'kind',label:'Appointment type',optional:true,options:options.types},{name:'date',label:'Date (UTC)',kind:'date',optional:true},
  ]}/></Panel>}</Data><Panel title="Available appointments">{list('slots/',data=>items(data.slots,row=><div className="slot" key={row.id}>
   <Row title={row.kind} detail={row.provider_name+' · '+date(row.starts_at)}/><Action path={path('appointments/')} label="Book" fixed={{slot:row.id}} confirm="Book this appointment?" onSuccess={value=>go('appointments/'+value.id)}/>
  </div>,'No matching appointments.'))}</Panel></>;
  if(id)return detail(row=><><Heading title={row.kind} description={row.provider_name+' · '+date(row.starts_at)} back={back}/><Panel title="Appointment details"><Tag value={row.status}/><Facts values={[['Department',row.department],['Instructions',row.instructions],['Cancellation reason',row.cancellation_reason],['Reschedule request',row.reschedule_requested?row.reschedule_reason:''],['Questionnaire',row.questionnaire]]}/></Panel>
  {['Scheduled','Confirmed'].includes(row.status)&&new Date(row.starts_at)>new Date()&&<div className="dashboard-grid"><Panel title="Before your visit">{action('Save questionnaire',[note('What would you like to discuss at this visit?')],{action:'questionnaire'})}{action('Complete eCheck-In',[],{action:'check-in'},'Complete simulated eCheck-In?')}</Panel><Panel title="Change appointment">{action('Request rescheduling',[note('Preferred dates or times')],{action:'reschedule'})}{action('Cancel appointment',[note('Cancellation reason')],{action:'cancel'},'Cancel this appointment?')}</Panel></div>}</>);
  return <>{header('View or manage your upcoming and past visits.',<Link className="button" to={nested('new')}><Plus size={17}/>Schedule appointment</Link>)}{list('appointments/',(rows:RecordData[])=>{
    const upcoming=(row:RecordData)=>new Date(row.starts_at)>new Date()&&!['Cancelled','Completed','No Show'].includes(row.status);
    const render=(row:RecordData)=><Row key={row.id} title={row.kind} detail={row.provider_name+' · '+date(row.starts_at)} status={row.status} to={open(row.id)}/>;
    return <><Panel title="Upcoming appointments">{items(rows.filter(upcoming),render)}</Panel><Panel title="Past appointments and cancellations">{items(rows.filter(row=>!upcoming(row)),render)}</Panel></>;
  })}</>;
 }
 case 'results':
  if(id)return detail(row=><><Heading title={row.name} description={row.provider_name} back={back}><DownloadLink href={'/api/'+path('results/'+id+'/download/')} label="Download summary"/></Heading><Panel title="Result details">
    <div className="result-value">{row.value??'—'} <small>{row.unit}</small> {row.flag&&<Tag value={row.flag}/>}</div>
    <Facts values={[['Status',row.status],['Collected',date(row.collected_at)],['Resulted',date(row.resulted_at)],['Reference range',row.reference_low===null&&row.reference_high===null?'—':(row.reference_low??'—')+' to '+(row.reference_high??'—')+' '+row.unit],['Comments',row.comments]]}/></Panel><Panel title="Historical measurements"><Trend rows={row.history}/></Panel></>);
  return <>{header('Review published lab reports and historical measurements.')}<Panel><Filters onChange={setFilter} fields={[{name:'q',label:'Test name',optional:true},{name:'after',label:'Collected from',kind:'date',optional:true},{name:'before',label:'Collected through',kind:'date',optional:true}]}/></Panel>
   <Panel title="Laboratory results">{list('results/',rows=>items(rows,row=><Row key={row.id} title={row.name} detail={date(row.collected_at)+' · '+(row.value??row.status)+' '+row.unit} status={row.flag||row.status} icon={<FlaskConical size={17}/>} to={open(row.id)}/>))}</Panel></>;
 case 'messages':
  if(id==='new'&&!staff)return <><Heading title="New message" back={back}/><Panel title="Compose"><p className="notice">Use this inbox for non-emergency communication.</p><Action path="messages/" label="Send message" onSuccess={value=>go('messages/'+value.id)} fields={[
   {name:'team',label:'Recipient',options:['Care team','Scheduling','Billing']},{name:'category',label:'Category',options:categories},{name:'subject',label:'Subject'},note('Message','body'),
  ]}/></Panel></>;
  if(id)return detail(row=><><Heading title={row.subject} description={row.category+' · '+row.team} back={back}/><Panel title="Conversation">
   {items(row.messages,message=><article className={'message '+(message.mine?'mine':'')} key={message.id}><strong>{message.sender}</strong><small>{date(message.created_at)}</small><p>{message.body}</p></article>)}
   <p className="notice">Use this inbox for non-emergency communication.</p>{action('Send reply',[note('Reply','body')],{action:'reply'})}
   <div className="inline-actions"><Action path={'messages/'+id+'/'} label="Archive" fixed={{action:'archive'}} confirm="Archive this conversation?" onSuccess={()=>go('messages')}/><Action path={'messages/'+id+'/'} label="Restore to inbox" fixed={{action:'restore'}}/></div></Panel></>);
  return <>{header('Secure, non-emergency conversations with your care team.',!staff&&<Link className="button" to="/messages/new"><Plus size={17}/>New message</Link>)}
   <Panel><div className="tabs">{['inbox','sent','archive'].map(box=><button key={box} aria-pressed={(mode||'inbox')===box} onClick={()=>setMode(box)}>{box}</button>)}</div>
   <Data path={withParams('messages/',{box:mode||'inbox'})}>{rows=>items(rows,row=><Row key={row.id} title={row.subject} detail={(staff?row.patient_name+' · ':'')+row.category+' · '+row.team} status={row.unread?row.unread+' unread':undefined} to={open(row.id)} icon={<MessageCircle size={18}/>}/>)}</Data></Panel></>;
 case 'medications': {
  const refill=(row:RecordData)=><Row key={row.id} title={row.medication_name} detail={row.decision||date(row.created_at)} status={row.status}/>;
  if(id)return detail(row=><><Heading title={row.name} description={row.strength+' · '+row.status} back={back}/>
   <Panel title="Prescription details"><Facts values={[['Dosage',row.dosage],['Route',row.route],['Frequency',row.frequency],['Started',date(row.start_date)],['Ended',date(row.end_date)],['Prescriber',row.provider_name],['Pharmacy',row.pharmacy],['Instructions',row.instructions]]}/></Panel>
   <div className="dashboard-grid"><Panel title="Refills">{items(row.refills,refill)}{row.status==='Active'&&action('Request refill',[note('Note for your care team','note',true)],{},'Submit this simulated refill request?')}</Panel><Panel title="Report information discrepancy"><Action path={path('report/')} label="Send report" fields={[note('What information should be reviewed?','details')]} fixed={{topic:'Medication'}}/></Panel></div></>);
  return <>{header('Review prescriptions and track refill requests.')}<Panel><Filters fields={[{name:'q',label:'Medication name',optional:true}]} onChange={setFilter}/></Panel>
   {list('medications/',data=><>{['Active','Discontinued'].map(status=><Panel key={status} title={status==='Active'?'Active medications':'Medication history'}>{items(data.medications.filter((row:RecordData)=>row.status===status),row=><Row key={row.id} title={row.name} detail={row.strength+' · '+row.frequency} to={open(row.id)} icon={<Pill size={17}/>}/>)}</Panel>)}<Panel title="Refill requests">{items(data.refills,refill)}</Panel></>)}</>;
 }
 case 'health':
  return <>{header('Your clinical records and care team.')}<Data path={path('health/')}>{value=><><Panel title="Demographics"><Facts values={[['Name',value.demographics.name],['Date of birth',date(value.demographics.birth_date)],['Phone',value.demographics.phone],['Address',value.demographics.address]]}/></Panel>
  <div className="equal-grid">{Object.entries(value.sections).map(([title,rows])=><Panel key={title} title={title}>{items(rows as RecordData[],row=><Row key={row.id} title={row.title} detail={row.details}/>)}</Panel>)}<Panel title="Current medications">{items(value.medications,row=><Row key={row.id} title={row.name} detail={row.strength+' · '+row.frequency}/>)}</Panel></div>
  <Panel title="Request a correction"><Action path={path('report/')} label="Send request" fields={[note('What information should be reviewed?','details')]} fixed={{topic:'Health summary'}}/></Panel></>}</Data></>;
 case 'visits':
  if(id)return detail(row=><><Heading title={row.kind} description={date(row.date)+' · '+row.provider_name} back={back}/><Panel title="Encounter summary">
    <Facts values={[['Department',row.department],['Reason for visit',row.reason],['Summary',row.summary],['Follow-up',row.follow_up]]}/></Panel><Panel title="Diagnoses">{items(row.diagnoses,item=><Row key={item.id} title={item.label} detail={item.code}/>)}</Panel>
    <Panel title="Shared clinical notes">{items(row.notes,item=><Row key={item.id} title={item.title} detail={item.body}/>)}</Panel><Panel title="After Visit Summary">{items(row.documents,item=><Row key={item.id} title={item.title} to={href('documents/'+item.id)}/>)}</Panel></>);
  return <>{header('Find encounter summaries and shared clinical notes.')}<Panel title="Past visits">{list('visits/',rows=>items(rows,row=><Row key={row.id} title={row.kind} detail={date(row.date)+' · '+row.provider_name} to={open(row.id)}/>))}</Panel></>;
 case 'billing': {
  const receipt=new URLSearchParams(location.search).get('receipt');
  if(receipt)return <><Heading title="Payment receipt" back={back}/><Panel><DownloadLink href={'/api/'+path('billing/receipt/'+encodeURIComponent(receipt)+'/')} label="Download receipt"/></Panel></>;
  if(id)return detail(row=><><Heading title={row.description} description={row.number} back={back}/><Panel title="Invoice details"><Tag value={row.status}/><Facts values={[['Service date',date(row.service_date)],['Due date',date(row.due_date)],['Charges',money(row.amount)],['Insurance adjustment',money(row.adjustment)],['Patient responsibility',money(row.responsibility)],['Paid',money(row.paid)],['Remaining',money(row.balance)]]}/></Panel>
   {Number(row.balance)>0&&<Panel title="Simulated payment"><Action path={path('billing/'+id+'/')} label="Submit simulated payment" confirm="Record this synthetic payment?" fixed={{key:paymentKey}} fields={[{name:'amount',label:'Payment amount (USD)',kind:'number',min:0.01,step:'0.01',value:row.balance}]} onSuccess={()=>setPaymentKey(crypto.randomUUID())}/></Panel>}
   <Panel title="Payment history">{paymentRows(row.payments)}</Panel></>);
  return <>{header('View invoices, insurance, and simulated transactions.')}<Data path={path('billing/')}>{row=><><Panel title="Outstanding balance"><div className="result-value">{money(row.balance)}</div></Panel>
   <Panel title="Invoices">{invoiceRows(row.invoices)}</Panel><Panel title="Payment history">{paymentRows(row.payments)}</Panel><Panel title="Insurance">{items(row.insurance,record=><Row key={record.id} title={record.carrier} detail={record.plan+' · '+record.member_id}/>)}</Panel></>}</Data></>;
 }
 case 'documents':
  if(id)return detail(row=><><Heading title={row.title} description={row.kind+' · '+date(row.created_at)} back={back}><DownloadLink href={'/api/'+path('documents/'+id+'/download/')} label="Download document"/></Heading><Panel><p className="pre-wrap">{row.content}</p>{row.encounter&&<Link to={href('visits/'+row.encounter)}>Associated visit</Link>}</Panel></>);
  return <>{header('Open and download your published medical documents.')}<Panel><Filters onChange={setFilter} fields={[{name:'kind',label:'Document type',options:documentTypes,optional:true}]}/><Data path={path('documents/')}>{rows=>items(rows.filter((row:RecordData)=>!filter.kind||row.kind===filter.kind),row=><Row key={row.id} title={row.title} detail={row.kind+' · '+date(row.created_at)+(row.encounter?' · Linked visit':'')} to={open(row.id)}/>)}</Data></Panel></>;
 case 'family':
  return <>{header('Open records shared with you through an authorized proxy relationship.')}<Panel title="Linked profiles"><Data path="family/">{rows=>items(rows,row=><div key={row.patient} className="family-profile"><h3>{row.name}</h3><div className="inline-actions">{row.sections.map((part:string)=><Link className="button secondary" key={part} to={withParams('/'+part,{patient:row.patient})}>{titles[part]}</Link>)}</div></div>,'No profiles have been shared with you.')}</Data></Panel></>;
 case 'notifications':
  return <>{header('Updates from your care team and account activity.')}<Panel><Action path="notifications/" label="Mark all as read"/><Data path="notifications/">{rows=>items(rows,row=><div className="slot" key={row.id}><Row title={row.title} detail={date(row.created_at)} status={row.read?'Read':'Unread'} to={row.destination}/>{!row.read&&<Action path="notifications/" label="Mark as read" fixed={{id:row.id}}/>}</div>)}</Data></Panel></>;
 case 'settings':
  return <>{header('Manage your contact information, password, and preferences.')}<Data path="profile/">{profile=><>
   <Panel title="Profile"><Action path="profile/" method="PATCH" label="Save profile" fields={[
    {name:'email',label:'Email',kind:'email',value:profile.email},...(!staff?[{name:'phone',label:'Phone',value:profile.phone,optional:true},{name:'address',label:'Address',value:profile.address,optional:true}]:[]),
   ]}/></Panel><Panel title="Change password"><Action path="password/" label="Change password" fields={[{name:'current',label:'Current password',kind:'password'},{name:'password',label:'New password',kind:'password'}]}/></Panel>
   {!staff&&<Panel title="Notification preferences"><p className="muted">Mute categories individually. Existing notifications remain visible.</p>{profile.notification_types.map((kind:string)=><div className="slot" key={kind}><Row title={kind}/><Action path="profile/" method="PATCH" label={profile.muted_notifications.includes(kind)?'Unmute':'Mute'} fixed={{muted_notifications:profile.muted_notifications.includes(kind)?profile.muted_notifications.filter((item:string)=>item!==kind):[...profile.muted_notifications,kind]}}/></div>)}</Panel>}</>}</Data></>;
 default:return <Heading title="Page unavailable" back={['/','Home']}/>;
 }
}

export function PatientPageRoute({staff}:{staff:boolean}){
 const {section,id}=useParams();
 return <PatientPage key={section+'/'+id} staff={staff}/>;
}
