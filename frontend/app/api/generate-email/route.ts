import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { product_url, client_url } = await request.json();

    if (!product_url || !client_url) {
      return NextResponse.json(
        { error: 'Product URL and Client URL are required' },
        { status: 400 }
      );
    }

    // Execute the Python script with the provided URLs
    const { stdout, stderr } = await execAsync(
      `python ../../main.py --product_url="${product_url}" --client_url="${client_url}"`
    );

    if (stderr) {
      console.error('stderr:', stderr);
      return NextResponse.json(
        { error: 'Error running the Python script', details: stderr },
        { status: 500 }
      );
    }

    // Parse the output to extract the email content
    // Assuming the email content is the last part of the output
    // You might need to adjust this based on your Python script's output format
    const emailContent = stdout.trim();

    return NextResponse.json(
      {
        status: 'success',
        email_content: emailContent,
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('Error processing request:', error);
    return NextResponse.json(
      { error: 'Failed to process request', details: String(error) },
      { status: 500 }
    );
  }
} 