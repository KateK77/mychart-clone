// Isolated evidence for a browser-history test setup correction. No application changes.
const {expect,launch,newPage,login,runSuite}=require('./harness.cjs');
(async()=>{
 const browser=await launch(),p=await newPage(browser);
 await runSuite('auth-navigation-followup',[{
  id:'A024',title:'Sign-out removes identity and protects browser-back access',difficulty:'hard',
  steps:['Sign in, then open Account Settings to create protected-page browser history.','Sign out, use browser Back and reload.'],
  expected:'Sign-in remains required and Atlas identity is absent.',page:p,
  run:async()=>{
   await login(p,'ai-a-20261115-r2','CareConnect-Atlas-Test-2026!');
   await p.getByRole('link',{name:'Account Settings',exact:true}).click();await expect(p.getByRole('heading',{name:'Account Settings',exact:true})).toBeVisible();
   await p.getByRole('button',{name:'Sign out',exact:true}).click();await expect(p.getByRole('heading',{name:'Welcome back'})).toBeVisible();
   await p.goBack();await p.reload();await expect(p.getByRole('heading',{name:'Welcome back'})).toBeVisible();await expect(p.getByText('Atlas Test',{exact:true})).toHaveCount(0);
  }
 }],browser);
})().catch(e=>{console.error(e.stack);process.exit(1)});
