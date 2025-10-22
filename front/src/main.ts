import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

// 导入 svelte-material-ui 样式
import 'svelte-material-ui/bare.css'

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
