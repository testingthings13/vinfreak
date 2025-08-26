import { useEffect, useState } from "react";
import "./App.css";
import { getCars } from "./api";
import FilterBar from "./components/FilterBar";
import CarCard from "./components/CarCard";
import SkeletonCard from "./components/SkeletonCard";

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

  // initial load + on filter change
  useEffect(() => { load(true); /* eslint-disable-next-line */ }, []);
  useEffect(() => { load(true); /* eslint-disable-next-line */ }, [JSON.stringify(filters)]);

  const canLoadMore = total ? cars.length < total : true;

  return (
    <div className="wrap">
      <header className="topbar">
        <div className="brand">VINFREAK</div>
        <div className="hint">Search by VIN, make, model, year, price</div>
      </header>

      <main className="main">
        <FilterBar initial={filters} onChange={setFilters} />

        {err && <div className="error">Error: {err}</div>}

        {!err && (
          <>
            <div className="count">Showing <b>{cars.length}</b>{total ? <> / <b>{total}</b></> : null} cars</div>

            <div className="grid">
              {cars.map((c, i) => <CarCard key={c.id ?? `${c.make}-${c.model}-${i}`} car={c} />)}
              {loading && !cars.length && Array.from({length: 8}).map((_,i)=><SkeletonCard key={i} />)}
            </div>

            <div className="actions">
              {canLoadMore && !loading && (
                <button className="btn" onClick={() => load(false)}>Load more</button>
              )}
              {loading && <div className="loading">Loading…</div>}
              {!loading && !cars.length && <div className="empty">No cars match your filters.</div>}
            </div>
          </>
        )}
      </main>

      <footer className="footer">
        <span>© {new Date().getFullYear()} VINFREAK</span>
      </footer>
    </div>
  );
}
