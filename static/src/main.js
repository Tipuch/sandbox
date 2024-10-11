import { createInertiaApp } from '@inertiajs/svelte'

createInertiaApp({
  id: "app",
  resolve: name => {
    const pages = import.meta.glob('./pages/**/*.svelte', { eager: true });
    console.log(pages);
    console.log(name);
    return pages[`./pages/${name}.svelte`];
  },
  setup({ el, App }) {
    new App({ target: el })
  },
})

