export type RecordData = {
  id: number;
  [field: string]: any;
};
export type User = {id:number; name:string; roles:string[]; patient:number|null};

export async function api<T = any>(path: string, data?: unknown, method = 'POST'): Promise<T> {
  const csrf = document.cookie.split('; ').find(value => value.startsWith('csrftoken_v2='))?.split('=').slice(1).join('=');
  const response = await fetch('/api/' + path, {
    credentials: 'same-origin',
    ...(data === undefined ? {} : {method, body: JSON.stringify(data), headers: {'Content-Type':'application/json','X-CSRFToken':csrf ?? ''}}),
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const errors = (value: unknown): string => typeof value === 'string' ? value : Array.isArray(value) ? value.map(errors).join(' ') :
      value && typeof value === 'object' ? Object.entries(value).map(([key, detail]) => key === 'detail' ? errors(detail) : key.replaceAll('_',' ') + ' — ' + errors(detail)).join(' ') : '';
    if (response.status === 403 && body?.detail === 'Authentication credentials were not provided.') {
      window.dispatchEvent(new Event('careconnect:session-expired'));
    }
    throw new Error(errors(body) || (response.status === 404 ? 'This record is unavailable.' : 'The request could not be completed.'));
  }
  return body;
}
export const date = (value: string) => value ? new Intl.DateTimeFormat('en-US',{dateStyle:'medium', ...(value.includes('T') ? {timeStyle:'short',timeZone:'UTC'} : {timeZone:'UTC'})}).format(new Date(value)) + (value.includes('T') ? ' UTC' : '') : '—';
export const money = (value: unknown) => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(Number(value || 0));
export function withParams(path: string, values: {[key:string]:string|number|undefined|null}) {
  const params = new URLSearchParams();
  Object.entries(values).forEach(([key,value]) => { if (value !== undefined && value !== null && value !== '') params.set(key,String(value)); });
  return path + (params.size ? '?' + params : '');
}
