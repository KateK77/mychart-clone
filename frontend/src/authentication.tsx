import {useState, type FormEvent} from 'react';
import {Link, useLocation, useNavigate} from 'react-router-dom';
import {useQueryClient} from '@tanstack/react-query';
import {Activity, ArrowLeft, ArrowRight, CalendarDays, Check, Eye, EyeOff, FlaskConical, Heart, LockKeyhole, Mail, MessageCircle, ShieldCheck} from 'lucide-react';
import {api, date} from './api';
import {Data, Empty, ErrorNotice, Panel} from './ui';

export const banner = 'DEMO — SYNTHETIC DATA ONLY — NOT FOR CLINICAL USE.';
export function Brand(){return <Link to="/" className="brand"><span><Activity size={25}/></span><div>CareConnect<small>YOUR HEALTH, CONNECTED</small></div></Link>}

export function PasswordInput({label, name, autoComplete='new-password'}:{label:string;name:string;autoComplete?:string}){
 const [visible,setVisible]=useState(false);
 return <label>{label}<span className="password-input"><input name={name} type={visible?'text':'password'} required maxLength={128} autoComplete={autoComplete}/><button type="button" aria-label={(visible?'Hide ':'Show ')+label.toLowerCase()} onClick={()=>setVisible(!visible)}>{visible?<EyeOff size={18}/>:<Eye size={18}/>}</button></span></label>;
}

export function ChangePassword(){
 const [busy,setBusy]=useState(false),[error,setError]=useState<unknown>(),[success,setSuccess]=useState(false);
 async function submit(event:FormEvent<HTMLFormElement>){
  event.preventDefault(); const form=event.currentTarget; const data=Object.fromEntries(new FormData(form));
  setError(undefined);setSuccess(false);
  if(data.password!==data.confirm_password){setError(new Error('The new passwords do not match.'));return;}
  setBusy(true);
  try{await api('password/',data);form.reset();setSuccess(true);}catch(e){setError(e);}finally{setBusy(false);}
 }
 return <form className="action-form" onSubmit={submit}>
  <p className="muted form-help">Use at least 8 characters. Choose a password you do not use elsewhere.</p>
  <PasswordInput label="Current password" name="current" autoComplete="current-password"/>
  <PasswordInput label="New password" name="password"/>
  <PasswordInput label="Confirm new password" name="confirm_password"/>
  <button className="button" disabled={busy}>{busy?'Updating…':'Change password'}</button>
  {error!=null&&<ErrorNotice error={error}/>}{success&&<p className="notice success" role="status"><Check size={17}/>Your password has been changed.</p>}
 </form>;
}

export function Authentication({demo}:{demo:boolean}){
 const location=useLocation(),navigate=useNavigate(),client=useQueryClient();
 const mode=location.pathname==='/register'?'register':location.pathname==='/forgot-password'?'forgot':location.pathname==='/reset-password'?'reset':location.pathname==='/demo-mailbox'?'mailbox':'login';
 const [busy,setBusy]=useState(false),[error,setError]=useState<unknown>(),[done,setDone]=useState(false);
 const token=new URLSearchParams(location.search).get('token');
 async function submit(event:FormEvent<HTMLFormElement>){
  event.preventDefault();const form=event.currentTarget;const data=Object.fromEntries(new FormData(form));setError(undefined);
  if(['register','reset'].includes(mode)&&data.password!==data.confirm_password){setError(new Error('The new passwords do not match.'));return;}
  setBusy(true);
  try{
   const response=await api(mode==='login'?'login/':mode==='register'?'register/':mode==='forgot'?'password/request-reset/':'password/reset/',mode==='reset'?{...data,token}:data);
   if(mode==='login'||mode==='register'){
    await client.cancelQueries({queryKey:['api']});client.removeQueries({queryKey:['api']});
    client.setQueryData(['session'],{...response,demo_mailbox:demo});navigate('/',{replace:true});
   }else{form.reset();setDone(true);if(mode==='reset')await client.invalidateQueries({queryKey:['session']});}
  }catch(e){setError(e);}finally{setBusy(false);}
 }
 const title={login:'Welcome back',register:'A little closer to better care',forgot:'Forgot your password?',reset:'Choose a new password',mailbox:'Your demo mailbox'}[mode];
 return <div className="auth-page"><div className="auth-story"><Brand/><div className="auth-story-copy"><span className="eyebrow light"><Heart size={15}/> CARE THAT STAYS WITH YOU</span><h1>One place.<br/>{' '}Your whole<br/>{' '}<em>health picture.</em></h1><p>More clarity. Less to keep track of. Connect with your care team and take the next step with confidence.</p>
  <div className="story-features"><span><CalendarDays/>Appointments that fit your life</span><span><FlaskConical/>Your results, clearly explained</span><span><MessageCircle/>A conversation with your care team</span></div></div><div className="story-foot"><ShieldCheck size={18}/>An independent, synthetic-data demonstration.</div><div className="story-orbit" aria-hidden="true"/></div>
  <div className="auth-content"><div className="auth-top"><span className="version-pill">CareConnect 2.0</span><span><LockKeyhole size={14}/> Patient & staff access</span></div>
   <div className="auth-card"><span className="auth-mark">{mode==='mailbox'?<Mail/>:mode==='forgot'||mode==='reset'?<LockKeyhole/>:<Heart/>}</span><h2>{title}</h2>
    <p className="muted">{mode==='login'?'Sign in to manage your health, all in one place.':mode==='register'?'Create your patient account to get started.':mode==='forgot'?'Enter your account email. We will send a link to reset your password.':mode==='reset'?'Choose a strong password and enter it twice to confirm.':'Simulated messages requested from this browser. No external email is sent.'}</p>
    {mode==='mailbox'?demo?<Data path="demo-mailbox/">{data=>data.messages.length?data.messages.map((message:any)=><article key={message.id} className="mail-card"><span className="eyebrow">CARECONNECT ACCOUNT SUPPORT</span><h3>{message.subject}</h3><small>To: {message.to} · {date(message.created_at)}</small><p>{message.body}</p><Link className="button" to={message.link}>Reset password <ArrowRight size={16}/></Link><small>Expires {date(message.expires_at)}</small></article>):<Empty text="No reset messages yet. Request a password reset first."/>}</Data>:<p className="notice">The simulated mailbox is only available in local demo mode.</p>:
    done?<div className="auth-done"><span className="done-icon"><Check/></span><h3>{mode==='forgot'?'Check your email':'Password reset complete'}</h3><p>{mode==='forgot'?'If an account matches that email, a password reset message has been sent.':'You can now sign in with your new password.'}</p>{mode==='forgot'&&demo?<Link className="button" to="/demo-mailbox">Open demo mailbox <Mail size={16}/></Link>:<Link className="button" to="/login">Back to sign in</Link>}</div>:
    mode==='reset'&&!token?<p className="notice error">This reset link is incomplete. Request a new link below.</p>:
    <form className="auth-form" onSubmit={submit}>
     {(mode==='login'||mode==='register')&&<label>Username<input name="username" required maxLength={150} autoComplete="username"/></label>}
     {mode==='register'&&<div className="two-fields"><label>First name<input name="first_name" required autoComplete="given-name"/></label><label>Last name<input name="last_name" required autoComplete="family-name"/></label></div>}
     {(mode==='forgot'||mode==='register')&&<label>Email<input name="email" type="email" required autoComplete="email"/></label>}
     {mode!=='forgot'&&<PasswordInput name="password" label={mode==='reset'?'New password':'Password'} autoComplete={mode==='login'?'current-password':'new-password'}/>}
     {(mode==='reset'||mode==='register')&&<><PasswordInput name="confirm_password" label="Confirm new password"/><p className="form-help muted">At least 8 characters. Avoid common or entirely numeric passwords.</p></>}
     {mode==='login'&&<Link className="forgot-link" to="/forgot-password">Forgot password?</Link>}
     {error!=null&&<ErrorNotice error={error}/>}<button className="button auth-submit" disabled={busy}>{busy?'Please wait…':mode==='login'?'Sign in':mode==='register'?'Create account':mode==='forgot'?'Send reset link':'Reset password'}<ArrowRight size={17}/></button>
    </form>}
    <div className="auth-links">{mode==='login'?<>New to CareConnect? <Link to="/register">Create an account</Link></>:<Link to="/login"><ArrowLeft size={15}/> Back to sign in</Link>}{mode==='reset'&&<Link to="/forgot-password">Request a new reset link</Link>}{mode==='mailbox'&&<Link to="/forgot-password">Request a reset message</Link>}</div>
   </div><footer className="auth-disclaimer">{banner}<small>Not affiliated with Epic Systems or MyChart.</small></footer>
  </div>
 </div>;
}
