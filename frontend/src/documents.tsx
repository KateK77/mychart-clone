import {useLocation,useParams} from 'react-router-dom';
import {Download,Printer,FileText} from 'lucide-react';
import {withParams} from './api';
import {Data,Heading} from './ui';

export function DocumentPreview({kind:givenKind,id:givenId}:{kind?:string;id?:string}){
 const params=useParams(),location=useLocation();
 const kind=givenKind||params.kind,id=givenId||params.id,patient=new URLSearchParams(location.search).get('patient');
 const path=withParams(`exports/${kind}/${id}/`,{patient});
 return <Data path={path}>{data=><><div className="print-controls"><Heading title="Document preview" description="Read, print, or keep a PDF copy." back={[withParams(kind==='lab'?'/results':kind==='document'?'/documents':'/billing',{patient}),'Back to records']}><div className="inline-actions"><a className="button" href={'/api/'+withParams(`exports/${kind}/${id}/download/`,{patient})}><Download size={17}/>Download PDF</a><button className="button secondary" onClick={()=>window.print()}><Printer size={17}/>Print</button></div></Heading></div><article className="document-paper"><header className="document-brand"><strong>CareConnect</strong><span><FileText size={17}/>{data.identifier}</span></header><p className="eyebrow">{data.subtitle}</p><h1>{data.title}</h1><p className="muted">{data.date}</p><dl className="document-facts">{[['Patient',data.patient],['Date of birth',data.birth_date],...data.facts].map(([label,value]:string[],i:number)=><div key={i}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>{data.sections.map((section:any,i:number)=><section key={i}><h2>{section.title}</h2><p className="pre-wrap">{section.body}</p></section>)}<footer>{data.disclaimer}<small>Independent demonstration. Not affiliated with Epic Systems or MyChart.</small></footer></article></>}</Data>;
}
