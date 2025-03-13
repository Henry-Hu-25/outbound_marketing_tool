# Icebreaker with Modern UI Frontend

This project has been enhanced with a modern UI frontend built with Next.js, React, and Framer Motion.

## Project Structure

The project now includes:

1. **Python Backend** - The original Icebreaker application with a Flask API server
2. **Next.js Frontend** - A modern frontend in the `/frontend` directory with animated UI

## Getting Started with the Frontend

### Prerequisites

- Node.js (v14.0.0 or later)
- npm, yarn, or pnpm

### Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install the dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the animated UI.

## Frontend Features

- **Animated Background**: Beautiful particle animations in the background
- **Animated Text**: Text that animates in with staggered animation
- **URL Input Fields**: Clean form for entering product and client URLs
- **Email Generation**: Integration with backend API for email generation
- **Results Page**: Well-formatted display of generated emails
- **Theme Switching**: Dark/light mode support
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Copy to Clipboard**: Easily copy generated emails
- **Beautiful Typography**: Enhanced text formatting with proper spacing
- **Error Handling**: User-friendly error messages

## Email Output Enhancements

The email output page has been improved with:

- **Paragraph Spacing**: Proper spacing between paragraphs for readability
- **Line Breaks**: Preserved line breaks within paragraphs
- **Typography**: Enhanced typography using Tailwind Typography
- **Copy Button**: One-click copy functionality for the entire email
- **Animations**: Smooth text reveal animations
- **Responsive Layout**: Proper formatting on all screen sizes

## Integrating with the Backend

The frontend and backend are integrated via:

1. Flask API server running on port 5001
2. Frontend API service for making requests to the backend
3. Structured JSON requests and responses

Example API service in the frontend:

```typescript
// frontend/lib/api.ts
export async function generateEmail(productUrl: string, clientUrl: string): Promise<EmailGenerationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_url: productUrl,
        client_url: clientUrl,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error generating email:', error);
    throw error;
  }
}
```

## Running the Complete Application

1. Start the Python backend API server:

```bash
python api_server.py
```

2. In a separate terminal, start the frontend:

```bash
cd frontend
npm run dev
```

3. Access the application at [http://localhost:3000](http://localhost:3000)

## Troubleshooting

- **API Connection Issues**: Ensure the Flask server is running on port 5001
- **Port Conflicts**: Check if port 5001 is available; change in `api_server.py` if needed
- **Visualization Errors**: The backend uses a non-GUI matplotlib backend to avoid display issues 