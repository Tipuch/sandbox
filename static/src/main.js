import { createInertiaApp } from '@inertiajs/svelte'
import { mount } from 'svelte';

createInertiaApp({
  id: "app",
  resolve: name => {
    const pages = import.meta.glob('./pages/**/*.svelte');
    const page = pages[`./pages/${name}.svelte`];
    if (!page) {
      console.error(`missing page with path: ./pages/${name}.svelte`);
    }
    return page();
  },
  setup({ el, App, props }) {
    mount(App, { target: el, props })
  },
})

