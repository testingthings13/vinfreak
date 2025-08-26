import { getCarImage } from "../utils/image";

function formatMoney(n, curr = "USD") {
  if (n == null || n === "") return "—";
  try { return new Intl.NumberFormat(undefined, { style: "currency", currency: curr }).format(Number(n)); }
  catch { return String(n); }
}

export default function CarCard({ car }){
  const img = getCarImage(car);
  const isCAB = (car?.source || "").toLowerCase().includes("carsandbids");
  const title = car.title || [car.year, car.make, car.model].filter(Boolean).join(" ");
  const location = [car.city, car.state].filter(Boolean).join(", ");
  const mileage = car.mileage != null ? `${Number(car.mileage).toLocaleString()} mi` : null;
  const price = formatMoney(car.price, car.currency || "USD");
  const href = car.url || car.link || "#";

  return (
    <a className="card" href={href} target="_blank" rel="noreferrer">
      <div className="imgwrap">
        {img
          ? <img className="img" src={img} alt={title} loading="lazy" />
          : <div className="img img-ph" aria-label="No image" />}
        {isCAB && <img className="brand" src="/carsandbidslogo.png" alt="Cars & Bids" />}
      </div>
      <div className="body">
        <div className="title" title={title}>{title || "Untitled vehicle"}</div>
        <div className="meta">
          {location && <span>{location}</span>}
          {location && mileage && <span className="dot">•</span>}
          {mileage && <span>{mileage}</span>}
        </div>
        <div className="price">{price}</div>
      </div>
    </a>
  );
}
