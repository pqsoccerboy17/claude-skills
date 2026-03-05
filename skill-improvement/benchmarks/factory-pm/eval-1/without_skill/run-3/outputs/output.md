# Client Portal

Here's a client portal implementation plan:

## Features
- Client login with email/password
- Project status dashboard
- Deliverable downloads
- Invoice viewing

## Tech Stack
- Next.js for the frontend
- PostgreSQL for the database
- Auth0 for authentication

## Implementation

```typescript
// app/dashboard/page.tsx
export default function Dashboard() {
  return (
    <div>
      <h1>Client Portal</h1>
      <ProjectStatus />
      <Deliverables />
      <Invoices />
    </div>
  );
}
```

Let me start building this out. I'll create the project structure first.
