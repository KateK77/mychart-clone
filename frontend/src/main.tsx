import {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {BrowserRouter,Link,NavLink,Navigate,Route,Routes,useLocation,useNavigate} from 'react-router-dom';
import {QueryClient,QueryClientProvider,useQuery,useQueryClient} from '@tanstack/react-query';
import {Bell,CalendarDays,ClipboardList,FileText,FlaskConical,HeartPulse,House,LogOut,Menu,MessageCircle,Pill,Settings,Users,Wallet,X,ChevronRight,ShieldCheck} from 'lucide-react';
import {api,type User} from './api';
import {ErrorNotice,Heading,Loading} from './ui';
import {Dashboard,PatientPageRoute} from './patient';
import {Staff} from './staff';
import {Authentication,Brand,banner} from './authentication';
import {FamilyAccess,AccessReviews,PendingAccount} from './access';
import {DocumentPreview} from './documents';
import './style.css';

const queryClient=new QueryClient({defaultOptions:{queries:{retry:false,staleTime:1000}}});
const groups=[
 {title:'OVERVIEW',items:[['','Dashboard',House],['appointments','Appointments',CalendarDays],['messages','Messages',MessageCircle]]},
 {title:'MY HEALTH',items:[['results','Test Results',FlaskConical],['medications','Medications',Pill],['health','Health Summary',HeartPulse],['visits','Visits',ClipboardList],['documents','Documents',FileText]]},
 {title:'MY ACCOUNT',items:[['billing','Billing',Wallet],['family','Family Access',Users],['settings','Account Settings',Settings]]},
] as const;
const items=groups.reduce<Array<readonly [string,string,typeof House]>>((all,group)=>[...all,...group.items],[]);
const labels:Record<string,string>={...Object.fromEntries(items.map(([route,label])=>[route,label])),preview:'Document preview','access-reviews':'Access reviews'};

function Shell({user}:{user:User}){
 const [menu,setMenu]=useState(false),[busy,setBusy]=useState(false),[logoutError,setLogoutError]=useState<unknown>();
 const client=useQueryClient(),location=useLocation(),navigate=useNavigate();
 const proxy=new URLSearchParams(location.search).get('patient'),staff=!user.patient;
 const section=location.pathname.split('/')[1]||'';
 const navigation=staff?[{title:'WORKSPACE',items:[['','Staff workspace',House],['messages','Messages',MessageCircle],...(user.roles.includes('Administrator')?[["access-reviews","Access reviews",ShieldCheck] as const]:[]),['settings','Account Settings',Settings]] as const}]:groups;
 const notices=useQuery({queryKey:['api','notifications/'],queryFn:()=>api('notifications/'),enabled:!staff,refetchInterval:30000});
 const family=useQuery({queryKey:['api','family/'],queryFn:()=>api('family/'),enabled:!staff&&!!proxy});
 const familyName=family.data?.find((row:any)=>String(row.patient)===proxy)?.name;
 useEffect(()=>{setMenu(false);window.scrollTo(0,0);},[location.pathname]);
 useEffect(()=>{if(!menu)return;const close=(event:KeyboardEvent)=>{if(event.key==='Escape')setMenu(false);};document.addEventListener('keydown',close);return()=>document.removeEventListener('keydown',close);},[menu]);
 async function leave(){
  setBusy(true);setLogoutError(undefined);
  try{await api('logout/',{});await client.cancelQueries();client.setQueryData(['session'],(previous:any)=>({...previous,user:null}));client.removeQueries({queryKey:['api']});navigate('/login',{replace:true});}
  catch(error){setLogoutError(error);setBusy(false);}
 }
 return <div className="app">
  {menu&&<button className="sidebar-backdrop" onClick={()=>setMenu(false)} aria-label="Close navigation"/>}
  <aside className={'sidebar '+(menu?'open':'')}><Brand/><div className="sidebar-context"><span className="context-dot"/>{staff?'Care team workspace':'Patient portal'}<span className="version-pill">3.0</span></div>
   <nav aria-label="Main navigation">{navigation.map(group=><div className="nav-group" key={group.title}><span className="nav-label">{group.title}</span>{group.items.map(([route,label,Icon])=><NavLink onClick={()=>setMenu(false)} key={route} end={!route} to={'/'+route+(proxy&&['appointments','results','medications','health','visits','billing','documents'].includes(route)?'?patient='+proxy:'')}><Icon size={19}/><span>{label}</span>{route==='messages'&&!staff&&notices.data?.some((row:any)=>!row.read&&row.kind==='Message')&&<span className="nav-dot"/>}</NavLink>)}</div>)}</nav>
   <div className="side-footer"><div className="identity"><div className="avatar">{user.name.split(' ').slice(0,2).map(word=>word[0]).join('')}</div><div><strong>{user.name}</strong><small>{staff?user.roles.join(' · '):'Personal account'}</small></div></div><button className="signout" aria-label="Sign out" onClick={()=>void leave()} disabled={busy}><LogOut size={17}/>{busy?'Signing out…':'Sign out'}</button></div>
  </aside>
  <div className="workspace"><header className="topbar"><button className="menu-toggle icon-button" aria-label={menu?'Close menu':'Open menu'} onClick={()=>setMenu(!menu)}>{menu?<X/>:<Menu/>}</button><div className="top-crumb"><span>{staff?'Care team':'My portal'}</span><ChevronRight size={13}/><strong>{section==='notifications'?'Notifications':staff&&!section?'Workspace':labels[section]??'Workspace'}</strong></div><div className="top-tools"><span className="secure-label"><ShieldCheck size={15}/>Secure session</span>{!staff&&<Link to="/notifications" className="icon-button bell" aria-label="Notifications"><Bell size={20}/>{notices.data?.some((notice:{read:boolean})=>!notice.read)&&<i/>}</Link>}<div className="avatar small-avatar" aria-hidden="true">{user.name.split(' ').map(n=>n[0]).slice(0,2).join('')}</div></div></header>
   <div className="demo-banner">{banner}</div><main id="main-content">
    {logoutError!=null&&<ErrorNotice error={logoutError}/>}
    {proxy&&<div className="notice proxy"><div><Users size={20}/><span><strong>{familyName?'Viewing '+familyName:'Family profile'}</strong><small>{familyName?'Only records shared with your account are available.':'Choose an available profile to continue.'}</small></span></div><Link to="/family">Switch profile <ChevronRight size={15}/></Link></div>}
    <Routes><Route path="/preview/:kind/:id" element={<DocumentPreview/>}/><Route path="/family" element={staff?<Navigate to="/"/>:<FamilyAccess/>}/><Route path="/access-reviews" element={user.roles.includes('Administrator')?<AccessReviews/>:<Navigate to="/"/>}/><Route path="/" element={staff?<Staff/>:<Dashboard/>}/><Route path="/staff" element={staff?<Staff/>:<Navigate to="/" replace/>}/><Route path="/login" element={<Navigate to={user.account_kind==='Caregiver'?'/family':'/'} replace/>}/><Route path="/:section/:id?" element={<PatientPageRoute staff={staff}/>}/><Route path="*" element={<Heading title="Page unavailable"><Link to="/">Return home</Link></Heading>}/></Routes>
    <footer className="app-footer"><span>CareConnect 3.0</span><span>Independent demonstration · Synthetic records only</span></footer>
   </main></div>
 </div>;
}
function App(){
 const location=useLocation(),client=useQueryClient();
 const session=useQuery({queryKey:['session'],queryFn:()=>api<{user:User|null;demo_mailbox:boolean}>('session/')});
 useEffect(()=>{const expire=()=>{void client.cancelQueries({queryKey:['api']});client.setQueryData(['session'],{user:null,demo_mailbox:session.data?.demo_mailbox});client.removeQueries({queryKey:['api']});};window.addEventListener('careconnect:session-expired',expire);return()=>window.removeEventListener('careconnect:session-expired',expire);},[client,session.data?.demo_mailbox]);
 if(session.isPending)return <Loading/>;
 if(session.isError)return <div className="connection-error"><ErrorNotice error={session.error}/><button className="button" onClick={()=>void session.refetch()}>Try again</button></div>;
 if(['/forgot-password','/reset-password','/demo-mailbox'].includes(location.pathname)||!session.data.user)return <Authentication key={location.pathname} demo={session.data.demo_mailbox}/>;
 if(session.data.user.application&&session.data.user.application.status!=='Approved')return <PendingAccount user={session.data.user}/>;
 return <Shell key={session.data.user.id} user={session.data.user}/>;
}
createRoot(document.getElementById('root')!).render(<QueryClientProvider client={queryClient}><BrowserRouter><App/></BrowserRouter></QueryClientProvider>);
