import {expect,test,type Page} from '@playwright/test';

const initial='CareConnect-Demo-2026!';
async function login(page:Page,name='patient',password=initial){
 await page.goto('/login');
 await page.getByLabel('Username',{exact:true}).fill(name);
 await page.getByLabel('Password',{exact:true}).fill(password);
 await page.getByRole('button',{name:'Sign in',exact:true}).click();
 await expect(page.getByRole('main')).toBeVisible();
}
async function confirm(page:Page,label:string){
 await page.getByRole('button',{name:label,exact:true}).click();
 await page.getByRole('dialog').last().getByRole('button',{name:'Confirm',exact:true}).click();
}
async function register(page:Page){
 const username='v2_'+Date.now();
 await page.goto('/register');
 await page.getByLabel('Username',{exact:true}).fill(username);
 await page.getByLabel('First name').fill('River');
 await page.getByLabel('Last name').fill('Demo');
 await page.getByLabel('Email',{exact:true}).fill(username+'@example.com');
 await page.getByLabel('Password',{exact:true}).fill(initial);
 await page.getByLabel('Confirm new password',{exact:true}).fill(initial);
 await page.getByRole('button',{name:'Create account',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Welcome, River'})).toBeVisible();
 return username;
}

test('sign-out leaves no stale staff shell and account switching works without refresh',async({page})=>{
 await login(page,'admin');
 await page.getByRole('button',{name:'Laboratory results',exact:true}).click();
 await page.getByRole('button',{name:'Sign out',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Welcome back'})).toBeVisible();
 await expect(page.getByText('Morgan Wren',{exact:true})).toHaveCount(0);
 await page.getByLabel('Username',{exact:true}).fill('patient');
 await page.getByLabel('Password',{exact:true}).fill(initial);
 await page.getByRole('button',{name:'Sign in',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Welcome, Jordan'})).toBeVisible();
 await page.getByRole('button',{name:'Sign out',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Welcome back'})).toBeVisible();
 const session=await page.request.get('/api/session/');
 expect((await session.json()).user).toBeNull();
});

test('password confirmation blocks mistakes, clears on success, and updates login',async({page})=>{
 const username=await register(page);
 await page.getByRole('link',{name:'Account Settings',exact:true}).click();
 await page.getByLabel('Current password',{exact:true}).fill(initial);
 await page.getByLabel('New password',{exact:true}).fill('CareConnect-V2-Test-2026!');
 await page.getByLabel('Confirm new password',{exact:true}).fill('Different-Password-2026!');
 await page.getByRole('button',{name:'Change password',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('do not match');
 await page.getByLabel('Confirm new password',{exact:true}).fill('CareConnect-V2-Test-2026!');
 await page.getByRole('button',{name:'Change password',exact:true}).click();
 await expect(page.getByRole('status')).toContainText('Your password has been changed.');
 await expect(page.getByLabel('New password',{exact:true})).toHaveValue('');
 await expect(page.getByLabel('Current password',{exact:true})).toHaveValue('');
 await page.getByRole('button',{name:'Sign out',exact:true}).click();
 await page.getByLabel('Username',{exact:true}).fill(username);
 await page.getByLabel('Password',{exact:true}).fill(initial);
 await page.getByRole('button',{name:'Sign in',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('Invalid username or password');
 await page.getByLabel('Password',{exact:true}).fill('CareConnect-V2-Test-2026!');
 await page.getByRole('button',{name:'Sign in',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Welcome, River'})).toBeVisible();
});

test('forgot password delivers a local message and reset link works once',async({page,browser})=>{
 const username=await register(page);
 await page.getByRole('button',{name:'Sign out',exact:true}).click();
 await page.getByRole('link',{name:'Forgot password?'}).click();
 await page.getByLabel('Email',{exact:true}).fill(username+'@example.com');
 await page.getByRole('button',{name:'Send reset link'}).click();
 await expect(page.getByRole('heading',{name:'Check your email'})).toBeVisible();
 await page.getByRole('link',{name:'Open demo mailbox'}).click();
 await expect(page.getByRole('heading',{name:'Reset your CareConnect password'})).toBeVisible();
 const other=await browser.newContext();
 const isolated=await other.newPage();
 await isolated.goto('/demo-mailbox');
 await expect(isolated.getByText('No reset messages yet. Request a password reset first.')).toBeVisible();
 await other.close();
 const link=await page.getByRole('link',{name:'Reset password',exact:true}).getAttribute('href');
 await page.getByRole('link',{name:'Reset password',exact:true}).click();
 await page.getByLabel('New password',{exact:true}).fill('Recovered-V2-Demo-2026!');
 await page.getByLabel('Confirm new password',{exact:true}).fill('Recovered-V2-Demo-2026!');
 await page.getByRole('button',{name:'Reset password',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Password reset complete'})).toBeVisible();
 await login(page,username,'Recovered-V2-Demo-2026!');
 await page.getByRole('button',{name:'Sign out',exact:true}).click();
 await page.goto(link!);
 await page.getByLabel('New password',{exact:true}).fill(initial);
 await page.getByLabel('Confirm new password',{exact:true}).fill(initial);
 await page.getByRole('button',{name:'Reset password',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('expired or has already been used');
});

test('staff records open immediately in a drawer, remember context and close with Escape',async({page})=>{
 await login(page,'admin');
 await page.getByLabel('Patient context').selectOption({label:'Jordan Vale (patient)'});
 await page.getByRole('button',{name:'Laboratory results',exact:true}).click();
 const record=page.getByRole('button',{name:/Hemoglobin A1c/}).first();
 await record.click();
 await expect(page.getByRole('dialog',{name:'Hemoglobin A1c'})).toBeVisible();
 await expect(page.getByRole('dialog').getByText('Jordan Vale',{exact:true})).toBeVisible();
 const bounds=await page.getByRole('dialog').boundingBox();
 expect(bounds?.y).toBe(0);
 await page.reload();
 await expect(page.getByRole('dialog',{name:'Hemoglobin A1c'})).toBeVisible();
 await page.keyboard.press('Escape');
 await expect(page.getByRole('dialog')).toHaveCount(0);
 await expect(page.getByLabel('Patient context')).toHaveValue('1');
 await expect(page.getByRole('heading',{name:'Laboratory results',exact:true})).toBeVisible();
 await page.setViewportSize({width:390,height:844});
 await record.click();
 await expect(page.getByRole('dialog')).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.getByRole('button',{name:'Close record'}).click();
});

test('staff rescheduling opens the new appointment and patient sees the replacement',async({page,browser})=>{
 await login(page,'frontdesk');
 await page.getByRole('button',{name:'Appointments',exact:true}).click();
 await page.getByRole('button',{name:/Annual Physical.*Confirmed/}).click();
 const option=page.getByLabel('New slot').locator('option').nth(1);
 const slot=await option.getAttribute('value');
 const selectedText=await option.innerText();
 await page.getByLabel('New slot').selectOption(slot!);
 await confirm(page,'Reschedule appointment');
 await expect(page.getByRole('dialog').getByText('Scheduled',{exact:true})).toBeVisible();
 const recordId=new URL(page.url()).searchParams.get('record');
 expect(recordId).toBeTruthy();
 const context=await browser.newContext();const patient=await context.newPage();
 await login(patient);
 await patient.goto('/appointments/'+recordId);
 await expect(patient.getByText('Scheduled',{exact:true})).toBeVisible();
 await expect(patient.getByRole('heading',{name:'Appointment details'})).toBeVisible();
 const detail=await patient.request.get('/api/appointments/'+recordId+'/');
 expect(String((await detail.json()).slot)).toBe(slot);
 await context.close();
});

test('unpublished record errors are readable and provide a way back',async({page})=>{
 await login(page);
 await page.goto('/results/999999');
 await expect(page.getByRole('alert')).toContainText('no longer available');
 await expect(page.getByText('No LabResult matches the given query.')).toHaveCount(0);
 await page.getByRole('link',{name:'Back to list'}).click();
 await expect(page.getByRole('heading',{name:'Test Results',exact:true})).toBeVisible();
});
