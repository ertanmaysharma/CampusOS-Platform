import http from 'http';
import https from 'https';

export default function handler(req, res) {
  const BACKEND_URL = process.env.BACKEND_URL;
  if (!BACKEND_URL) {
    return res.status(500).json({ error: 'BACKEND_URL is not configured' });
  }

  // req.url in Vercel is a full URL (e.g. https://app.vercel.app/api/auth/login)
  // Extract just the path so BACKEND_URL is actually used as the base.
  const parsedOriginal = new URL(req.url, 'http://localhost');
  const targetUrl = new URL(parsedOriginal.pathname + parsedOriginal.search, BACKEND_URL);

  const headers = { ...req.headers };
  delete headers.host;
  headers.host = targetUrl.host;

  const protocol = targetUrl.protocol === 'https:' ? https : http;

  const proxyReq = protocol.request(
    {
      hostname: targetUrl.hostname,
      port: targetUrl.port,
      path: targetUrl.pathname + targetUrl.search,
      method: req.method,
      headers,
    },
    (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    }
  );

  proxyReq.on('error', (err) => {
    console.error('Proxy error:', err.message);
    if (!res.headersSent) {
      res.status(502).json({
        success: false,
        error: { code: 'BAD_GATEWAY', message: 'Could not reach backend server' },
      });
    }
  });

  req.pipe(proxyReq);
}

export const config = {
  api: {
    bodyParser: false,
  },
};
