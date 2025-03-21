# Modern UI Frontend

This project has been enhanced with a modern UI frontend built with Next.js, React, and Framer Motion.

### Prerequisites

- Node.js (v14.0.0 or later)
- npm, yarn, or pnpm

# Getting Started

### Installing Dependencies

```bash
# Navigate to the frontend directory
cd frontend

# Install all dependencies
npm install
# or
yarn install
# or
pnpm install
```

### Build and Deployment

To build the application for production:

```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `.next/` directory, which should also not be committed to version control.

### Running the Complete Application

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


# Development Notes

### Project Structure

The project now includes:

1. **Python Backend** - The application with a Flask API server
2. **Next.js Frontend** - A modern frontend in the `/frontend` directory with animated UI

### Key Dependencies

- **Next.js**: React framework for production
- **React**: UI library
- **Framer Motion**: Animation library
- **Tailwind CSS**: Utility-first CSS framework
- **next-themes**: Theme switching functionality
- **Lucide React**: Icon library
- **Radix UI**: Accessible UI components

### Development Workflow

- Use TypeScript for type safety and better developer experience
- Component architecture follows a common pattern with UI components in `/components/ui`
- Leverage custom hooks for reusable logic
- Use server components where appropriate for better performance

### Frontend Features

- **Animated Background**: Beautiful particle animations in the background
- **Animated Text**: Text that animates in with staggered animation
- **URL Input Fields**: Clean form for entering product and client URLs
- **Email Generation**: Integration with backend API for email generation
- **Results Page**: Well-formatted display of generated emails with copy functionality
- **Theme Switching**: Dark/light mode support via next-themes
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Copy to Clipboard**: Easily copy generated emails
- **Beautiful Typography**: Enhanced text formatting with proper spacing
- **Error Handling**: User-friendly error messages

### Email Output Enhancements

- **Paragraph Spacing**: Proper spacing between paragraphs for readability
- **Line Breaks**: Preserved line breaks within paragraphs
- **Typography**: Enhanced typography using Tailwind Typography
- **Copy Button**: One-click copy functionality for the entire email
- **Animations**: Smooth text reveal animations using Framer Motion
- **Responsive Layout**: Proper formatting on all screen sizes

### Integrating with the Backend

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

### Troubleshooting

- **API Connection Issues**: Ensure the Flask server is running on port 5001
- **Port Conflicts**: Check if port 5001 is available; change in `api_server.py` if needed
- **Visualization Errors**: The backend uses a non-GUI matplotlib backend to avoid display issues
- **Missing Dependencies**: If you encounter errors about missing modules, run `npm install` again
- **Large File Git Issues**: If you encounter GitHub rejection due to large files:
  - Remove node_modules from Git tracking: `git filter-branch --tree-filter 'rm -rf frontend/node_modules' --prune-empty HEAD`
  - Force push changes: `git push -f origin main`
- **Next.js Build Errors**: Try clearing the cache with `rm -rf .next` then rebuild
- **Module Not Found Errors**: Make sure all imports use correct paths and all dependencies are installed 

# Additional Notes
### Important Note on node_modules

- The `node_modules` directory is automatically created when you run `npm install` and contains all the project dependencies
- This directory is **large** (often hundreds of MB) and should **never** be committed to version control
- The `.gitignore` file is configured to exclude `node_modules/` from Git
- If you encounter Git issues with large files, ensure node_modules is completely removed from your Git history

### Environment Files

- `.env` files containing sensitive information should be excluded from Git
- Use `.env.example` as a template to show required environment variables