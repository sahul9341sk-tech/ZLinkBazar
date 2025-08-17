import React, { useState, useEffect } from "react";

// ZLink Bazar - Single-file starter React component // - Features included (frontend-only starter): //   1. Deals list (mock) with "Create Affiliate Link" button //   2. Affiliate short-link generator (simple hashing) //   3. Vote (upvote) deals and persist in localStorage //   4. Price watch: add desired price; "Check Price" simulates current price //   5. Subscribe to WhatsApp (mock) — stores number locally //   6. Export affiliate links as CSV // // Usage: drop this component in a React app (Vite/Create React App). Tailwind CSS classes are used; // if Tailwind is not available, the layout will still work but look basic.

export default function ZLinkBazarStarter() { // Mock deals data const initialDeals = [ { id: "d1", title: "Noise Buds X Bluetooth Earbuds", store: "Flipkart", price: 1199, image: "https://via.placeholder.com/120x90?text=Earbuds", url: "https://www.flipkart.com/example-product-1", }, { id: "d2", title: "Redmi Note Budget Phone", store: "Amazon", price: 8999, image: "https://via.placeholder.com/120x90?text=Phone", url: "https://www.amazon.in/example-product-2", }, { id: "d3", title: "Boat Smartwatch", store: "Myntra", price: 2499, image: "https://via.placeholder.com/120x90?text=Watch", url: "https://www.myntra.com/example-product-3", }, ];

const [deals, setDeals] = useState(() => { const saved = localStorage.getItem("zb_deals"); return saved ? JSON.parse(saved) : initialDeals; });

const [votes, setVotes] = useState(() => { return JSON.parse(localStorage.getItem("zb_votes") || "{}"); });

const [affiliateLinks, setAffiliateLinks] = useState(() => { return JSON.parse(localStorage.getItem("zb_afflinks") || "{}"); });

const [watchlist, setWatchlist] = useState(() => { return JSON.parse(localStorage.getItem("zb_watchlist") || "[]"); });

const [whatsappNumber, setWhatsappNumber] = useState( localStorage.getItem("zb_whatsapp") || "" );

useEffect(() => { localStorage.setItem("zb_deals", JSON.stringify(deals)); }, [deals]);

useEffect(() => { localStorage.setItem("zb_votes", JSON.stringify(votes)); }, [votes]);

useEffect(() => { localStorage.setItem("zb_afflinks", JSON.stringify(affiliateLinks)); }, [affiliateLinks]);

useEffect(() => { localStorage.setItem("zb_watchlist", JSON.stringify(watchlist)); }, [watchlist]);

useEffect(() => { if (whatsappNumber) localStorage.setItem("zb_whatsapp", whatsappNumber); }, [whatsappNumber]);

// Simple affiliate short link generator function makeAffiliateLink(originalUrl) { // Simple deterministic short-id: base64 of url + "-zlb" truncated const payload = ${originalUrl}::zlinkbazar; const id = btoa(unescape(encodeURIComponent(payload))).slice(0, 10); const short = https://zlinkb.in/${id}; return ${short}?u=${encodeURIComponent(originalUrl)}; }

function handleCreateAff(deal) { const link = makeAffiliateLink(deal.url); setAffiliateLinks((s) => ({ ...s, [deal.id]: link })); alert("Affiliate link created for " + deal.title); }

function handleUpvote(dealId) { setVotes((prev) => { const next = { ...prev }; next[dealId] = (next[dealId] || 0) + 1; return next; }); }

function handleAddWatch(deal) { const exists = watchlist.find((w) => w.id === deal.id); if (exists) { alert("Already in watchlist"); return; } const item = { id: deal.id, title: deal.title, targetPrice: deal.price - 100 }; setWatchlist((s) => [...s, item]); alert("Added to watchlist with target price " + item.targetPrice); }

function simulateCheckPrices() { // Simulate by randomly changing current price +- 10% const updates = deals.map((d) => { const change = Math.round(d.price * (Math.random() * 0.2 - 0.1)); return { ...d, currentPrice: Math.max(1, d.price + change) }; }); setDeals(updates);

// Notify if any watchlist hit
const hits = watchlist.filter((w) => {
  const deal = updates.find((x) => x.id === w.id);
  return deal && deal.currentPrice <= w.targetPrice;
});
if (hits.length) {
  alert(
    `Price alert! ${hits.length} item(s) reached your target. Check watchlist.`
  );
} else {
  alert("No price alerts right now. Prices simulated.");
}

}

function handleExportCSV() { const rows = ["title,store,affiliate_link"]; for (const d of deals) { const link = affiliateLinks[d.id] || makeAffiliateLink(d.url); rows.push("${d.title}","${d.store}","${link}"); } const csv = rows.join("\n"); const blob = new Blob([csv], { type: "text/csv" }); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "zlinkbazar_affiliate_links.csv"; a.click(); URL.revokeObjectURL(url); }

function handleSubscribeWhatsApp() { if (!/^\d{10,15}$/.test(whatsappNumber)) { alert("Enter valid number (10-15 digits)"); return; } alert("Subscribed " + whatsappNumber + " to WhatsApp deals (mock)"); }

function handleAddManualDeal() { const id = "d" + Math.random().toString(36).slice(2, 8); const newDeal = { id, title: "New Item " + id, store: "Other", price: Math.round(Math.random() * 5000 + 300), image: "https://via.placeholder.com/120x90?text=New", url: "https://example.com/new-item", }; setDeals((s) => [newDeal, ...s]); }

return ( <div className="p-4 max-w-4xl mx-auto"> <h1 className="text-2xl font-bold mb-4">ZLink Bazar — Starter Dashboard</h1>

<div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-3">
    <div className="p-3 border rounded">
      <h3 className="font-semibold">WhatsApp Broadcast</h3>
      <p className="text-sm mb-2">Subscribe to receive curated deals on WhatsApp (mock).</p>
      <input
        className="w-full border rounded p-2 mb-2"
        placeholder="Enter mobile (e.g. 91xxxxxxxxxx)"
        value={whatsappNumber}
        onChange={(e) => setWhatsappNumber(e.target.value)}
      />
      <button className="w-full py-2 rounded bg-blue-600 text-white" onClick={handleSubscribeWhatsApp}>
        Subscribe
      </button>
    </div>

    <div className="p-3 border rounded">
      <h3 className="font-semibold">Watchlist / Price Alerts</h3>
      <p className="text-sm mb-2">Add items to watchlist and simulate price checks.</p>
      <button className="w-full py-2 rounded border" onClick={simulateCheckPrices}>
        Check Prices (simulate)
      </button>
      <div className="mt-2 text-xs text-gray-600">Watchlist: {watchlist.length} items</div>
    </div>

    <div className="p-3 border rounded">
      <h3 className="font-semibold">Export</h3>
      <p className="text-sm mb-2">Export affiliate links CSV for campaigns.</p>
      <button className="w-full py-2 rounded bg-green-600 text-white" onClick={handleExportCSV}>
        Export CSV
      </button>
    </div>
  </div>

  <div className="mb-4 flex items-center justify-between">
    <h2 className="text-xl font-semibold">Deals</h2>
    <div className="space-x-2">
      <button className="px-3 py-1 border rounded" onClick={handleAddManualDeal}>
        Add Random Deal
      </button>
    </div>
  </div>

  <div className="grid gap-3">
    {deals.map((d) => (
      <div key={d.id} className="flex items-center gap-3 p-3 border rounded">
        <img src={d.image} alt="img" className="w-28 h-20 object-cover rounded" />
        <div className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <div className="font-semibold">{d.title}</div>
              <div className="text-sm text-gray-600">{d.store}</div>
            </div>
            <div className="text-right">
              <div className="font-semibold">₹{d.currentPrice ?? d.price}</div>
              <div className="text-xs text-gray-500">MRP</div>
            </div>
          </div>

          <div className="mt-3 flex gap-2">
            <button
              className="px-3 py-1 border rounded text-sm"
              onClick={() => handleCreateAff(d)}
            >
              Create Affiliate Link
            </button>

            <button className="px-3 py-1 border rounded text-sm" onClick={() => handleUpvote(d.id)}>
              Upvote ({votes[d.id] || 0})
            </button>

            <button className="px-3 py-1 border rounded text-sm" onClick={() => handleAddWatch(d)}>
              Add to Watchlist
            </button>

            <a
              className="px-3 py-1 border rounded text-sm"
              href={affiliateLinks[d.id] || makeAffiliateLink(d.url)}
              target="_blank"
              rel="noreferrer"
            >
              Open Link
            </a>
          </div>

          {affiliateLinks[d.id] && (
            <div className="mt-2 text-xs text-gray-700">
              Short Link: <span className="font-mono">{affiliateLinks[d.id]}</span>
            </div>
          )}
        </div>
      </div>
    ))}
  </div>

  <div className="mt-6 p-3 border rounded">
    <h3 className="font-semibold">Watchlist Details</h3>
    {watchlist.length === 0 ? (
      <div className="text-sm text-gray-600">No items in watchlist.</div>
    ) : (
      <table className="w-full mt-2 text-sm">
        <thead>
          <tr className="text-left">
            <th>Title</th>
            <th>Target Price</th>
            <th>Current Price</th>
          </tr>
        </thead>
        <tbody>
          {watchlist.map((w) => {
            const deal = deals.find((d) => d.id === w.id);
            return (
              <tr key={w.id}>
                <td>{w.title}</td>
                <td>₹{w.targetPrice}</td>
                <td>₹{deal?.currentPrice ?? deal?.price ?? "-"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    )}
  </div>

  <div className="mt-6 text-sm text-gray-600">
    This is a frontend-only starter. For a production-ready app you should:
    <ul className="list-disc ml-6 mt-2">
      <li>Build a backend (Node/Express or serverless) to store deals, affiliate links, and track clicks.</li>
      <li>Use a proper short-link service and database for analytics (clicks, geo, device).</li>
      <li>Integrate WhatsApp Business API or third-party provider for real broadcasts.</li>
      <li>Scrape or use APIs from marketplaces to auto-update deals and prices (respect terms of service).</li>
    </ul>
  </div>
</div>

); }

