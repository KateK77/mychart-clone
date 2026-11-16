const {chromium,expect:baseExpect}=require('@playwright/test');
const expect=baseExpect.configure({timeout:20000});
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const base=process.env.CC_AI_URL||'https://careconnect-demo-rc0t.onrender.com';
const password='CareConnect-Demo-2026!';
const runKey=process.env.CC_AI_RUN||'20261115';
async function launch(){
 return chromium.launch({headless:true,executablePath:process.env.CC_BROWSER_BIN||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
}
async function newPage(browser){
 const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:1000},acceptDownloads:true});
 context.setDefaultTimeout(15000);context.setDefaultNavigationTimeout(45000);
 return await context.newPage();
}
async function login(page,username='patient',pass=password){
 await page.goto('/login');await page.getByLabel('Username',{exact:true}).fill(username);await page.getByLabel('Password',{exact:true}).fill(pass);
 await page.getByRole('button',{name:'Sign in',exact:true}).click();await expect(page.locator('main')).toBeVisible();
}
async function register(page,username,role='patient',first='AI',last='Synthetic'){
 await page.goto('/register?role='+role);
 await page.getByLabel('Username',{exact:true}).fill(username);await page.getByLabel('First name',{exact:true}).fill(first);await page.getByLabel('Last name',{exact:true}).fill(last);
 await page.getByLabel('Email',{exact:true}).fill(username+'@example.test');await page.getByLabel('Password',{exact:true}).fill(password);await page.getByLabel('Confirm new password',{exact:true}).fill(password);
 await page.getByRole('button',{name:'Create account',exact:true}).click();await expect(page.locator('main')).toBeVisible();
}
async function confirm(page,label){
 await page.getByRole('button',{name:label,exact:true}).click();await page.getByRole('dialog').last().getByRole('button',{name:'Confirm',exact:true}).click();
}
async function runSuite(group,tasks,browser){
 const root=path.resolve(__dirname,'../../experiments/ai-browser-100');
 fs.mkdirSync(root,{recursive:true});
 const attempt=group+'-'+new Date().toISOString().replace(/[:.]/g,'-');
 const dir=path.join(root,attempt);fs.mkdirSync(dir,{recursive:true});
 const plan=tasks.map(({run,page,...meta})=>meta);
 fs.writeFileSync(path.join(root,group+'-tasks.json'),JSON.stringify(plan,null,2));
 const results=[];
 const started=new Date().toISOString();
 const save=()=>fs.writeFileSync(path.join(dir,'results.json'),JSON.stringify({group,base,runKey,started,updated:new Date().toISOString(),method:'AI-authored Playwright UI browser automation; no direct API assertions',results},null,2));
 for(const t of tasks){
  const before=Date.now();const result={id:t.id,title:t.title,difficulty:t.difficulty,status:'passed',durationMs:0};
  const blockers=(t.depends||[]).filter(id=>results.find(r=>r.id===id)?.status!=='passed');
  if(blockers.length){result.status='blocked';result.error='Prerequisite did not pass: '+blockers.join(', ');}
  else{
   try{await t.run();}catch(error){result.status='failed';result.error=String(error.stack||error).slice(0,6000);}
   try{const p=typeof t.page==='function'?t.page():t.page;if(p&&!p.isClosed()){
    result.url=p.url();result.screenshot=t.id+'.png';await p.screenshot({path:path.join(dir,result.screenshot),fullPage:true,timeout:10000});
    if(result.status==='failed'){fs.writeFileSync(path.join(dir,t.id+'.txt'),await p.locator('body').innerText());result.pageText=t.id+'.txt';}
   }}catch(error){result.evidenceError=String(error.message);}
  }
  result.durationMs=Date.now()-before;results.push(result);save();console.log(t.id+' '+result.status+' '+t.title);
 }
 await browser.close();save();console.log('RESULTS '+path.join(dir,'results.json'));
}
module.exports={expect,assert,fs,path,base,password,runKey,launch,newPage,login,register,confirm,runSuite};
