# exchange_price_exporter

![CI](https://github.com/setten-io/exchange_price_exporter/workflows/CI/badge.svg)

Prometheus blockchain exchange price exporter

## Usage

```
Usage: exchange-price-exporter [OPTIONS]

  Exchange price exporter.

Options:
  -c FILE    TOML config file.
  --version  Show the version and exit.
  --help     Show this message and exit.
```

### Docker

Build the image

```
docker build -t exchange_price_exporter .
```

Run it

```
docker run exchange_price_exporter
```

## Configuration

Configured via a toml, use `./config.toml` if the `-c` flag is not set

```toml
[server]
port=8000  # int, default: 8000

[log]
debug=true  # bool, default: false

[exporter]
interval=1  # int, default: 1 (minutes)
start_at_second=30  # int, default: 30 (will run at 01:30, 02:30, 03:30, etc.)
threads=8  # int, default: 8

[[exporter.pairs]]
exchange="coinone"
currency="luna"
market="krw"

[[exporter.pairs]]
exchange="bithumb"
currency="luna"
market="krw"
```

If an exporter pair doesn't exist on the exchange, all olhcv data will be `NaN`.

## Exchanges

Available exchanges:

- [Coinone](https://coinone.co.kr/) - `coinone`
- [Bithumb global](https://bithumb.com) - `bithumb`

## Others

In the assets folder, you can find some useful files such as:

- A grafana dashboard ready to import
- a prometheus example target config
