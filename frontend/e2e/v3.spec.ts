import {expect,test,type Page} from '@playwright/test';
const password='CareConnect-Demo-2026!';
async function login(page:Page,user='patient'){
 await page.goto('/login');await page.getByLabel('Username',{exact:true}).fill(user);await page.getByLabel('Password',{exact:true}).fill(password);await page.getByRole('button',{name:'Sign in',exact:true}).click();await expect(page.getByRole('main')).toBeVisible();
}
async function confirm(page:Page,label:string){await page.getByRole('button',{name:label,exact:true}).click();await page.getByRole('dialog').last().getByRole('button',{name:'Confirm',exact:true}).click();}

test('restore confirms and redirects to Inbox with the conversation and clear feedback',async({page})=>{
 await login(page);await page.goto('/messages');await page.getByRole('link',{name:/Your upcoming physical/}).click();
 await expect(page.getByRole('button',{name:'Restore to inbox',exact:true})).toHaveCount(0);
 await confirm(page,'Archive');await expect(page).toHaveURL(/box=archive/);await expect(page.getByRole('button',{name:'archive',exact:true})).toHaveAttribute('aria-pressed','true');
 await page.getByRole('link',{name:/Your upcoming physical/}).click();await expect(page.getByRole('button',{name:'Archive',exact:true})).toHaveCount(0);
 await page.getByRole('button',{name:'Restore to inbox',exact:true}).click();await page.getByRole('button',{name:'Keep unchanged',exact:true}).click();await expect(page.getByRole('heading',{name:'Your upcoming physical'})).toBeVisible();
 await confirm(page,'Restore to inbox');await expect(page).toHaveURL(/box=inbox/);await expect(page.getByRole('button',{name:'inbox',exact:true})).toHaveAttribute('aria-pressed','true');
 await expect(page.getByRole('status')).toContainText('Conversation restored to inbox.');await expect(page.getByRole('link',{name:/Your upcoming physical/})).toBeVisible();
});

test('registration chooses a role and staff approval unlocks the matching workspace',async({page,browser})=>{
 const username='v3doctor'+Date.now();await page.goto('/register');await page.getByRole('link',{name:/Care team Apply/}).click();
 await page.getByLabel('Care-team role').selectOption('Physician');await page.getByLabel('Organization').fill('Synthetic Clinic');
 await page.getByLabel('Username',{exact:true}).fill(username);await page.getByLabel('First name').fill('River');await page.getByLabel('Last name').fill('Stone');await page.getByLabel('Email',{exact:true}).fill(username+'@example.test');await page.getByLabel('Password',{exact:true}).fill(password);await page.getByLabel('Confirm new password',{exact:true}).fill(password);await page.getByRole('button',{name:'Create account'}).click();
 await expect(page.getByRole('heading',{name:'Your care-team application'})).toBeVisible();await expect(page.getByText('Pending',{exact:true})).toBeVisible();
 const context=await browser.newContext();const admin=await context.newPage();await login(admin,'admin');await admin.getByRole('link',{name:'Access reviews',exact:true}).click();
 const card=admin.locator('.family-card').filter({hasText:username+'@example.test'});await card.getByLabel('Decision',{exact:true}).selectOption('approve');await card.getByLabel('Verification / decision note').fill('Demo clinician role verified.');await card.getByRole('button',{name:'Save access decision'}).click();await admin.getByRole('dialog').getByRole('button',{name:'Confirm',exact:true}).click();await expect(card.getByText('Approved',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Check application status'}).click();await expect(page.getByRole('heading',{name:'Staff workspace'})).toBeVisible();await expect(page.getByRole('button',{name:'Laboratory results',exact:true})).toBeVisible();await context.close();
});

test('family invitation requires consent, then permits shared results and supports revocation',async({page,browser})=>{
 await login(page);await page.goto('/family');await page.getByRole('button',{name:'Link a family member'}).click();
 await page.getByLabel("Family member's account email").fill('caregiver@careconnect.example');await page.getByLabel('Relationship',{exact:true}).fill('Family caregiver');
 await page.getByRole('button',{name:'Send invitation',exact:true}).click();await expect(page.getByRole('status')).toContainText('Request sent');
 const context=await browser.newContext();const caregiver=await context.newPage();await login(caregiver,'caregiver');await expect(caregiver).toHaveURL(/family/);
 const pending=caregiver.locator('.family-card').filter({hasText:'From Jordan Vale'}).filter({hasText:'Pending'});await expect(pending).toBeVisible();await pending.getByRole('button',{name:'Accept request',exact:true}).click();await caregiver.getByRole('dialog').getByRole('button',{name:'Confirm',exact:true}).click();
 await expect(caregiver.getByRole('heading',{name:'Jordan Vale',exact:true})).toBeVisible();await caregiver.getByRole('main').getByRole('link',{name:'Test Results',exact:true}).click();await expect(caregiver.getByText('Viewing Jordan Vale')).toBeVisible();await expect(caregiver.getByRole('link',{name:/Hemoglobin A1c/}).first()).toBeVisible();
 await page.reload();await confirm(page,'Revoke access');await caregiver.reload();await expect(caregiver.getByRole('alert')).toContainText('no longer available');await context.close();
});

test('report and document previews download genuine PDFs and provide printing',async({page})=>{
 await login(page);await page.goto('/results');await page.getByRole('link',{name:/Hemoglobin A1c/}).first().click();await page.getByRole('link',{name:'View report',exact:true}).click();
 await expect(page.locator('.document-paper')).toContainText('Jordan Vale');await expect(page.getByRole('button',{name:'Print',exact:true})).toBeVisible();
 const download=page.waitForEvent('download');await page.getByRole('link',{name:'Download PDF',exact:true}).click();expect((await download).suggestedFilename()).toMatch(/\.pdf$/);
 const href=await page.getByRole('link',{name:'Download PDF',exact:true}).getAttribute('href');const response=await page.request.get(href!);expect(response.headers()['content-type']).toBe('application/pdf');expect((await response.body()).subarray(0,5).toString()).toBe('%PDF-');
 await page.goto('/documents');await page.getByRole('link',{name:/Primary care visit summary/}).click();await expect(page.locator('.document-paper')).toContainText('Return for your scheduled annual physical.');
 await page.setViewportSize({width:390,height:844});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();
 await page.goto('/preview/lab/999999');await expect(page.getByRole('alert')).toBeVisible();await page.getByRole('link',{name:'Back to list',exact:true}).click();await expect(page.getByRole('heading',{name:'Test Results',exact:true})).toBeVisible();
});
