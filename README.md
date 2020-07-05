# luna_price_exporter
LUNA price prometheus exporter 

## Usage

### Docker

Build the image

```
docker build -t luna_price_exporter .
```

Run it

```
docker run luna_price_exporter
```

## Configuration

Configuration is done through environment variables

| Environment | Default | Description                                      |
|-------------|---------|--------------------------------------------------|
| `DEBUG`     | -       | Set to any value to enable debug logs            |
| `PORT`      | `8000`  | Port to serve the prometheus exporter on         |
| `INTERVAL`  | `10`    | Interval for fetching price sources              |
| `DENOMS`    | -       | Comma separated set of denoms to fetch price for |

## Denoms

The available prices denoms are:

- ukrw
