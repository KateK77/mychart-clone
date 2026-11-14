import {useState} from 'react';
import {createRoot} from 'react-dom/client';
import {BrowserRouter,Link,NavLink,Navigate,Route,Routes,useLocation,useNavigate} from 'react-router-dom';
import {QueryClient,QueryClientProvider,useQuery,useQueryClient} from '@tanstack/react-query';
import {Activity,Bell,CalendarDays,ClipboardList,FileText,FlaskConical,HeartPulse,House,LogOut,Menu,MessageCircle,Pill,Settings,Users,Wallet,X} from 'lucide-react';
import {api,type User} from './api';
import {Action,ErrorNotice,Heading,Loading,Panel} from './ui';
import {Dashboard,PatientPageRoute} from './patient';
import {Staff} from './staff';
import './style.css';

const queryClient=new QueryClient({defaultOptions:{queries:{retry:false,staleTime:1000}}});
const items=[
 ['','Dashboard',House],['appointments','Appointments',CalendarDays],['messages','Messages',MessageCircle],
 ['results','Test Results',FlaskConical],['medications','Medications',Pill],['health','Health Summary',HeartPulse],
 ['visits','Visits',ClipboardList],['billing','Billing',Wallet],['documents','Documents',FileText],
 ['family','Family Access',Users],['settings','Account Settings',Settings],
] as const;
export const sectionLabels=Object.fromEntries(items.map(([route,label])=>[route,label]));
export const banner='DEMO — SYNTHETIC DATA ONLY — NOT FOR CLINICAL USE.';

function Brand(){return <Link to="/" className="brand"><span><Activity size={23}/></span><div>CareConnect<small>PATIENT PORTAL</small></div></Link>}
function Login(){
 const [registration,setRegistration]=useState(false);
 const client=useQueryClient();
 return <div className="login-page"><Brand/><div className="login-main">
   <div className="login-intro"><div className="login-symbol"><HeartPulse size={58}/></div><h1>Your health,<br/>within reach.</h1><p>Manage appointments, view test results and stay in touch with your care team.</p></div>
   <Panel title={registration?'Create your account':'Welcome to CareConnect'}>
    <p className="muted">{registration?'Register for the synthetic patient portal.':'Sign in to access your patient or staff account.'}</p>
    <Action key={String(registration)} path={registration?'register/':'login/'} label={registration?'Create account':'Sign in'} onSuccess={response=>client.setQueryData(['session'],response)}
      fields={[{name:'username',label:'Username'},...(registration?[{name:'first_name',label:'First name'},{name:'last_name',label:'Last name'},{name:'email',label:'Email',kind:'email'}]:[]),{name:'password',label:'Password',kind:'password'}]}/>
    <button className="text-button" onClick={()=>setRegistration(!registration)}>{registration?'Back to sign in':'Create a patient account'}</button>
   </Panel>
 </div><div className="demo-banner">{banner}</div></div>;
}
function Shell({user}:{user:User}){
 const [menu,setMenu]=useState(false);
 const client=useQueryClient();
 const location=useLocation();
 const navigate=useNavigate();
 const proxy=new URLSearchParams(location.search).get('patient');
 const staff=!user.patient;
 const sidebar=staff?[['','Staff workspace',House],['messages','Messages',MessageCircle],['settings','Account Settings',Settings]] as const:items;
 const [logoutError,setLogoutError]=useState<unknown>(null);
 const leave=async()=>{try{await api('logout/',{});client.clear();client.setQueryData(['session'],{user:null});navigate('/');}catch(error){setLogoutError(error);}};
 const badge=useQuery({queryKey:['api','notifications/'],queryFn:()=>api('notifications/'),enabled:!staff});
 return <div className="app"><aside className={'sidebar '+(menu?'open':'')}><Brand/><nav aria-label="Main navigation">{sidebar.map(([route,label,Icon])=>
   <NavLink onClick={()=>setMenu(false)} key={route} end={!route} to={'/'+route+(proxy&&['appointments','results','medications','health','visits','billing','documents'].includes(route)?'?patient='+proxy:'')}><Icon size={18}/>{label}</NavLink>
 )}</nav><div className="side-footer"><div className="avatar">{user.name.split(' ').slice(0,2).map(word=>word[0]).join('')}</div><div><strong>{user.name}</strong><small>{user.roles[0]}</small></div><button aria-label="Sign out" title="Sign out" onClick={()=>void leave()}><LogOut size={17}/></button></div></aside>
 <div className="workspace"><div className="topbar"><button className="menu-toggle icon-button" aria-label={menu?'Close menu':'Open menu'} onClick={()=>setMenu(!menu)}>{menu?<X/>:<Menu/>}</button><span className="top-title">{staff?'Staff workspace':'Patient portal'}</span>
 {!staff&&<Link to="/notifications" className="icon-button bell" aria-label="Notifications"><Bell size={20}/>{badge.data?.some((notice:{read:boolean})=>!notice.read)&&<i/>}</Link>}
 </div><div className="demo-banner">{banner}</div><main>
 {logoutError!=null&&<ErrorNotice error={logoutError}/>}
 {proxy&&<div className="notice proxy">Viewing a linked family profile <Link to="/family">Switch profile</Link></div>}
 <Routes>
 <Route path="/" element={staff?<Staff/>:<Dashboard/>}/>
 <Route path="/staff" element={staff?<Staff/>:<Navigate to="/" replace/>}/>
 <Route path="/:section/:id?" element={<PatientPageRoute staff={staff}/>}/>
 <Route path="*" element={<Heading title="Page unavailable"><Link to="/">Return home</Link></Heading>}/>
 </Routes></main></div></div>;
}
function App(){
 const session=useQuery({queryKey:['session'],queryFn:()=>api<{user:User|null}>('session/')});
 if(session.isPending)return <Loading/>;
 if(session.isError)return <ErrorNotice error={session.error}/>;
 return session.data.user?<Shell key={session.data.user.id} user={session.data.user}/>:<Login/>;
}
createRoot(document.getElementById('root')!).render(<QueryClientProvider client={queryClient}><BrowserRouter><App/></BrowserRouter></QueryClientProvider>);
