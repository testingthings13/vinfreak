import { useEffect, useState } from "react";
import "./App.css";
import { getCars } from "./api";
import FilterBar from "./FilterBar";

function formatMoney(n, curr = "USD") {
  if (n == null) return "—";
  try { return new Intl.NumberFormat(undefined, { style: "currency", currency: curr }).format(n); }
  catch { return String(n); }
}

function Card({ car }) {
  const isCAB = (car?.source || "").toLowerCase().includes("carsandbids");
  return (
    <a className="car-card" href={car.url || "#"} target="_blank" rel="noreferrer">
      <div className="thumb">
        {isCAB && <img className="brand" src="/carsandbidslogo.png" alt="Cars & Bids" />}
      </div>
      <div className="meta">
        <div className="title">{car.title || `${car.year ?? ""} ${car.make ?? ""} ${car.model ?? ""}`}</div>
        <div className="sub">
          <span>{car.city || ""}{car.state ? `, ${car.state}` : ""}</span>
          <span>•</span>
          <span>{car.mileage != null ? `${Number(car.mileage).toLocaleString()} mi` : "—"}</span>
        </div>
        <div className="price">{formatMoney(car.price, car.currency || "USD")}</div>
      </div>
    </a>
  );
}

export default function App() {
  const [filters, setFilters] = useState({});
  const [cars, setCars] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(24);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load(reset = false) {
    setLoading(true);
    setErr("");
    try {
      const p = reset ? 1 : page;
      const { items, total: t } = await getCars(filters, { page: p, pageSize });
      setTotal(t ?? items.length);
      setCars(reset ? items : [...cars, ...items]);
      setPage(p + 1);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(true); /* eslint-disable-next-line */ }, []);
  useEffect(() => { load(true); /* eslint-disable-next-line */ }, [JSON.stringify(filters)]);

  const canLoadMore = total ? cars.length < total : true;

  return (
    <div className="container">
      <h1>VINFREAK</h1>

      <FilterBar initial={filters} onChange={setFilters} />

      {err && <div className="error">Error: {err}</div>}
      {!err && (
        <>
          <div style={{marginBottom:8, color:"#6b7280"}}>
            Showing <b>{cars.length}</b>{total ? <> / <b>{total}</b></> : null} cars
          </div>
          <div className="grid">
            {cars.map((c, i) => <Card key={c.id ?? `${c.make}-${c.model}-${i}`} car={c} />)}
          </div>

          <div style={{display:"flex", justifyContent:"center", margin:"16px 0"}}>
            {canLoadMore && !loading && (
              <button onClick={() => load(false)} style={{padding:"10px 14px", borderRadius:10, border:"1px solid #111827", background:"#111827", color:"#fff"}}>
                Load more
              </button>
            )}
            {loading && <div className="loading">Loading…</div>}
          </div>
        </>
      )}
    </div>
  );
}
