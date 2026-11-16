const {expect,fs,path,launch,newPage,register,confirm,runSuite}=require('./harness.cjs');
(async()=>{
 const browser=await launch(),page=await newPage(browser),stamp=Date.now(),username='ai-b-focus-'+stamp,subject='AI focused archive '+stamp;
 // UI-only fixture. These actions are not counted as additional test cases.
 await register(page,username,'patient','Blair','Focused Test');
 await page.goto('/messages/new');await page.getByLabel('Recipient').selectOption('Care team');await page.getByLabel('Category').selectOption('General Request');await page.getByLabel('Subject').fill(subject);await page.getByLabel('Message',{exact:true}).fill('Synthetic fixture for archive/restore selector correction.');await page.getByRole('button',{name:'Send message',exact:true}).click();await expect(page.getByRole('heading',{name:subject,exact:true})).toBeVisible();
 const plan=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../../experiments/ai-browser-100/clinical-tasks.json'),'utf8'));
 const tasks=[
  {...plan.find(t=>t.id==='B054'),depends:[],page,run:async()=>{
   await confirm(page,'Archive');await expect(page).toHaveURL(/box=archive/);await expect(page.getByRole('button',{name:'archive',exact:true})).toHaveAttribute('aria-pressed','true');await expect(page.getByRole('status').filter({hasText:'Conversation archived.'})).toBeVisible();await expect(page.getByRole('link',{name:new RegExp(subject)})).toBeVisible();
  }},
  {...plan.find(t=>t.id==='B055'),depends:['B054'],page,run:async()=>{
   await page.getByRole('link',{name:new RegExp(subject)}).click();await expect(page.getByRole('button',{name:'Archive',exact:true})).toHaveCount(0);await confirm(page,'Restore to inbox');await expect(page).toHaveURL(/box=inbox/);await expect(page.getByRole('button',{name:'inbox',exact:true})).toHaveAttribute('aria-pressed','true');await expect(page.getByRole('status').filter({hasText:'Conversation restored to inbox.'})).toBeVisible();await page.reload();await expect(page.getByRole('link',{name:new RegExp(subject)})).toBeVisible();
  }}
 ];await runSuite('clinical-focused',tasks,browser);
})().catch(error=>{console.error(error);process.exit(1)});
