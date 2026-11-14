// @vitest-environment jsdom
import {afterEach,describe,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen} from '@testing-library/react';
import {Filters,Tag,Trend} from './ui';

afterEach(cleanup);
describe('patient portal controls',()=>{
 it('submits filters and omits empty optional values',()=>{
  const onChange=vi.fn();
  render(<Filters fields={[{name:'q',label:'Test name',optional:true},{name:'date',label:'Date',kind:'date',optional:true}]} onChange={onChange}/>);
  fireEvent.change(screen.getByLabelText('Test name'),{target:{value:'Hemoglobin'}});
  fireEvent.click(screen.getByRole('button',{name:'Apply filters'}));
  expect(onChange).toHaveBeenCalledWith({q:'Hemoglobin'});
 });
 it('displays abnormal flags as text',()=>{
  render(<Tag value="High"/>);
  expect(screen.getByText('High').classList.contains('warm')).toBe(true);
 });
 it('shows individual lab measurements when focused',()=>{
  render(<Trend rows={[{id:1,value:'4.5',unit:'%',collected_at:'2026-01-01'},{id:2,value:'5.0',unit:'%',collected_at:'2026-02-01'}]}/>);
  fireEvent.focus(screen.getByLabelText('Feb 1, 2026 5.0 %'));
  expect(screen.getByText('Feb 1, 2026 · 5.0 %')).toBeTruthy();
 });
});
