// API service for communicating with the backend

interface EmailGenerationResponse {
  email_content: string;
  status: string;
}

// The base URL for the API
const API_BASE_URL = 'http://localhost:5001';

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