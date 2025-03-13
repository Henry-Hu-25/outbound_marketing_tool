# Icebreaker Frontend

A modern UI for the Icebreaker application featuring animated backgrounds and interactive elements.

## Features

- Beautiful animated SVG background with flowing paths
- Letter-by-letter animated text
- Responsive design
- Dark mode support
- Modern UI components

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Integration with Python Backend

This frontend is designed to work with the Python backend of the Icebreaker application. 

To connect the frontend with the backend:

1. Ensure the Python backend is running
2. Frontend API calls will communicate with the backend endpoints
3. Modify API call endpoints in the frontend code as needed based on your backend configuration

## Technologies Used

- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion for animations
- Radix UI for accessible components

## Project Structure

- `/app` - Next.js app router pages
- `/components` - Reusable UI components
- `/components/ui` - Base UI components
- `/lib` - Utility functions 