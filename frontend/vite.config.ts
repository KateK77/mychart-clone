import {defineConfig} from 'vite';
import tailwind from '@tailwindcss/vite';
export default defineConfig({plugins:[tailwind()],server:{host:'127.0.0.1',port:15270,strictPort:true,proxy:{'/api':(process.env.CC_BACKEND_URL ?? 'http://127.0.0.1:18270'),'/static':(process.env.CC_BACKEND_URL ?? 'http://127.0.0.1:18270')}}});
