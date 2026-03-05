# Dark Mode Toggle

I'll add a dark mode toggle to your website. Here's the plan:

## Approach

Use CSS custom properties with a toggle button that saves to localStorage.

```css
:root {
  --bg-color: #ffffff;
  --text-color: #1a1a1a;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #ffffff;
}
```

```javascript
const toggle = document.getElementById('dark-mode-toggle');
toggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// Load saved preference
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

Want me to implement this?
