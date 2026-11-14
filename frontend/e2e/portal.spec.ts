import {expect,test,type Page} from '@playwright/test';

async function login(page:Page,username:string) {
 await page.goto('/');
 await page.getByLabel('Username').fill(username);
 await page.getByLabel('Password',{exact:true}).fill('CareConnect-Demo-2026!');
 await page.getByRole('button',{name:'Sign in'}).click();
 await expect(page.getByRole('main')).toBeVisible();
}

test('patient books, requests a different slot, and cancels an appointment',async({page})=>{
 page.on('dialog',dialog=>dialog.accept());
 await login(page,'patient');
 await expect(page.getByRole('heading',{name:'Welcome, Jordan'})).toBeVisible();
 await page.getByRole('link',{name:'Schedule appointment'}).click();
 await page.getByRole('button',{name:'Book',exact:true}).first().click();
 await expect(page.getByRole('heading',{name:'Appointment details'})).toBeVisible();
 await page.getByLabel('Preferred dates or times').fill('Friday afternoon');
 await page.getByRole('button',{name:'Request rescheduling'}).click();
 await expect(page.getByText('Friday afternoon',{exact:true})).toBeVisible();
 await page.getByLabel('Cancellation reason').fill('A scheduling conflict');
 await page.getByRole('button',{name:'Cancel appointment'}).click();
 await expect(page.getByText('A scheduling conflict',{exact:true})).toBeVisible();
});

test('care team replies and the patient receives an in-app notification',async({page,browser})=>{
 await login(page,'patient');
 await page.getByRole('link',{name:'Send message'}).click();
 await page.getByLabel('Recipient').selectOption('Care team');
 await page.getByLabel('Category').selectOption('Medical Question');
 const subject='Browser demo question '+Date.now();
 await page.getByLabel('Subject').fill(subject);
 await page.getByLabel('Message',{exact:true}).fill('Synthetic portal question.');
 await page.getByRole('button',{name:'Send message'}).click();
 await expect(page.getByRole('heading',{name:subject})).toBeVisible();
 const context=await browser.newContext();
 const staff=await context.newPage();
 await login(staff,'nurse');
 await staff.getByRole('link',{name:'Messages',exact:true}).click();
 await staff.getByRole('link',{name:new RegExp(subject)}).click();
 await staff.getByLabel('Reply').fill('Synthetic response from the care team.');
 await staff.getByRole('button',{name:'Send reply'}).click();
 await expect(staff.getByText('Synthetic response from the care team.')).toBeVisible();
 await context.close();
 await page.getByRole('link',{name:'Notifications',exact:true}).click();
 await page.getByRole('link',{name:/New reply from your care team/}).first().click();
 await expect(page.getByText('Synthetic response from the care team.')).toBeVisible();
});

test('family switching and mobile portal navigation',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 await login(page,'patient');
 await page.getByRole('button',{name:'Open menu'}).click();
 await page.getByRole('link',{name:'Family Access',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Avery Vale'})).toBeVisible();
 await page.getByRole('link',{name:'Test Results',exact:true}).click();
 await expect(page.getByText('Viewing a linked family profile')).toBeVisible();
 await expect(page.getByRole('link',{name:/Hemoglobin/})).toBeVisible();
});



test('physician publishes a result and the patient opens it',async({page,browser})=>{
 page.on('dialog',dialog=>dialog.accept());
 await login(page,'physician');
 await page.getByRole('button',{name:'Laboratory results',exact:true}).click();
 await page.getByRole('button',{name:'Create record'}).click();
 const name='Synthetic glucose '+Date.now();
 await page.getByLabel('Patient',{exact:true}).selectOption({label:'Jordan Vale'});
 await page.getByLabel('Provider',{exact:true}).selectOption({label:'Dr. Maya Rowan'});
 await page.getByLabel('Test name').fill(name);
 await page.getByLabel('Collection date').fill('2026-01-10');
 await page.getByLabel('Value',{exact:true}).fill('90');
 await page.getByLabel('Units').fill('mg/dL');
 await page.getByLabel('Result status').selectOption('Final');
 await page.getByRole('button',{name:'Save record'}).click();
 await expect(page.getByRole('button',{name:'Publish to patient'})).toBeVisible();
 await page.getByRole('button',{name:'Publish to patient'}).click();
 await expect(page.getByRole('button',{name:'Unpublish',exact:true})).toBeVisible();
 const context=await browser.newContext();
 const patient=await context.newPage();
 await login(patient,'patient');
 await patient.getByRole('link',{name:'Notifications',exact:true}).click();
 await patient.getByRole('link',{name:new RegExp(name)}).click();
 await expect(patient.getByRole('heading',{name,exact:true})).toBeVisible();
 await expect(patient.getByRole('heading',{name:'Historical measurements'})).toBeVisible();
 await context.close();
});

test('patient submits a refill and a physician approves it',async({page,browser})=>{
 page.on('dialog',dialog=>dialog.accept());
 await login(page,'patient');
 await page.getByRole('link',{name:'Medications',exact:true}).click();
 await page.getByRole('link',{name:/Cetirizine/}).click();
 await page.getByRole('button',{name:'Request refill'}).click();
 await expect(page.getByText('Requested',{exact:true})).toBeVisible();
 const context=await browser.newContext();
 const staff=await context.newPage();
 await login(staff,'physician');
 await staff.getByRole('button',{name:'Refill requests',exact:true}).click();
 await staff.getByRole('button',{name:/Cetirizine.*Requested/}).first().click();
 await staff.getByLabel('New status').selectOption('Approved');
 await staff.getByRole('button',{name:'Save refill decision'}).click();
 await expect(staff.getByRole('button',{name:/Cetirizine.*Approved/})).toBeVisible();
 await staff.getByLabel('New status').selectOption('Completed');
 await staff.getByRole('button',{name:'Save refill decision'}).click();
 await expect(staff.getByRole('button',{name:/Cetirizine.*Completed/})).toBeVisible();
 await page.reload();
 await expect(page.getByText('Completed',{exact:true}).first()).toBeVisible();
 await context.close();
});

test('billing staff issues a statement and the patient pays and downloads a receipt',async({page,browser})=>{
 await login(page,'billing');
 await page.getByRole('button',{name:'Invoices and payments'}).click();
 await page.getByRole('button',{name:'Create record'}).click();
 const stamp=Date.now();
 const name='Synthetic billing visit '+stamp;
 await page.getByLabel('Patient',{exact:true}).selectOption({label:'Jordan Vale'});
 await page.getByLabel('Invoice number').fill('BROWSER-'+stamp);
 await page.getByLabel('Service date').fill('2026-01-10');
 await page.getByLabel('Description').fill(name);
 await page.getByLabel('Billed amount').fill('65');
 await page.getByLabel('Insurance adjustment').fill('40');
 await page.getByLabel('Due date').fill('2027-01-10');
 await page.getByRole('button',{name:'Save record'}).click();
 await expect(page.getByRole('heading',{name,exact:true})).toBeVisible();
 const context=await browser.newContext();
 const patient=await context.newPage();
 patient.on('dialog',dialog=>dialog.accept());
 await login(patient,'patient');
 await patient.getByRole('link',{name:'Billing',exact:true}).click();
 await patient.getByRole('link',{name:new RegExp(name)}).click();
 await patient.getByRole('button',{name:'Submit simulated payment'}).click();
 await expect(patient.getByText('Paid',{exact:true}).first()).toBeVisible();
 await patient.getByRole('link',{name:/\$25\.00/}).click();
 const download=patient.waitForEvent('download');
 await patient.getByRole('link',{name:'Download receipt'}).click();
 expect((await download).suggestedFilename()).toMatch(/^receipt-\d+\.txt$/);
 await context.close();
});
