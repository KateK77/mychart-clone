import {useState,type FormEvent} from 'react';
import {Link} from 'react-router-dom';
import {useQueryClient} from '@tanstack/react-query';
import {Users,UserPlus,ShieldCheck,ArrowRight} from 'lucide-react';
import {api,date,withParams,type User} from './api';
import {Action,Data,Empty,ErrorNotice,Heading,Modal,Panel,Tag} from './ui';

const labels:Record<string,string>={appointments:'Appointments',results:'Test Results',medications:'Medications',health:'Health Summary',visits:'Visits',billing:'Billing',documents:'Documents'};

function LinkForm({sections,onDone}:{sections:string[];onDone:()=>void}){
 const [direction,setDirection]=useState('Invite'),[selected,setSelected]=useState(['appointments','results','visits']);
 const [busy,setBusy]=useState(false),[error,setError]=useState<unknown>();
 const client=useQueryClient();
 async function submit(event:FormEvent<HTMLFormElement>){
  event.preventDefault();setError(undefined);if(!selected.length){setError(new Error('Choose at least one section to share.'));return;}
  const values=Object.fromEntries(new FormData(event.currentTarget));setBusy(true);
  try{await api('family-requests/',{...values,direction,sections:selected});await client.invalidateQueries({queryKey:['api']});onDone();}catch(e){setError(e);}finally{setBusy(false);}
 }
 return <form className="action-form" onSubmit={submit}>
  <fieldset className="action-fields" disabled={busy}><label>How would you like to connect?<select value={direction} onChange={e=>setDirection(e.target.value)}><option value="Invite">Invite someone to access my records</option><option value="Request">Request access to a family member's records</option><option value="Guardian">Request dependent / guardian access</option></select></label>
  <p className="notice">{direction==='Invite'?'Your family member must accept before they can view the sections you choose.':direction==='Request'?'Your family member must consent before you can access their records.':'An administrator must verify your guardian relationship before access is granted.'}</p>
  <label>Family member's account email<input type="email" name="email" required maxLength={254}/></label>
  <label>Relationship<input name="relationship" required maxLength={100} placeholder="For example, parent or spouse"/></label>
  <fieldset className="scope-fields"><legend>Sections to share</legend>{sections.map(section=><label key={section}><input type="checkbox" checked={selected.includes(section)} onChange={e=>setSelected(e.target.checked?[...selected,section]:selected.filter(s=>s!==section))}/>{labels[section]}</label>)}</fieldset>
  <p className="muted">Invitations appear in the recipient's Family Access page and expire after 14 days. This demo sends no external email. Use synthetic accounts only.</p></fieldset>
  {error!=null&&<ErrorNotice error={error}/>}<button className="button" disabled={busy}>{busy?'Sending…':direction==='Invite'?'Send invitation':'Send access request'}</button>
 </form>;
}

export function FamilyAccess(){
 const [linking,setLinking]=useState(false),[sent,setSent]=useState(false);
 return <><Heading title="Family Access" description="Stay connected, with permission at every step."><button className="button" onClick={()=>{setSent(false);setLinking(true);}}><UserPlus size={18}/>Link a family member</button></Heading>
  {sent&&<p className="notice success" role="status">Request sent. Access stays pending until consent or guardian review is complete.</p>}
  <Data path="family-requests/">{data=><>
   <div className="equal-grid"><Panel title="Profiles I can access">{!data.linked.length&&<Empty text="No linked profiles yet. Invite or request access to get started."/>}{data.linked.map((row:any)=><article className="family-card" key={row.id}><h3><Users size={20}/>{row.name}</h3><p className="muted">Shared sections</p><div className="inline-actions">{row.sections.map((section:string)=><Link className="button secondary" key={section} to={withParams('/'+section,{patient:row.patient})}>{labels[section]}</Link>)}</div><Action label="Remove my access" path={`family-grants/${row.id}/revoke/`} confirm={`Remove your access to ${row.name}'s shared records?`} success="Access removed."/></article>)}</Panel>
   <Panel title="People who can access my records">{!data.shared.length&&<Empty text="You have not shared your records with anyone."/>}{data.shared.map((row:any)=><article className="family-card" key={row.id}><h3>{row.name} <Tag value={row.active?'Active':'Revoked'}/></h3><p>{row.sections.map((s:string)=>labels[s]).join(', ')}</p>{row.active?<Action label="Revoke access" path={`family-grants/${row.id}/revoke/`} confirm={`Revoke ${row.name}'s access to your records?`} success="Access revoked."/>:<p className="muted">Send a new invitation to share again.</p>}</article>)}</Panel></div>
   <Panel title="Invitations and requests"><p className="muted">Incoming requests need your consent. Outgoing requests show their current status here.</p>{!data.requests.length&&<Empty text="No invitations or requests yet."/>}{data.requests.map((row:any)=><article className="family-card" key={row.id}><div className="request-title"><h3>{row.incoming?`From ${row.from_name}`:`To ${row.to_email}`}</h3><Tag value={row.status}/></div><p>{row.direction==='Invite'?'Invitation to view shared records':row.direction==='Guardian'?'Guardian access review':'Request to view family records'} · {row.relationship}</p><p><strong>Sections:</strong> {row.sections.map((s:string)=>labels[s]).join(', ')}</p>{row.incoming&&row.direction==='Request'&&<p className="notice">Accepting shares these sections of your records with {row.from_name}.</p>}{row.incoming&&row.direction==='Invite'&&<p className="notice">Accepting lets you view these sections of {row.from_name}'s records.</p>}<small>Expires {date(row.expires_at)}</small>{row.decision&&<p>Review note: {row.decision}</p>}<div className="inline-actions">{row.incoming&&row.status==='Pending'&&<><Action label="Accept request" path={`family-requests/${row.id}/`} fixed={{action:'accept'}} confirm="Accept this request and activate access to the listed sections?" success="Family access is now active."/><Action label="Decline request" path={`family-requests/${row.id}/`} fixed={{action:'decline'}} confirm="Decline this request?" success="Request declined."/></>}{row.outgoing&&['Pending','Awaiting review'].includes(row.status)&&<Action label="Cancel request" path={`family-requests/${row.id}/`} fixed={{action:'cancel'}} confirm="Cancel this pending request?" success="Request cancelled."/>}</div></article>)}</Panel>
   {linking&&<Modal title="Link a family member" onClose={()=>setLinking(false)}><LinkForm sections={data.sections} onDone={()=>{setLinking(false);setSent(true);}}/></Modal>}
  </>}</Data>
 </>;
}

export function PendingAccount({user}:{user:User}){
 const client=useQueryClient();const [error,setError]=useState<unknown>();
 async function refresh(){try{const data=await api('session/');client.setQueryData(['session'],data);}catch(e){setError(e);}}
 async function leave(){try{await api('logout/',{});client.removeQueries({queryKey:['api']});client.setQueryData(['session'],(old:any)=>({...old,user:null}));}catch(e){setError(e);}}
 return <main className="pending-account"><span className="eyebrow"><ShieldCheck size={18}/> CARECONNECT 3.0</span><Heading title={user.application?.status==='Declined'?'Application reviewed':'Your care-team application'} description="Your account is created. Workspace access follows administrator approval."/><Panel title={user.application?.role||'Care team'}><Tag value={user.application?.status||'Pending'}/><p>{user.application?.decision||'An administrator will verify your role and organization. You can check your application status here.'}</p><p className="muted">In this local demo, the administrator reviews applications under Access reviews. No external verification email is sent.</p><div className="inline-actions"><button className="button" onClick={()=>void refresh()}>Check application status <ArrowRight size={16}/></button><button className="button secondary" onClick={()=>void leave()}>Sign out</button></div>{error!=null&&<ErrorNotice error={error}/>}</Panel></main>;
}

export function AccessReviews(){
 return <><Heading title="Access reviews" description="Verify staff roles and guardian relationships before granting access."/><Data path="access-reviews/">{data=><>{(['staff','guardian'] as const).map(kind=><Panel key={kind} title={kind==='staff'?'Care-team applications':'Guardian access requests'}>{!data[kind].length&&<Empty text="No applications to review."/>}{data[kind].map((row:any)=><article className="family-card" key={row.id}><h3>{row.name||row.from_name} <Tag value={row.status}/></h3>{kind==='staff'?<p>{row.role} · {row.organization}<br/>{row.email}<br/>{row.reason}</p>:<p>Requested access to {row.to_email} · {row.relationship}<br/>Sections: {row.sections.join(', ')}</p>}{row.decision&&<p>{row.decision}</p>}{['Pending','Awaiting review'].includes(row.status)&&<><p className="notice">{kind==='staff'?'Confirm the applicant’s role and organization before approval.':'Verify the guardian relationship and the dependent account before approval. Approval grants access to the listed sections.'} Demo records only.</p><Action path={`access-reviews/${kind}/${row.id}/`} label="Save access decision" fields={[{name:'action',label:'Decision',options:[{value:'approve',label:'Approve'},{value:'decline',label:'Decline'}]},{name:'decision',label:'Verification / decision note',kind:'textarea'}]} confirm="Save this access decision?" success="Access decision saved."/></>}</article>)}</Panel>)}</>}</Data></>;
}
