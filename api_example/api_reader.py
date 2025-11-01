import argparse
from pathlib import Path
from typing import List, Dict, Any

import requests
import pandas as pd


BASE_URL = "https://api.open-meteo.com/v1/forecast"

DEFAULT_LAT = 40.7128   # Нью-Йорк
DEFAULT_LON = -74.0060
DEFAULT_HOURLY = "temperature_2m"
DEFAULT_TZ = "auto"     # Время по координатам
DEFAULT_OUT = str(Path("processed") / "weather_hourly.csv")


def build_params(latitude: float,
                 longitude: float,
                 hourly_vars: List[str],
                 start_date: str | None,
                 end_date: str | None,
                 timezone: str) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(hourly_vars),
        "timezone": timezone,
    }
    if start_date:
        params["start_date"] = start_date  # ГГГГ-ММ-ДД
    if end_date:
        params["end_date"] = end_date      # ГГГГ-ММ-ДД
    return params


def fetch_open_meteo(params: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    resp = requests.get(BASE_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def hourly_to_dataframe(payload: Dict[str, Any], hourly_vars: List[str]) -> pd.DataFrame:
    if "hourly" not in payload or "time" not in payload["hourly"]:
        raise RuntimeError("Open‑Meteo response does not contain 'hourly' time series. "
                           "Check chosen variables/dates/coords.")

    hourly = payload["hourly"]
    times = pd.to_datetime(hourly["time"])
    df = pd.DataFrame({"time": times})

    for var in hourly_vars:
        if var in hourly:
            df[var] = hourly[var]
        else:
            df[var] = pd.NA

    return df


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download hourly weather from Open‑Meteo and save to a CSV via pandas."
    )
    parser.add_argument("--latitude", type=float, default=DEFAULT_LAT,
                        help=f"Latitude (default: {DEFAULT_LAT})")
    parser.add_argument("--longitude", type=float, default=DEFAULT_LON,
                        help=f"Longitude (default: {DEFAULT_LON})")
    parser.add_argument("--hourly", default=DEFAULT_HOURLY,
                        help=("Comma‑separated hourly variables, e.g. "
                              "temperature_2m,relative_humidity_2m,wind_speed_10m "
                              f"(default: {DEFAULT_HOURLY})"))
    parser.add_argument("--start", dest="start_date", default=None,
                        help="Start date in YYYY-MM-DD (optional)")
    parser.add_argument("--end", dest="end_date", default=None,
                        help="End date in YYYY-MM-DD (optional)")
    parser.add_argument("--timezone", default=DEFAULT_TZ,
                        help=f"Timezone string like 'Europe/Moscow' or 'auto' (default: {DEFAULT_TZ})")
    parser.add_argument("--out", default=DEFAULT_OUT,
                        help=f"Output CSV path (default: {DEFAULT_OUT})")

    args = parser.parse_args(argv)

    hourly_vars = [v.strip() for v in args.hourly.split(",") if v.strip()]
    params = build_params(
        latitude=args.latitude,
        longitude=args.longitude,
        hourly_vars=hourly_vars,
        start_date=args.start_date,
        end_date=args.end_date,
        timezone=args.timezone,
    )

    payload = fetch_open_meteo(params)
    df = hourly_to_dataframe(payload, hourly_vars)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print("Параметры запроса OpenMeteo:", params)
    if "hourly_units" in payload:
        print("Еденицы:", payload["hourly_units"])
    print(f"\nFetched {len(df)} hourly rows. First rows:\n")
    print(df.head(min(10, len(df))).to_string(index=False))
    print(f"\nSaved CSV to: {out_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
