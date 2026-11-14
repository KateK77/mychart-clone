import {useEffect,useRef,useState,type FormEvent,type ReactNode} from 'react';
import {Link,useLocation} from 'react-router-dom';
import {useMutation,useQuery,useQueryClient} from '@tanstack/react-query';
import {ArrowUpRight,ChevronRight, CircleAlert, FolderOpen, X, Check} from 'lucide-react';
import {api,date,type RecordData} from './api';

export function Loading(){return <div className="panel loading" role="status">Loading…</div>}
export function ErrorNotice({error}:{error:unknown}){return <div className="notice error" role="alert"><CircleAlert size={17}/>{error instanceof Error ? error.message : 'The request could not be completed.'}</div>}
export function Empty({text='There are no records to show.'}:{text?:string}){return <div className="empty"><FolderOpen size={24}/><p>{text}</p></div>}
export function Data({path,children}:{path:string;children:(value:any)=>ReactNode}){
  const query = useQuery({queryKey:['api',path],queryFn:()=>api(path),refetchOnMount:'always'});
  if(query.isPending) return <Loading/>;
  if(query.isError) return <DataError error={query.error}/>;
  return <>{children(query.data)}</>;
}
function DataError({error}:{error:unknown}){
 const location=useLocation();
 const base='/'+location.pathname.split('/')[1];
 return <div className="panel error-state"><ErrorNotice error={error}/><Link className="button secondary" to={base+location.search}>Back to list</Link><Link className="text-button" to="/">Return to overview</Link></div>;
}
export function Modal({title,children,onClose,drawer=false}:{title:string;children:ReactNode;onClose:()=>void;drawer?:boolean}){
 const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{const dialog=ref.current!;const trigger=document.activeElement as HTMLElement;const overflow=document.body.style.overflow;dialog.showModal();document.body.style.overflow='hidden';return()=>{dialog.close();document.body.style.overflow=overflow;trigger?.focus();};},[]);
 return <dialog ref={ref} className={drawer?'record-drawer':'confirm-dialog'} onCancel={event=>{event.preventDefault();onClose();}} aria-label={title}>
  <header className="drawer-header"><div><span className="eyebrow">{drawer?'RECORD WORKSPACE':'PLEASE CONFIRM'}</span><h2>{title}</h2></div><button type="button" className="icon-button" onClick={onClose} aria-label={drawer?'Close record':'Close confirmation'}><X size={20}/></button></header><div className="drawer-body">{children}</div>
 </dialog>;
}
export function Heading({title,description,children,back}:{title:string;description?:string;children?:ReactNode;back?:[string,string]}){
  return <header className="page-heading">{back && <Link className="back" to={back[0]}>{back[1]} <ChevronRight size={14}/></Link>}<div className="heading-line"><div><h1>{title}</h1>{description && <p>{description}</p>}</div>{children}</div></header>;
}
export function Panel({title,action,children,className=''}:{title?:string;action?:[string,string];children:ReactNode;className?:string}){
  return <section className={'panel '+className}>{(title||action)&&<div className="panel-head">{title&&<h2>{title}</h2>}{action&&<Link to={action[0]}>{action[1]} <ArrowUpRight size={15}/></Link>}</div>}{children}</section>
}
export function Row({title,detail,status,to,icon}:{title:string;detail?:string;status?:string;to?:string;icon?:ReactNode}){
  const content = <>{icon&&<span className="row-icon">{icon}</span>}<span className="row-copy"><strong>{title}</strong>{detail&&<small>{detail}</small>}</span>{status&&<Tag value={status}/ >}{to&&<ChevronRight className="row-arrow" size={16}/>}</>;
  return to ? <Link className="row" to={to}>{content}</Link> : <div className="row">{content}</div>;
}
export function Tag({value}:{value:string}){
  const color = ['High','Low','Overdue','Denied','Cancelled','Voided','No Show'].includes(value)?'warm':
    ['Paid','In range','Completed','Approved','Published','Active','Confirmed'].includes(value)?'good':'';
  return <span className={'tag '+color}>{value}</span>;
}
export function Facts({values}:{values:[string,ReactNode][]}){
  return <dl className="facts">{values.map(([key,value])=><div key={key}><dt>{key}</dt><dd>{value === '' || value == null ? '—' : value}</dd></div>)}</dl>;
}
export type Field = {name:string; label:string; kind?:string; options?:ReadonlyArray<string|{value:string|number;label:string}>; optional?:boolean; value?:string|number|boolean; min?:number; step?:string};
export function Controls({fields}:{fields:Field[]}){
  return <>{fields.map(field=><label key={field.name}>{field.label}
    {field.kind==='textarea' ? <textarea name={field.name} required={!field.optional} defaultValue={String(field.value??'')} rows={4}/> :
    field.options ? <select name={field.name} required={!field.optional} defaultValue={String(field.value??'')}><option value="">{field.optional?'Any':'Select an option'}</option>{field.options.map(item=>{
      const option=typeof item==='string'?{value:item,label:item}:item;
      return <option key={option.value} value={option.value}>{option.label}</option>;
    })}</select> : field.kind==='checkbox' ? <input type="checkbox" name={field.name} defaultChecked={Boolean(field.value)}/> :
    <input name={field.name} type={field.kind??'text'} required={!field.optional} defaultValue={String(field.value??'')} min={field.min} step={field.step}/>}</label>)}</>;
}
export function readForm(event:FormEvent<HTMLFormElement>,fields:Field[]){
  const form = new FormData(event.currentTarget);
  return Object.fromEntries(fields.flatMap<[string, FormDataEntryValue | boolean | null]>(field=>{
    const value=form.get(field.name);
    if(field.kind==='checkbox') return [[field.name, form.has(field.name)]];
    if(value===''&&field.optional&&field.value===undefined) return [];
    return [[field.name,value]];
  }));
}
export function Action({path,label,fields=[],fixed={},confirm,method='POST',onSuccess,success='Changes saved.'}:{
  path:string;label:string;fields?:Field[];fixed?:object;confirm?:string;method?:string;
  onSuccess?:(response:any)=>void;success?:string;
}){
  const client=useQueryClient();
  const formRef=useRef<HTMLFormElement>(null);
  const [pendingValues,setPendingValues]=useState<object|null>(null);
  const mutation=useMutation({mutationFn:(values:object)=>api(path,{...values,...fixed},method),
    onSuccess:async response=>{
      if(fields.some(field=>field.kind==='textarea')&&!fields.some(field=>field.value!==undefined))formRef.current?.reset();
      await client.invalidateQueries({queryKey:['api']});
      onSuccess?.(response);}});
  return <form ref={formRef} className="action-form" onSubmit={event=>{
    event.preventDefault();
    const values=readForm(event,fields);
    if(confirm){setPendingValues(values);return;}
    mutation.mutate(values);
  }}><fieldset className="action-fields" disabled={mutation.isPending}><Controls fields={fields}/></fieldset><button className="button" disabled={mutation.isPending}>{mutation.isPending?'Saving…':label}</button>
    {mutation.isError&&<ErrorNotice error={mutation.error}/>}
    {mutation.isSuccess&&<p className="notice success" role="status"><Check size={16}/>{success}</p>}
    {pendingValues&&<Modal title={label} onClose={()=>setPendingValues(null)}><p>{confirm}</p><div className="dialog-actions"><button type="button" className="button secondary" onClick={()=>setPendingValues(null)}>Keep unchanged</button><button type="button" className="button" onClick={()=>{mutation.mutate(pendingValues);setPendingValues(null);}}>Confirm</button></div></Modal>}
  </form>;
}
export function Filters({fields,onChange,label='Apply filters'}:{fields:Field[];onChange:(values:any)=>void;label?:string}){
  return <form className="filters" onSubmit={event=>{event.preventDefault();onChange(readForm(event,fields));}}>
    <Controls fields={fields}/><button className="button secondary">{label}</button>
  </form>;
}
export function Trend({rows}:{rows:RecordData[]}){
  const [index,setIndex]=useState<number|null>(null);
  if(rows.length===0)return <Empty text="No numeric measurements." />;
  const values=rows.map(row=>Number(row.value));
  const min=Math.min(...values);
  const range=Math.max(...values)-min;
  const width=520;
  const x=(i:number)=>rows.length===1?width/2:28+i*(width-56)/(rows.length-1);
  const y=(i:number)=>range===0?66:114-90*(values[i]-min)/range;
  return <><svg viewBox="0 0 520 132" className="trend" role="img" aria-label="Historical measurement trend">
    <path d="M12 24H508 M12 66H508 M12 114H508" stroke="#e0eae9" fill="none"/>
    <polyline points={rows.map((_,i)=>x(i)+','+y(i)).join(' ')} fill="none" stroke="#168374" strokeWidth="3"/>
    {rows.map((row,i)=><circle key={row.id} cx={x(i)} cy={y(i)} r={i===index?7:5} fill="#168374" tabIndex={0} aria-label={date(row.collected_at)+' '+row.value+' '+row.unit} onMouseEnter={()=>setIndex(i)} onFocus={()=>setIndex(i)}/>)}
  </svg><p className="muted">{index===null ? date(rows[0].collected_at)+' – '+date(rows.at(-1)?.collected_at) : date(rows[index].collected_at)+' · '+rows[index].value+' '+rows[index].unit}</p>
  {rows.map(row=><Row key={row.id} title={row.value+' '+row.unit} detail={date(row.collected_at)} status={row.flag}/>)}</>;
}
