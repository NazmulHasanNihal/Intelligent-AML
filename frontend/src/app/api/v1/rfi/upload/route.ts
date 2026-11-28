import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;
    const rfiId = formData.get('rfiId') as string | null;
    const clientSha256 = formData.get('clientSha256') as string | null;

    if (!file || !rfiId) {
      return NextResponse.json({ error: 'Missing file or RFI ID' }, { status: 400 });
    }

    const buffer = Buffer.from(await file.arrayBuffer());
    const serverSha256 = crypto.createHash('sha256').update(buffer).digest('hex');

    const hashVerified = clientSha256 ? clientSha256.toLowerCase() === serverSha256.toLowerCase() : true;

    return NextResponse.json({
      success: true,
      documentId: `DOC-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      fileName: file.name,
      fileSizeBytes: file.size,
      mimeType: file.type || 'application/pdf',
      sha256: serverSha256,
      hashVerified,
      uploadedAt: new Date().toISOString()
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Upload failed';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
