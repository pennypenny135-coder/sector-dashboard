export default async function handler(req, res) {
  const sym = String(req.query.sym || "").toUpperCase();
  const range = String(req.query.range || "6mo");
  if (!/^[A-Z.]{1,10}$/.test(sym)) {
    return res.status(400).json({ error: "bad symbol" });
  }
  if (!/^\d+mo$/.test(range)) {
    return res.status(400).json({ error: "bad range" });
  }
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=1d&range=${range}&includePrePost=false`;
  try {
    const upstream = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0",
        Accept: "application/json",
      },
    });
    if (!upstream.ok) {
      return res.status(upstream.status).json({ error: "upstream" });
    }
    const data = await upstream.json();
    res.setHeader("Cache-Control", "public, s-maxage=120, stale-while-revalidate=300");
    return res.status(200).json(data);
  } catch (err) {
    return res.status(502).json({ error: "fetch failed" });
  }
}
