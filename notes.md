# Server Architecture

1. Providers -> Classes which provide an common interface to connect to external systems / APIs

For example, the database provider interface defines methods which a database provider must have. It doesnt matter "how" the database connection is managed in background

_Providers talk to the infrastructure_

2. Repositories

Repositories use providers and implement provider specific logic to access data.

Repositories are also defined under a common schema

3. Services

Services use repositories and provide business logic to the application

```
┌─────────────────────────────┐
│                             │
│      Providers              │
│                             │
└───────┬─────────────────────┘
        │   Consumed by
┌───────▼─────────────────────┐
│                             │
│      Repositories           │
│                             │
└────────┬────────────────────┘
         │
         │  Consumed by
┌────────▼────────────────────┐
│                             │
│      Services               │
│                             │
└─────────────────────────────┘
```
